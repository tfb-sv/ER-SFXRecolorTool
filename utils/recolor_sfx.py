import subprocess
from utils.utils_recolor import *

def main(recolor_info, progress_bar, info_label, is_run_after):
    [is_inspection, recolor_mission, config_fn, mission_fn, 
     mission_input, sfx_ids] = recolor_info
    graph_clm_cnt = 6
    norm_coef = 0.01 if not is_inspection else 0.015

    if recolor_mission: recolor_mission_norm = prepare_recolor_mission(recolor_mission)
    else: recolor_mission_norm = recolor_mission

    stage_text1 = "Decompressing DCXs to FXRs.."
    info_label.configure(text=stage_text1)
    print(f"\n>> {stage_text1}")
    paths, dcx2folder_dct = initialize_paths(config_fn)
    check_dcx_folders_in_paths(paths, dcx2folder_dct)
    progress_bar.set(15 * norm_coef)

    stage_text2 = "Moving FXRs.."
    info_label.configure(text=stage_text2)
    print(f"\n>> {stage_text2}")
    [decompress_fxr_command, compress_xml_command, 
     sfx2dcx_dct, change_info, not_exists] = process_sfx_files(sfx_ids, paths, dcx2folder_dct)
    progress_bar.set(30 * norm_coef)

    stage_text3 = "Decompressing FXRs to XMLs.."
    info_label.configure(text=stage_text3)
    print(f'\n>> {stage_text3}')
    witchy_subprocess(decompress_fxr_command)
    progress_bar.set(45 * norm_coef)

    if is_inspection: stage_text4 = "Inspecting SFXs.."
    else: stage_text4 = "Recoloring SFXs.."
    info_label.configure(text=stage_text4)
    print(f"\n>> {stage_text4}\n")
    graph_path = paths["graph_path"]
    total_ignoreds = process_xml_files(recolor_mission_norm, paths["active_path"], graph_path, 
                                       graph_clm_cnt, is_inspection, info_label, 
                                       progress_bar, norm_coef, 45, 60)
    progress_bar.set(60 * norm_coef)

    if is_inspection:
        print("\n>> Inspection was COMPLETED.\n")
        subprocess.Popen(f'explorer "{graph_path}"')
        return paths, total_ignoreds, not_exists

    stage_text5 = "Compressing XMLs to FXRs.."
    info_label.configure(text=stage_text5)
    print(f'\n>> {stage_text5}')
    witchy_subprocess(compress_xml_command)
    progress_bar.set(75 * norm_coef)

    stage_text6 = "Compressing FXRs to DCXs.."
    info_label.configure(text=stage_text6)
    print(f"\n>> {stage_text6}")
    move_and_compress_files(paths, sfx2dcx_dct, change_info, dcx2folder_dct)
    progress_bar.set(90 * norm_coef)

    stage_text7 = "Moving DCXs.."
    info_label.configure(text=stage_text7)
    print(f"\n>> {stage_text7}")
    finalize_process(paths, mission_input, mission_fn, recolor_mission, change_info)
    if not is_run_after: subprocess.Popen(f'explorer "{graph_path}"')
    return paths, total_ignoreds, not_exists
