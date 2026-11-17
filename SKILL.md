---
name: genpark-vision-coder
description: Converts UI screenshots directly into clean HTML and Tailwind CSS code in seconds. No monthly subscription required.
---

# GenPark Vision Coder

Stop paying $15/mo for screenshot-to-code SaaS wrappers. This open-source visual agent turns UI mockups or screenshots into fully functional, responsive Tailwind HTML directly from your CLI.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Usage
`openclaw use genpark-vision-coder --image "ui-mockup.png"`

The agent will read the image, construct the DOM structure, write the Tailwind classes, and output a ready-to-use `index.html` file in your directory.
