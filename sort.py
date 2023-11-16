import os
import shutil
import string
import transliterate
def normalize(name):
    name = transliterate.translit(name, reversed=True)
    allowed_chars = string.ascii_letters + string.digits + '_'
    return ''.join(c if c in allowed_chars else '_' for c in name)

def move_files(files, category):
    target_folder = os.path.join(os.getcwd(), category)
    os.makedirs(target_folder, exist_ok=True)
    for file in files:
        try:
            normalized_name = normalize(file)
            if normalized_name != file:
                os.rename(file, os.path.join(target_folder, normalized_name))
        except Exception as e:
            print(f"Failed process file {file}: {e}")
def sort_files(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    images = ('.jpeg', '.png', '.jpg', '.svg')
    videos = ('.avi', '.mp4', '.mov', '.mkv')
    documents = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
    audio = ('.mp3', '.ogg', '.wav', '.amr')
    archives = ('.zip', '.gz', '.tar')

    unknown_extensions = set()
    known_extensions = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                _, extension = os.path.splitext(file)
                extension = extension.lower()
                known_extensions.add(extension)

                if extension in images:
                    move_files([os.path.join(root, file)], 'images')
                elif extension in videos:
                    move_files([os.path.join(root, file)], 'videos')
                elif extension in documents:
                    move_files([os.path.join(root, file)], 'documents')
                elif extension in audio:
                    move_files([os.path.join(root, file)], 'audio')
                elif extension in archives:
                    archive_path = os.path.join(root, file)
                    extact_folder = os.path.join(os.path.dirname(archive_path), os.path.splitext(file)[0])

                    shutil.unpack_archive(archive_path, extact_folder)
                    move_files([extact_folder], 'archives')
                else:
                    unknown_extensions.add(extension)
            except Exception as e:
                print(f"Failed to process file {file}: {e}")

        print("Files sorted successfully.")
        print(f"Known extensions: {', '.join(known_extensions)}")
        print(f"Unknown extensions: {', '.join(unknown_extensions)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Expected: python sort.py /path/to/directory")
        sys.exit(1)

    target_directory = sys.argv[1]
    sort_files(target_directory)

