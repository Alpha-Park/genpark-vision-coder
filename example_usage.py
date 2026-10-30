# -*- coding: utf-8 -*-
from client import GenParkVisionCoder

coder = GenParkVisionCoder()

elements = [
    {"id": "header_title", "type": "title", "text": "Analytics Overview", "x": 100, "y": 50, "width": 300, "height": 40},
    {"id": "search_input", "type": "input", "text": "Search metrics...", "x": 500, "y": 50, "width": 250, "height": 40},
    {"id": "export_btn", "type": "button", "text": "Export Report", "x": 800, "y": 50, "width": 150, "height": 40},
    {"id": "kpi_card", "type": "div", "text": "", "x": 100, "y": 150, "width": 850, "height": 200}
]

# 1. Flexbox Hierarchy
parsed = coder.parse_bounding_boxes_to_flexbox_hierarchy(elements)
print(f"Flexbox Hierarchy: Flow={parsed['layout_flow']} ({parsed['root_element_count']} root elements)")

# 2. Tailwind Code Generation
ast = coder.synthesize_tailwind_css_dom_ast(parsed['hierarchy'])
print()
print("Synthesized Tailwind HTML Snippet:")
print(ast['html_output'][:350] + "...")

# 3. Visual Balance & Whitespace
bal = coder.evaluate_visual_hierarchy_balance(elements, canvas_width=1000.0, canvas_height=600.0)
print()
print(f"Visual Balance: Score={bal['balance_score']} ({bal['balance_classification']}, Whitespace: {bal['whitespace_percentage']}%)")
