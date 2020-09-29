from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna", "autoit", "steam", "google", "cryptography", "time", "os", "json", "subprocess", "base64", "sys"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "SteamAccountManager",
    options = options,
    version = "1.0",
    description = 'by st4ck3r',
    executables = executables
)