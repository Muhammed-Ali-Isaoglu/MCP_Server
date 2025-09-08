from mcp.server.fastmcp import FastMCP
import os 

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

Note_file=os.path.join(os.path.dirname(__file__),'notes.txt')

def ensure():
    if not os.path.exists(Note_file):
        with open(Note_file,'w') as f:
            return f.write("")

@mcp.tool()

def add_note(message:str) -> str:
    ensure()
    with open(Note_file,'a') as f:
        f.write(f"{message} \n")
    return "Note_saved"

@mcp.tool()

def read_notes()->str:
    ensure()
    with open(Note_file,'r') as f:
        content=f.read().strip()
    return content or "no notes"

mcp.resource("notes://lastest")

def read_last_note()->str:
    ensure()
    with open(Note_file,'r') as f:
        lines=f.readlines()
    return lines[-1].strip() if lines else "NO Notes Exist"

mcp.prompt()

def summarize_notes()->str:
    ensure()
    with open(Note_file,'r') as f:
        content=f.read().strip()
    if not content:
        return "No notes exist"
    else:
        return f"summarize the current notes{content}"
if __name__ == "__main__":
    print("🚀 MCP server starting...")
    mcp.run()



