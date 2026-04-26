# mcp-sms-reader

An MCP (Model Context Protocol) server that lets AI assistants read SMS messages from Android devices over ADB (Android Debug Bridge). Built with [FastMCP](https://github.com/jlowin/fastmcp) and [adb-pywrapper](https://pypi.org/project/adb-pywrapper/).

---

## Prerequisites

### 1. ADB (Android Debug Bridge) installed on your machine

ADB must be installed and available in your system `PATH`.

- **Windows**: Download the [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) and add the extracted folder to your `PATH` environment variable.
- **macOS**: `brew install android-platform-tools`
- **Linux (Debian/Ubuntu)**: Download the [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) and add the extracted folder to your `PATH` environment variable.

Verify the installation:

```bash
adb version
```

### 2. Developer Options enabled on your Android device

1. Open **Settings** on your Android device.
2. Go to **About phone** (or **About device**).
3. Tap **Build number** seven times in quick succession until you see _"You are now a developer!"_.
4. Go back to **Settings** — a new **Developer options** menu will now be visible (usually under **System** or directly in Settings).

### 3. USB Debugging enabled on your Android device

1. Open **Settings > Developer options**.
2. Enable **USB Debugging**.
3. When prompted on the device, tap **Allow** to authorize the connected computer.

### 4. Device connected via USB

Connect your Android device to your computer using a USB cable. Confirm the device is recognized:

```bash
adb devices
```

Expected output:

```
List of devices attached
XXXXXXXXXXXXXXXX    device
```

If the status shows `unauthorized`, unlock your phone and accept the RSA key fingerprint prompt.

---

## Installation

This project uses [uv](https://github.com/astral-sh/uv) as the package manager.

```bash
# Clone the repository
git clone https://github.com/your-username/mcp-sms-reader.git
cd mcp-sms-reader

# Install dependencies
uv sync
```

**Python 3.14+** is required (see `pyproject.toml`).

---

## Running the server

```bash
uv run python server.py
```

The MCP server starts and listens for connections from any MCP-compatible client (e.g., Claude Desktop, Claude Code, or a custom agent).

---

## MCP Tools

### `list_all_android_devices_connected`

Lists all Android devices currently connected to the host machine via ADB.

**Parameters:** none

**Returns:**

```json
{
  "devices_connected": ["emulator-5554", "XXXXXXXXXXXXXXXX"]
}
```

Use this tool first to discover the exact device identifier needed for the other tools.

---

### `read_all_sms`

Reads all SMS messages from the inbox of a specific Android device.

**Parameters:**

| Name          | Type   | Description                                                         |
|---------------|--------|---------------------------------------------------------------------|
| `device_name` | string | The device identifier returned by `list_all_android_devices_connected` |

**Returns:**

A dictionary where each key is `"Message 1"`, `"Message 2"`, etc., and each value is a flat dictionary of SMS fields (e.g., `address`, `date`, `body`, `read`, `type`, and others).

Reports progress back to the MCP client as each message is processed.

---

### `read_sms_between_dates`

Reads all SMS messages received between two dates from the inbox of a specific Android device.

**Parameters:**

| Name          | Type     | Description                                                         |
|---------------|----------|---------------------------------------------------------------------|
| `device_name` | string   | The device identifier returned by `list_all_android_devices_connected` |
| `start`       | datetime | Start of the date range (inclusive)                                 |
| `end`         | datetime | End of the date range (inclusive)                                   |

**Returns:**

A dictionary where each key is `"Message 1"`, `"Message 2"`, etc., and each value is a flat dictionary of SMS fields for messages whose timestamp falls within the specified range.

---

### `read_first_n_sms`

Reads the first `n` SMS messages from the inbox of a specific Android device.

**Parameters:**

| Name          | Type   | Description                                                         |
|---------------|--------|---------------------------------------------------------------------|
| `device_name` | string | The device identifier returned by `list_all_android_devices_connected` |
| `n`           | int    | Number of messages to read from the beginning of the inbox          |

**Returns:**

A dictionary where each key is `"Message 1"`, `"Message 2"`, etc., and each value is a flat dictionary of SMS fields as stored by Android's content provider (e.g., `address`, `date`, `body`, `read`, `type`, and others).

**Example response:**

```json
{
  "Message 1": {
    "address": "+1234567890",
    "date": "1714123456789",
    "body": "Your OTP is 123456",
    "read": "1",
    "type": "1"
  },
  "Message 2": {
    "address": "ShortCode",
    "date": "1714000000000",
    "body": "Welcome to the service!",
    "read": "0",
    "type": "1"
  }
}
```

Reports progress back to the MCP client as each message is processed.

---

## Connecting to Claude Desktop

Add the server to your `claude_desktop_config.json`.

**Option A — dependencies installed globally**

If you installed the dependencies globally (or via `uv` without a local virtualenv), this is enough:

```json
{
  "mcpServers": {
    "mcp-sms-reader": {
      "command": "uv",
      "args": ["run", "/path/to/mcp-sms-reader/server.py"]
    }
  }
}
```

**Option B — local virtual environment (`.venv`)**

If you created a local virtual environment (e.g. with `uv sync` or `python -m venv .venv`), point `command` directly to the Python executable inside that environment and pass the full absolute path to `server.py` as the argument:

- **Windows**
```json
{
  "mcpServers": {
    "mcp-sms-reader": {
      "command": "C:\\path\\to\\mcp-sms-reader\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\mcp-sms-reader\\server.py"]
    }
  }
}
```

- **macOS / Linux**
```json
{
  "mcpServers": {
    "mcp-sms-reader": {
      "command": "/path/to/mcp-sms-reader/.venv/bin/python",
      "args": ["/path/to/mcp-sms-reader/server.py"]
    }
  }
}
```

Replace `/path/to/mcp-sms-reader` (or the Windows equivalent) with the actual absolute path to the cloned repository on your machine.

---

## Project structure

```
mcp-sms-reader/
├── server.py        # MCP server definition and tool handlers
├── utils.py         # ADB row parser
├── pyproject.toml   # Project metadata and dependencies
└── uv.lock          # Locked dependency tree
```

---

## Dependencies

| Package           | Purpose                                      |
|-------------------|----------------------------------------------|
| `fastmcp`         | MCP server framework                         |
| `adb-pywrapper`   | Python wrapper around the ADB CLI            |

---

## License

MIT
