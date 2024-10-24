import shutil
import subprocess

def run_pyinstaller(main_script, spec_fn, icon_fn, is_debug):
    print(f"\nPyInstaller-0 is started.")
    command_0 = ["pyinstaller", "-y", "-i", icon_fn]
    if is_debug: command_0.append("-c")
    command_0.append(main_script)
    result = subprocess.run(command_0, capture_output=True, text=True)
    if result.returncode != 0: print(f"Error during PyInstaller-0: {result.stderr}")
    else: print(f"PyInstaller-0 successful: {result.stdout}")
    if not is_debug:
        with open(spec_fn, 'r', encoding='utf8') as f: spec_text = f.read()
        spec_text = spec_text.replace('console=True', 'console=False')
        with open(spec_fn, 'w', encoding='utf8') as f: f.write(spec_text)
    print(f"PyInstaller-1 is started.")
    command_1 = ["pyinstaller", "-y", spec_fn]
    result = subprocess.run(command_1, capture_output=True, text=True)
    if result.returncode != 0: print(f"Error during PyInstaller-1: {result.stderr}")
    else: print(f"PyInstaller-1 successful: {result.stdout}")
    print("\n")

def main(): 
    app_proj_name = "ER-SFXRecolorTool"
    app_py_fn = f"{app_proj_name}.py"
    app_spec_fn = f"{app_proj_name}.spec"
    app_icon_fn = "builder/recolor_icon.ico"
    is_debug = True
    run_pyinstaller(app_py_fn, app_spec_fn, app_icon_fn, is_debug)
    from_fp = "examples"
    to_fp = f"dist/{app_proj_name}/{from_fp}"
    shutil.copytree(from_fp, to_fp)

if __name__ == '__main__': main()
