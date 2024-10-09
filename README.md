# Elden Ring SFX Recolor Tool (ER-SFXRecolorTool)

## Overview
This tool automates and simplifies the SFX (FXR) recoloring process for Elden Ring, particularly the cumbersome task of finding and adjusting RGB values within XML files. I have identified a pattern for RGB values in XML files and utilized this information in this tool.

## Prerequisites
- Ensure all game files are uncompressed using `UXM Selective Unpacker`.
- Be familiar with `ModEngine2`.
- Download `WitchyBND` to your computer.

## Notes
- This tool is designed for Windows.
- The tool does not make any changes to the original game folder, ensuring the integrity of the game files is maintained.
- Applies toning to the entered RGB values, making the recoloring appear more realistic and aesthetically pleasing.
- No manual file or folder transfers required.

## Installation
1. Download the latest release of this tool.
2. Place the downloaded folder in a directory, such as the `Users` directory, where file read/write permissions are unrestricted.

## Configuration
- Modify the first 3 lines in the `path_config.json` to reflect your system paths.
- List the SFX (FXR) numbers you want to modify in `recolor_mission.json`.

## Usage
0. Ensure that the steps outlined in the `Configuration` section are completed.
1. Run `ER-SFXRecolorTool.exe`.
2. Ensure `INSPECT` mode is selected.
3. Click the `INSPECT` button.
4. After inspection, the tool automatically switches from `INSPECT` to `RECOLOR` mode.
5. Review the color palettes displayed, and decide which colors to change.
6. Input new RGB values for the colors you want to change directly on the screen.
7. Click the `RECOLOR` button.
8. Launch the game with `ModEngine2` after the recoloring process completes, no further action is needed.

9. Probably, you want to fine-tune the RGB values you've entered. So you can continue from `RECOLOR` mode
until you satisfied the RGB values that you've entered. But with every change you need to check in-game the sfx
whether it is okay.

## Additional Information
- Logs each recoloring process in the `logs` folder.
- Saves changes in `recolor_mission.json`, which autoloads at program startup.
- Before and after color of the SFX can be found in the `sfx_palettes`.
- `sfx_palettes` is resetted in the beginning of every recoloring process.

- The inspection process is not strictly necessary, but it serves as an important sanity check.
- To completely reset all modifications and start fresh, delete the `sfx/modified_files` folder.
- If there are no mods in the `ModEngine2` folder, use `ModEngine2/mod` as an input for `path_config.json`.
- JSON files are editable with text editors like `Notepad++`.

- Benzer SFXleri bi arada değiştirin.

## TODOs
- CLI commands will be integrated into the tool for enhanced functionality.
- yeni sfx için program güncellenmeli

## Contributing
- Report issues or bugs, especially if you see `IGNORED` in the command line outputs.
Feedback and contributions are highly appreciated. If you encounter any issues or have suggestions for improvement, please open an issue on the GitHub repository.
