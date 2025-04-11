import os
from pathlib import Path

def list_directory_structure(start_path, output_file):
    print(f"🔍 Scanning directory: {start_path}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(start_path):
            level = root.replace(str(start_path), '').count(os.sep)
            indent = ' ' * 4 * level
            folder_name = os.path.basename(root)
            f.write(f'{indent}{folder_name}/\n')
            print(f"📂 Processing folder: {root}")
            
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f'{subindent}{file}\n')

    print("✅ Directory structure has been written.")

if __name__ == '__main__':
    print("🚀 Starting script...")
    home_path = Path.home()  # e.g., /home/username
    script_dir = Path(__file__).resolve().parent
    output_txt = script_dir / 'directory_structure.txt'

    list_directory_structure(home_path, output_txt)

    print(f"📄 Output saved to: {output_txt}")
