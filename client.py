# -*- coding: utf-8 -*-
"""
GenPark Vision Coder Client
Pure Python Standard Library (Zero External Dependencies)
Implements 2D AABB bounding-box Flexbox hierarchy layout solving,
Tailwind CSS semantic HTML AST generation, and visual whitespace center-of-mass balancing.
"""

import math
from typing import Dict, Any, List, Optional

class GenParkVisionCoder:
    """
    Algorithmic UI layout tree resolution and semantic code synthesizer.
    """

    def __init__(self):
        pass

    def parse_bounding_boxes_to_flexbox_hierarchy(
        self,
        elements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Parses visual UI bounding boxes [x, y, width, height] into an ordered Flexbox hierarchy
        detecting containment (parent-child) and spatial flow direction (row vs column).
        """
        if not elements:
            return {"layout": "empty", "total_elements": 0, "root_children": []}

        # Sort elements by y then x
        sorted_elements = sorted(
            elements,
            key=lambda e: (float(e.get("y", 0.0)), float(e.get("x", 0.0)))
        )

        nodes = []
        for i, el in enumerate(sorted_elements):
            x = float(el.get("x", 0.0))
            y = float(el.get("y", 0.0))
            w = float(el.get("width", 100.0))
            h = float(el.get("height", 40.0))
            tag = el.get("type", "div")
            text = el.get("text", "")

            nodes.append({
                "id": el.get("id", f"node_{i}"),
                "tag": tag,
                "text": text,
                "bbox": [x, y, w, h],
                "area": round(w * h, 2),
                "children": []
            })

        # Determine containment hierarchy
        root_nodes = []
        for i, node in enumerate(nodes):
            bx, by, bw, bh = node["bbox"]
            parent_found = False

            # Check if contained inside any other larger node
            for j, candidate in enumerate(nodes):
                if i == j:
                    continue
                cx, cy, cw, ch = candidate["bbox"]
                if cx <= bx and cy <= by and (cx + cw) >= (bx + bw) and (cy + ch) >= (by + bh):
                    candidate["children"].append(node)
                    parent_found = True
                    break

            if not parent_found:
                root_nodes.append(node)

        # Detect flow direction for root (if vertical delta > horizontal delta -> col)
        if len(root_nodes) > 1:
            y_diff = abs(root_nodes[-1]["bbox"][1] - root_nodes[0]["bbox"][1])
            x_diff = abs(root_nodes[-1]["bbox"][0] - root_nodes[0]["bbox"][0])
            flow = "flex-col" if y_diff >= x_diff else "flex-row"
        else:
            flow = "flex-col"

        return {
            "layout_flow": flow,
            "total_elements": len(elements),
            "root_element_count": len(root_nodes),
            "hierarchy": root_nodes
        }

    def synthesize_tailwind_css_dom_ast(
        self,
        hierarchy_tree: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Translates resolved Flexbox hierarchy into semantic HTML strings with production Tailwind CSS utility classes.
        """
        html_lines = []

        def render_node(node, depth=1):
            indent = "  " * depth
            tag = node.get("tag", "div").lower()
            text = node.get("text", "")
            children = node.get("children", [])

            # Determine tailwind classes based on tag
            classes = ["flex"]
            if children:
                classes.extend(["flex-col", "gap-4", "p-4", "border", "border-slate-200", "rounded-lg"])
            elif tag in ["button", "btn"]:
                tag = "button"
                classes = ["px-4", "py-2", "bg-blue-600", "hover:bg-blue-700", "text-white", "font-medium", "rounded-md", "shadow-sm"]
            elif tag in ["heading", "h1", "title"]:
                tag = "h1"
                classes = ["text-2xl", "font-bold", "text-slate-900", "tracking-tight"]
            elif tag in ["text", "p", "label"]:
                tag = "p"
                classes = ["text-sm", "text-slate-600"]
            elif tag in ["input", "textbox"]:
                tag = "input"
                classes = ["px-3", "py-2", "border", "border-slate-300", "rounded-md", "focus:ring-2", "focus:ring-blue-500"]

            cls_str = " ".join(classes)
            if tag == "input":
                html_lines.append(f'{indent}<input class="{cls_str}" placeholder="{text}" />')
            elif not children and text:
                html_lines.append(f'{indent}<{tag} class="{cls_str}">{text}</{tag}>')
            elif not children:
                html_lines.append(f'{indent}<{tag} class="{cls_str}"></{tag}>')
            else:
                html_lines.append(f'{indent}<{tag} class="{cls_str}">')
                for ch in children:
                    render_node(ch, depth + 1)
                html_lines.append(f'{indent}</{tag}>')

        html_lines.append('<div class="w-full max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">')
        for root in hierarchy_tree:
            render_node(root, depth=1)
        html_lines.append('</div>')

        return {
            "html_output": chr(10).join(html_lines),
            "css_framework": "TailwindCSS v3.4+",
            "semantic_tags_utilized": list(set(n.get("tag", "div") for n in hierarchy_tree))
        }

    def evaluate_visual_hierarchy_balance(
        self,
        elements: List[Dict[str, Any]],
        canvas_width: float = 1200.0,
        canvas_height: float = 800.0
    ) -> Dict[str, Any]:
        """
        Evaluates visual balance, whitespace ratio, and center-of-mass coordinates:
          X_c = sum( Area * x_mid ) / Total_Area
          Y_c = sum( Area * y_mid ) / Total_Area
        """
        if not elements or canvas_width <= 0 or canvas_height <= 0:
            return {"visual_balance_ratio": 1.0, "whitespace_pct": 100.0}

        canvas_area = canvas_width * canvas_height
        total_element_area = 0.0
        weighted_x = 0.0
        weighted_y = 0.0

        for el in elements:
            x = float(el.get("x", 0.0))
            y = float(el.get("y", 0.0))
            w = float(el.get("width", 50.0))
            h = float(el.get("height", 20.0))

            area = w * h
            x_mid = x + (w / 2.0)
            y_mid = y + (h / 2.0)

            total_element_area += area
            weighted_x += area * x_mid
            weighted_y += area * y_mid

        center_x = round(weighted_x / max(1.0, total_element_area), 2)
        center_y = round(weighted_y / max(1.0, total_element_area), 2)

        # Expected center of canvas
        ideal_cx = canvas_width / 2.0
        ideal_cy = canvas_height / 2.0

        # Offset normalized
        dx = abs(center_x - ideal_cx) / ideal_cx
        dy = abs(center_y - ideal_cy) / ideal_cy
        balance_score = round(max(0.0, 1.0 - math.sqrt((dx**2 + dy**2) / 2.0)), 3)

        whitespace_pct = round(max(0.0, (canvas_area - total_element_area) / canvas_area * 100.0), 1)

        return {
            "center_of_visual_mass": {"x": center_x, "y": center_y},
            "ideal_center": {"x": ideal_cx, "y": ideal_cy},
            "balance_score": balance_score,
            "whitespace_percentage": whitespace_pct,
            "balance_classification": "OPTIMALLY_CENTERED" if balance_score >= 0.8 else "ASYMMETRICAL_UNBALANCED"
        }
