import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox

from utils.utils_common import log, witchy_subprocess, custom_json_dumper
from utils.utils_download import download_Witchy, download_ME2, download_UXM

tool_path_add_dct = {"Elden Ring": "Game/eldenring.exe",
                     "UXM Selective Unpacker": "Game/sfx",
                     "WitchyBND": "launchmod_eldenring.bat",
                     "ModEngine2": "WitchyBND.exe"}

def first_controls(config_fn, mission_fn):
    # assert_config_text = f"\n>> The file {config_fn} could not be found in the tool directory. The tool is ABORTED.\n"
    assert_mission_text = f"\n>> The file {mission_fn} could not be found in the tool directory. The tool is ABORTED.\n"
    assert_length_text = f"\n>> There must be at least 1 SFX ID in the {mission_fn} file. The tool is ABORTED.\n"
    # assert os.path.exists(config_fn), assert_config_text
    check_tools_are_ready(config_fn)
    assert os.path.exists(mission_fn), assert_mission_text
    with open(mission_fn, "r", encoding="utf8") as f: mission_input = json.load(f)
    sfx_ids = mission_input["sfx_ids"]
    assert len(sfx_ids) > 0, assert_length_text
    suffix = "" if len(sfx_ids) == 1 else "s"
    return mission_input, sfx_ids, suffix

def check_tools_are_ready(config_fn):
    if not os.path.exists(config_fn): 
        is_ER_correct = False
        is_UXM_correct = False
        is_Witchy_correct = False
        is_ME2_correct = False
        all_paths = ["", "", "", ""]
    else: 
        with open(config_fn, "r", encoding="utf8") as f: config = json.load(f)
        elden_ring_abs_path = config.get("elden_ring_abs_path", "").replace("\\", "/")
        mod_abs_path = config.get("mod_abs_path", "").replace("\\", "/")
        mod_engine_abs_path = str(Path(mod_abs_path).parent).replace("\\", "/")
        witchyBND_path = config.get("witchyBND_abs_path", "").replace("\\", "/")
        if not witchyBND_path.endswith(".exe"): witchyBND_path += "/WitchyBND.exe"   # change this control later
        is_ER_correct = check_tool_path_correct("Elden Ring", elden_ring_abs_path)
        is_UXM_correct = check_tool_path_correct("UXM Selective Unpacker", elden_ring_abs_path)
        is_Witchy_correct = check_tool_path_correct("WitchyBND", witchyBND_path)   # exe'siz lazim!
        is_ME2_correct = check_tool_path_correct("ModEngine2", mod_engine_abs_path)
        all_paths = [elden_ring_abs_path, "", witchyBND_path, mod_engine_abs_path]
    is_correct_all_lst = [is_ER_correct, is_UXM_correct, is_Witchy_correct, is_ME2_correct]
    if not all(is_correct_all_lst):
        fix_tools_path_procedure(is_correct_all_lst, all_paths)

def fix_tools_path_procedure(is_correct_all_lst, all_paths):
    [is_ER_correct, is_UXM_correct, is_Witchy_correct, is_ME2_correct] = is_correct_all_lst
    if not is_ER_correct:
        elden_ring_abs_path = make_user_choose_tool_path("Elden Ring")
    if not is_UXM_correct:
        messagebox.showinfo(
            title="UXM Selective Unpack Required",
            message="Download UXM Selective Unpack from the page that opens and unpack the game before restarting the tool.\n\nThe tool is aborted."
        )
        download_UXM()
        sys.exit(0)
    if not is_Witchy_correct:
        witchyBND_path = make_user_choose_tool_path("WitchyBND", download_Witchy)
    if not is_ME2_correct:
        mod_abs_path = make_user_choose_tool_path("ModEngine2", download_ME2)
    # tum paths kaydet json

def check_tool_path_correct(tool_name, tool_fp):
    tool_path_add = tool_path_add_dct[tool_name]
    tool_check_path = f"{tool_fp}/{tool_path_add}"
    if not os.path.exists(tool_check_path): return False
    else: return True

def make_user_choose_tool_path(tool_name, download_function=None):
    is_abort = False
    exists = messagebox.askyesno(
        title=f"{tool_name} Availability",
        message=f"Does {tool_name} already exist on your computer? If yes, please select the folder of it."
    )
    if exists:
        tool_fp = filedialog.askdirectory(
            title=f"Select the {tool_name} folder",
            initialdir="."
        )
        tool_fp = tool_fp.replace("\\", "/")
        is_tool_correct = check_tool_path_correct(tool_name, tool_fp)
        if is_tool_correct: return tool_fp
        else: is_abort = True
    else:
        if download_function:
            download = messagebox.askyesno(
                title=f"Download {tool_name}",
                message=f"Would you like to download {tool_name}? This process will automatically handle everything for you."
            )
            if download: tool_fp, version = download_function(tool_name)
            else: is_abort = True
        else: is_abort = True
    if is_abort:
        messagebox.showerror(
        title=f"{tool_name} Required",
        message=f"{tool_name} is required to proceed. Exiting the tool."
        )
        sys.exit(0)
    return tool_fp

