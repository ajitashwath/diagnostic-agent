# Windows System Diagnostic Agent
An AI-powered system diagnostic tool that uses CrewAI agents to analyze Windows system problems and generate automated fix scripts. The agent investigates system issues through safe diagnostic commands and creates customized batch scripts to resolve identified problems.

![Diagnostic Agent](https://i.ibb.co/k2XFxJJd/Screenshot-2025-08-10-143107.png)

## Features
- **AI-Powered Diagnosis**: Uses Google Gemini LLM through CrewAI framework for intelligent system analysis
- **Safe Command Execution**: Only executes read-only, non-destructive diagnostic commands
- **Automated Fix Generation**: Creates Windows batch scripts tailored to identified issues
- **User-Friendly GUI**: Tkinter-based interface with step-by-step workflow
- **Comprehensive System Analysis**: Covers hardware, software, network, and performance issues
- **Multi-Platform Support**: Primary focus on Windows with basic Linux/macOS compatibility

## Architecture
The system uses a multi-agent architecture:
- **Lead Diagnostician Agent**: Orchestrates diagnosis, analyzes data, creates fix scripts
- **System Command Executor Tool**: Executes safe diagnostic commands and returns raw output
- **GUI Interface**: Manages user interaction and displays results

## Prerequisites
- **Python 3.8+**
- **Windows OS** (primary target, basic support for Linux/macOS)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

## Installation
### Method 1: Use Pre-built Executable (Recommended)
1. Download the latest release
2. Run `installer.bat` as Administrator for system-wide installation
3. Or use `launch.bat` for portable execution

### Method 2: Install from Source
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ajitashwath/diagnostic-agent.git
   cd diagnostic-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API key**:
   ```bash
   set GEMINI_API_KEY=your_api_key_here
   ```
   Or export on Linux/macOS:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### GUI Application

1. **Launch the application**:
   ```bash
   python main_gui.py
   ```

2. **Enter your Gemini API key** in the provided field
3. **Describe your problem** in detail (e.g., "My computer is running slowly and the fan is always loud")
4. **Click "Diagnose My System"** and wait for analysis
5. **Review the diagnosis results**
6. **Approve script generation** if you want an automated fix
7. **Save and run the generated batch script** as Administrator

### Command Line Interface

```bash
python src/laptop_repair/main.py "My computer keeps freezing randomly"
```

## Building Executable

Use the provided build script to create a standalone executable:

```bash
python build_exe.py
```

This creates:
- `dist/WindowsSystemDiagnostic.exe` - Main executable
- `installer.bat` - System installer
- `uninstaller.bat` - Removal tool
- `launch.bat` - Portable launcher

## Project Structure

```
├── main_gui.py                    # Main GUI application
├── build_exe.py                   # Executable build script
├── src/laptop_repair/
│   ├── crew.py                    # CrewAI orchestration
│   ├── main.py                    # CLI interface
│   ├── config/
│   │   ├── agents.yaml           # Agent configurations
│   │   └── tasks.yaml            # Task definitions
│   └── tools/
│       └── custom_tool.py        # System command executor
├── installer.bat                 # Windows installer
├── uninstaller.bat              # Windows uninstaller
└── launch.bat                   # Portable launcher
```

## Diagnostic Capabilities

### Windows Commands
- **System Info**: `systeminfo`, `wmic` queries
- **Process Analysis**: `tasklist`, process monitoring
- **Hardware Diagnostics**: CPU, memory, disk status
- **Network Analysis**: `netstat`, `ipconfig`
- **File System**: `sfc /verifyonly`, DISM health checks
- **Performance**: Power settings, startup programs
- **Event Logs**: System and application errors

### Generated Fix Scripts
- **System Cleanup**: Temp file removal, disk cleanup
- **System Repair**: SFC scans, DISM repairs
- **Service Management**: Restart critical services
- **Network Reset**: DNS flush, Winsock reset
- **Performance Optimization**: Power settings, defragmentation
- **Registry Maintenance**: Safe registry operations
- **Windows Updates**: Automated update installation

## Configuration
### Agent Configuration (`agents.yaml`)
- **Lead Diagnostician**: Main analysis agent
- **Command Executor**: System command execution

### Task Configuration (`tasks.yaml`)
- **System Analysis**: Complete diagnostic workflow
- **Command Execution**: Individual command tasks

### Environment Variables
- `GEMINI_API_KEY`: Required for AI functionality

## Safety Features
- **Command Whitelist**: Only approved, safe commands allowed
- **Read-Only Operations**: No destructive commands during diagnosis
- **User Confirmation**: Scripts require explicit user approval
- **Administrator Check**: Critical operations require elevated privileges
- **Error Handling**: Comprehensive exception management
- **Timeout Protection**: Commands automatically timeout after 180 seconds

## Supported Diagnostic Scenarios

- **Performance Issues**: Slow boot, high CPU/memory usage
- **Hardware Problems**: Overheating, hardware failures
- **Network Connectivity**: Internet issues, DNS problems
- **System Crashes**: BSOD analysis, stability issues
- **Software Conflicts**: Application errors, service failures
- **Disk Problems**: Storage issues, file system errors
- **Security Concerns**: Malware symptoms, suspicious activity

## Troubleshooting
### Common Issues

**"Gemini API Key not found"**
- Ensure API key is set in environment or GUI
- Verify key is valid and has proper permissions

**"Command not permitted"**
- Tool only allows safe, predefined commands
- Check `custom_tool.py` for allowed command list

**"Build failed"**
- Install PyInstaller: `pip install pyinstaller`
- Ensure all source files are present
- Check Python version compatibility

**"Script execution failed"**
- Run batch scripts as Administrator
- Check Windows execution policy
- Verify system permissions

### Debug Mode

Enable verbose logging by setting:
```bash
set CREW_DEBUG=true
```

## API Usage
The tool integrates with Google Gemini API for AI-powered analysis. Ensure you have:
- Valid API key from Google AI Studio
- Sufficient API quota for analysis requests
- Network connectivity for API calls

## Security Considerations
- **Limited Command Set**: Only safe diagnostic commands allowed
- **No Destructive Operations**: Read-only analysis mode
- **User Approval Required**: Scripts need explicit permission
- **API Key Protection**: Keys masked in GUI, stored as environment variables
- **Local Processing**: System data processed locally when possible

## Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### Development Setup
```bash
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

## Support
For issues and questions:
1. Check the troubleshooting section above
2. Review the diagnostic output for error messages
3. Ensure all prerequisites are met
4. Verify API key configuration

## Disclaimer
This tool generates automated system repair scripts. While designed with safety in mind:
- Always backup important data before running repair scripts
- Test scripts in safe environments when possible
- Review generated code before execution
- Use at your own risk on production systems
