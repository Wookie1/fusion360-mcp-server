"""
MCP tool definitions for every command the Fusion360MCP add-in supports.

Each entry becomes a tool that Claude can call.  The ``inputSchema`` is
JSON Schema that the MCP SDK validates before forwarding arguments.
"""

import mcp.types as types

TOOLS: list[dict] = [
    # ── scene / query ────────────────────────────────────────────────
    {
        "name": "get_scene_info",
        "title": "Get Scene Info",
        "description": "Get design name, bodies, sketches, features, camera info",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_object_info",
        "title": "Get Object Info",
        "description": "Get detailed info about a named body or sketch",
        "inputSchema": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "description": "Object name"},
            },
        },
    },
    {
        "name": "get_bounding_box",
        "title": "Get Bounding Box",
        "description": (
            "Axis-aligned bounding box for a body or component by name. "
            "Returns min, max, size, and center in cm (Fusion internal units). "
            "For components, unions bounding boxes of all contained bodies. "
            "Useful for measuring imported reference geometry."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Body or component name",
                },
            },
        },
    },
    # ── sketch ───────────────────────────────────────────────────────
    {
        "name": "create_sketch",
        "title": "Create Sketch",
        "description": (
            "Create a new sketch on the xy (front, Z-up), yz (side, X-up), or "
            "xz (top, Y-up) construction plane. All subsequent draw_* commands "
            "use this sketch until a new one is created."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "default": "xy",
                    "description": (
                        "Construction plane: xy (front, Z-up), "
                        "yz (side, X-up), xz (top, Y-up)"
                    ),
                },
                "z_offset": {
                    "type": "number",
                    "description": "Offset distance from the plane origin (cm)",
                },
            },
        },
    },
    {
        "name": "draw_rectangle",
        "title": "Draw Rectangle",
        "description": (
            "Draw a rectangle in the most recent sketch. Width extends along "
            "the sketch X-axis, height along the sketch Y-axis. All coords in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["width", "height"],
            "properties": {
                "width": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Width along sketch X-axis (cm)",
                },
                "height": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Height along sketch Y-axis (cm)",
                },
                "origin_x": {
                    "type": "number",
                    "default": 0,
                    "description": "X coordinate of bottom-left corner (cm)",
                },
                "origin_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Y coordinate of bottom-left corner (cm)",
                },
                "origin_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Z coordinate of bottom-left corner (cm)",
                },
            },
        },
    },
    {
        "name": "draw_circle",
        "title": "Draw Circle",
        "description": (
            "Draw a circle in the most recent sketch. Center and radius in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["radius"],
            "properties": {
                "radius": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Circle radius (cm)",
                },
                "center_x": {
                    "type": "number",
                    "default": 0,
                    "description": "Center X coordinate (cm)",
                },
                "center_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Center Y coordinate (cm)",
                },
                "center_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Center Z coordinate (cm)",
                },
            },
        },
    },
    {
        "name": "draw_line",
        "title": "Draw Line",
        "description": (
            "Draw a straight line segment in the most recent sketch. "
            "All coordinates in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["start_x", "start_y", "end_x", "end_y"],
            "properties": {
                "start_x": {
                    "type": "number",
                    "description": "Start X coordinate (cm)",
                },
                "start_y": {
                    "type": "number",
                    "description": "Start Y coordinate (cm)",
                },
                "start_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Start Z coordinate (cm)",
                },
                "end_x": {
                    "type": "number",
                    "description": "End X coordinate (cm)",
                },
                "end_y": {
                    "type": "number",
                    "description": "End Y coordinate (cm)",
                },
                "end_z": {
                    "type": "number",
                    "default": 0,
                    "description": "End Z coordinate (cm)",
                },
            },
        },
    },
    # ── features ─────────────────────────────────────────────────────
    {
        "name": "extrude",
        "title": "Extrude",
        "description": (
            "Extrude a sketch profile from the most recent sketch. "
            "Positive direction extrudes along the sketch plane's positive "
            "normal (Z on xy, X on yz, Y on xz). Negative extrudes opposite. "
            "Symmetric extrudes equally both ways. Height in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["height"],
            "properties": {
                "height": {
                    "type": "number",
                    "description": (
                        "Extrusion distance (cm). Negative values reverse "
                        "direction."
                    ),
                },
                "profile_index": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": (
                        "Index of the closed profile within the sketch "
                        "(0-based). Call get_object_info on the sketch to "
                        "see available profiles."
                    ),
                },
                "operation": {
                    "type": "string",
                    "enum": ["new_body", "join", "cut", "intersect"],
                    "default": "new_body",
                    "description": (
                        "new_body creates a new body, join merges into "
                        "existing bodies, cut removes material, intersect "
                        "keeps only overlapping volume"
                    ),
                },
                "direction": {
                    "type": "string",
                    "enum": ["positive", "negative", "symmetric"],
                    "default": "positive",
                    "description": (
                        "positive extrudes along the sketch plane's "
                        "positive normal, negative extrudes opposite, "
                        "symmetric extrudes equally both ways"
                    ),
                },
            },
        },
    },
    {
        "name": "revolve",
        "title": "Revolve",
        "description": (
            "Revolve a sketch profile around an axis counter-clockwise "
            "(right-hand rule). Default axis is X-axis. Angle in degrees."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["angle"],
            "properties": {
                "angle": {
                    "type": "number",
                    "minimum": 0.1,
                    "maximum": 360,
                    "description": (
                        "Revolve angle in degrees "
                        "(counter-clockwise by right-hand rule)"
                    ),
                },
                "profile_index": {
                    "type": "integer",
                    "default": 0,
                    "description": (
                        "Index of the closed profile within "
                        "the sketch (0-based)"
                    ),
                },
                "axis_origin_x": {
                    "type": "number",
                    "default": 0,
                    "description": "Axis origin X (cm)",
                },
                "axis_origin_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Axis origin Y (cm)",
                },
                "axis_origin_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Axis origin Z (cm)",
                },
                "axis_direction_x": {
                    "type": "number",
                    "default": 1,
                    "description": "Axis direction X (default 1=X-axis)",
                },
                "axis_direction_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Axis direction Y",
                },
                "axis_direction_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Axis direction Z",
                },
                "operation": {
                    "type": "string",
                    "enum": ["new_body", "join", "cut", "intersect"],
                    "default": "new_body",
                    "description": (
                        "new_body creates a new body, join merges, "
                        "cut removes, intersect keeps overlap"
                    ),
                },
            },
        },
    },
    {
        "name": "fillet",
        "title": "Fillet Edges",
        "description": (
            "Round edges of a body. edge_selection='all' rounds all edges, "
            "'top'/'bottom' selects edges at the highest/lowest Z, "
            "'vertical' selects edges parallel to Z. Radius in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["radius"],
            "properties": {
                "radius": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Fillet radius (cm)",
                },
                "body_name": {
                    "type": "string",
                    "description": "Body name (preferred over body_index)",
                },
                "body_index": {
                    "type": "integer",
                    "default": 0,
                    "description": "Body index (fallback if body_name not provided)",
                },
                "edge_selection": {
                    "type": "string",
                    "enum": ["all", "top", "bottom", "vertical"],
                    "default": "all",
                    "description": (
                        "all=every edge, top=edges at highest Z, "
                        "bottom=edges at lowest Z, "
                        "vertical=edges parallel to Z-axis"
                    ),
                },
            },
        },
    },
    {
        "name": "chamfer",
        "title": "Chamfer Edges",
        "description": (
            "Chamfer edges of a body at 45° angle. Distance is the cut "
            "length on each face. Same edge_selection options as fillet. "
            "Distance in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["distance"],
            "properties": {
                "distance": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Chamfer distance on each face (cm)",
                },
                "body_name": {
                    "type": "string",
                    "description": "Body name (preferred)",
                },
                "body_index": {
                    "type": "integer",
                    "default": 0,
                    "description": "Body index (fallback)",
                },
                "edge_selection": {
                    "type": "string",
                    "enum": ["all", "top", "bottom", "vertical"],
                    "default": "all",
                    "description": (
                        "all=every edge, top=edges at highest Z, "
                        "bottom=edges at lowest Z, "
                        "vertical=edges parallel to Z-axis"
                    ),
                },
            },
        },
    },
    {
        "name": "shell",
        "title": "Shell Body",
        "description": (
            "Hollow out a body by removing a face, leaving uniform wall "
            "thickness. face_selection='top' removes the face at the highest Z, "
            "'bottom' at lowest Z. Thickness in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["thickness"],
            "properties": {
                "thickness": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Wall thickness (cm)",
                },
                "body_name": {
                    "type": "string",
                    "description": "Body name (preferred)",
                },
                "body_index": {
                    "type": "integer",
                    "default": 0,
                    "description": "Body index (fallback)",
                },
                "face_selection": {
                    "type": "string",
                    "enum": ["top", "bottom"],
                    "default": "top",
                    "description": (
                        "top=remove face at highest Z, "
                        "bottom=remove face at lowest Z"
                    ),
                },
            },
        },
    },
    {
        "name": "mirror",
        "title": "Mirror Body",
        "description": (
            "Mirror a body across a construction plane (xy/yz/xz) creating "
            "a new body. The original body is preserved."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["mirror_plane"],
            "properties": {
                "mirror_plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "description": (
                        "Plane to mirror across: xy (flips Z), "
                        "yz (flips X), xz (flips Y)"
                    ),
                },
                "body_name": {
                    "type": "string",
                    "description": "Body name (preferred)",
                },
                "body_index": {
                    "type": "integer",
                    "default": 0,
                    "description": "Body index (fallback)",
                },
            },
        },
    },
    # ── new commands ─────────────────────────────────────────────────
    {
        "name": "rename_body",
        "title": "Rename Body",
        "description": (
            "Rename a body. Searches root component and all sub-components. "
            "Call get_scene_info first to see current body names."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "new_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Current body name",
                },
                "new_name": {
                    "type": "string",
                    "description": "New name for the body",
                },
            },
        },
    },
    {
        "name": "move_body",
        "title": "Move Body",
        "description": (
            "Translate a named body by (x, y, z) in cm relative to its "
            "current position. Positive X=right, positive Y=up, "
            "positive Z=forward (toward viewer on xy plane)."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Body name to move",
                },
                "x": {
                    "type": "number",
                    "default": 0,
                    "description": "Translation along X-axis (cm)",
                },
                "y": {
                    "type": "number",
                    "default": 0,
                    "description": "Translation along Y-axis (cm)",
                },
                "z": {
                    "type": "number",
                    "default": 0,
                    "description": "Translation along Z-axis (cm)",
                },
            },
        },
    },
    {
        "name": "export_stl",
        "title": "Export STL",
        "description": (
            "Export a named body as an STL mesh file. "
            "Default output is ~/Desktop/<name>.stl."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Body name to export",
                },
                "file_path": {
                    "type": "string",
                    "description": "Destination path (default: ~/Desktop/<name>.stl)",
                },
            },
        },
    },
    {
        "name": "boolean_operation",
        "title": "Boolean Operation",
        "description": (
            "Combine two named bodies. 'join' merges tool into target "
            "(target absorbs tool). 'cut' removes tool volume from target. "
            "'intersect' keeps only overlapping volume. "
            "Always verify names with get_scene_info first."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["target_body", "tool_body"],
            "properties": {
                "target_body": {
                    "type": "string",
                    "description": (
                        "Primary body (absorbs on join, "
                        "loses material on cut)"
                    ),
                },
                "tool_body": {
                    "type": "string",
                    "description": (
                        "Secondary body (merged into target on join, "
                        "acts as cutter on cut)"
                    ),
                },
                "operation": {
                    "type": "string",
                    "enum": ["join", "cut", "intersect"],
                    "default": "join",
                    "description": (
                        "join=merge bodies, cut=remove tool from target, "
                        "intersect=keep only overlap"
                    ),
                },
            },
        },
    },
    {
        "name": "delete_all",
        "title": "Delete All",
        "description": "Clear the design (delete all timeline items)",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "undo",
        "title": "Undo",
        "description": "Undo the last operation",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    # ── code execution ───────────────────────────────────────────────
    {
        "name": "execute_code",
        "title": "Execute Code",
        "description": (
            "Run arbitrary Python in Fusion 360. "
            "The last expression's value is returned (REPL-style). "
            "Pre-defined names: app, ui, design, component, adsk, math."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["code"],
            "properties": {
                "code": {"type": "string"},
            },
        },
    },
    # ── additional geometry ───────────────────────────────────────────
    {
        "name": "sweep",
        "title": "Sweep",
        "description": (
            "Sweep a sketch profile along a path curve in another sketch. "
            "profile_index selects the closed profile in the most recent sketch. "
            "path_sketch_name names the sketch containing the path curve."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["profile_index", "path_sketch_name"],
            "properties": {
                "profile_index": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": (
                        "Index of the closed profile in the most recent "
                        "sketch (0-based)"
                    ),
                },
                "path_sketch_name": {
                    "type": "string",
                    "description": (
                        "Name of the sketch containing the sweep path curve"
                    ),
                },
                "path_curve_index": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": (
                        "Index of the path curve within path_sketch_name "
                        "(0-based)"
                    ),
                },
                "operation": {
                    "type": "string",
                    "enum": ["new_body", "join", "cut", "intersect"],
                    "default": "new_body",
                    "description": (
                        "new_body creates a new body, join merges, "
                        "cut removes, intersect keeps overlap"
                    ),
                },
            },
        },
    },
    {
        "name": "loft",
        "title": "Loft",
        "description": (
            "Loft between two or more sketch profiles to create a smooth "
            "transitional body. Sketches should be on parallel planes. "
            "First profile of each sketch is used."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["profile_sketch_names"],
            "properties": {
                "profile_sketch_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                    "description": (
                        "Ordered list of sketch names whose first profile "
                        "will be lofted"
                    ),
                },
                "operation": {
                    "type": "string",
                    "enum": ["new_body", "join", "cut", "intersect"],
                    "default": "new_body",
                    "description": (
                        "new_body creates a new body, join merges, "
                        "cut removes, intersect keeps overlap"
                    ),
                },
            },
        },
    },
    {
        "name": "create_polygon",
        "title": "Create Polygon",
        "description": (
            "Draw a regular polygon in the most recent sketch. "
            "First vertex points along the positive X-axis. All coords in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["sides", "radius"],
            "properties": {
                "sides": {
                    "type": "integer",
                    "minimum": 3,
                    "maximum": 64,
                    "description": (
                        "Number of sides (3=triangle, 4=square, 6=hexagon)"
                    ),
                },
                "radius": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Circumradius from center to vertices (cm)",
                },
                "center_x": {
                    "type": "number",
                    "default": 0,
                    "description": "Center X coordinate (cm)",
                },
                "center_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Center Y coordinate (cm)",
                },
                "center_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Center Z coordinate (cm)",
                },
            },
        },
    },
    {
        "name": "draw_arc",
        "title": "Draw Arc",
        "description": (
            "Draw an arc in the most recent sketch defined by center, start "
            "point, and sweep angle. Positive angles sweep counter-clockwise, "
            "negative clockwise. All coordinates in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["center_x", "center_y", "start_x", "start_y", "sweep_angle"],
            "properties": {
                "center_x": {
                    "type": "number",
                    "description": "Arc center X (cm)",
                },
                "center_y": {
                    "type": "number",
                    "description": "Arc center Y (cm)",
                },
                "center_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Arc center Z (cm)",
                },
                "start_x": {
                    "type": "number",
                    "description": "Arc start point X (cm)",
                },
                "start_y": {
                    "type": "number",
                    "description": "Arc start point Y (cm)",
                },
                "start_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Arc start point Z (cm)",
                },
                "sweep_angle": {
                    "type": "number",
                    "description": (
                        "Sweep angle in degrees: positive=counter-clockwise, "
                        "negative=clockwise"
                    ),
                    "minimum": -360,
                    "maximum": 360,
                },
            },
        },
    },
    {
        "name": "create_hole",
        "title": "Create Hole",
        "description": (
            "Create a hole on a body face at the specified center coordinates. "
            "face_selection='top' drills from the highest Z face, 'bottom' from "
            "lowest Z. center_x/center_y define the hole center. Diameter and depth in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["diameter", "depth"],
            "properties": {
                "diameter": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Hole diameter (cm)",
                },
                "depth": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Hole depth (cm)",
                },
                "body_name": {
                    "type": "string",
                    "description": "Body name (preferred)",
                },
                "body_index": {
                    "type": "integer",
                    "default": 0,
                    "description": "Body index (fallback)",
                },
                "face_selection": {
                    "type": "string",
                    "enum": ["top", "bottom"],
                    "default": "top",
                    "description": (
                        "top=drill from highest Z face, "
                        "bottom=drill from lowest Z face"
                    ),
                },
                "center_x": {
                    "type": "number",
                    "default": 0,
                    "description": "Hole center X (cm)",
                },
                "center_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Hole center Y (cm)",
                },
            },
        },
    },
    {
        "name": "rectangular_pattern",
        "title": "Rectangular Pattern",
        "description": (
            "Pattern a body in a grid. x_count includes the original body. "
            "x_spacing is distance between copies along X. Spacing in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Body to pattern",
                },
                "x_count": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1,
                    "description": "Number of columns including original",
                },
                "x_spacing": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Distance between columns (cm)",
                },
                "y_count": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1,
                    "description": "Number of rows including original",
                },
                "y_spacing": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Distance between rows (cm)",
                },
            },
        },
    },
    {
        "name": "circular_pattern",
        "title": "Circular Pattern",
        "description": (
            "Pattern a body in a circle around an axis. count includes the "
            "original. total_angle distributes copies evenly (default 360°)."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "count"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Body to pattern",
                },
                "count": {
                    "type": "integer",
                    "minimum": 2,
                    "description": "Total instances including original",
                },
                "axis": {
                    "type": "string",
                    "enum": ["x", "y", "z"],
                    "default": "z",
                    "description": "Rotation axis: x=X-axis, y=Y-axis, z=Z-axis",
                },
                "total_angle": {
                    "type": "number",
                    "default": 360,
                    "minimum": 1,
                    "maximum": 360,
                    "description": (
                        "Total angle to distribute copies over (degrees). "
                        "Default 360=full circle"
                    ),
                },
            },
        },
    },
    # ── assembly ───────────────────────────────────────────────────────
    {
        "name": "create_component",
        "title": "Create Component",
        "description": "Create a new component (sub-assembly) in the design",
        "inputSchema": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "description": "Component name"},
                "parent_name": {
                    "type": "string",
                    "description": "Parent component name (omit for root)",
                },
            },
        },
    },
    {
        "name": "add_joint",
        "title": "Add Joint",
        "description": (
            "Add a joint between two components to constrain their relative "
            "motion. rigid=fuse components, revolute=hinge, slider=linear slide, "
            "cylindrical=slide+rotate, ball=spherical pivot."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["component_one", "component_two"],
            "properties": {
                "component_one": {
                    "type": "string",
                    "description": "First component name",
                },
                "component_two": {
                    "type": "string",
                    "description": "Second component name",
                },
                "joint_type": {
                    "type": "string",
                    "enum": [
                        "rigid",
                        "revolute",
                        "slider",
                        "cylindrical",
                        "pin_slot",
                        "planar",
                        "ball",
                    ],
                    "default": "rigid",
                },
            },
        },
    },
    {
        "name": "list_components",
        "title": "List Components",
        "description": "List all components in the design",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    # ── export ─────────────────────────────────────────────────────────
    {
        "name": "export_step",
        "title": "Export STEP",
        "description": (
            "Export a named body or component as a STEP (.step) CAD file. "
            "Default output is ~/Desktop/<name>.step."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Body or component name to export",
                },
                "file_path": {
                    "type": "string",
                    "description": "Destination path (default: ~/Desktop/<name>.step)",
                },
            },
        },
    },
    {
        "name": "export_f3d",
        "title": "Export F3D",
        "description": "Export the design as a native Fusion 360 archive (.f3d)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Destination path (default: ~/Desktop/<design_name>.f3d)"
                    ),
                },
            },
        },
    },
    {
        "name": "export_view_sheet",
        "title": "Export View Sheet",
        "description": (
            "Render canonical orthographic + isometric views as PNGs and "
            "emit a self-contained HTML sheet suitable for sharing with a "
            "mechanical engineer. Opens in any browser; Print -> Save as "
            "PDF for a static artifact. Restores the viewport camera "
            "after rendering."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": (
                        "Heading shown on the sheet "
                        "(default: document name)."
                    ),
                },
                "notes": {
                    "type": "string",
                    "description": (
                        "Free-form notes rendered below the views. "
                        "Newlines preserved; HTML is escaped."
                    ),
                },
                "views": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "iso", "iso_ne", "iso_nw", "iso_sw",
                            "front", "back", "top", "bottom",
                            "right", "left",
                        ],
                    },
                    "description": (
                        "Ordered list of views to render "
                        "(default: iso, front, top, right)."
                    ),
                },
                "image_size": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "minItems": 2,
                    "maxItems": 2,
                    "description": (
                        "[width, height] in pixels (default [1200, 900])."
                    ),
                },
                "output_dir": {
                    "type": "string",
                    "description": (
                        "Destination folder "
                        "(default: ~/Desktop/<doc>_views_<timestamp>)."
                    ),
                },
            },
        },
    },
    {
        "name": "export",
        "title": "Export (unified)",
        "description": (
            "Unified export wrapper — dispatches to export_stl / export_step / "
            "export_f3d based on format or file extension. "
            "Format is auto-detected from file_path extension if not specified. "
            "STL and STEP require body_name; F3D exports the whole design."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["stl", "step", "stp", "f3d"],
                    "description": (
                        "Output format. Inferred from file_path extension "
                        "if omitted."
                    ),
                },
                "body_name": {
                    "type": "string",
                    "description": "Body to export (required for stl/step)",
                },
                "file_path": {
                    "type": "string",
                    "description": (
                        "Destination path (default: ~/Desktop/<name>.<ext>)"
                    ),
                },
            },
        },
    },
    # ── import ─────────────────────────────────────────────────────────
    {
        "name": "import_mesh",
        "title": "Import Mesh",
        "description": (
            "Import a mesh file (STL, OBJ, or 3MF) as a mesh body. "
            "Returns the mesh name and bounding box. "
            "Use for reference geometry (e.g. exported SketchUp model)."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to mesh file (.stl/.obj/.3mf)",
                },
                "component_name": {
                    "type": "string",
                    "description": (
                        "Target component name (omit for root component)"
                    ),
                },
                "units": {
                    "type": "string",
                    "enum": ["mm", "cm", "m", "in", "ft"],
                    "default": "mm",
                    "description": "Source mesh units (default: mm)",
                },
            },
        },
    },
    # ── parameters ─────────────────────────────────────────────────────
    {
        "name": "get_parameters",
        "title": "Get Parameters",
        "description": "List all user parameters in the design",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "create_parameter",
        "title": "Create Parameter",
        "description": "Create a new user parameter",
        "inputSchema": {
            "type": "object",
            "required": ["name", "value", "unit"],
            "properties": {
                "name": {"type": "string", "description": "Parameter name"},
                "value": {"type": "number", "description": "Numeric value"},
                "unit": {
                    "type": "string",
                    "description": "Unit expression (e.g. 'mm', 'cm', 'in', 'deg')",
                },
                "comment": {"type": "string", "description": "Optional comment"},
            },
        },
    },
    {
        "name": "set_parameter",
        "title": "Set Parameter",
        "description": "Update the value of an existing user parameter",
        "inputSchema": {
            "type": "object",
            "required": ["name", "value"],
            "properties": {
                "name": {"type": "string", "description": "Parameter name"},
                "value": {"type": "number", "description": "New numeric value"},
            },
        },
    },
    {
        "name": "delete_parameter",
        "title": "Delete Parameter",
        "description": "Remove a user parameter",
        "inputSchema": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "description": "Parameter name"},
            },
        },
    },
    # ── sketch constraints ─────────────────────────────────────────────
    {
        "name": "add_constraint",
        "title": "Add Sketch Constraint",
        "description": (
            "Add a geometric constraint in the active sketch. Entities are "
            "referenced by 0-based index in creation order. Call get_object_info "
            "on the sketch to see curve indices before constraining."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["constraint_type"],
            "properties": {
                "constraint_type": {
                    "type": "string",
                    "enum": [
                        "coincident",
                        "parallel",
                        "perpendicular",
                        "tangent",
                        "equal",
                        "fix",
                        "midpoint",
                        "concentric",
                        "horizontal",
                        "vertical",
                        "symmetry",
                        "collinear",
                        "smooth",
                    ],
                    "description": (
                        "coincident=points touch, parallel=entities parallel, "
                        "perpendicular=90 degrees, tangent=smooth contact, "
                        "equal=same length/radius, fix=lock in place, "
                        "midpoint=center on entity, concentric=share center, "
                        "horizontal/vertical=align axis, symmetry=mirror across "
                        "line, collinear=on same line, smooth=C1 continuity"
                    ),
                },
                "entity_one": {
                    "type": "integer",
                    "description": (
                        "0-based index of the first sketch entity "
                        "(see get_object_info for indices)"
                    ),
                    "minimum": 0,
                },
                "entity_two": {
                    "type": "integer",
                    "description": (
                        "0-based index of the second sketch entity "
                        "(not needed for fix/horizontal/vertical)"
                    ),
                    "minimum": 0,
                },
                "symmetry_line": {
                    "type": "integer",
                    "description": (
                        "0-based index of the symmetry line "
                        "(only for symmetry constraint)"
                    ),
                    "minimum": 0,
                },
                "sketch_name": {
                    "type": "string",
                    "description": "Sketch name (default: most recent)",
                },
            },
        },
    },
    # ── sketch dimensions ──────────────────────────────────────────────
    {
        "name": "add_dimension",
        "title": "Add Sketch Dimension",
        "description": (
            "Add a driving dimension to constrain sketch geometry. Value in cm "
            "for distances/radii/diameters, degrees for angles. Entities are "
            "0-based indices in creation order — call get_object_info first."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["dimension_type", "value"],
            "properties": {
                "dimension_type": {
                    "type": "string",
                    "enum": [
                        "distance",
                        "horizontal",
                        "vertical",
                        "angular",
                        "radial",
                        "diameter",
                    ],
                    "description": (
                        "distance=point-to-point, horizontal/vertical=projected "
                        "distance, angular=angle between entities, "
                        "radial=circle radius, diameter=circle diameter"
                    ),
                },
                "value": {
                    "type": "number",
                    "description": "Dimension value (cm for distances, degrees for angles)",
                },
                "entity_one": {
                    "type": "integer",
                    "description": "0-based index of first entity (point or curve)",
                    "minimum": 0,
                },
                "entity_two": {
                    "type": "integer",
                    "description": (
                        "0-based index of second entity "
                        "(for distance/angular; not for radial/diameter)"
                    ),
                    "minimum": 0,
                },
                "sketch_name": {
                    "type": "string",
                    "description": "Sketch name (default: most recent)",
                },
            },
        },
    },
    # ── construction geometry ──────────────────────────────────────────
    {
        "name": "create_construction_plane",
        "title": "Create Construction Plane",
        "description": (
            "Create a construction plane for sketching. Each method requires "
            "different parameters: 'offset' needs plane+offset (cm), "
            "'angle' needs plane+angle(deg)+edge_name, 'midplane' needs "
            "plane_one+plane_two, 'three_points' needs three [x,y,z] points."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["method"],
            "properties": {
                "method": {
                    "type": "string",
                    "enum": [
                        "offset",
                        "angle",
                        "midplane",
                        "three_points",
                        "tangent",
                    ],
                    "description": (
                        "offset=parallel plane at distance, "
                        "angle=rotated around edge, "
                        "midplane=equidistant between two planes, "
                        "three_points=through three points, "
                        "tangent=angled from face"
                    ),
                },
                "plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "description": "Reference plane for offset/angle methods",
                },
                "offset": {
                    "type": "number",
                    "description": "Offset distance in cm (for offset method)",
                },
                "angle": {
                    "type": "number",
                    "description": "Angle in degrees (for angle method)",
                },
                "edge_name": {
                    "type": "string",
                    "description": (
                        "Edge or axis name to rotate around "
                        "(for angle method)"
                    ),
                },
                "plane_one": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "description": "First reference plane (for midplane method)",
                },
                "plane_two": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "description": "Second reference plane (for midplane method)",
                },
                "point_one": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                    "description": "[x,y,z] first point in cm (for three_points)",
                },
                "point_two": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                    "description": "[x,y,z] second point in cm (for three_points)",
                },
                "point_three": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                    "description": "[x,y,z] third point",
                },
            },
        },
    },
    {
        "name": "create_construction_axis",
        "title": "Create Construction Axis",
        "description": (
            "Create a construction axis. Methods: 'two_points' through two "
            "[x,y,z] points, 'intersection' of two planes, 'edge' uses an "
            "existing body edge. All coordinates in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["method"],
            "properties": {
                "method": {
                    "type": "string",
                    "enum": [
                        "two_points",
                        "intersection",
                        "edge",
                        "perpendicular_at_point",
                    ],
                    "description": (
                        "two_points=through two points, "
                        "intersection=plane intersection, "
                        "edge=existing edge, "
                        "perpendicular_at_point=normal through point"
                    ),
                },
                "point_one": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                    "description": (
                        "[x,y,z] first point in cm "
                        "(for two_points/perpendicular_at_point)"
                    ),
                },
                "point_two": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                    "description": "[x,y,z] second point in cm (for two_points)",
                },
                "plane_one": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "description": "First plane (for intersection method)",
                },
                "plane_two": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "description": "Second plane (for intersection method)",
                },
                "body_name": {
                    "type": "string",
                    "description": "Body name containing the edge (for edge method)",
                },
                "edge_index": {
                    "type": "integer",
                    "description": (
                        "0-based edge index on the body (for edge method)"
                    ),
                    "minimum": 0,
                },
            },
        },
    },
    # ── splines ────────────────────────────────────────────────────────
    {
        "name": "draw_spline",
        "title": "Draw Spline",
        "description": (
            "Draw a spline in the most recent sketch. 'fit_points' creates "
            "a curve passing through all given points. 'control_points' "
            "creates a Bézier-like spline guided by control points. "
            "Points are [x,y] or [x,y,z] in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["spline_type", "points"],
            "properties": {
                "spline_type": {
                    "type": "string",
                    "enum": ["fit_points", "control_points"],
                    "description": (
                        "fit_points=curve passes through all points, "
                        "control_points=Bézier-like guided by control polygon"
                    ),
                },
                "points": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 3,
                    },
                    "minItems": 2,
                    "description": "Array of [x,y] or [x,y,z] coordinates in cm",
                },
                "degree": {
                    "type": "integer",
                    "enum": [3, 5],
                    "default": 3,
                    "description": (
                        "Spline degree (only for control_points: "
                        "3=cubic, 5=fifth-order)"
                    ),
                },
            },
        },
    },
    # ── sketch curve operations ────────────────────────────────────────
    {
        "name": "offset_curve",
        "title": "Offset Curve",
        "description": (
            "Offset connected sketch curves by a distance in the direction "
            "specified by (direction_x, direction_y). direction_x=1, "
            "direction_y=0 offsets to the right (positive X). All distances in cm."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["curve_index", "offset_distance"],
            "properties": {
                "curve_index": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "0-based index of a curve in the connected loop",
                },
                "offset_distance": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Offset distance (cm)",
                },
                "direction_x": {
                    "type": "number",
                    "default": 1,
                    "description": "X component of offset direction (default 1=right)",
                },
                "direction_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Y component of offset direction (default 0)",
                },
                "sketch_name": {
                    "type": "string",
                    "description": "Sketch name (default: most recent)",
                },
            },
        },
    },
    {
        "name": "trim_curve",
        "title": "Trim Curve",
        "description": (
            "Trim a sketch curve at its intersections, removing the segment "
            "nearest to the given (point_x, point_y). curve_index is 0-based."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["curve_index", "point_x", "point_y"],
            "properties": {
                "curve_index": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "0-based index of the curve to trim",
                },
                "point_x": {
                    "type": "number",
                    "description": "X coordinate near the segment to remove (cm)",
                },
                "point_y": {
                    "type": "number",
                    "description": "Y coordinate near the segment to remove (cm)",
                },
                "sketch_name": {
                    "type": "string",
                    "description": "Sketch name (default: most recent)",
                },
            },
        },
    },
    {
        "name": "extend_curve",
        "title": "Extend Curve",
        "description": (
            "Extend a sketch curve to the nearest intersection. The end "
            "nearest to (point_x, point_y) is extended. curve_index is 0-based."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["curve_index", "point_x", "point_y"],
            "properties": {
                "curve_index": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "0-based index of the curve to extend",
                },
                "point_x": {
                    "type": "number",
                    "description": "X coordinate near the end to extend (cm)",
                },
                "point_y": {
                    "type": "number",
                    "description": "Y coordinate near the end to extend (cm)",
                },
                "sketch_name": {
                    "type": "string",
                    "description": "Sketch name (default: most recent)",
                },
            },
        },
    },
    # ── advanced features ──────────────────────────────────────────────
    {
        "name": "create_thread",
        "title": "Create Thread",
        "description": ("Add threads to a cylindrical face (cosmetic or modeled)"),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "face_index"],
            "properties": {
                "body_name": {"type": "string"},
                "face_index": {
                    "type": "integer",
                    "minimum": 0,
                    "description": ("Index of the cylindrical face"),
                },
                "is_internal": {
                    "type": "boolean",
                    "default": False,
                    "description": "True for internal (nut) threads",
                },
                "thread_type": {
                    "type": "string",
                    "default": "ISO Metric profile",
                    "description": (
                        "Thread standard "
                        "(e.g. 'ISO Metric profile', 'ANSI Unified Screw Threads')"
                    ),
                },
                "thread_designation": {
                    "type": "string",
                    "default": "M10x1.5",
                    "description": ("Size designation (e.g. 'M10x1.5')"),
                },
                "thread_class": {
                    "type": "string",
                    "default": "6g",
                    "description": "Thread class (e.g. '6g', '6H')",
                },
                "is_modeled": {
                    "type": "boolean",
                    "default": False,
                    "description": ("True = physical geometry, False = cosmetic"),
                },
                "is_full_length": {
                    "type": "boolean",
                    "default": True,
                    "description": "Thread entire cylinder length",
                },
                "thread_length": {
                    "type": "number",
                    "description": (
                        "Thread length in cm (only if is_full_length=false)"
                    ),
                },
            },
        },
    },
    {
        "name": "draft_faces",
        "title": "Draft / Taper Faces",
        "description": (
            "Add a draft angle to faces of a body "
            "(for mold release / injection molding)"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "angle"],
            "properties": {
                "body_name": {"type": "string"},
                "angle": {
                    "type": "number",
                    "minimum": 0.1,
                    "maximum": 89,
                    "description": "Draft angle in degrees",
                },
                "face_selection": {
                    "type": "string",
                    "enum": ["all", "top", "bottom", "vertical"],
                    "default": "vertical",
                    "description": "Which faces to draft",
                },
                "pull_direction_plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "default": "xy",
                    "description": "Plane defining the pull direction",
                },
                "is_tangent_chain": {
                    "type": "boolean",
                    "default": True,
                    "description": ("Include tangent-connected faces"),
                },
            },
        },
    },
    {
        "name": "split_body",
        "title": "Split Body",
        "description": "Split a body using a plane or face",
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {"type": "string"},
                "splitting_plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "default": "xy",
                    "description": ("Plane to split with (or use splitting_body)"),
                },
                "splitting_body": {
                    "type": "string",
                    "description": (
                        "Name of a body/surface to use "
                        "as splitting tool (overrides plane)"
                    ),
                },
                "extend_tool": {
                    "type": "boolean",
                    "default": True,
                    "description": ("Extend tool to cut through entire body"),
                },
            },
        },
    },
    {
        "name": "split_face",
        "title": "Split Face",
        "description": "Split faces of a body using a plane",
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {"type": "string"},
                "face_indices": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0},
                    "description": ("Indices of faces to split (default: all faces)"),
                },
                "splitting_plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "default": "xy",
                },
                "extend_tool": {
                    "type": "boolean",
                    "default": True,
                },
            },
        },
    },
    {
        "name": "offset_faces",
        "title": "Offset Faces",
        "description": ("Push/pull faces of a body by a distance"),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "distance"],
            "properties": {
                "body_name": {"type": "string"},
                "distance": {
                    "type": "number",
                    "description": ("Offset distance in cm (positive = outward)"),
                },
                "face_selection": {
                    "type": "string",
                    "enum": ["all", "top", "bottom"],
                    "default": "top",
                    "description": "Which faces to offset",
                },
                "face_indices": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0},
                    "description": ("Specific face indices (overrides face_selection)"),
                },
            },
        },
    },
    {
        "name": "scale_body",
        "title": "Scale Body",
        "description": "Scale a body uniformly or non-uniformly",
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "scale"],
            "properties": {
                "body_name": {"type": "string"},
                "scale": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Uniform scale factor",
                },
                "scale_x": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": ("X scale (overrides uniform scale)"),
                },
                "scale_y": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Y scale",
                },
                "scale_z": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Z scale",
                },
                "anchor_x": {
                    "type": "number",
                    "default": 0,
                    "description": "Scale anchor point X",
                },
                "anchor_y": {
                    "type": "number",
                    "default": 0,
                    "description": "Scale anchor point Y",
                },
                "anchor_z": {
                    "type": "number",
                    "default": 0,
                    "description": "Scale anchor point Z",
                },
            },
        },
    },
    # ── direct primitives ──────────────────────────────────────────────
    {
        "name": "create_box",
        "title": "Create Box",
        "description": (
            "Create a box primitive (non-parametric via TemporaryBRepManager)"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["length", "width", "height"],
            "properties": {
                "length": {"type": "number", "minimum": 0.001},
                "width": {"type": "number", "minimum": 0.001},
                "height": {"type": "number", "minimum": 0.001},
                "center_x": {"type": "number", "default": 0},
                "center_y": {"type": "number", "default": 0},
                "center_z": {"type": "number", "default": 0},
            },
        },
    },
    {
        "name": "create_box_parametric",
        "title": "Create Parametric Box",
        "description": (
            "Create a history-based rectangular box via sketch rectangle + "
            "extrude (unlike create_box which uses TemporaryBRepManager). "
            "length/width/height accept a number (cm, Fusion internal unit) "
            "or a string expression referencing User Parameters "
            "(e.g. 'boxL', '56 mm', 'outer - 2 * wall_t'). "
            "Call create_parameter first to define named parameters."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["length", "width", "height"],
            "properties": {
                "length": {
                    "oneOf": [
                        {"type": "number", "minimum": 0.001},
                        {"type": "string"},
                    ],
                    "description": "Along sketch X: number (cm) or expression",
                },
                "width": {
                    "oneOf": [
                        {"type": "number", "minimum": 0.001},
                        {"type": "string"},
                    ],
                    "description": "Along sketch Y: number (cm) or expression",
                },
                "height": {
                    "oneOf": [
                        {"type": "number", "minimum": 0.001},
                        {"type": "string"},
                    ],
                    "description": "Extrude distance: number (cm) or expression",
                },
                "origin_x": {"type": "number", "default": 0},
                "origin_y": {"type": "number", "default": 0},
                "origin_z": {
                    "type": "number", "default": 0,
                    "description": "Z-offset of sketch plane (cm)",
                },
                "plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "default": "xy",
                },
                "component_name": {
                    "type": "string",
                    "description": "Target component (omit for root)",
                },
                "body_name": {
                    "type": "string",
                    "description": "Optional name for the resulting body",
                },
            },
        },
    },
    {
        "name": "create_cylinder",
        "title": "Create Cylinder",
        "description": (
            "Create a cylinder primitive (non-parametric via TemporaryBRepManager)"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["radius", "height"],
            "properties": {
                "radius": {"type": "number", "minimum": 0.001},
                "height": {"type": "number", "minimum": 0.001},
                "base_x": {"type": "number", "default": 0},
                "base_y": {"type": "number", "default": 0},
                "base_z": {"type": "number", "default": 0},
                "axis": {
                    "type": "string",
                    "enum": ["x", "y", "z"],
                    "default": "z",
                    "description": "Cylinder axis direction",
                },
            },
        },
    },
    {
        "name": "create_sphere",
        "title": "Create Sphere",
        "description": (
            "Create a sphere primitive (non-parametric via TemporaryBRepManager)"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["radius"],
            "properties": {
                "radius": {"type": "number", "minimum": 0.001},
                "center_x": {"type": "number", "default": 0},
                "center_y": {"type": "number", "default": 0},
                "center_z": {"type": "number", "default": 0},
            },
        },
    },
    {
        "name": "create_torus",
        "title": "Create Torus",
        "description": (
            "Create a torus primitive (non-parametric via TemporaryBRepManager)"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["major_radius", "minor_radius"],
            "properties": {
                "major_radius": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Distance from center to tube center",
                },
                "minor_radius": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Tube cross-section radius",
                },
                "center_x": {"type": "number", "default": 0},
                "center_y": {"type": "number", "default": 0},
                "center_z": {"type": "number", "default": 0},
                "axis": {
                    "type": "string",
                    "enum": ["x", "y", "z"],
                    "default": "z",
                },
            },
        },
    },
    # ── assembly (extended) ────────────────────────────────────────────
    {
        "name": "create_as_built_joint",
        "title": "Create As-Built Joint",
        "description": (
            "Create a joint from components' current positions "
            "(easier than geometric joints)"
        ),
        "inputSchema": {
            "type": "object",
            "required": [
                "component_one",
                "component_two",
                "joint_type",
            ],
            "properties": {
                "component_one": {"type": "string"},
                "component_two": {"type": "string"},
                "joint_type": {
                    "type": "string",
                    "enum": [
                        "rigid",
                        "revolute",
                        "slider",
                        "cylindrical",
                        "pin_slot",
                        "planar",
                        "ball",
                    ],
                    "default": "rigid",
                },
            },
        },
    },
    {
        "name": "create_rigid_group",
        "title": "Create Rigid Group",
        "description": "Lock multiple components together",
        "inputSchema": {
            "type": "object",
            "required": ["component_names"],
            "properties": {
                "component_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                    "description": "Names of components to group",
                },
                "include_children": {
                    "type": "boolean",
                    "default": True,
                    "description": ("Include child sub-components"),
                },
            },
        },
    },
    # ── inspection / analysis ──────────────────────────────────────────
    {
        "name": "measure_distance",
        "title": "Measure Distance",
        "description": ("Measure minimum distance between two entities"),
        "inputSchema": {
            "type": "object",
            "required": ["entity_one", "entity_two"],
            "properties": {
                "entity_one": {
                    "type": "string",
                    "description": (
                        "First entity name (body, sketch, or point 'x,y,z')"
                    ),
                },
                "entity_two": {
                    "type": "string",
                    "description": "Second entity name or point",
                },
            },
        },
    },
    {
        "name": "measure_angle",
        "title": "Measure Angle",
        "description": "Measure angle between two entities",
        "inputSchema": {
            "type": "object",
            "required": ["entity_one", "entity_two"],
            "properties": {
                "entity_one": {
                    "type": "string",
                    "description": "First entity name (face, edge)",
                },
                "entity_two": {
                    "type": "string",
                    "description": "Second entity name",
                },
            },
        },
    },
    {
        "name": "get_physical_properties",
        "title": "Get Physical Properties",
        "description": (
            "Get mass, volume, surface area, center of mass, and density of a body"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {"type": "string"},
                "accuracy": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "very_high"],
                    "default": "medium",
                },
            },
        },
    },
    {
        "name": "create_section_analysis",
        "title": "Create Section Analysis",
        "description": "Cut a section plane through the model",
        "inputSchema": {
            "type": "object",
            "properties": {
                "plane": {
                    "type": "string",
                    "enum": ["xy", "yz", "xz"],
                    "default": "yz",
                },
                "offset": {
                    "type": "number",
                    "default": 0,
                    "description": "Offset from the plane (cm)",
                },
            },
        },
    },
    {
        "name": "check_interference",
        "title": "Check Interference",
        "description": ("Detect collisions between components/bodies"),
        "inputSchema": {
            "type": "object",
            "required": ["component_names"],
            "properties": {
                "component_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                    "description": ("Names of components to check"),
                },
                "include_coincident_faces": {
                    "type": "boolean",
                    "default": False,
                    "description": ("Count touching faces as interference"),
                },
            },
        },
    },
    # ── appearance / material ──────────────────────────────────────────
    {
        "name": "set_appearance",
        "title": "Set Appearance",
        "description": (
            "Assign a material appearance to a body, face, "
            "or component from the Fusion appearance library"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["target_name", "appearance_name"],
            "properties": {
                "target_name": {
                    "type": "string",
                    "description": "Name of body or component",
                },
                "appearance_name": {
                    "type": "string",
                    "description": (
                        "Library appearance name "
                        "(e.g. 'Steel - Satin', "
                        "'Aluminum - Anodized Red')"
                    ),
                },
                "target_type": {
                    "type": "string",
                    "enum": ["body", "component", "face"],
                    "default": "body",
                },
                "face_index": {
                    "type": "integer",
                    "minimum": 0,
                    "description": ("Face index (if target_type=face)"),
                },
            },
        },
    },
    # ── project geometry ───────────────────────────────────────────────
    {
        "name": "project_geometry",
        "title": "Project Geometry",
        "description": ("Project edges or bodies onto the active sketch plane"),
        "inputSchema": {
            "type": "object",
            "required": ["source_name"],
            "properties": {
                "source_name": {
                    "type": "string",
                    "description": ("Name of body or edge to project"),
                },
                "is_linked": {
                    "type": "boolean",
                    "default": True,
                    "description": ("True = parametrically linked to source geometry"),
                },
                "sketch_name": {
                    "type": "string",
                    "description": ("Target sketch (default: most recent)"),
                },
            },
        },
    },
    # ── timeline control ──────────────────────────────────────────────
    {
        "name": "suppress_feature",
        "title": "Suppress Feature",
        "description": "Suppress (disable) a feature in the timeline",
        "inputSchema": {
            "type": "object",
            "required": ["feature_name"],
            "properties": {
                "feature_name": {"type": "string"},
            },
        },
    },
    {
        "name": "unsuppress_feature",
        "title": "Unsuppress Feature",
        "description": "Unsuppress (re-enable) a feature in the timeline",
        "inputSchema": {
            "type": "object",
            "required": ["feature_name"],
            "properties": {
                "feature_name": {"type": "string"},
            },
        },
    },
    # ── surface operations ─────────────────────────────────────────────
    {
        "name": "patch_surface",
        "title": "Patch Surface",
        "description": ("Create a patch surface from boundary edges"),
        "inputSchema": {
            "type": "object",
            "required": ["sketch_name"],
            "properties": {
                "sketch_name": {
                    "type": "string",
                    "description": "Sketch with boundary curves",
                },
                "profile_index": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                },
                "continuity": {
                    "type": "string",
                    "enum": ["connected", "tangent", "curvature"],
                    "default": "connected",
                },
            },
        },
    },
    {
        "name": "stitch_surfaces",
        "title": "Stitch Surfaces",
        "description": ("Stitch surface bodies into a single body"),
        "inputSchema": {
            "type": "object",
            "required": ["body_names"],
            "properties": {
                "body_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                },
                "tolerance": {
                    "type": "number",
                    "default": 0.01,
                    "description": "Stitch tolerance (cm)",
                },
            },
        },
    },
    {
        "name": "thicken_surface",
        "title": "Thicken Surface",
        "description": "Thicken a surface body into a solid",
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "thickness"],
            "properties": {
                "body_name": {"type": "string"},
                "thickness": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Thickness (cm)",
                },
                "direction": {
                    "type": "string",
                    "enum": ["positive", "negative", "symmetric"],
                    "default": "symmetric",
                },
            },
        },
    },
    {
        "name": "ruled_surface",
        "title": "Ruled Surface",
        "description": ("Create a ruled surface from an edge or sketch curve"),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "edge_index"],
            "properties": {
                "body_name": {"type": "string"},
                "edge_index": {
                    "type": "integer",
                    "minimum": 0,
                },
                "distance": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Ruled surface distance (cm)",
                },
                "rule_type": {
                    "type": "string",
                    "enum": ["normal", "tangent"],
                    "default": "normal",
                },
            },
        },
    },
    {
        "name": "trim_surface",
        "title": "Trim Surface",
        "description": "Trim a surface body with another body",
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "tool_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Surface body to trim",
                },
                "tool_name": {
                    "type": "string",
                    "description": "Trimming tool body",
                },
            },
        },
    },
    # ── sheet metal ────────────────────────────────────────────────────
    {
        "name": "create_flange",
        "title": "Create Flange",
        "description": ("Create a sheet metal flange on an edge"),
        "inputSchema": {
            "type": "object",
            "required": ["body_name", "edge_index"],
            "properties": {
                "body_name": {"type": "string"},
                "edge_index": {
                    "type": "integer",
                    "minimum": 0,
                },
                "height": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Flange height (cm)",
                },
                "angle": {
                    "type": "number",
                    "default": 90,
                    "description": "Bend angle (degrees)",
                },
                "bend_radius": {
                    "type": "number",
                    "description": "Bend radius (cm)",
                },
            },
        },
    },
    {
        "name": "create_bend",
        "title": "Create Bend",
        "description": "Add a bend to a sheet metal body",
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {"type": "string"},
                "bend_line_sketch": {
                    "type": "string",
                    "description": "Sketch with bend line",
                },
                "angle": {
                    "type": "number",
                    "default": 90,
                    "description": "Bend angle (degrees)",
                },
                "bend_radius": {
                    "type": "number",
                    "description": "Override bend radius (cm)",
                },
            },
        },
    },
    {
        "name": "flat_pattern",
        "title": "Flat Pattern",
        "description": ("Create a flat pattern from a sheet metal body"),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {"type": "string"},
            },
        },
    },
    {
        "name": "unfold",
        "title": "Unfold",
        "description": "Unfold specific bends in a sheet metal body",
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {"type": "string"},
                "bend_indices": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0},
                    "description": ("Indices of bends to unfold (omit to unfold all)"),
                },
            },
        },
    },
    # ── CAM / manufacturing ──────────────────────────────────────────
    {
        "name": "cam_create_setup",
        "title": "Create CAM Setup",
        "description": (
            "Create a manufacturing setup for a body. "
            "Defines the stock, coordinate system, and "
            "operation type (milling/turning/cutting)."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["body_name"],
            "properties": {
                "body_name": {
                    "type": "string",
                    "description": "Body to machine",
                },
                "name": {
                    "type": "string",
                    "description": "Setup name",
                },
                "operation_type": {
                    "type": "string",
                    "enum": ["milling", "turning", "cutting"],
                    "default": "milling",
                },
                "stock_mode": {
                    "type": "string",
                    "enum": [
                        "relative_box",
                        "fixed_box",
                        "from_body",
                    ],
                    "default": "relative_box",
                },
                "stock_offset_sides": {
                    "type": "number",
                    "default": 0,
                    "description": "Side offset (cm)",
                },
                "stock_offset_top": {
                    "type": "number",
                    "default": 0,
                    "description": "Top offset (cm)",
                },
                "stock_offset_bottom": {
                    "type": "number",
                    "default": 0,
                    "description": "Bottom offset (cm)",
                },
            },
        },
    },
    {
        "name": "cam_create_operation",
        "title": "Create CAM Operation",
        "description": (
            "Add a machining operation to a setup. "
            "Strategy determines the toolpath type."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["setup_name", "strategy"],
            "properties": {
                "setup_name": {
                    "type": "string",
                    "description": "Name of the parent setup",
                },
                "strategy": {
                    "type": "string",
                    "enum": [
                        "face",
                        "2d_contour",
                        "2d_pocket",
                        "2d_adaptive",
                        "3d_adaptive",
                        "3d_pocket",
                        "3d_contour",
                        "3d_scallop",
                        "3d_parallel",
                        "drilling",
                        "bore",
                        "thread_milling",
                        "slot",
                        "trace",
                        "engrave",
                    ],
                    "description": "Machining strategy",
                },
                "name": {
                    "type": "string",
                    "description": "Operation name",
                },
                "tool_number": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Tool number from library",
                },
                "tool_diameter": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": (
                        "Tool diameter (cm) — used if tool_number not specified"
                    ),
                },
                "stepdown": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": "Axial depth of cut (cm)",
                },
                "stepover": {
                    "type": "number",
                    "minimum": 0.001,
                    "description": ("Radial stepover (cm)"),
                },
                "feed_rate": {
                    "type": "number",
                    "description": "Feed rate (cm/min)",
                },
                "spindle_speed": {
                    "type": "number",
                    "description": "Spindle speed (RPM)",
                },
                "coolant": {
                    "type": "string",
                    "enum": [
                        "disabled",
                        "flood",
                        "mist",
                        "through_tool",
                    ],
                    "default": "flood",
                },
            },
        },
    },
    {
        "name": "cam_generate_toolpath",
        "title": "Generate Toolpath",
        "description": (
            "Generate toolpaths for a specific operation or all operations in a setup"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "setup_name": {
                    "type": "string",
                    "description": ("Setup name (generates all its operations)"),
                },
                "operation_name": {
                    "type": "string",
                    "description": ("Specific operation name (overrides setup_name)"),
                },
                "generate_all": {
                    "type": "boolean",
                    "default": False,
                    "description": "Generate all toolpaths",
                },
            },
        },
    },
    {
        "name": "cam_post_process",
        "title": "Post Process",
        "description": ("Post-process toolpaths to generate NC code (G-code)"),
        "inputSchema": {
            "type": "object",
            "required": ["setup_name"],
            "properties": {
                "setup_name": {
                    "type": "string",
                    "description": "Setup to post-process",
                },
                "operation_name": {
                    "type": "string",
                    "description": ("Specific operation (omit to post all in setup)"),
                },
                "post_processor": {
                    "type": "string",
                    "default": "fanuc",
                    "description": (
                        "Post processor name "
                        "(e.g. 'fanuc', 'grbl', 'haas', "
                        "'linuxcnc', 'mach3')"
                    ),
                },
                "output_folder": {
                    "type": "string",
                    "description": ("Output directory (default: ~/Desktop)"),
                },
                "output_units": {
                    "type": "string",
                    "enum": ["mm", "in"],
                    "default": "mm",
                },
            },
        },
    },
    {
        "name": "cam_list_setups",
        "title": "List CAM Setups",
        "description": ("List all manufacturing setups in the document"),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "cam_list_operations",
        "title": "List CAM Operations",
        "description": ("List operations within a setup"),
        "inputSchema": {
            "type": "object",
            "required": ["setup_name"],
            "properties": {
                "setup_name": {
                    "type": "string",
                },
            },
        },
    },
    {
        "name": "cam_get_operation_info",
        "title": "Get CAM Operation Info",
        "description": (
            "Get details about a specific operation "
            "(strategy, tool, parameters, toolpath status)"
        ),
        "inputSchema": {
            "type": "object",
            "required": ["setup_name", "operation_name"],
            "properties": {
                "setup_name": {"type": "string"},
                "operation_name": {"type": "string"},
            },
        },
    },
    # ── health ───────────────────────────────────────────────────────
    {
        "name": "ping",
        "title": "Ping",
        "description": (
            "Health check — returns immediately without touching Fusion API"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    # ── design type safety ──────────────────────────────────────────────
    {
        "name": "get_design_type",
        "title": "Get Design Type",
        "description": (
            "Check if the design is in parametric or direct mode. "
            "Use this to detect accidental mode switches."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "set_design_type",
        "title": "Set Design Type",
        "description": (
            "Switch design type between 'parametric' and 'direct'. "
            "Use 'parametric' to recover from accidental direct-mode "
            "switches (equivalent to Capture Design History in the UI)."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["design_type"],
            "properties": {
                "design_type": {
                    "type": "string",
                    "enum": ["parametric", "direct"],
                    "description": "Target design type",
                },
            },
        },
    },
    # ── perception ──────────────────────────────────────────────────────
    {
        "name": "render_view",
        "title": "Render Viewport",
        "description": (
            "Capture the active viewport as a PNG so you can visually verify "
            "the model. Pass a canonical view (iso/front/top/etc.) to "
            "reposition the camera first, or 'current' to keep it as is. "
            "Returns base64-encoded image bytes alongside metadata; the MCP "
            "server delivers it as an image content block."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "view": {
                    "type": "string",
                    "enum": [
                        "current",
                        "iso",
                        "front",
                        "back",
                        "top",
                        "bottom",
                        "left",
                        "right",
                    ],
                    "default": "current",
                    "description": (
                        "Camera preset; 'current' preserves the existing view"
                    ),
                },
                "width": {
                    "type": "integer",
                    "minimum": 64,
                    "maximum": 4096,
                    "default": 1024,
                },
                "height": {
                    "type": "integer",
                    "minimum": 64,
                    "maximum": 4096,
                    "default": 768,
                },
                "fit": {
                    "type": "boolean",
                    "default": True,
                    "description": "Call Viewport.fit() before capture",
                },
            },
        },
    },
]

# ── tool annotations ──────────────────────────────────────────────────
# Applied after definition for cleanliness. Classifies each tool by its
# side-effect profile so MCP clients can auto-approve safe operations.

_READ_ONLY = {
    "get_scene_info",
    "get_object_info",
    "get_bounding_box",
    "list_components",
    "get_parameters",
    "get_physical_properties",
    "measure_distance",
    "measure_angle",
    "check_interference",
    "ping",
    "cam_list_setups",
    "cam_list_operations",
    "cam_get_operation_info",
    "get_design_type",
    "render_view",
}
_DESTRUCTIVE = {"delete_all", "delete_parameter"}
_IDEMPOTENT = {
    "ping",
    "get_scene_info",
    "get_object_info",
    "get_bounding_box",
    "list_components",
    "get_parameters",
    "get_physical_properties",
    "measure_distance",
    "measure_angle",
    "check_interference",
    "set_parameter",
    "set_appearance",
    "cam_list_setups",
    "cam_list_operations",
    "cam_get_operation_info",
    "get_design_type",
    "set_design_type",
    "rename_body",
    "render_view",
}

for _t in TOOLS:
    _name = _t["name"]
    _t["annotations"] = {
        "readOnlyHint": _name in _READ_ONLY,
        "destructiveHint": _name in _DESTRUCTIVE,
        "idempotentHint": _name in _IDEMPOTENT,
    }


def get_tool_list() -> list[types.Tool]:
    """Convert tool dicts to MCP Tool objects."""
    result = []
    for t in TOOLS:
        ann = t.get("annotations")
        tool = types.Tool(
            name=t["name"],
            title=t["title"],
            description=t["description"],
            inputSchema=t["inputSchema"],
            annotations=types.ToolAnnotations(**ann) if ann else None,
        )
        result.append(tool)
    return result


def get_tool_by_name(name: str) -> dict | None:
    for t in TOOLS:
        if t["name"] == name:
            return t
    return None
