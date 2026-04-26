from fastmcp import Context, FastMCP
from adb_pywrapper.adb_device import AdbDevice

from utils import parse_adb_row
from datetime import datetime


mcp = FastMCP(name="MCP SMS Android reader", instructions="This server is used for reading sms from Android devices through ADB.")


@mcp.tool("list_all_android_devices_connected")
async def list_devices():
    """Tool for finding all Android devices connected to PC"""

    return { "devices_connected": AdbDevice.list_devices() }


@mcp.tool("read_all_sms")
async def read_all_sms(device_name: str, ctx: Context):
    """Given device_name in input as string, this tool returns all the sms stored in it."""

    try:
        device = AdbDevice(device=device_name)
    except Exception:
        return f"Error while trying to connect to device {device}. Is {device_name} connected or is the correct name?"
    
    result_command = device.shell("content query --uri content://sms/inbox")
    rows = result_command.stdout.split("Row: ")[1::]
    messages = {}

    for i, row in enumerate(rows):
        if len(row.strip()) > 0:
            ctx.report_progress(i, len(rows), "Processing sms...")
                
            m = parse_adb_row(row)
            messages[f"Message {i+1}"] = m 
    
    ctx.info(f"Read {len(messages)} messages.")
    return messages  


@mcp.tool("read_sms_between_dates")
async def read_sms_between_dates(start: datetime, end: datetime, device_name: str, ctx: Context):
    """Given start - end dates as datetime and device_name as string, this tool extracts all sms between this dates."""

    try:
        device = AdbDevice(device=device_name)
    except Exception:
        return f"Error while trying to connect to device {device}. Is {device_name} connected or is the correct name?"
    
    result_command = device.shell("content query --uri content://sms/inbox")
    rows = result_command.stdout.split("Row: ")[1::]

    messages = {}

    for i, row in enumerate(rows):
        if len(row.strip()) > 0:
            m = parse_adb_row(row)
            date = datetime.fromtimestamp(float(m['date']) / 1000 )
            if start <= date <= end:
                messages[f"Message {i+1}"] = m

    return messages

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
