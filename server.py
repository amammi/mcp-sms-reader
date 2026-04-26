from fastmcp import Context, FastMCP
from adb_pywrapper.adb_device import AdbDevice

from utils import parse_adb_row


mcp = FastMCP(name="MCP SMS Android reader", instructions="This server is used for reading sms from Android devices through ADB.")


@mcp.tool("list_all_android_devices_connected")
async def list_devices():
    """Tool for finding all Android devices connected to PC"""

    return { "devices_connected": AdbDevice.list_devices() }

@mcp.tool("read_first_n_sms")
async def read_first_n_sms(device_name: str, n: int, ctx: Context):
    """Given device_name as string, n as int number representing the number of first n sms to read, 
    this tool extracts the first n sms saved in Android device through ADB"""

    try:
        device = AdbDevice(device=device_name)
    except Exception:
        return f"Error while trying to connect to device {device}. Is {device_name} connected or is the correct name?"
    result_command = device.shell("content query --uri content://sms/inbox")
    rows = result_command.stdout.split("Row: ")[1::]
    messages = {}

    for i in range(n):
        row = rows[i]
        if len(row.strip()) > 0:
            ctx.report_progress(i, len(rows), "Processing sms...")
                
            m = parse_adb_row(row)
            messages[f"Message {i+1}"] = m    
    
    return messages

if __name__ == '__main__':
    mcp.run()
