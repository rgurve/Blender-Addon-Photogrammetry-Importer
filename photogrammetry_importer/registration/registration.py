import importlib
import bpy

from photogrammetry_importer.operators.colmap_import_op import (
    ImportColmapOperator,
)
from photogrammetry_importer.operators.meshroom_import_op import (
    ImportMeshroomOperator,
)
from photogrammetry_importer.operators.mve_import_op import ImportMVEOperator
from photogrammetry_importer.operators.nvm_import_op import ImportNVMOperator
from photogrammetry_importer.operators.openmvg_import_op import (
    ImportOpenMVGOperator,
)
from photogrammetry_importer.operators.opensfm_import_op import (
    ImportOpenSfMOperator,
)
from photogrammetry_importer.operators.open3d_import_op import (
    ImportOpen3DOperator,
)
from photogrammetry_importer.operators.point_data_import_op import (
    ImportPointDataOperator,
)

from photogrammetry_importer.operators.nvm_export_op import ExportNVMOperator
from photogrammetry_importer.operators.colmap_export_op import (
    ExportColmapOperator,
)


# Import Functions
def colmap_import_operator_function(self, context):
    self.layout.operator(
        ImportColmapOperator.bl_idname, text="Colmap (model/workspace)"
    )


def meshroom_import_operator_function(self, context):
    self.layout.operator(
        ImportMeshroomOperator.bl_idname,
        text="Meshroom (.sfm/.json/.mg)",
    )


def mve_import_operator_function(self, context):
    self.layout.operator(ImportMVEOperator.bl_idname, text="MVE (workspace)")


def open3d_import_operator_function(self, context):
    self.layout.operator(
        ImportOpen3DOperator.bl_idname, text="Open3D (.log/.json)"
    )


def opensfm_import_operator_function(self, context):
    self.layout.operator(
        ImportOpenSfMOperator.bl_idname, text="OpenSfM (.json)"
    )


def openmvg_import_operator_function(self, context):
    self.layout.operator(
        ImportOpenMVGOperator.bl_idname,
        text="OpenMVG / Regard3D (.json)",
    )


def point_data_import_operator_function(self, context):
    module_spec = importlib.util.find_spec("pyntcloud")
    if module_spec is not None:
        suffix = "(.ply/.pcd/.las/.asc/.pts/.csv)"
    else:
        suffix = "[Pyntcloud is NOT installed]"
    self.layout.operator(
        ImportPointDataOperator.bl_idname,
        text="Point Data " + suffix,
    )


def visualsfm_import_operator_function(self, context):
    self.layout.operator(ImportNVMOperator.bl_idname, text="VisualSfM (.nvm)")


# Export Functions
def colmap_export_operator_function(self, context):
    self.layout.operator(
        ExportColmapOperator.bl_idname, text="Colmap (folder)"
    )


def visualsfm_export_operator_function(self, context):
    self.layout.operator(ExportNVMOperator.bl_idname, text="VisualSfM (.nvm)")


# Define register/unregister Functions
def bl_idname_to_bpy_types_name(bl_idname, bpy_types_prefix):
    assert bpy_types_prefix in ["IMPORT", "EXPORT"]
    bl_idname_suffix = bl_idname.split(".")[1]
    return bpy_types_prefix + "_SCENE_OT_" + bl_idname_suffix


def is_registered(import_or_export_operator, operator_type):
    """ Determine if an importer/exporter is already registered. """
    assert operator_type in ["IMPORT", "EXPORT"]
    return hasattr(
        bpy.types,
        bl_idname_to_bpy_types_name(
            import_or_export_operator.bl_idname, operator_type
        ),
    )


def register_importer(condition, importer, append_function):
    """ Register a single importer. """
    # https://blenderartists.org/t/find-out-if-a-class-is-registered/602335
    if condition:
        if not is_registered(importer, operator_type="IMPORT"):
            bpy.utils.register_class(importer)
            bpy.types.TOPBAR_MT_file_import.append(append_function)


def unregister_importer(importer, append_function):
    """ Unregister a single importer. """
    if is_registered(importer, operator_type="IMPORT"):
        bpy.utils.unregister_class(importer)
        bpy.types.TOPBAR_MT_file_import.remove(append_function)


def register_exporter(condition, exporter, append_function):
    """ Register a single exporter. """
    # https://blenderartists.org/t/find-out-if-a-class-is-registered/602335
    if condition:
        if not is_registered(exporter, operator_type="EXPORT"):
            bpy.utils.register_class(exporter)
            bpy.types.TOPBAR_MT_file_export.append(append_function)


def unregister_exporter(exporter, append_function):
    """ Unregister a single exporter. """
    if is_registered(exporter, operator_type="EXPORT"):
        bpy.utils.unregister_class(exporter)
        bpy.types.TOPBAR_MT_file_export.remove(append_function)


def register_importers(import_prefs):
    """ Register importers selected by the user. """
    register_importer(
        import_prefs.colmap_importer_bool,
        ImportColmapOperator,
        colmap_import_operator_function,
    )
    register_importer(
        import_prefs.meshroom_importer_bool,
        ImportMeshroomOperator,
        meshroom_import_operator_function,
    )
    register_importer(
        import_prefs.mve_importer_bool,
        ImportMVEOperator,
        mve_import_operator_function,
    )
    register_importer(
        import_prefs.open3d_importer_bool,
        ImportOpen3DOperator,
        open3d_import_operator_function,
    )
    register_importer(
        import_prefs.opensfm_importer_bool,
        ImportOpenSfMOperator,
        opensfm_import_operator_function,
    )
    register_importer(
        import_prefs.openmvg_importer_bool,
        ImportOpenMVGOperator,
        openmvg_import_operator_function,
    )
    register_importer(
        import_prefs.ply_importer_bool,
        ImportPointDataOperator,
        point_data_import_operator_function,
    )
    register_importer(
        import_prefs.visualsfm_importer_bool,
        ImportNVMOperator,
        visualsfm_import_operator_function,
    )


def unregister_importers():
    """ Unregister importers. """
    unregister_importer(ImportColmapOperator, colmap_import_operator_function)
    unregister_importer(
        ImportMeshroomOperator, meshroom_import_operator_function
    )
    unregister_importer(ImportMVEOperator, mve_import_operator_function)
    unregister_importer(ImportOpen3DOperator, open3d_import_operator_function)
    unregister_importer(
        ImportOpenSfMOperator, opensfm_import_operator_function
    )
    unregister_importer(
        ImportOpenMVGOperator, openmvg_import_operator_function
    )
    unregister_importer(
        ImportPointDataOperator, point_data_import_operator_function
    )
    unregister_importer(ImportNVMOperator, visualsfm_import_operator_function)


def register_exporters(export_prefs):
    """ Register exporters selected by the user. """
    register_exporter(
        export_prefs.colmap_exporter_bool,
        ExportColmapOperator,
        colmap_export_operator_function,
    )
    register_exporter(
        export_prefs.visualsfm_exporter_bool,
        ExportNVMOperator,
        visualsfm_export_operator_function,
    )


def unregister_exporters():
    """ Unregister exporters. """
    unregister_exporter(ExportColmapOperator, colmap_export_operator_function)
    unregister_exporter(ExportNVMOperator, visualsfm_export_operator_function)
