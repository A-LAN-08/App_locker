
import ctypes
import sys
import os
import subprocess

def main(out_name, exe_path):
    # admin_check()

    ps_script = f"""
    $action = New-ScheduledTaskAction -Execute '{exe_path}'
    $trigger = New-ScheduledTaskTrigger -AtLogon
    $principal = New-ScheduledTaskPrincipal -GroupId "S-1-5-32-545" -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

    Register-ScheduledTask -TaskName "{out_name}" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    """

    # result = subprocess.run(
    #     ["powershell", "-NoProfile", "-Command", ps_script],
    #     capture_output=True,
    #     text=True
    # )

    single_line_ps = f"-NoProfile -WindowStyle Hidden -Command {ps_script}"

    print("Requesting Admin for Task Scheduler...")
    result = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", "powershell.exe", single_line_ps, None, 1
    )

    if result > 32:
        print("PowerShell: Task registered successfully.")
    else:
        print("PowerShell error.")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin_privileges():
    try:
        script_path = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])

        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script_path}" {params}', None, 1
        )
        return result > 32  # Success if result > 32
    except Exception as e:
        print("Error:", str(e))
        return False

def admin_check():
    if not is_admin():
        success = request_admin_privileges()
        if success:
            print("Requested admin privileges. Relaunching...")
            sys.exit(0)
        else:
            print("Admin privilege request was denied.")
            input("Press enter to exit...")
            sys.exit(1)

    else:
        print("Running with admin privileges!")

