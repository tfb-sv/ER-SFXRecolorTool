import os
import sys
import json
from pathlib import Path
from tkinter import filedialog, messagebox

from utils.utils_common import tool_path_add_dct
from utils.utils_download import download_Witchy, download_ME2, download_UXM

def fix_tools_path_procedure(is_correct_all_lst, all_paths, config_fn, info_label):
    [is_ER_correct, is_UXM_correct, is_Witchy_correct, is_ME2_correct] = is_correct_all_lst
    [elden_ring_abs_path, _, witchyBND_path, mod_abs_path] = all_paths
    if not is_ER_correct:
        elden_ring_abs_path = make_user_choose_tool_path("Elden Ring")
    if not is_UXM_correct:
        messagebox.showinfo(
            title="UXM Selective Unpack Required",
            message="Download UXM Selective Unpack from the page that opens and UNPACK the game before restarting the tool. Exiting the tool."
        )
        download_UXM()
        sys.exit(0)
    if not is_Witchy_correct:
        witchyBND_path = make_user_choose_tool_path("WitchyBND", download_Witchy, info_label)
    if not is_ME2_correct:
        mod_abs_path = make_user_choose_tool_path("ModEngine2", download_ME2, info_label)
    config = {
        "elden_ring_abs_path": elden_ring_abs_path,
        "witchyBND_abs_path": witchyBND_path,
        "mod_abs_path": mod_abs_path
    }
    with open(config_fn, "w", encoding="utf8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)   # indirilen ME2 ile calisir mi!

def check_tool_path_correct(tool_name, tool_fp):
    if tool_name == "ModEngine2":
        tool_check_path = tool_fp
        if not os.path.exists(tool_check_path): return False   # mod folder
        tool_fp = str(Path(tool_fp).parent).replace("\\", "/")
        tool_path_add = tool_path_add_dct[tool_name]
        tool_check_path = f"{tool_fp}/{tool_path_add}"
        if not os.path.exists(tool_check_path): return False   # parent folder
        return True
    else:
        tool_path_add = tool_path_add_dct[tool_name]
        tool_check_path = f"{tool_fp}/{tool_path_add}"
        if not os.path.exists(tool_check_path): return False
        return True

def make_user_choose_tool_path(tool_name, download_function=None, info_label=None):
    is_abort = False
    yesno_msg_text = f"Does {tool_name} exist on your computer?"
    if tool_name != "ModEngine2": 
        yesno_msg_text += " If yes, please select the folder of it."
        dir_title_text = f"Select the {tool_name} folder"
    else: 
        yesno_msg_text += " If yes, please select the mod folder that you NORMALLY use." 
        dir_title_text = f"Select the {tool_name} mod folder"
    exists = messagebox.askyesno(title=f"{tool_name} Availability",
                                 message=yesno_msg_text)
    if exists:
        tool_fp = filedialog.askdirectory(title=dir_title_text,
                                          initialdir=".")
        tool_fp = tool_fp.replace("\\", "/")
        is_tool_correct = check_tool_path_correct(tool_name, tool_fp)
        if is_tool_correct: return tool_fp
        else: 
            # you selected a wrong folder, please chose a correct one.
            is_abort = True
    else:
        if download_function:
            download_msg_text = f"Would you like to download {tool_name}? The tool will automatically handle everything for you."
            download = messagebox.askyesno(title=f"Download {tool_name}",
                                           message=download_msg_text)
            if download: 
                info_text = f"Downloading {tool_name}.."
                info_label.configure(text=info_text)
                tool_fp, version = download_function()
                info_text = f"{tool_name} was downloaded successfully."
                info_label.configure(text=info_text)
            else: is_abort = True
        else: is_abort = True
    if is_abort:
        messagebox.showerror(title=f"{tool_name} Required",
                             message=f"{tool_name} is required to proceed. Exiting the tool.")
        sys.exit(0)
    return tool_fp

def main(config_fn, info_label):
    if not os.path.exists(config_fn):   # burayi bi test etmeli
        is_ER_correct = False
        is_UXM_correct = False
        is_Witchy_correct = False
        is_ME2_correct = False
        all_paths = ["", "", "", ""]
    else: 
        with open(config_fn, "r", encoding="utf8") as f: config = json.load(f)
        elden_ring_abs_path = config.get("elden_ring_abs_path", "").replace("\\", "/")
        mod_abs_path = config.get("mod_abs_path", "").replace("\\", "/")
        witchyBND_path = config.get("witchyBND_abs_path", "").replace("\\", "/")
        is_ER_correct = check_tool_path_correct("Elden Ring", elden_ring_abs_path)
        # uxm path icin yeni secileni vermeli!!
        is_UXM_correct = check_tool_path_correct("UXM Selective Unpacker", elden_ring_abs_path)
        is_Witchy_correct = check_tool_path_correct("WitchyBND", witchyBND_path)
        is_ME2_correct = check_tool_path_correct("ModEngine2", mod_abs_path)
        all_paths = [elden_ring_abs_path, "", witchyBND_path, mod_abs_path]
    is_correct_all_lst = [is_ER_correct, is_UXM_correct, is_Witchy_correct, is_ME2_correct]
    if not all(is_correct_all_lst):
        fix_tools_path_procedure(is_correct_all_lst, all_paths, config_fn, info_label)
