# Elden Ring SFX Recolor Tool (ER-SFXRecolorTool)

## Overview
ER-SFXRecolorTool is a modding tool for Elden Ring that automates and simplifies the SFX (FXR) recoloring process, particularly the cumbersome task of finding and adjusting RGB values within the XML files. I have identified a pattern for RGB values in the XML files and utilized this information into this tool.

- [NexusMods Page](<link-to-your-NexusMods-page>)

## Prerequisites
- Ensure all game files are uncompressed using `UXM Selective Unpacker`.
- Be familiar with and ready to use `ModEngine2`.
- Download `WitchyBND` to your computer.

## Notes
- This tool is specifically designed to operate on the `Windows` platform.
- The tool does not make any changes to the original game folder, ensuring the integrity of the game files is maintained.
- Applies toning to entered RGB values, making the recoloring appear more realistic and aesthetically pleasing.
- No manual transfers of SFX-related files or folders are required.

## Installation
1. Download the latest release of this tool.
2. Place the downloaded folder in a directory, such as the `Users` directory, where file read/write permissions are unrestricted.

## Configuration
- Modify the first three lines in the `path_config.json` to reflect your system paths.
- Enter the SFX (FXR) numbers you want to modify into the `recolor_mission.json`.

## Usage
0. Ensure that the steps outlined in the `Configuration` section are completed.
1. Run `ER-SFXRecolorTool.exe`.
2. Ensure `INSPECTION` mode is selected.
3. Click the `INSPECT` button.
4. After inspection, the tool automatically switches from `INSPECTION` to `RECOLORING` mode.
5. Review the color palettes displayed, and decide which colors to change.
6. Enter new RGB values for the colors you want to change into the tool's interface.
7. Click the `RECOLOR` button.
8. Launch the game using `ModEngine2` after the recoloring session is complete, no further action is needed.
9. (Optional) Fine-tune entered RGB values as needed. You may repeat the recoloring session from `RECOLORING` mode and check the effects in-game after each adjustment until the results meet your satisfaction.

## Additional Information
- Logs are stored in the `logs` folder for each recoloring session.
- Changes are saved in the `recolor_mission.json`, which automatically loads when the program starts.
- The before and after colors of the SFX are available in the `sfx_palettes`, which is reset at the beginning of each recoloring session.
- The inspection session is not strictly necessary, but it serves as an important sanity check.
- To completely reset all modifications and start from scratch, simply delete the `sfx/modified_files` folder.
- If there are no mods in the `ModEngine2` folder, use `ModEngine2/mod` as one of the required inputs for the `path_config.json`.
- JSON files are editable with text editors like `Notepad++`.

## Hints
- Group similar SFX files together for batch modifications and restart the program for the recoloring session of each group.
- Several iterations may be needed until a satisfactory result is achieved.

## TODOs
- CLI commands will be integrated into the tool for enhanced functionality.
- Eliminate the need to restart the program for updates in the `recolor_mission.json` to take effect.

## Contributing
Feedback and contributions are highly valued. Issues or suggestions for improvements can be reported by opening an issue on the GitHub repository or posting a bug on NexusMods. Please report any anomalies or `IGNORED` outputs seen in the command line.

Your input helps improve the tool for all users!