def initialize_paths(config_fn):
    with open(config_fn, "r", encoding="utf8") as f: config = json.load(f)
    dcx2folder_dct = obtain_all_sfx_files()
    sfx_tmp_path = "sfx"
    graph_path = "sfx_palettes"
    
    elden_ring_abs_path = config["elden_ring_abs_path"].replace("\\", "/")
    mod_abs_path = config["mod_abs_path"].replace("\\", "/")
    witchyBND_path = config["witchyBND_abs_path"].replace("\\", "/")
    witchyBND_path += "/WitchyBND.exe"
    
    main_path = f"{sfx_tmp_path}/original_files"
    save_path = f"{sfx_tmp_path}/modified_files"
    active_path = f"{sfx_tmp_path}/active_files"
    if not os.path.exists(sfx_tmp_path): os.mkdir(sfx_tmp_path)
    if not os.path.exists(main_path): os.mkdir(main_path)
    if not os.path.exists(save_path): os.mkdir(save_path)
    if os.path.exists(active_path): shutil.rmtree(active_path) 
    os.mkdir(active_path)
    if os.path.exists(graph_path): shutil.rmtree(graph_path) 
    os.mkdir(graph_path)
    paths = {
        "elden_ring_abs_path": elden_ring_abs_path,
        "mod_abs_path": mod_abs_path,
        "witchyBND_abs_path": witchyBND_path,
        "sfx_tmp_path": sfx_tmp_path,
        "graph_path": graph_path,
        "main_path": main_path,
        "save_path": save_path,
        "active_path": active_path
    }
    return paths, dcx2folder_dct

def obtain_all_sfx_files():
    dcx2folder_dct = {"sfxbnd_commoneffects.ffxbnd.dcx": None,
                      "sfxbnd_commoneffects_dlc02.ffxbnd.dcx": None} 
    for dcx_fn, _ in dcx2folder_dct.items():
        dcx2folder_dct[dcx_fn] = dcx_fn.replace(".", "-") + "-wffxbnd"
    dcx2folder_dct = speed_up_search(dcx2folder_dct)
    return dcx2folder_dct

def speed_up_search(dcx2folder_dct): return dcx2folder_dct   # order common sfx fns to the top

def check_dcx_folder_in_path(paths, dcx_fn, dcx_folder_name):
    elden_ring_abs_path = paths["elden_ring_abs_path"]
    witchyBND_path = paths["witchyBND_abs_path"]
    main_path = paths['main_path']
    save_path = paths['save_path']
    if not os.path.exists(f"{main_path}/{dcx_folder_name}"):
        log.info(f'\t- Decompressing original "{dcx_folder_name}"..')
        from_fp = f"{elden_ring_abs_path}/Game/sfx/{dcx_fn}"
        to_fp = f"{main_path}/{dcx_fn}"
        command_fp = f"{main_path}/{dcx_fn}"
        shutil.copyfile(from_fp, to_fp)
        command = [witchyBND_path, command_fp]
        witchy_subprocess(command)
    else: log.info(f'\t- Found original "{dcx_folder_name}".')
    if not os.path.exists(f"{save_path}/{dcx_folder_name}"):
        log.info(f'\t- Loading modified "{dcx_folder_name}"..')
        from_fp = f"{main_path}/{dcx_folder_name}"
        to_fp = f"{save_path}/{dcx_folder_name}"
        shutil.copytree(from_fp, to_fp)
    else: log.info(f'\t- Found modified "{dcx_folder_name}".')

def finalize_process(paths, mission_input, mission_fn, recolor_mission, change_info):
    save_path = paths["save_path"]
    mod_abs_path = paths["mod_abs_path"]
    if not os.path.exists(f"{mod_abs_path}/sfx"): os.mkdir(f"{mod_abs_path}/sfx")
    for dcx_fn, is_changed in change_info.items():
        fp = f"{save_path}/{dcx_fn}"
        mod_fp = f"{mod_abs_path}/sfx/{dcx_fn}"
        if is_changed: shutil.copyfile(fp, mod_fp)
    for color, rgba in recolor_mission.items():
        mission_input["target_colors"][color] = rgba 
    prev_folder_name = "prev_missions"
    if not os.path.exists(prev_folder_name): os.mkdir(prev_folder_name)
    curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_sn = f"{prev_folder_name}/{mission_fn[:-4]}_{curr_time}.json"
    custom_json_dumper(mission_input, log_sn)
    custom_json_dumper(mission_input, mission_fn)
    log.info("\n>> Recoloring was COMPLETED.\n")

def move_and_compress_files(paths, sfx2dcx_dct, change_info, dcx2folder_dct):
    active_path = paths["active_path"]
    save_path = paths["save_path"]
    witchyBND_path = paths["witchyBND_abs_path"]
    for fn in os.listdir(active_path):
        from_path = f"{active_path}/{fn}"
        if fn.endswith(".fxr"): 
            final_dest = f"{save_path}/{sfx2dcx_dct[fn]}/effect/{fn}"
            shutil.move(from_path, final_dest) 
    for cnt, (dcx_fn, is_changed) in enumerate(change_info.items()):
        if is_changed:
            dcx_folder_name = dcx2folder_dct[dcx_fn]
            log.info(f'\t{cnt + 1} - Compressing "{dcx_folder_name}"..')
            witchy_subprocess([witchyBND_path, f"{save_path}/{dcx_folder_name}"])
