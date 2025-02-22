import os
import tarfile
import requests
import csv
from huggingface_hub import HfFolder

# Define the dataset repository and base directory
repo_id = "speechcolab/gigaspeech"
remote_base_dir = "data/audio"  # Updated base directory

# Define the output directory for downloaded files
output_dir = "downloaded_audio"
os.makedirs(output_dir, exist_ok=True)

# Path to the directory containing filtered metadata files
filtered_metadata_dir = "cleaned_giga"

# Verify the filtered_metadata_dir exists
if not os.path.exists(filtered_metadata_dir):
    print(f"Error: Directory does not exist: {filtered_metadata_dir}")
    exit(1)


# Function to map a metadata file to its corresponding .tar.gz archive and folder
def get_archive_info(metadata_file, metadata_root):
    # Extract the subfolder name (e.g., "l_metadata_additional", "xl_metadata_additional")
    relative_path = os.path.relpath(os.path.dirname(metadata_file), metadata_root)
    folder = os.path.basename(relative_path)  # e.g., "l_metadata_additional"

    # Map the local metadata folder to the remote archive folder
    if folder == "l_metadata_additional":
        remote_folder = "l_files_additional"
    elif folder == "m_metadata_additional":
        remote_folder = "m_files_additional"
    elif folder == "s_metadata_additional":
        remote_folder = "s_files_additional"
    elif folder == "xl_metadata_additional":
        remote_folder = "xl_files_additional"
    elif folder == "xs_metadata":
        remote_folder = "xs_files"
    elif folder == "test_metadata":
        remote_folder = "test_files"
    elif folder == "dev_metadata":
        remote_folder = "dev_files"
    else:
        raise ValueError(f"Unknown metadata folder: {folder}")

    # Get the archive name
    base_name = os.path.basename(metadata_file)  # e.g., xl_chunks_0001_metadata.csv
    archive_name = base_name.replace("_metadata.csv", ".tar.gz")  # e.g., xl_chunks_0001.tar.gz

    return archive_name, remote_folder


# Function to convert .opus path to .wav path
def opus_to_wav_path(opus_path, archive_name, segment_id):
    # Example: audio/youtube/P0004/YOU0000000315.opus -> xs_chunks_0000/YOU0000000315_S0000660.wav
    archive_folder = archive_name.replace(".tar.gz", "")  # e.g., xs_chunks_0000
    wav_name = f"{segment_id}.wav"  # e.g., YOU0000000315_S0000660.wav
    return f"{archive_folder}/{wav_name}"  # e.g., xs_chunks_0000/YOU0000000315_S0000660.wav


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

# Get the Hugging Face token (automatically uses the token from `huggingface-cli login`)
token = HfFolder.get_token()
if not token:
    print("Error: No Hugging Face token found. Please log in using `huggingface-cli login`.")
    exit(1)

# Iterate through all filtered metadata files
for metadata_path in metadata_files:
    metadata_file = os.path.basename(metadata_path)
    archive_name, remote_folder = get_archive_info(metadata_path, filtered_metadata_dir)
    archive_path = os.path.join(remote_base_dir, remote_folder, archive_name).replace("\\",
                                                                                "/")   # Use forward slashes for URLs

    print(f"\nProcessing metadata file: {metadata_path}")
    print(f"Corresponding archive: {archive_name} (remote folder: {remote_folder})")

    # Read the filtered metadata to get the list of audio files to download
    audio_files_to_download = set()  # Use a set to avoid duplicates
    with open(metadata_path, "r", encoding="utf-8") as f:
        print(f"Contents of {metadata_file}:")
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 7:  # Ensure there are at least 8 columns
                segment_id = row[0].strip()  # 1st column (0-indexed, "segment_id")
                opus_path = row[7].strip()  # 8th column (0-indexed, "path")
                if opus_path.endswith(".opus"):  # Only process valid audio file paths
                    wav_path = opus_to_wav_path(opus_path, archive_name, segment_id)  # Convert .opus path to .wav path
                    if wav_path not in audio_files_to_download:  # Avoid duplicates
                        audio_files_to_download.add(wav_path)
                        print(f"Found audio file: {opus_path} -> {wav_path}")
                    else:
                        print(f"Skipping duplicate audio file: {opus_path} -> {wav_path}")
                else:
                    print(f"Skipping invalid file path: {opus_path}")

    # Download and extract specific files from the remote .tar.gz archive
    try:
        print(f"Streaming archive: {archive_name}")
        # Get the URL for the .tar.gz archive
        archive_url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{archive_path}"
        print(f"Archive URL: {archive_url}")

        # Stream the .tar.gz archive with authentication
        headers = {"Authorization": f"Bearer {token}"}
        with requests.get(archive_url, headers=headers, stream=True) as response:
            response.raise_for_status()
            with tarfile.open(fileobj=response.raw, mode="r|gz") as tar:
                # Process the archive in a single pass
                for member in tar:
                    if member.name in audio_files_to_download:
                        # Create the output directory structure
                        output_file_path = os.path.join(output_dir, member.name)
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                        # Save the extracted file
                        with tar.extractfile(member) as member_file:
                            with open(output_file_path, "wb") as outfile:
                                outfile.write(member_file.read())
                        print(f"Extracted: {member.name}")
                        # Remove the file from the set to avoid duplicates
                        audio_files_to_download.remove(member.name)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"Error: Unauthorized. Please ensure your Hugging Face token is valid.")
        else:
            print(f"Error processing {archive_name}: {e}")
    except Exception as e:
        print(f"Error processing {archive_name}: {e}")

print(f"\nDownloaded files saved in: {output_dir}")
