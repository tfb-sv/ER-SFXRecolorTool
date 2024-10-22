######################################################################################
import subprocess
from utils_recolor import *
######################################################################################

def main(recolor_info, progress_bar, info_label):
    [is_inspection, recolor_mission, config_fn, mission_fn, mission_input, sfx_ids, is_debug] = recolor_info
    graph_clm_cnt = 6
    norm_coef = 0.01 if not is_inspection else 0.015

    if recolor_mission: recolor_mission_norm = prepare_recolor_mission(recolor_mission)
    else: recolor_mission_norm = recolor_mission
    
    paths = initialize_paths(config_fn)
    check_if_original_files_in_path(paths)
    progress_bar.set(15*norm_coef)
    
    decompress_fxr_command, compress_xml_command, sfx2fn_dct, change_info = process_sfx_files(sfx_ids, paths)
    stage_text1 = "DCX files were decompressed to FXR files via WitchyBND"
    info_label.configure(text="")
    
    print("\n>> DCX files were decompressed to FXR files via WitchyBND.")
    progress_bar.set(30*norm_coef)
    
    witchy_subprocess(decompress_fxr_command)
    print('\n>> FXR files were decompressed to XML files via WitchyBND.\n')
    progress_bar.set(45*norm_coef)
    
    process_xml_files(recolor_mission_norm, paths["active_path"], paths["graph_path"], 
                      graph_clm_cnt, is_inspection, is_debug)
    print("\n>> XML files were recolored successfully.\n")
    progress_bar.set(60*norm_coef)
    
    if is_inspection:
        print("\n>> Inspection was COMPLETED !\n")
        subprocess.Popen(f'explorer "{paths["graph_path"]}"')
        return paths

    witchy_subprocess(compress_xml_command)
    print('\n>> XML files were compressed to FXR files via WitchyBND.')
    progress_bar.set(75*norm_coef)

    move_and_compress_files(paths, sfx2fn_dct, change_info)
    print("\n>> FXR files were compressed to DCX files via WitchyBND.\n")
    progress_bar.set(90*norm_coef)
    
    finalize_process(paths, mission_input, mission_fn, recolor_mission, change_info)
    subprocess.Popen(f'explorer "{paths["graph_path"]}"')
    return paths

###################################################################################### 
