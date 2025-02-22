import os
import tarfile
from huggingface_hub import hf_hub_download

# Define the dataset repository and base directory. I was too lazy to enter placeholders, this is one of the datasets I used.
repo_id = "speechcolab/gigaspeech" #change me
base_dir = "data/audio/s_files_additional" #change me

# Define the output directory for downloaded files
output_dir = "downloaded_audio"
os.makedirs(output_dir, exist_ok=True)

# Path to the directory containing filtered metadata files
filtered_metadata_dir = "cleaned_giga"

# Verify the filtered_metadata_dir exists
if not os.path.exists(filtered_metadata_dir):
    print(f"Error: Directory does not exist: {filtered_metadata_dir}")
    exit(1)


# Function to map a metadata file to its corresponding .tar.gz archive
def get_archive_name(metadata_file):
    # Example: metadata_file1.csv -> file1.tar.gz
    base_name = os.path.basename(metadata_file)  # e.g., metadata_file1.csv
    archive_name = base_name.replace("metadata_", "").replace(".csv", ".tar.gz")  # e.g., file1.tar.gz
    return archive_name


# Recursively find all metadata files in the filtered_metadata_dir
metadata_files = []
for root, dirs, files in os.walk(filtered_metadata_dir):
    for file in files:
        if file.endswith(".csv"):
            metadata_files.append(os.path.join(root, file))

if not metadata_files:
    print(f"No CSV files found in directory: {filtered_metadata_dir}")
    exit(1)
else:
    print(f"Found {len(metadata_files)} CSV files to process.")

# Iterate through all filtered metadata files
for metadata_path in metadata_files:
    metadata_file = os.path.basename(metadata_path)
    archive_name = get_archive_name(metadata_file)
    archive_path = os.path.join(base_dir, archive_name)  # Full path in the dataset

    print(f"\nProcessing metadata file: {metadata_path}")
    print(f"Corresponding archive: {archive_name}")

    # Read the filtered metadata to get the list of audio files to download
    audio_files_to_download = []
    with open(metadata_path, "r", encoding="utf-8") as f:
        print(f"Contents of {metadata_file}:")
        for line in f:
            print(line.strip())
            # Assuming each line in the metadata is: /path/to/audio/file.wav,phrase
            audio_path = line.split(",")[0].strip()
            audio_files_to_download.append(audio_path)

    # Download the archive using huggingface_hub
    try:
        print(f"Downloading archive: {archive_name}")
        local_archive_path = hf_hub_download(
            repo_id=repo_id,
            filename=archive_path,
            repo_type="dataset",
        )

        # Extract the specific files from the archive
        with tarfile.open(local_archive_path, "r:gz") as tar:
            for audio_file in audio_files_to_download:
                # Get the base name of the audio file (e.g., file1.wav)
                audio_file_name = os.path.basename(audio_file)
                # Extract the file
                try:
                    tar.extract(audio_file_name, path=output_dir)
                    print(f"Extracted: {audio_file_name}")
                except KeyError:
                    print(f"File not found in archive: {audio_file_name}")

    except Exception as e:
        print(f"Error processing {archive_name}: {e}")

print(f"\nDownloaded files saved in: {output_dir}")
