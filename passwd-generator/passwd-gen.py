import random
import secrets
import string

def generate_password(length=12, use_digits=True, use_special_chars=True):
    # Define character sets
    letters = string.ascii_letters  # Upper and lowercase letters
    digits = string.digits if use_digits else ''
    special_chars = string.punctuation if use_special_chars else ''

    # Combine selected character sets
    all_chars = letters + digits + special_chars

    if not all_chars:
        raise ValueError("At least one character set must be selected.")

    # Generate a secure password
    password = ''.join(secrets.choice(all_chars) for _ in range(length))
    
    return password

# Example usage
if __name__ == "__main__":
    length = int(input("Enter password length: "))
    use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
    use_special_chars = input("Include special characters? (y/n): ").strip().lower() == 'y'

    password = generate_password(length, use_digits, use_special_chars)
    print(f"Generated Password: {password}")
