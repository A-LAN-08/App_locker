# App Locker

A lightweight application locker that prevents specific programs from running without a password. AppLocker registers itself as a high-privilege system task to ensure it stays active across reboots.

> [!WARNING]
> **Important Disclaimer:** This tool only blocks `.exe` files from starting. It **does not** encrypt your files or lock folders. If you need to protect sensitive data from being read, please use a dedicated encryption tool like BitLocker.

---

### How to Install

1. **Clone the Repository:** 
    Download the source code to your computer. GitHub may flag pre-built executables that edit system files, so building it yourself is the safest method.
   
2. **Install Dependencies:**
   Open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   
3. **Configure settings:** Open the `settings.ini` file in a text editor.
   - List the programs you want to block, leaving no white space e.g. firefox.exe,discord.exe.
   - Set your desired unlock password (defaults to password123 but CHANGE THIS).
   - (optional) change the output name of the exe to something inconspicuous. Defaults to WinSystemHost.
   - (optional) change whether a program's authorised status is reset when it is fully closed.

4. **Deploy:** Run `run.py` via your preferred method. It will prompt for admin access when creating a schedule which is needed for the program to automatically run on Windows startup.

---

### Tips

- Once the deployment finishes successfully, I highly suggest deleting the source files from your desktop and recycling bin. Although the `settings.ini` file is reset after running, leaving these may hint to others that this app was run.
- If you want to run the deployment again for the same output name, ensure the previous task is completely killed via task manager otherwise the code will fail to run properly.
- If you change the name of the deployment and run it again, it will NOT delete the previous instance. To remove this you need to manually navigate to `C:\ProgramData\` and delete the folder name of the previous deployment.

---

### Troubleshooting
Before sending any issue requests check the following:
- **Dependencies:** Run  `pip install -r requirements` again to ensure the required libraries are installed.
- **Admin rights:** The task registration will fail if you deny the Admin prompt during deployment. This does not stop the exe from being prodceed, but it will not run automatically on startup.
- **No ghost processes:** Ensure no previous versions of the script are already running, as it can cause permission errors to over-write the old files.

---

### License

[MIT](https://choosealicense.com/licenses/mit/)

---

*Use this tool responsibly. The author is not responsible for any lost access to your applications or accidental lockouts.*
