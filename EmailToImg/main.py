import base64
import argparse
import os

# Initialize parser
parser = argparse.ArgumentParser(
    description="Parses .eml file(s) to extract image data"
)

def add_options():
    # Mutually exclusive group to allow either single file or folder parsing
    group = parser.add_mutually_exclusive_group(required=True)

    # Group for parsing a single file
    group.add_argument(
        "filename", 
        nargs="?",  # Optional positional argument
        help="Specify a single .eml file to parse"
    )
    
    # Group for parsing a folder
    group.add_argument(
        "--parse-folder", 
        nargs="?",  # Optional folder argument
        const=".",  # Defaults to the current directory if no folder is specified
        default=None,  # Default when --parse-folder is not provided
        help="Specify a folder to parse. Defaults to the current folder if no folder name is provided."
    )

    # Optional output directory for both single file and folder parsing
    parser.add_argument(
        "-o", "--output", 
        help="Specify a destination folder for output images."
    )

def main():
    add_options()
    args = parser.parse_args()

    output_folder = args.output

    if args.parse_folder:
        parse_folder(args.parse_folder, output_folder)
    else:
        with open(args.filename, 'r') as file:
            parse_file(file, output_folder)

def parse_folder(folder_name, output_folder):
    if output_folder is None:
        output_folder = "."
        
    for root, _, files in os.walk(folder_name):
        for file in files:
            if file.endswith(".eml"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as eml_file:
                    parse_file(eml_file, os.path.join(output_folder, extract_file_name_no_extension(eml_file.name)))

def parse_file(file, output_folder):
    # Create the output folder if not provided
    if output_folder is None:
        output_folder = extract_file_name_no_extension(file.name)

    os.makedirs(output_folder, exist_ok=True)

    boundary = ""
    has_found_image = False
    is_reading_image_data = False
    image_name = ""
    image_content = ""
    looking_for_image_name = False
    looking_for_boundary = False

    for line in file:
        # Detect boundary for multipart sections
        if 'Content-Type: multipart/' in line:
            boundary = extract_boundary(line)
            if not boundary:  # Boundary is on next line
                looking_for_boundary = True
            continue
        
        # Look for boundary on the next line
        if looking_for_boundary and 'boundary=' in line:
            boundary = '--' + line.strip().split('boundary="')[1].split('"')[0]
            looking_for_boundary = False
            continue
        
        # If we're reading image data, check if this line is a boundary (end of data)
        if is_reading_image_data and line.startswith(boundary):
            # Save the content to file
            image_path = os.path.join(output_folder, image_name)
            save_image(image_path, image_content)

            has_found_image = False
            is_reading_image_data = False
            looking_for_image_name = False
            continue

        # If we're reading image data, accumulate the content
        if is_reading_image_data:
            image_content += line
        
        # Check if we're looking for the image name on the next line
        if looking_for_image_name:
            image_name = extract_image_name_from_line(line)
            has_found_image = True
            is_reading_image_data = False
            looking_for_image_name = False
            image_content = ""
        
        if 'Content-Type: image/png;' in line or 'Content-Type: image/jpeg;' in line:
            # Check if name is on the same line
            if 'name=' in line:
                image_name = extract_image_name(line)
                has_found_image = True
                is_reading_image_data = False
                image_content = ""
            else:
                # Name is likely on the next line
                looking_for_image_name = True
        
        # Start reading base64 data after we find an image and encounter an empty line
        if has_found_image and not is_reading_image_data and len(line.strip()) == 0:
            is_reading_image_data = True
            continue  # Skip the empty line itself

def extract_file_name_no_extension(file_name):
    """Removes the file extension from the file name"""
    return os.path.splitext(file_name)[0]

def extract_boundary(str):
    """Extracts the boundary string from the Content-Type header"""
    try:
        # Handle both single-line and multi-line boundary declarations
        if 'boundary=' in str:
            return '--' + str.split('boundary="')[1].split('"')[0]
        else:
            # Boundary might be on the next line, return empty for now
            return ""
    except IndexError:
        print("Error: Could not find boundary in Content-Type.")
        return ""

def save_image(path, content):
    """Saves the Base64-decoded image content to a file"""
    try:
        with open(path, "wb") as image_file:
            image_file.write(base64.b64decode(content))
            print(f"Extracted image: {path}")
    except Exception as e:
        print(f"Error saving image: {e}")

def extract_image_name(line):
    """Extracts the image file name from the Content-Type header"""
    try:
        return line.split('; ')[1].split('"')[1]  # name="image.png" or name="image.jpg"
    except IndexError:
        print("Error: Could not extract image name.")
        return "unknown_image"

def extract_image_name_from_line(line):
    """Extracts the image file name from a line that starts with tab and contains name="..." """
    try:
        # Handle lines like: \tname="4 months - Pose 1.jpg"
        return line.strip().split('name="')[1].split('"')[0]
    except IndexError:
        print("Error: Could not extract image name from line.")
        return "unknown_image" 

main()
