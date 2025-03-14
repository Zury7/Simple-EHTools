import random
import secrets
import string
import nltk
from nltk.corpus import words

# Download words dataset if not already downloaded
try:
    nltk.data.find('corpora/words.zip')
except LookupError:
    nltk.download('words')

def generate_password(length=12, use_digits=True, use_special_chars=True, use_words=False):
    word_list = words.words()
    password_parts = []
    
    if use_words:
        word_part = '-'.join(secrets.choice(word_list) for _ in range(max(1, length // 6)))
        password_parts.append(word_part)
    
    # Define character sets
    letters = string.ascii_letters  # Upper and lowercase letters
    digits = string.digits if use_digits else ''
    special_chars = string.punctuation if use_special_chars else ''
    
    # Ensure at least one digit and one special character if required
    if use_digits:
        password_parts.append(secrets.choice(digits))
    if use_special_chars:
        password_parts.append(secrets.choice(special_chars))
    
    # Fill remaining length with random characters
    all_chars = letters + digits + special_chars
    remaining_length = length - sum(len(part) for part in password_parts)
    if remaining_length > 0:
        password_parts.append(''.join(secrets.choice(all_chars) for _ in range(remaining_length)))
    
    # Mix all parts randomly
    password = list(''.join(password_parts))
    random.shuffle(password)
    
    return ''.join(password)

# Example usage
if __name__ == "__main__":
    length = int(input("Enter password length: "))
    use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
    use_special_chars = input("Include special characters? (y/n): ").strip().lower() == 'y'
    use_words = input("Use known English words? (y/n): ").strip().lower() == 'y'
    num_passwords = int(input("How many passwords to generate?: "))

    passwords = [generate_password(length, use_digits, use_special_chars, use_words) for _ in range(num_passwords)]
    
    print("Generated Passwords:")
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}: {pwd}")