
import os
import subprocess
import shutil

def main(config, out_name, exe_path):
    apps = config.get('Settings', 'Apps', fallback='')
    apps_list = str([app.strip().lower() for app in apps.split(',')])
    password = config.get('Settings', 'Password', fallback='')

    with open("main.py", "r") as f:
        content = f.read()

    content = content.replace('["REPLACE_APPS"]', apps_list)
    content = content.replace('"REPLACE_PASSWORD"', f'"{password}"')

    with open("temp.py", "w") as f:
        f.write(content)

    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--log-level", "WARN",
        f"--name={out_name}",
        "temp.py"
    ])

    shutil.copy(os.path.join("dist", f"{out_name}.exe"), exe_path)
