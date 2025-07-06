import re
import logging

# File handler and stream handler setup
logger = logging.getLogger("Contact_Book_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("contact_book.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# --- Custom Exceptions ---
class ContactBookError(Exception):
    """Custom exception class for Contact book related errors."""
    pass

class ContactAlreadyExistsError(ContactBookError):
    def __init__(self, name):
        super().__init__(f"Contact {name} already exists!")

class ContactNotFoundError(ContactBookError):
    def __init__(self, name):
        super().__init__(f"Contact {name} not found!")

class InvalidContactDataError(ContactBookError):
    def __init__(self, message=(" ")):
        super().__init__(message)

class ContactBook:
    def __init__(self):
        self.contacts = {}

    def create_contact(self):
        name = input("Enter your name = ")
        if name in self.contacts:
            print(f"Contact {name} already exists!")
            logger.warning(f"Create failed: {name} already exists.", exc_info=True)
            raise ContactAlreadyExistsError(name)
        else:

            try:
                age = int(input("Enter the age = "))
                email = input("Enter the email = ").strip()
                gmail_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
                if not re.match(gmail_pattern, email):
                    raise InvalidContactDataError("Email must be a valid Gmail address ending with '@gmail.com'.")
                mobile_no = input("Enter the mobile number = ")

                if not mobile_no.isdigit():
                    raise InvalidContactDataError("Mobile number must be digits only.")
                
                if len(mobile_no) != 10:
                    raise InvalidContactDataError("Mobile number must be 10 digit.")
                
                self.contacts[name] = {'age': age, 'email': email, 'mobile_no': mobile_no}
                print(f"Contact {name} has been created successfully!")
                logger.info(f"Contact {name} created.")
            except ValueError as ve:
                logger.error(f"Invalid input while creating contact", exc_info=True)
                raise InvalidContactDataError("Age must be an integer.")

    def view_contact(self):
        name = input("Enter contact name to view = ")
        if name not in self.contacts:
            logger.warning(f"View failed: {name} not found.", exc_info=True)
            raise ContactNotFoundError(name)
        self.display_contact(name)

    def update_contact(self):
        name = input("Enter contact name to update = ")
        if name not in self.contacts:
            logger.warning(f"Update failed: {name} not found.", exc_info=True)
            raise ContactNotFoundError(name)
    
        try:
            age = int(input("Enter the updated age = "))
            email = input("Enter the updated email = ")
            gmail_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
            if not re.match(gmail_pattern, email):
                raise InvalidContactDataError("Email must be a valid Gmail address ending with '@gmail.com'.")
            mobile_no = input("Enter the updated mobile number = ")
            if not mobile_no.isdigit():
                raise InvalidContactDataError("Mobile number must be digits only.")
            
            if len(mobile_no) != 10:
                raise InvalidContactDataError("Mobile number must be 10 digit")
            
            self.contacts[name] = {'age': age, 'email': email, 'mobile_no': mobile_no}
            print(f"Contact {name} updated successfully!")
            logger.info(f"Contact {name} updated.")

        except ValueError as ve:
            logger.error(f"Invalid input while updating contact", exc_info=True)
            raise InvalidContactDataError("Age must be an integer.")

    def delete_contact(self):
        name = input("Enter contact name to delete = ")
        if name not in self.contacts:
            logger.warning(f"Delete failed: {name} not found.", exc_info=True)
            raise ContactNotFoundError(name)
        del self.contacts[name]
        print(f"Contact {name} has been deleted successfully!")
        logger.info(f"Contact {name} deleted.")

    def search_contact(self):
        search_name = input("Enter name to search = ")
        found = False
        for name, contact in self.contacts.items():
            if search_name.lower() in name.lower():
                self.display_contact(name)
                found = True

        if not found:
            print("No contact found with that name!")
            logger.info(f"No contact found with name like '{search_name}'")

    def count_contacts(self):
        print(f"Total contacts in your book: {len(self.contacts)}")
        logger.info(f"Total contact count: {len(self.contacts)}")

    def display_contact(self, name):
        contact = self.contacts[name]
        print(f"Name: {name}, Age: {contact['age']}, Email: {contact['email']}, Mobile No: {contact['mobile_no']}")

    def run(self):
        while True:
            print("\nContact Book System")
            print("1. Create Contact")
            print("2. View Contact")
            print("3. Update Contact")
            print("4. Delete Contact")
            print("5. Search Contact")
            print("6. Count Contact")
            print("7. Exit")

            try:
                choice = int(input("Enter your choice = "))

                if choice == 1:
                    self.create_contact()
                    
                elif choice == 2:
                    self.view_contact()

                elif choice == 3:
                    self.update_contact()

                elif choice == 4:
                    self.delete_contact()

                elif choice == 5:
                    self.search_contact()

                elif choice == 6:
                    self.count_contacts()

                elif choice == 7:
                    print("Closing the program...")
                    logger.info("Program exited by user.")
                    break

                else:
                    print("Invalid input! Enter a number between 1 and 7.")
                    logger.warning(f"Invalid menu choice: {choice}", exc_info=True)

            except (ContactAlreadyExistsError, ContactNotFoundError, InvalidContactDataError) as ce:
                print(f"Error: {ce}")
                logger.error(f"Custom error: {ce}", exc_info=True)

            except Exception as e:
                logger.error(f"Unexpected error while choosing", exc_info=True)
                print(f"An Unexpected error occurred : {e}")

if __name__ == "__main__":
    ContactBook().run()