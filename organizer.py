from pathlib import Path
import shutil
from categories import FILE_CATEGORIES
from logger import logger


def get_unique_filename(destination_folder, filename):
    """
    Generate a unique filename if the file already exists.
    Example:
    photo.jpg
    photo(1).jpg
    photo(2).jpg
    """

    destination = destination_folder / filename

    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix

    counter = 1

    while True:

        new_name = f"{stem}({counter}){suffix}"

        new_destination = destination_folder / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_folder(folder_path):
    """
    Organize files into category folders.
    Returns a summary dictionary.
    """

    folder = Path(folder_path)

    logger.info("===================================")
    logger.info("Organizer Started")
    logger.info(f"Folder: {folder}")

    if not folder.exists():
        logger.error("Folder does not exist.")
        return {
            "moved": 0,
            "failed": 1,
            "skipped": 0,
            "message": "Folder does not exist."
        }

    if not folder.is_dir():
        logger.error("Path is not a directory.")
        return {
            "moved": 0,
            "failed": 1,
            "skipped": 0,
            "message": "Given path is not a folder."
        }

    moved = 0
    skipped = 0
    failed = 0

    print("\n========== ORGANIZING FILES ==========\n")

    for item in folder.iterdir():

        # Ignore folders
        if not item.is_file():
            continue

        extension = item.suffix.lower()

        category = "Others"

        # Find category
        for folder_name, extensions in FILE_CATEGORIES.items():

            if extension in extensions:
                category = folder_name
                break

        destination_folder = folder / category

        destination_folder.mkdir(exist_ok=True)

        destination_file = get_unique_filename(
            destination_folder,
            item.name
        )

        try:

            shutil.move(str(item), str(destination_file))

            moved += 1

            print(f"✅ {item.name} → {category}")

            logger.info(f"Moved {item.name} -> {category}")

        except PermissionError:

            failed += 1

            print(f"❌ Permission denied: {item.name}")

            logger.error(f"Permission denied: {item.name}")

        except Exception as error:

            failed += 1

            print(f"❌ Error moving {item.name}")

            print(error)

            logger.exception(f"Unexpected error while moving {item.name}")

    print("\n========== SUMMARY ==========")
    print(f"Moved Files   : {moved}")
    print(f"Skipped Files : {skipped}")
    print(f"Failed Files  : {failed}")

    logger.info("Organizer Finished")
    logger.info(f"Moved: {moved}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"Failed: {failed}")

    return {
        "moved": moved,
        "failed": failed,
        "skipped": skipped,
        "message": "Files organized successfully."
    }


if __name__ == "__main__":

    folder_path = input("Enter folder path: ")

    result = organize_folder(folder_path)

    print("\nReturned Summary:")
    print(result)