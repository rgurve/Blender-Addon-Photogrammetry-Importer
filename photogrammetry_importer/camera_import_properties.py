import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatProperty,
                       IntProperty)

from photogrammetry_importer.blender_utils import adjust_render_settings_if_possible
from photogrammetry_importer.blender_camera_utils import principal_points_initialized
from photogrammetry_importer.blender_camera_utils import set_principal_point_for_cameras
from photogrammetry_importer.blender_camera_utils import add_cameras
from photogrammetry_importer.blender_camera_utils import add_camera_animation

class CameraImportProperties():
    """ This class encapsulates Blender UI properties that are required to visualize the reconstructed cameras correctly. """
    import_cameras: BoolProperty(
        name="Import Cameras",
        description = "Import Cameras", 
        default=True)
    default_width: IntProperty(
        name="Default Width",
        description = "Width, which will be used used if corresponding image is not found.", 
        default=-1)
    default_height: IntProperty(
        name="Default Height", 
        description = "Height, which will be used used if corresponding image is not found.",
        default=-1)
    default_pp_x: FloatProperty(
        name="Principal Point X Component",
        description = "Principal Point X Component, which will be used if not contained in the NVM file. " + \
                      "If no value is provided, the principal point is set to the image center.", 
        default=float('nan'))
    default_pp_y: FloatProperty(
        name="Principal Point Y Component", 
        description = "Principal Point Y Component, which will be used if not contained in the NVM file. " + \
                      "If no value is provided, the principal point is set to the image center.", 
        default=float('nan'))
    add_background_images: BoolProperty(
        name="Add a Background Image for each Camera",
        description = "The background image is only visible by viewing the scene from a specific camera.", 
        default=False)
    add_image_planes: BoolProperty(
        name="Add an Image Plane for each Camera",
        description = "Add an Image Plane for each Camera - only for non-panoramic cameras.", 
        default=True)
    path_to_images: StringProperty(
        name="Image Directory",
        description =   "Assuming the reconstruction result is located in <some/path/rec.ext> or <some/path/colmap_model>. " + 
                        "The addons uses <some/path/images> (if available) or <some/path> as default image path." , 
        default=""
        # Can not use subtype='DIR_PATH' while importing another file (i.e. .nvm)
        )
    add_image_plane_emission: BoolProperty(
        name="Add Image Plane Color Emission",
        description = "Add image plane color emission to increase the visibility of the image planes.", 
        default=True)
    image_plane_transparency: FloatProperty(
        name="Image Plane Transparency Value", 
        description = "Transparency value of the image planes: 0 = invisible, 1 = opaque.",
        default=0.5,
        min=0,
        max=1)
    add_camera_motion_as_animation: BoolProperty(
        name="Add Camera Motion as Animation",
        description =   "Add an animation reflecting the camera motion. " + 
                        " The order of the cameras is determined by the corresponding file name.", 
        default=True)
    number_interpolation_frames: IntProperty(
        name="Number of Frames Between two Reconstructed Cameras",
        description = "The poses of the animated camera are interpolated.", 
        default=0,
        min=0)

    interpolation_items = [
        ("LINEAR", "LINEAR", "", 1),
        ("BEZIER", "BEZIER", "", 2),
        ("SINE", "SINE", "", 3),
        ("QUAD", "QUAD", "", 4),
        ("CUBIC", "CUBIC", "", 5),
        ("QUART", "QUART", "", 6),
        ("QUINT", "QUINT", "", 7),
        ("EXPO", "EXPO", "", 8),
        ("CIRC", "CIRC", "", 9),
        ("BACK", "BACK", "", 10),
        ("BOUNCE", "BOUNCE", "", 11),
        ("ELASTIC", "ELASTIC", "", 12),
        ("CONSTANT", "CONSTANT", "", 13)
        ]
    interpolation_type: EnumProperty(
        name="Interpolation Type",
        description = "Blender string that defines the type of the interpolation.", 
        items=interpolation_items)

    consider_missing_cameras_during_animation: BoolProperty(
        name="Adjust Frame Numbers of Camera Animation",
        description =   "Assume there are three consecutive images A,B and C, but only A and C have been reconstructed. " + 
                        "This option adjusts the frame number of C and the number of interpolation frames between camera A and C.",
        default=True)

    remove_rotation_discontinuities: BoolProperty(
        name="Remove Rotation Discontinuities",
        description =   "The addon uses quaternions q to represent the rotation." + 
                        "A quaternion q and its negative -q describe the same rotation. " + 
                        "This option allows to remove different signs.",
        default=True)

    adjust_render_settings: BoolProperty(
        name="Adjust Render Settings",
        description = "Adjust the render settings according to the corresponding images. "  +
                      "All images have to be captured with the same device). " +
                      "If disabled the visualization of the camera cone in 3D view might be incorrect.", 
        default=True)
    camera_extent: FloatProperty(
        name="Initial Camera Extent (in Blender Units)", 
        description = "Initial Camera Extent (Visualization)",
        default=1)

    def draw_camera_options(self, layout, draw_size_and_pp=False):
        camera_box = layout.box()
        camera_box.prop(self, "path_to_images")

        if draw_size_and_pp:
            image_box = camera_box.box()
            image_box.prop(self, "default_width")
            image_box.prop(self, "default_height")
            image_box.prop(self, "default_pp_x")
            image_box.prop(self, "default_pp_y")

        import_camera_box = camera_box.box()
        import_camera_box.prop(self, "import_cameras")
        if self.import_cameras:
            import_camera_box.prop(self, "camera_extent")
            import_camera_box.prop(self, "add_background_images")

            image_plane_box = import_camera_box.box()
            image_plane_box.prop(self, "add_image_planes")
            if self.add_image_planes:
                image_plane_box.prop(self, "add_image_plane_emission")
                image_plane_box.prop(self, "image_plane_transparency")

        box = camera_box.box()
        box.prop(self, "add_camera_motion_as_animation")
        if self.add_camera_motion_as_animation:
            box.prop(self, "number_interpolation_frames")
            box.prop(self, "interpolation_type")
            box.prop(self, "consider_missing_cameras_during_animation")
            box.prop(self, "remove_rotation_discontinuities")

        camera_box.prop(self, "adjust_render_settings")

    def enhance_camera_with_images(self, cameras):
        # This function should be overwritten, 
        # if image size is not part of the reconstruction data
        # (e.g. nvm file)
        success = True
        return cameras, success

    def import_photogrammetry_cameras(self, cameras, parent_collection):
        if self.import_cameras or self.add_camera_motion_as_animation:
            cameras, success = self.enhance_camera_with_images(cameras)
            if success:
                # The principal point information may be provided in the reconstruction data
                if not principal_points_initialized(cameras):
                    set_principal_point_for_cameras(
                        cameras, 
                        self.default_pp_x,
                        self.default_pp_y,
                        self)
                
                if self.adjust_render_settings:
                    adjust_render_settings_if_possible(
                        self, 
                        cameras)

                if self.import_cameras:
                    add_cameras(
                        self, 
                        cameras, 
                        parent_collection,
                        path_to_images=self.path_to_images, 
                        add_background_images=self.add_background_images,
                        add_image_planes=self.add_image_planes, 
                        camera_scale=self.camera_extent,
                        image_plane_transparency=self.image_plane_transparency,
                        add_image_plane_emission=self.add_image_plane_emission)

                if self.add_camera_motion_as_animation:
                    add_camera_animation(
                        self,
                        cameras,
                        parent_collection,
                        self.number_interpolation_frames,
                        self.interpolation_type,
                        self.consider_missing_cameras_during_animation,
                        self.remove_rotation_discontinuities,
                        self.path_to_images)
            else:
                return {'FINISHED'}