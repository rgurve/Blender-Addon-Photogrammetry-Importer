import os
import bpy
from bpy.props import StringProperty

from photogrammetry_importer.operators.import_op import ImportOperator
from photogrammetry_importer.properties.camera_import_properties import (
    CameraImportProperties,
)
from photogrammetry_importer.properties.point_import_properties import (
    PointImportProperties,
)
from photogrammetry_importer.properties.general_import_properties import (
    GeneralImportProperties,
)

from photogrammetry_importer.file_handlers.mve_file_handler import (
    MVEFileHandler,
)
from photogrammetry_importer.utility.blender_utility import add_collection
from photogrammetry_importer.utility.blender_logging_utility import log_report


class ImportMVEOperator(
    ImportOperator,
    CameraImportProperties,
    PointImportProperties,
    GeneralImportProperties,
):

    """Import a Multi-View Environment reconstruction folder."""

    bl_idname = "import_scene.mve_folder"
    bl_label = "Import MVE Folder"
    bl_options = {"PRESET"}

    directory: StringProperty()

    def execute(self, context):

        path = self.directory
        # Remove trailing slash
        path = os.path.dirname(path)
        log_report("INFO", "path: " + str(path), self)

        cameras, points = MVEFileHandler.parse_mve_workspace(
            path,
            self.default_width,
            self.default_height,
            self.add_depth_maps_as_point_cloud,
            self.suppress_distortion_warnings,
            self,
        )

        log_report("INFO", "Number cameras: " + str(len(cameras)), self)
        log_report("INFO", "Number points: " + str(len(points)), self)

        reconstruction_collection = add_collection("Reconstruction Collection")
        self.import_photogrammetry_cameras(cameras, reconstruction_collection)
        self.import_photogrammetry_points(points, reconstruction_collection)
        self.apply_general_options()

        return {"FINISHED"}

    def invoke(self, context, event):

        addon_name = self.get_addon_name()
        import_export_prefs = bpy.context.preferences.addons[
            addon_name
        ].preferences
        self.initialize_options(import_export_prefs)
        # See:
        # https://blender.stackexchange.com/questions/14738/use-filemanager-to-select-directory-instead-of-file/14778
        # https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def draw(self, context):
        layout = self.layout
        self.draw_camera_options(
            layout,
            draw_image_fp=False,
            draw_image_size=True,
            draw_depth_map_import=True,
        )
        self.draw_point_options(layout)
        self.draw_general_options(layout)
