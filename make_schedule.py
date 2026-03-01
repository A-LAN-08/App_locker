
import ctypes

def main(out_name, exe_path):
    ps_script = f"""
    $action = New-ScheduledTaskAction -Execute '{exe_path}'
    $trigger = New-ScheduledTaskTrigger -AtLogon
    $principal = New-ScheduledTaskPrincipal -GroupId "S-1-5-32-545" -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

    Register-ScheduledTask -TaskName "{out_name}" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    """

    print("Requesting Admin for Task Scheduler...")
    result = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", "powershell.exe", f"-NoProfile -WindowStyle Hidden -Command {ps_script}", None, 1
    )

    if result > 32:
        print("PowerShell: Task registered successfully.")
    else:
        print("PowerShell error.")
