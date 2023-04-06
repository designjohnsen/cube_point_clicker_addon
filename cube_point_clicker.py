import bpy
import random
from bpy.app.handlers import persistent

def count_cube_points(context):
    return sum(1 for obj in context.scene.objects if obj.name.startswith('cube_point'))

class CUBE_POINT_OT_clicker(bpy.types.Operator):
    bl_idname = "object.cube_point_clicker"
    bl_label = "Cube Point Clicker"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        points_per_click = bpy.context.scene.cube_point_clicker_points_per_click

        for _ in range(points_per_click):
            # Generate a random cube point location
            cube_point_location = (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-10, 10)
            )

            # Create a simple mesh and object for the cube point
            mesh = bpy.data.meshes.new(name='cube_point_mesh')
            obj = bpy.data.objects.new(name='cube_point', object_data=mesh)

            # Set the object's location and link it to the scene
            obj.location = cube_point_location
            context.collection.objects.link(obj)

            # Set the object's display type to a circle
            obj.empty_display_type = 'CIRCLE'
            obj.empty_display_size = 1

        # Increment the clicker score
        bpy.context.scene.cube_point_clicker_score += points_per_click

        return {'FINISHED'}

class CUBE_POINT_OT_upgrade_clicker(bpy.types.Operator):
    bl_idname = "object.cube_point_upgrade_clicker"
    bl_label = "Upgrade Clicker"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        upgrade_cost = context.scene.cube_point_upgrade_clicker_cost
        if context.scene.cube_point_clicker_score >= upgrade_cost:
            context.scene.cube_point_clicker_score -= upgrade_cost
            context.scene.cube_point_clicker_points_per_click += 1
            context.scene.cube_point_upgrade_clicker_cost = int(upgrade_cost * 5)
        else:
            self.report({'WARNING'}, "Not enough points to upgrade clicker.")
        return {'FINISHED'}

class CUBE_POINT_OT_auto_clicker(bpy.types.Operator):
    bl_idname = "object.cube_point_auto_clicker"
    bl_label = "Buy Auto Clicker"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        auto_clicker_cost = context.scene.cube_point_auto_clicker_cost
        if context.scene.cube_point_clicker_score >= auto_clicker_cost:
            context.scene.cube_point_clicker_score -= auto_clicker_cost
            context.scene.cube_point_auto_clicker_count += 1
            context.scene.cube_point_auto_clicker_cost = int(auto_clicker_cost * 2)
        else:
            self.report({'WARNING'}, "Not enough points to buy auto clicker.")
        return {'FINISHED'}

@persistent
def auto_clicker_update(scene):
    scene.cube_point_clicker_score += scene.cube_point_auto_clicker_count

class CUBE_POINT_PT_clicker_panel(bpy.types.Panel):
    bl_label = "Cube Point Clicker"
    bl_idname = "CUBE_POINT_PT_clicker_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cube Point Clicker'

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.operator("object.cube_point_clicker", text="Make Cube Points")
        
        layout.label(text=f"Cube Points: {count_cube_points(context)}")
        layout.label(text=f"Money: {bpy.context.scene.cube_point_clicker_score} $")
        layout.separator()

        layout.operator("object.cube_point_upgrade_clicker", text="Upgrade Clicker")
        layout.label(text=f"Points per click: {bpy.context.scene.cube_point_clicker_points_per_click}")
        layout.label(text=f"Cost: {bpy.context.scene.cube_point_upgrade_clicker_cost} $")
        layout.separator()

        layout.operator("object.cube_point_auto_clicker", text="Buy Money Generator")
        layout.label(text=f"Money Generators: {bpy.context.scene.cube_point_auto_clicker_count}")
        layout.label(text=f"Cost: {bpy.context.scene.cube_point_auto_clicker_cost} $")

def register():
    bpy.utils.register_class(CUBE_POINT_OT_clicker)
    bpy.utils.register_class(CUBE_POINT_OT_upgrade_clicker)
    bpy.utils.register_class(CUBE_POINT_OT_auto_clicker)
    bpy.utils.register_class(CUBE_POINT_PT_clicker_panel)
    bpy.types.Scene.cube_point_clicker_score = bpy.props.IntProperty(name="Score", default=0)
    bpy.types.Scene.cube_point_clicker_points_per_click = bpy.props.IntProperty(name="Points per Click", default=1)
    bpy.types.Scene.cube_point_upgrade_clicker_cost = bpy.props.IntProperty(name="Upgrade Clicker Cost", default=50)
    bpy.types.Scene.cube_point_auto_clicker_count = bpy.props.IntProperty(name="Auto Clicker Count", default=0)
    bpy.types.Scene.cube_point_auto_clicker_cost = bpy.props.IntProperty(name="Auto Clicker Cost", default=20)
    bpy.app.handlers.frame_change_post.append(auto_clicker_update)

def unregister():
    bpy.utils.unregister_class(CUBE_POINT_OT_clicker)
    bpy.utils.unregister_class(CUBE_POINT_OT_upgrade_clicker)
    bpy.utils.unregister_class(CUBE_POINT_OT_auto_clicker)
    bpy.utils.unregister_class(CUBE_POINT_PT_clicker_panel)
    del bpy.types.Scene.cube_point_clicker_score
    del bpy.types.Scene.cube_point_clicker_points_per_click
    del bpy.types.Scene.cube_point_upgrade_clicker_cost
    del bpy.types.Scene.cube_point_auto_clicker_count
    del bpy.types.Scene.cube_point_auto_clicker_cost
    bpy.app.handlers.frame_change_post.remove(auto_clicker_update)
