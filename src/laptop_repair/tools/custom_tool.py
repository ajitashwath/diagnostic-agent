import subprocess
import platform
import os
import tempfile
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

def _get_allowed_commands():
    if platform.system() == "Windows":
        return [
            "systeminfo",
            "tasklist",
            "wmic process get name,commandline,processid",
            "wmic logicaldisk get size,freespace,caption",
            "wmic memorychip get capacity,speed,manufacturer",
            "wmic cpu get name,maxclockspeed,numberofcores",
            "netstat -an",
            "ipconfig /all",
            "sfc /verifyonly",
            "dism /online /cleanup-image /checkhealth",
            "powercfg /batteryreport",
            "wmic startup get caption,command,location",
            "wmic service where state='running' get name,displayname,processid",
            "dir %temp% /a",
            "wmic qfe list brief",
            "bcdedit /enum",
            "wmic diskdrive get status,size,model",
            "wmic temperature get currenttemperature",
            "wmic computersystem get totalphysicalmemory",
            "powershell Get-EventLog -LogName System -EntryType Error -Newest 10",
            "powershell Get-WmiObject -Class Win32_PhysicalMemory",
            "powershell Get-WmiObject -Class Win32_LogicalDisk",
        ]
    else:
        return [
            "uname -a",
            "lscpu",
            "free -h",
            "df -h",
            "lsblk",
            "ps aux",
            "netstat -tuln",
            "ifconfig",
            "dmesg | tail -20",
            "journalctl -xe --no-pager -n 10",
            "systemctl --failed",
            "top -bn1 | head -20",
            "lsusb",
            "lspci",
        ]

def _get_safe_fix_commands():
    if platform.system() == "Windows":
        return {
            "disk_cleanup": [
                "cleanmgr /sagerun:1",
                "del /q /f %temp%\\*.*",
                "rd /s /q %temp%",
                "md %temp%",
                "powershell Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
            ],
            "system_files": [
                "sfc /scannow",
                "dism /online /cleanup-image /restorehealth"
            ],
            "restart_services": [
                "net stop spooler & net start spooler",
                "net stop bits & net start bits",
                "net stop wuauserv & net start wuauserv",
                "net stop cryptsvc & net start cryptsvc"
            ],
            "network_reset": [
                "ipconfig /flushdns",
                "netsh winsock reset",
                "netsh int ip reset",
                "netsh advfirewall reset"
            ],
            "performance_boost": [
                "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                "defrag c: /o",
                "powershell Optimize-Volume -DriveLetter C -ReTrim"
            ],
            "registry_cleanup": [
                "reg delete HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v tempentry /f",
                "powershell Clear-Variable -Name * -ErrorAction SilentlyContinue"
            ],
            "windows_update": [
                "powershell Install-Module PSWindowsUpdate -Force",
                "powershell Get-WUInstall -AcceptAll -AutoReboot"
            ]
        }
    else:
        return {
            "system_cleanup": [
                "sudo apt-get clean",
                "sudo apt-get autoremove",
                "sudo journalctl --vacuum-time=3d"
            ],
            "system_update": [
                "sudo apt-get update",
                "sudo apt-get upgrade -y"
            ],
            "service_restart": [
                "sudo systemctl restart networking",
                "sudo systemctl restart NetworkManager"
            ],
            "disk_check": [
                "sudo fsck -f /dev/sda1",
                "sudo e2fsck -f /dev/sda1"
            ]
        }

class SystemCommandInput(BaseModel):
    command: str = Field(description=f"The specific, safe command to execute. Must be one of the approved diagnostic commands or 'get_fix_commands' to retrieve available fix commands.")

