import PyPDF2
import argparse
import getpass
import random
import string
import time
from termcolor import colored

# Function to validate the strength of the password
def validate_password_strength(password):
    """
    Validates the strength of a password.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password meets strength requirements, False otherwise.

    Raises:
        ValueError: If the password does not meet strength requirements.
    """
    if len(password) < 16:  # Password must be at least 16 characters long
        raise ValueError("Password must be at least 16 characters long.")
    if not any(char.isdigit() for char in password):  # Must contain at least one digit
        raise ValueError("Password must include at least one digit.")
    if not any(char.isupper() for char in password):  # Must contain at least one uppercase letter
        raise ValueError("Password must include at least one uppercase letter.")
    if not any(char.islower() for char in password):  # Must contain at least one lowercase letter
        raise ValueError("Password must include at least one lowercase letter.")
    if not any(char in "!@#$%^&*()-_+=<>?/" for char in password):  # Must contain at least one special character
        raise ValueError("Password must include at least one special character (!@#$%^&*()-_+=<>?/).")
    return True  # If all checks pass, password is strong

# Function to generate a strong random password
def generate_random_password():
    """
    Generates a strong random password that meets all the required criteria.

    Returns:
        str: A randomly generated password.
    """
    # Define the character sets for each password requirement
    digits = string.digits
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    special_characters = "!@#$%^&*()-_+=<>?/"

    # Start the password with one character from each required set
    password = [
        random.choice(digits),  # At least one digit
        random.choice(uppercase),  # At least one uppercase letter
        random.choice(special_characters),  # At least one special character
        random.choice(lowercase)  # At least one lowercase letter
    ]
    
    # Fill the rest of the password with random characters from all sets to ensure it's 16 characters long
    all_characters = string.ascii_letters + string.digits + special_characters
    password += [random.choice(all_characters) for _ in range(12)]  # Fill the remaining 12 characters
    
    # Shuffle the password to ensure the characters are randomly distributed
    random.shuffle(password)
    
    # Return the password as a string
    return ''.join(password)

# Function to create a password-protected PDF from an existing one
def create_password_protected_pdf(input_pdf, output_pdf, password):
    """
    Creates a password-protected PDF from an input PDF.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path to the output password-protected PDF file.
        password (str): Password to encrypt the PDF.
    """
    try:
        # Validate the password strength before proceeding
        validate_password_strength(password)

        # Print message indicating the password being used
        print(colored(f"Locking with password: {password}", 'green'))

        # Open the input PDF file in read-binary mode
        with open(input_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)  # Read the input PDF
            pdf_writer = PyPDF2.PdfWriter()  # Prepare a writer object for the output PDF

            # Add all pages from the input PDF to the writer
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Encrypt the PDF with the given password
            pdf_writer.encrypt(password)

            # Write the encrypted PDF to the output file
            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)

            print(colored(f"Password-protected PDF saved as {output_pdf}", 'blue'))

    except FileNotFoundError:
        print(colored(f"Error: The file '{input_pdf}' was not found.", 'red'))
    except PyPDF2.errors.PdfReadError:
        print(colored(f"Error: The file '{input_pdf}' is not a valid PDF.", 'red'))
    except ValueError as e:
        print(colored(f"Password Error: {e}", 'red'))
    except Exception as e:
        print(colored(f"Error: {e}", 'red'))

# Main function that drives the program
def main():
    # Display a fun intro message
    print(colored("Welcome to the PDF Password Protector!", 'yellow'))
    print(colored("Your PDFs will be safely encrypted with a strong password.\n", 'cyan'))
    
    # Add a cool prompt for the user
    parser = argparse.ArgumentParser(description="Create a password-protected PDF.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input PDF file.")
    parser.add_argument('-o', '--output', required=True, help="Path to the output password-protected PDF file")
    args = parser.parse_args()

    # Ask the user if they want to generate a strong random password
    generate_password = input(colored("Would you like to generate a strong random password? (y/n): ", 'light_magenta')).strip().lower()

    if generate_password == 'y':
        print(colored("Generating a strong random password...\n", 'magenta'))
        time.sleep(1)  # Simulate a loading pause
        password = generate_random_password()
        print(colored(f"Generated password: {password}\n", 'green'))
    else:
        # Loop to ensure the password meets the criteria
        while True:
            # Prompt for password securely
            password = getpass.getpass("Enter the password for the PDF: ")

            if not password:
                print(colored("No password entered. Generating a strong random password...", 'magenta'))
                time.sleep(1)
                password = generate_random_password()
                print(colored(f"Generated password: {password}", 'green'))
                break
            
            try:
                # Validate the entered password
                validate_password_strength(password)
                break  # Exit the loop if the password is valid
            except ValueError as e:
                print(colored(f"Password Error: {e}", 'red'))
                print(colored("Please try again.", 'yellow'))

    create_password_protected_pdf(args.input, args.output, password)

    print(colored("\nNote: No PDF protection is 100% secure. Use strong passwords and additional encryption layers if needed.", 'grey'))


# Execute the main function when the script runs
if __name__ == "__main__":
    main()
