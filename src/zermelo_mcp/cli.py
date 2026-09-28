"""CLI entry point for Zermelo MCP Server."""

import argparse
import sys
from zermelo_mcp.server import app


def main() -> None:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Zermelo Model Context Protocol (MCP) Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport type to use (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address for SSE server (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for SSE server (default: 8000)",
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        app.run(transport="stdio")
    else:
        app.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
