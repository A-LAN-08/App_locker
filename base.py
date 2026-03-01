
import psutil
import time
import ctypes

TARGET_APPS = ["REPLACE_APPS"]
PASSWORD = "REPLACE_PASSWORD"
RESET_ON_EXIT = "REPLACE_RESET"

CREDUI_MAX_PASSWORD_LENGTH = 256
CREDUI_FLAGS_GENERIC_CREDENTIALS = 0x1
CREDUI_FLAGS_ALWAYS_SHOW_UI = 0x8
CREDUI_FLAGS_DO_NOT_PERSIST = 0x2

def ask_password(app_name):
    username = (ctypes.c_wchar * 1024)()
    password = (ctypes.c_wchar * 1024)()
    auth_status = ctypes.c_bool(False)

    result = ctypes.windll.credui.CredUIPromptForCredentialsW(
        None,
        f"Security Check: {app_name}",
        None,
        0,
        username, 1024,
        password, 1024,
        ctypes.byref(auth_status),
        CREDUI_FLAGS_GENERIC_CREDENTIALS | CREDUI_FLAGS_ALWAYS_SHOW_UI | CREDUI_FLAGS_DO_NOT_PERSIST
    )

    if result == 0:
        return password.value
    return None

def monitor():
    authorized = set()

    while True:
        procs = [p for p in psutil.process_iter(['name']) if p.info['name'].lower() in TARGET_APPS]
        if not procs:
            if RESET_ON_EXIT:
                authorized = set()
            time.sleep(0.5)
            continue

        for name in list(authorized):
            if name not in [p.info['name'].lower() for p in procs] and RESET_ON_EXIT:
                authorized.remove(name)

        unauthorized = set()
        clean_proc = []
        for p in procs:
            try:
                if p.info["name"].lower() in authorized:
                    p.resume()
                    continue
                clean_proc.append(p)
                p.suspend()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        for proc in clean_proc:
            app_name = proc.info['name'].lower()
            if app_name in authorized: continue
            if app_name in unauthorized: continue

            if ask_password(app_name) == PASSWORD:
                proc.resume()
                authorized.add(app_name)
            else:
                [p.kill() for p in clean_proc if p.info['name'].lower() == app_name]
                unauthorized.add(app_name)

        time.sleep(0.5)


if __name__ == "__main__":
    monitor()