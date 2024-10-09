######################################################################################
import subprocess
from utils_recolor import *
######################################################################################

def main(recolor_info):
    [is_inspection, recolor_mission, config_fp, mission_fn, mission_input, sfx_ids] = recolor_info
    graph_clm_cnt = 6
    isDeactivateAlpha = False

    if recolor_mission: 
        recolor_mission = prepare_recolor_mission(recolor_mission)
        validate_colors(recolor_mission)
    
    paths = initialize_paths(config_fp)
    check_if_original_files_in_path(paths)
    
    decompress_fxr_command, compress_xml_command, sfx2fn_dct, change_info = process_sfx_files(sfx_ids, paths)
    decompress_fxr_files(decompress_fxr_command)
    process_xml_files(recolor_mission, paths["active_path"], paths["graph_path"], 
                      isDeactivateAlpha, graph_clm_cnt, is_inspection)

    if is_inspection:
        print("\n>> Inspection was COMPLETED !\n")
        subprocess.Popen(f'explorer "{paths["graph_path"]}"')
        return

    compress_xml_files(compress_xml_command)
    move_and_compress_files(paths, sfx2fn_dct, change_info)
    finalize_process(paths, mission_input, mission_fn, recolor_mission, sfx2fn_dct, change_info)

###################################################################################### 
