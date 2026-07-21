__version__ = "0.1.0"

import asyncio

from agno.tools.mcp import MCPTools


async def main():
    print("=" * 65)
    print("US LEGAL MCP SERVER CONNECTION TEST")
    print("=" * 65)

    command = (
        r'node "C:\Users\Aks Raj Singh\us-legal-mcp\dist\index.js"'
    )

    mcp_tools = MCPTools(command=command)

    print("\n[1] Agno MCP client initialized")
    print(f"[2] Server command: {command}")
    print("[3] Opening stdio transport...")
    print("[4] Establishing MCP session...")

    try:
        await mcp_tools.connect()

        print("\n[SUCCESS] MCP SERVER CONNECTION ESTABLISHED")
        print("Transport : stdio")
        print("Client    : Agno MCPTools")
        print("Server    : JamesANZ US Legal MCP")

        print("\n[5] MCP tool discovery completed")
        print("\nDiscovered MCP tools:")

        if mcp_tools.functions:
            for tool_name in mcp_tools.functions.keys():
                print(f"  - {tool_name}")
        else:
            print("  No MCP tools discovered.")

        print("\n" + "=" * 65)
        print("MCP CONNECTION AND TOOL DISCOVERY VERIFIED")
        print("=" * 65)

    except Exception as error:
        print("\n[FAILED] MCP CONNECTION FAILED")
        print(f"Error type: {type(error).__name__}")
        print(f"Error: {error}")

    finally:
        try:
            await mcp_tools.close()
            print("\nMCP connection closed successfully.")
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())