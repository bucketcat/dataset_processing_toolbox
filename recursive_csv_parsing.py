import os

def process_files(input_dir, output_dir, phrase, recursive=False):
    """
    Process CSV files in the input directory (and optionally its subdirectories).
    Only lines containing the specified phrase are written to the output directory.
    """
    # Verify the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory does not exist: {input_dir}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Counters for debugging
    total_files_processed = 0
    total_matching_lines = 0

    # Function to process a single file
    def process_file(input_file, output_file):
        nonlocal total_matching_lines
        try:
            with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
                for line in infile:
                    if phrase in line:
                        outfile.write(line)
                        total_matching_lines += 1
            return True
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")
            return False

    # Recursive or non-recursive file search
    if recursive:
        # Recursively iterate through all files in the input directory and its subdirectories
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                if filename.endswith(".csv"):
                    input_file = os.path.join(root, filename)
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    output_file = os.path.join(output_subdir, filename)

                    # Create the output subdirectory if it doesn't exist
                    os.makedirs(output_subdir, exist_ok=True)

                    if process_file(input_file, output_file):
                        print(f"Processed file: {input_file}")
                        total_files_processed += 1
    else:
        # Non-recursive: Only process files in the top-level input directory
        for filename in os.listdir(input_dir):
            if filename.endswith(".csv"):
                input_file = os.path.join(input_dir, filename)
                output_file = os.path.join(output_dir, filename)

                if process_file(input_file, output_file):
                    print(f"Processed file: {input_file}")
                    total_files_processed += 1

    # Verbose console spam
    print(f"\nProcessing complete!")
    print(f"Total files processed: {total_files_processed}")
    print(f"Total matching lines found: {total_matching_lines}")
    print(f"Filtered files saved in: {output_dir}")


# Example usage
if __name__ == "__main__":
    # Define the phrase to search for
    phrase = "Word1 word2"

    # Input and output directories (use absolute paths)
    input_dir = "/home/<user>/<venv>/<input_folder>"
    output_dir = "/home/<user>/<venv>/<output_folder>"
    
    # input_dir = "C:\\path\\to\\metadata\\"  # Replace for windows
    
    # output_dir = "C:\path\to\output\\"  # Replace for windows

    # Set recursive=True to process subdirectories
    process_files(input_dir, output_dir, phrase, recursive=True)