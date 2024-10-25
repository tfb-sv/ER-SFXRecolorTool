import os
import shutil
import argparse
import subprocess
from utils import app_proj_name, version_str

def run_pyinstaller(main_script, spec_fn, icon_fn, is_debug):
    print(f"\nPyInstaller is started with arguments..")
    command_args = ["pyinstaller", "-y", "--name", app_proj_name, "-i", icon_fn]
    if is_debug: command_args.append("-c")
    command_args.append(main_script)
    result = subprocess.run(command_args, capture_output=True, text=True)
    if result.returncode != 0: print(f"Error during PyInstaller with arguments: {result.stderr}")
    else: print(f"PyInstaller with arguments is successful: {result.stdout}")
    if not is_debug:
        with open(spec_fn, 'r', encoding='utf8') as f: spec_text = f.read()
        spec_text = spec_text.replace('console=True', 'console=False')
        with open(spec_fn, 'w', encoding='utf8') as f: f.write(spec_text)
    print("\n")
    print(f"PyInstaller is started with .SPEC file..")
    command_spec = ["pyinstaller", "-y", spec_fn]
    result = subprocess.run(command_spec, capture_output=True, text=True)
    if result.returncode != 0: print(f"Error during PyInstaller with .SPEC file: {result.stderr}")
    else: print(f"PyInstaller with .SPEC file is successful: {result.stdout}")
    print("\n")

def main(args): 
    app_py_fn = f"{app_proj_name.replace('-', '_')}.py"
    app_spec_fn = f"{app_proj_name}.spec"
    app_icon_fn = "builders/recolor_icon.ico"
    is_debug = args.is_debug

    will_deleted_folders = ["build", "dist", "utils/__pycache__", "__pycache__"]
    for delete_path in will_deleted_folders:
        if os.path.exists(delete_path): shutil.rmtree(delete_path)

    run_pyinstaller(app_py_fn, app_spec_fn, app_icon_fn, is_debug)

    from_fp = "examples"
    to_fp = f"dist/{app_proj_name}/{from_fp}"
    shutil.copytree(from_fp, to_fp)

    dist_folder = f"dist/{app_proj_name}"
    zip_fp = f"dist/{app_proj_name}-v{version_str}"
    if not is_debug: shutil.make_archive(output_filename, 'zip', dist_folder)

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--is_debug', action='store_true')
    args = parser.parse_args()
    main(args)
