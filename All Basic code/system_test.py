import sys
import subprocess

# --------------------------------------------------
# Utility: attempt to install missing packages
# --------------------------------------------------
def install_package(package_name):
    try:
        print(f"[INFO] Attempting to install '{package_name}'...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"[SUCCESS] Installed '{package_name}'")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to install '{package_name}': {e}")
        return False


# --------------------------------------------------
# Safe import with auto-fix
# --------------------------------------------------
def safe_import(module_name, pip_name=None):
    try:
        return __import__(module_name)
    except ImportError:
        print(f"[WARN] Module '{module_name}' not found.")
        pip_pkg = pip_name if pip_name else module_name
        if install_package(pip_pkg):
            try:
                return __import__(module_name)
            except Exception as e:
                print(f"[ERROR] Import failed after install: {e}")
        return None


# --------------------------------------------------
# Import required modules (auto-fix enabled)
# --------------------------------------------------
platform = safe_import("platform")
psutil = safe_import("psutil")
torch = safe_import("torch")


# --------------------------------------------------
# System Information Functions
# --------------------------------------------------
def get_system_info():
    try:
        print("\n=== SYSTEM INFORMATION ===")
        print(f"OS           : {platform.system()} {platform.release()}")
        print(f"OS Version   : {platform.version()}")
        print(f"Architecture : {platform.machine()}")
        print(f"Python       : {platform.python_version()}")
    except Exception as e:
        print(f"[ERROR] System info error: {e}")


def get_cpu_info():
    try:
        print("\n=== CPU INFORMATION ===")
        print(f"Processor     : {platform.processor()}")
        print(f"Physical Cores: {psutil.cpu_count(logical=False)}")
        print(f"Total Cores   : {psutil.cpu_count(logical=True)}")
        print(f"CPU Usage     : {psutil.cpu_percent(interval=1)} %")
    except Exception as e:
        print(f"[ERROR] CPU info error: {e}")


def get_memory_info():
    try:
        memory = psutil.virtual_memory()
        print("\n=== MEMORY (RAM) INFORMATION ===")
        print(f"Total RAM     : {memory.total / (1024**3):.2f} GB")
        print(f"Available RAM : {memory.available / (1024**3):.2f} GB")
        print(f"Used RAM      : {memory.used / (1024**3):.2f} GB")
        print(f"RAM Usage     : {memory.percent} %")
    except Exception as e:
        print(f"[ERROR] Memory info error: {e}")


def get_gpu_info():
    try:
        print("\n=== GPU INFORMATION ===")

        if torch is None:
            print("PyTorch not available. GPU info skipped.")
            return

        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")

        if cuda_available:
            print(f"CUDA Version  : {torch.version.cuda}")
            print(f"GPU Count     : {torch.cuda.device_count()}")

            for i in range(torch.cuda.device_count()):
                try:
                    name = torch.cuda.get_device_name(i)
                    props = torch.cuda.get_device_properties(i)
                    print(f"GPU {i} Name   : {name}")
                    print(f"  VRAM        : {props.total_memory / (1024**3):.2f} GB")
                except Exception as gpu_err:
                    print(f"[ERROR] GPU {i} detail error: {gpu_err}")
        else:
            print("No CUDA-capable GPU detected or CUDA not configured.")

    except Exception as e:
        print(f"[ERROR] GPU info error: {e}")


def get_disk_info():
    try:
        disk = psutil.disk_usage('/')
        print("\n=== DISK INFORMATION ===")
        print(f"Total Disk    : {disk.total / (1024**3):.2f} GB")
        print(f"Used Disk     : {disk.used / (1024**3):.2f} GB")
        print(f"Free Disk     : {disk.free / (1024**3):.2f} GB")
        print(f"Disk Usage    : {disk.percent} %")
    except Exception as e:
        print(f"[ERROR] Disk info error: {e}")


# --------------------------------------------------
# Main Execution (fully guarded)
# --------------------------------------------------
if __name__ == "__main__":
    try:
        get_system_info()
        get_cpu_info()
        get_memory_info()
        get_gpu_info()
        get_disk_info()
    except KeyboardInterrupt:
        print("\n[INFO] Execution interrupted by user.")
    except Exception as e:
        print(f"[FATAL ERROR] Unexpected failure: {e}")
