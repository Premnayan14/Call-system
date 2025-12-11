# core/syscalls.py

import os
import subprocess
import platform
import psutil  # install via: pip install psutil


class SyscallEngine:
    """Simulates privileged system-call operations with controlled behavior."""

    @staticmethod
    def read_file(path):
        if not os.path.exists(path):
            return False, "File does not exist."

        try:
            with open(path, "r") as file:
                content = file.read()
            return True, content
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def write_file(path, text):
        try:
            with open(path, "w") as file:
                file.write(text)
            return True, "File written successfully."
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def list_processes():
        try:
            processes = []
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                processes.append(f"{proc.info['pid']} — {proc.info['name']}")
            return True, "\n".join(processes)
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def spawn_process(command):
        try:
            subprocess.Popen(command.split())
            return True, f"Process '{command}' started successfully."
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def ping_host(host):
        try:
            result = os.popen(f"ping -n 1 {host}").read()
            return True, result
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def system_info():
        try:
            info = {
                "OS": platform.system(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "CPU Cores": psutil.cpu_count(),
                "Memory": f"{psutil.virtual_memory().total // (1024**2)} MB",
            }

            formatted = "\n".join(f"{k}: {v}" for k, v in info.items())
            return True, formatted
        except Exception as exc:
            return False, str(exc)
