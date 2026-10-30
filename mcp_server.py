# -*- coding: utf-8 -*-
"""
GenPark Vision Coder MCP Server
FastMCP standard interface for visual layout parsing and Tailwind CSS AST synthesis.
"""

import json
from typing import Dict, Any, List
from client import GenParkVisionCoder

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("genpark-vision-coder")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("genpark-vision-coder")

vc = GenParkVisionCoder()

@mcp.tool()
def parse_bounding_boxes_to_flexbox_hierarchy(
    elements: List[Dict[str, Any]]
) -> str:
    """
    Parses visual UI bounding boxes into an ordered Flexbox hierarchy.
    """
    res = vc.parse_bounding_boxes_to_flexbox_hierarchy(elements)
    return json.dumps(res, indent=2)

@mcp.tool()
def synthesize_tailwind_css_dom_ast(
    hierarchy_tree: List[Dict[str, Any]]
) -> str:
    """
    Translates resolved Flexbox hierarchy into semantic HTML strings with Tailwind CSS classes.
    """
    res = vc.synthesize_tailwind_css_dom_ast(hierarchy_tree)
    return json.dumps(res, indent=2)

@mcp.tool()
def evaluate_visual_hierarchy_balance(
    elements: List[Dict[str, Any]],
    canvas_width: float = 1200.0,
    canvas_height: float = 800.0
) -> str:
    """
    Evaluates visual balance, whitespace ratio, and center-of-mass coordinates.
    """
    res = vc.evaluate_visual_hierarchy_balance(elements, canvas_width, canvas_height)
    return json.dumps(res, indent=2)

def main():
    print("Testing Vision Coder:")
    sample = [{"type": "title", "text": "Dashboard", "x": 50, "y": 40, "width": 200, "height": 30}]
    print(parse_bounding_boxes_to_flexbox_hierarchy(sample))

if __name__ == "__main__":
    main()
