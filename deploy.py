
import os
import shutil
import configparser

def main():
    import build_exe
    import make_schedule

    print("Reading settings...")
    config = configparser.ConfigParser()
    config.read('settings.ini')

    out_name = config.get('Settings', 'OutputName', fallback='').replace(" ", "")
    dest_folder = rf"C:\ProgramData\{out_name}"
    os.makedirs(dest_folder, exist_ok=True)
    exe_path = os.path.join(dest_folder, f"{out_name}.exe")

    print("Creating exe...")
    build_exe.main(config, out_name, exe_path)

    print("Adding to startup schedule...")
    make_schedule.main(out_name, exe_path)

    print("Removing residual files...")
    os.remove("temp.py")
    os.remove(f"{out_name}.spec")
    shutil.rmtree("build")
    shutil.rmtree("dist")

    config.set('Settings', 'Apps', 'firefox.exe,discord.exe')
    config.set('Settings', 'Password', 'password123')
    config.set("Settings", "OutputName", "WinSystemHost")
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    print(f"\nSuccess! {out_name}.exe is now standalone in {rf'C:\ProgramData\{out_name}'}.")
    input("Press any key to continue...")

if __name__ == "__main__":
    main()




