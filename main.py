import os
import logging


# File handler and stream handler setup
logger = logging.getLogger("File_Manager_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("file_manager.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

class FileManager:
    """File Management System for basic file operations."""
    def create_file(self,filename):
        try:

            with open(filename, 'x') as f:
                logger.info(f"File {filename} created successfully.")
                print(f"File {filename} created successfully!")

        except FileExistsError as fe:
            logger.warning(f"File {filename} already exists", exc_info=True)
            print(str(fe))

        except Exception as e:
            logger.error(f"Unexpected error while creating file", exc_info=True)
            print(str(e))


    def view_all_files(self):
        try:

            files = os.listdir()
            if not files:
                logger.info("No files found in the directory.")
                print("No files found in the directory.")

            else:
                print("Files in the directory:")
                for file in files:
                    print(file)
                logger.info("Listed all files.")

        except Exception as e:
            logger.error(f"Unexpected error while viewing files", exc_info=True)
            print(str(e))


    def delete_file(self, filename):
        try:

            os.remove(filename)
            logger.info(f"File {filename} deleted.")
            print(f"{filename} has been deleted successfully!")
        
        except FileNotFoundError as fe:
            logger.info(f"Attempted to delete non existent file {filename}.")
            print(str(fe))

        except Exception as e:
            logger.error(f"Unexpected error while deleting file", exc_info=True)
            print(str(e))


    def read_file(self, filename):
        try:

            with open(filename,'r') as f:
                content = f.read()
                logger.info(f"Read file {filename}")
                print(f"Content of {filename} : \n{content }")

        except FileNotFoundError as fe:
            logger.error(f"File {filename} not found for reading.", exc_info=True)
            print(str(fe))
        
        except Exception as e:
            logger.error(f"Unexpected error occurred while reading file", exc_info=True)
            print(str(e))


    def edit_file(self, filename):
        try:

            with open(filename,'a') as f:
                content = input("Enter data to add = ")
                f.write(content + "\n")
                logger.info(f"Appended content to {filename}")
                print(f"Content added to {filename} successfully!")
        
        except FileNotFoundError as fe:
            logger.warning(f"File {filename} not found for editing.",exc_info=True)
            print(str(fe))
        
        except Exception as e:
            logger.error(f"Unexpected error occured while editing file", exc_info=True)
            print(str(e))


    def run(self):
        while True:
            print("\n********** Welcome to File Management System **********")
            print("1: Create file")
            print("2: View all files")
            print("3: Delete file")
            print("4: Read file")
            print("5: Edit file")
            print("6: Exit")

            try:
                choice = int(input("Enter your choice(1-6) = "))

                if choice == 1:
                    filename = input("Enter the file-name to create = ").strip()
                    self.create_file(filename)

                elif choice == 2:
                    self.view_all_files()

                elif choice == 3:
                    filename = input("Enter the file-name to delete = ").strip()
                    self.delete_file(filename)

                elif choice == 4:
                    filename = input("Enter the file-name to read = ").strip()
                    self.read_file(filename)

                elif choice == 5:
                    filename = input("Enter the file-name to edit = ").strip()
                    self.edit_file(filename)

                elif choice == 6 :
                    logger.info("Program exited by user.")
                    print("Closing the program.")
                    break

                else:
                    print("Invalid input!")

            except ValueError as ve:
                logger.warning(f"Invalid menu input", exc_info=True)
                print(str(ve))


if __name__ == "__main__":
    FileManager().run()
