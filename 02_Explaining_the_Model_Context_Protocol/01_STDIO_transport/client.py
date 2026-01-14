# client.py
import subprocess
import json

# . The client creates a server as a sub-process and ends up writing outgoing messages to
#   said processes via writing to stdin using the send_message method
# . Conversely, it listens to stdout for the child process (server) to send back responses with
#   the proc.stdout.readline() code

# This code is a great start to build on to start implementing MCP and the STDIO transport. In fact,
# this is pretty much what happens, except for the fact that MCP communicates with JSON-RPC messages.

# Start the child process
proc = subprocess.Popen(
    ["python3", "server_updated.py"], # Replace with your child script
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

list_tools_message = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}

message = "hello\n"

unknown_message = "hi this is unknown\n"

def send_message(message):
    """
    Send a message to the child process.
    """
    print(f"[CLIENT] Sending message to server... Message: {message.strip()}")
    proc.stdin.write(message)
    proc.stdin.flush()


def serialize_message(message):
    """
    Serialize a message to JSON format.
    """
    return json.dumps(message) + "\n"


# Send a message to the child
send_message(message)

# Read response from child
response = proc.stdout.readline()
print("[SERVER]:", response.strip())

# Send a JSON-RPC message
send_message(serialize_message(list_tools_message))

response = proc.stdout.readline()

print("[SERVER]:", response.strip())

# Send a message to the child
send_message(unknown_message)

# Read response from child
response = proc.stdout.readline()
print("[SERVER]:", response.strip())

# This closes down the child process aka server
send_message("exit\n")

proc.stdin.close()
exit_code = proc.wait()
print(f"Child exited with code {exit_code}")