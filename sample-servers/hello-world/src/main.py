from fastmcp import FastMCP

# The name given here is what the gateway reports back to clients as
# io.modelcontextprotocol/serverInfo, so pick something identifiable.
app = FastMCP("Hello World Server")


@app.tool()
def say_hello(name: str = "World") -> str:
    """Greet someone by name."""
    print(f"[hello-world] say_hello({name})")
    return f"Hello, {name}!"


@app.resource("greeting://default")
def default_greeting() -> str:
    """The greeting used when no name is supplied."""
    return "Hello, World!"