class SystemCommandTool(BaseTool):
    name: str = "System Diagnostic Command Executor"
    description: str = """
    Executes safe, read-only system diagnostic commands to gather system information for analysis.
    Supports Windows, Linux, and macOS. Can also provide safe fix commands for script generation.
    Use 'get_fix_commands' to retrieve available repair commands.
    """
    args_schema: Type[BaseModel] = SystemCommandInput

    def _run(self, command: str) -> str:
        try:
            if command.lower() == "get_fix_commands":
                fix_commands = _get_safe_fix_commands()
                result = f"Available safe fix command categories for {platform.system()}:\n\n"
                for category, commands in fix_commands.items():
                    result += f"{category.upper().replace('_', ' ')}:\n"
                    for cmd in commands:
                        result += f"  - {cmd}\n"
                    result += "\n"
                return result

            allowed_commands = _get_allowed_commands()
            command_allowed = False
            for allowed_cmd in allowed_commands:
                if command.lower().startswith(allowed_cmd.lower().split()[0]):
                    command_allowed = True
                    break
                    
            if not command_allowed:
                return f"Error: The command '{command}' is not permitted for security reasons.\n\nAllowed commands for {platform.system()}:\n" + "\n".join(f"  - {cmd}" for cmd in allowed_commands)

            if command.lower().startswith("powershell "):
                if platform.system() == "Windows":
                    ps_command = command[11:]
                    full_command = ["powershell", "-Command", ps_command]
                else:
                    return "Error: PowerShell commands are only available on Windows systems."
            else:
                full_command = command

            if platform.system() == "Windows":
                if isinstance(full_command, str):
                    process = subprocess.Popen(
                        full_command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                else:
                    process = subprocess.Popen(
                        full_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
            else:
                process = subprocess.Popen(
                    full_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )

            try:
                stdout, stderr = process.communicate(timeout=180)
            except subprocess.TimeoutExpired:
                process.kill()
                return f"Error: The command '{command}' timed out after 180 seconds."

            if process.returncode != 0 and stderr:
                if stdout:
                    return f"Command completed with warnings.\nWarnings: {stderr.strip()}\n\nOutput:\n{stdout}"
                else:
                    return f"Command failed with error: {stderr.strip()}"

            if stdout.strip():
                return f"--- Command Output for '{command}' ---\nSystem: {platform.system()} {platform.release()}\n\n{stdout}"
            else:
                return f"Command '{command}' executed successfully but returned no output."

        except FileNotFoundError:
            return f"Error: The command '{command}' was not found on this system. This may indicate the required tool is not installed."
        except PermissionError:
            return f"Error: Permission denied executing '{command}'. This command may require administrator/root privileges."
        except Exception as e:
            return f"An unexpected error occurred while running '{command}': {str(e)}"

    def get_system_info(self) -> str:
        """Get basic system information for debugging purposes."""
        try:
            info = {
                "OS": platform.system(),
                "OS Version": platform.release(),
                "Architecture": platform.machine(),
                "Processor": platform.processor(),
                "Python Version": platform.python_version(),
            }
            
            result = "=== System Information ===\n"
            for key, value in info.items():
                result += f"{key}: {value}\n"
            
            return result
        except Exception as e:
            return f"Unable to retrieve system information: {str(e)}"

    def get_safe_fix_commands(self):
        return _get_safe_fix_commands()

    def validate_command_safety(self, command: str) -> bool:
        allowed_commands = _get_allowed_commands()
        return any(command.lower().startswith(allowed_cmd.lower().split()[0]) 
                  for allowed_cmd in allowed_commands)

    def get_os_specific_diagnostics(self) -> str:
        os_name = platform.system()
        
        if os_name == "Windows":
            return """
Windows-specific diagnostic commands available:
- systeminfo: Complete system configuration
- tasklist: Running processes
- wmic: Windows Management Interface queries
- sfc /verifyonly: System file integrity check
- dism: Windows image management
- powercfg: Power configuration analysis
- Event log queries via PowerShell
            """
        elif os_name == "Linux":
            return """
Linux-specific diagnostic commands available:
- uname -a: Kernel and system information
- lscpu: CPU information
- free -h: Memory usage
- df -h: Disk space usage
- systemctl: Service status
- journalctl: System logs
- dmesg: Kernel messages
            """
        elif os_name == "Darwin":
            return """
macOS-specific diagnostic commands available:
- system_profiler: Hardware information
- top: Process information
- df -h: Disk usage
- netstat: Network connections
- launchctl: Service management
- Console app logs via command line
            """
        else:
            return f"Unknown operating system: {os_name}. Limited diagnostic capabilities available."