# eml2img

`eml2img` is a Python-based tool that extracts images from `.eml` files, commonly used for email messages. This utility scans `.eml` files or entire folders containing `.eml` files to extract image data encoded in Base64 format and saves them as image files. It supports extracting images from both individual files and directories, with options to specify output directories.

## Features
- Extracts images from individual `.eml` files or entire directories.
- Supports Base64-decoded images.
- Allows specifying custom output directories.
- Easily adaptable for automation or batch processing.

## Requirements
- Python 3.9+
- [`uv`](https://docs.astral.sh/uv/) (no other dependencies)

## Installation

No installation needed. Run directly with `uvx`:

```bash
uvx git+https://github.com/jeffreyparker/eml2img your_file.eml
```

Install `uv` if you don't have it yet:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Usage

All examples use `uvx git+https://github.com/jeffreyparker/eml2img` as the command.

### 1. Display Help

```bash
uvx git+https://github.com/jeffreyparker/eml2img -h
```

### 2. Parse a Single `.eml` File

Extract images from a single `.eml` file and save them to a folder based on the filename:

```bash
uvx git+https://github.com/jeffreyparker/eml2img ./email.eml
```
> This command will extract images into a folder named `./email` by default.

To extract into a specific folder, use the `-o` option:

```bash
uvx git+https://github.com/jeffreyparker/eml2img ./email.eml -o ./OutputDir
```

### 3. Parse All `.eml` Files in a Directory

Scan the current directory:

```bash
uvx git+https://github.com/jeffreyparker/eml2img --parse-folder
```

Scan a specific directory with a custom output folder:

```bash
uvx git+https://github.com/jeffreyparker/eml2img --parse-folder ./DirToScan -o ./OutputDir
```

## How it Works

1. The tool detects and parses `.eml` files for `Content-Type: image/png;` or other image types.
2. Images are Base64-decoded and saved in the specified output directory.
3. For multipart `.eml` files, boundaries are detected and used to extract individual images.

## Example Scenarios

### Extracting Images from Multiple Emails

If you have a folder full of `.eml` files and you want to extract all images to a single directory:

```bash
uvx git+https://github.com/jeffreyparker/eml2img --parse-folder ./Emails -o ./AllImages
```

This will scan all `.eml` files in the `./Emails` directory and save any extracted images to the `./AllImages` folder.

### Frames Extraction for Game Development
You can also use eml2img to automate tasks like extracting image frames from .eml files for game development projects like I do ;).
For example, if you need to extract sprite frames for a game, you can create a batch file to automate the process and place the frames into their respective project directories.
Here’s a sample batch script (framesToUndercup.bat) for extracting frames and saving them into the asset directory for my game:

```batch
:: framesToUndercup.bat
:: Run this in a folder containing the "just downloaded" .eml files
eml2img --parse-folder . -o D:\Projects\Cupflow\Undercup\Assets\Sprites %1
```

Usage:
To extract all frames for a specific game asset (e.g., "Player"), run:
```batch
framesToUndercup Player
```

This will extract all frames into the Player folder inside your game project directory `D:\Projects\Cupflow\Undercup\Assets\Sprites\Player`.