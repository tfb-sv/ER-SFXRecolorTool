import subprocess

from utils.utils_common import log, witchy_subprocess
from utils.utils_paths import initialize_paths, witchy_subprocess, move_and_compress_files, finalize_process
from utils.utils_recolor import prepare_recolor_mission, check_dcx_folders_in_paths, process_sfx_files, process_xml_files

def main(recolor_info, progress_bar, info_label, is_run_after, suffix):
    [is_inspection, recolor_mission, config_fn, mission_fn, 
     mission_input, sfx_ids] = recolor_info
    graph_clm_cnt = 6
    norm_coef = 0.01 if not is_inspection else 0.015

    if recolor_mission: recolor_mission_norm = prepare_recolor_mission(recolor_mission)
    else: recolor_mission_norm = recolor_mission

    stage_text1 = f"Decompressing DCX{suffix} to FXR{suffix}.."
    info_label.configure(text=stage_text1)
    log.info(f"\n>> {stage_text1}\n")
    paths, dcx2folder_dct = initialize_paths(config_fn)
    check_dcx_folders_in_paths(paths, dcx2folder_dct)
    progress_bar.set(15 * norm_coef)

    stage_text2 = f"Moving FXR{suffix}.."
    info_label.configure(text=stage_text2)
    log.info(f"\n>> {stage_text2}")
    [decompress_fxr_command, compress_xml_command, 
     sfx2dcx_dct, change_info, not_exists] = process_sfx_files(sfx_ids, paths, dcx2folder_dct)
    progress_bar.set(30 * norm_coef)

    stage_text3 = f"Decompressing FXR{suffix} to XML{suffix}.."
    info_label.configure(text=stage_text3)
    log.info(f'\n>> {stage_text3}')
    witchy_subprocess(decompress_fxr_command)
    progress_bar.set(45 * norm_coef)

    if is_inspection: stage_text4 = f"Inspecting SFX.."
    else: stage_text4 = f"Recoloring SFX.."
    info_label.configure(text=stage_text4)
    log.info(f"\n>> {stage_text4}\n")
    graph_path = paths["graph_path"]
    total_ignoreds = process_xml_files(recolor_mission_norm, paths["active_path"], graph_path, 
                                       graph_clm_cnt, is_inspection, info_label, 
                                       progress_bar, norm_coef, 45, 60)
    progress_bar.set(60 * norm_coef)

    if is_inspection:
        log.info("\n>> Inspection was COMPLETED.\n")
        subprocess.Popen(f'explorer "{graph_path}"')
        return paths, total_ignoreds, not_exists

    stage_text5 = f"Compressing XML{suffix} to FXR{suffix}.."
    info_label.configure(text=stage_text5)
    log.info(f'\n>> {stage_text5}')
    witchy_subprocess(compress_xml_command)
    progress_bar.set(75 * norm_coef)

    stage_text6 = f"Compressing FXR{suffix} to DCX{suffix}.."
    info_label.configure(text=stage_text6)
    log.info(f"\n>> {stage_text6}\n")
    move_and_compress_files(paths, sfx2dcx_dct, change_info, dcx2folder_dct)
    progress_bar.set(90 * norm_coef)

    stage_text7 = f"Moving DCX{suffix}.."
    info_label.configure(text=stage_text7)
    log.info(f"\n>> {stage_text7}")
    finalize_process(paths, mission_input, mission_fn, recolor_mission, change_info)
    if not is_run_after: subprocess.Popen(f'explorer "{graph_path}"')
    return paths, total_ignoreds, not_exists
