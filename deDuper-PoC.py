# Check and install required dependencies
try:
    import psutil
    import os
    import shutil
    import sys
except ImportError:
    print("psutil library not found. Installing...")
    os.system("pip install psutil")
    os.system("pip install shutil")
    os.system("pip install os")
    os.system("pip install sys")
    import psutil
    import os
    import shutil
    import sys

# Function to get the list of connected drives
def get_connected_drives():
    drives = [drive.device for drive in psutil.disk_partitions()]
    return drives

# Function to get the folder path based on user input
def get_folder_path(choice):
    if choice == '1':
        # Option 1: Current Directory
        return os.getcwd()
    elif choice == '2':
        # Option 2: Specify a Drive
        # Display the list of connected drives and let the user choose
        drives = get_connected_drives()
        print("Available Drives:")
        for i, drive in enumerate(drives, start=1):
            print(f"{i}) {drive}")

        drive_choice = input("Enter the number corresponding to the drive you want to check: ")
        try:
            drive_index = int(drive_choice) - 1
            return drives[drive_index]
        except (ValueError, IndexError):
            # Handle invalid drive choice by defaulting to the current directory
            print("Invalid drive choice. Defaulting to current directory.")
            return os.getcwd()

    elif choice == '3':
        # Option 3: Downloads Folder
        return os.path.join(os.path.expanduser("~"), "Downloads")
    elif choice == '4':
        # Option 4: Desktop Folder
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif choice == '5':
        # Option 5: Entire System
        return '\\'

    else:
        # Handle invalid choices by defaulting to the current directory
        print("Invalid choice. Defaulting to current directory.")
        return os.getcwd()

# Function to check for duplicates and move files
def check_for_duplicates(directory, fileExtensions, duplicate_folder_path):
    # Initialize a list to track filenames and detect duplicates
    fileList = {}
    # Initialize a list to store files that had duplicates
    kept_files_list = []

    # Traverse through the chosen directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        print(f"Checking directory: {root}")
        for fileType in fileExtensions:
            for filename in files:
                if filename.lower().endswith("." + fileType):
                    # Form the complete path to the current file
                    current_file_path = os.path.join(root, filename)
                    current_filename = filename.lower()

                    # Check if the filename is already in the list
                    if current_filename not in fileList:
                        # If not, add it to the list with its path
                        fileList[current_filename] = [current_file_path]
                    else:
                        # If it's a duplicate, append its path to the list
                        fileList[current_filename].append(current_file_path)

    # Iterate through the file list and handle duplicates
    for filename, paths in fileList.items():
        if len(paths) > 1:
            # If multiple duplicates are found, add a number to the duplicate file's name
            for i, path in enumerate(paths, start=1):
                _, file_extension = os.path.splitext(path)
                dst_filename = f"duplicateFile_{i}_{filename}{file_extension}"
                dst_path = os.path.join(duplicate_folder_path, dst_filename)
                shutil.move(path, dst_path)
                print(f"Duplicate file moved: {dst_path}")

            # Store the path of the duplicate file that is kept
            kept_files_list.append(paths[0])

        else:
            # If only one duplicate is found, move it without adding a number
            src_path = paths[0]
            _, file_extension = os.path.splitext(src_path)
            dst_filename = f"duplicateFile_{filename}{file_extension}"
            dst_path = os.path.join(duplicate_folder_path, dst_filename)
            shutil.move(src_path, dst_path)
            print(f"Duplicate file moved: {dst_path}")

    return kept_files_list

# Get user input for the folder choice
print("Select the folder to check:")
print("1) Current Directory")
print("2) Specify a Drive")
print("3) Downloads")
print("4) Desktop")
print("5) Entire System")

folder_choice = input("Enter the number corresponding to your choice: ")

# Get the chosen folder path based on user input
directory = get_folder_path(folder_choice)

# Define the list of file extensions to check for duplicates
fileExtensions = ['xlsx', 'pdf', 'docx', 'txt', 'doc', 'xls', 'csv']

# Define the path to the folder where duplicate files will be moved
duplicate_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Duplicates")

# Create the duplicate folder if it doesn't exist
if not os.path.exists(duplicate_folder_path):
    os.makedirs(duplicate_folder_path)

# Perform the duplicate check and get a list of files that had duplicates
kept_files_list = check_for_duplicates(directory, fileExtensions, duplicate_folder_path)

# Print completion message
print("Duplicate check completed.")

# Print files that had duplicates and were kept
print("\nFiles that had duplicates and were kept:")
for kept_file in kept_files_list:
    print(f"- {kept_file}")

# Ask the user if they want to restart the code
restart_choice = input("Do you want to restart the code? (yes/y or no/n): ").lower()

if restart_choice == 'y':
    # Restart the script
    os.execv(__file__, sys.argv)
elif restart_choice == 'Y':
    # Restart the script
    os.execv(__file__, sys.argv)
elif restart_choice == 'yes':
    # Restart the script
    os.execv(__file__, sys.argv)
elif restart_choice == 'Yes':
    # Restart the script
    os.execv(__file__, sys.argv)
else:
    print("Exiting the program.")
