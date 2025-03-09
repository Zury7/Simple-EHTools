import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PyPDF2 import PdfReader
from pymediainfo import MediaInfo

def write_to_file(content, output_file):
    """Append metadata to the specified output file."""
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def extract_image_metadata(image_path, output_file):
    """Extract metadata from an image file and save to a file."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            write_to_file(f"\n[Image Metadata] - {image_path}\nNo EXIF metadata found.\n", output_file)
            return
        
        write_to_file(f"\n[Image Metadata] - {image_path}", output_file)
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            write_to_file(f"{tag_name}: {value}", output_file)

            # Extract GPS info
            if tag_name == "GPSInfo":
                gps_data = {GPSTAGS.get(t, t): v for t, v in value.items()}
                write_to_file(f"GPS Data: {gps_data}", output_file)

    except Exception as e:
        write_to_file(f"Error reading image metadata: {e}", output_file)

def extract_pdf_metadata(pdf_path, output_file):
    """Extract metadata from a PDF file and save to a file."""
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        write_to_file(f"\n[PDF Metadata] - {pdf_path}", output_file)
        for key, value in metadata.items():
            write_to_file(f"{key}: {value}", output_file)
    except Exception as e:
        write_to_file(f"Error reading PDF metadata: {e}", output_file)

def extract_media_metadata(file_path, output_file):
    """Extract metadata from audio/video files and save to a file."""
    try:
        media_info = MediaInfo.parse(file_path)
        write_to_file(f"\n[Media Metadata] - {file_path}", output_file)
        for track in media_info.tracks:
            for key, value in track.to_data().items():
                if value:
                    write_to_file(f"{key}: {value}", output_file)
    except Exception as e:
        write_to_file(f"Error reading media metadata: {e}", output_file)

def main():
    if len(sys.argv) < 2:
        print("Usage: python metadata_extractor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print("File does not exist.")
        sys.exit(1)

    # Generate metadata filename based on input file name
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"{base_name}_metadata.txt"

    # Clear previous metadata output
    open(output_file, "w").close()

    ext = file_path.lower()
    if ext.endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp")):
        extract_image_metadata(file_path, output_file)
    elif ext.endswith(".pdf"):
        extract_pdf_metadata(file_path, output_file)
    elif ext.endswith((".mp4", ".avi", ".mkv", ".mp3", ".wav")):
        extract_media_metadata(file_path, output_file)
    else:
        write_to_file(f"\nUnsupported file format: {file_path}", output_file)

    print(f"Metadata extracted and saved to {output_file}")

if __name__ == "__main__":
    main()
