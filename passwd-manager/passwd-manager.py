import sqlite3
import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from getpass import getpass
import json

db_file = "passwords.db"
salt = b"this_is_a_fixed_salt"  # Use a securely generated salt in production

# Function to derive key from password
def derive_key(master_password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(master_password.encode())

# Function to encrypt data
def encrypt(plain_text: str, key: bytes) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    padder = PKCS7(128).padder()
    padded_text = padder.update(plain_text.encode()) + padder.finalize()
    
    encrypted = encryptor.update(padded_text) + encryptor.finalize()
    
    return base64.b64encode(iv + encrypted).decode()

# Function to decrypt data
def decrypt(encrypted_text: str, key: bytes) -> str:
    try:
        data = base64.b64decode(encrypted_text)
        iv, encrypted = data[:16], data[16:]
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
        
        unpadder = PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        return decrypted.decode()
    except Exception as e:
        print("Decryption failed! Possible incorrect password or corrupted data.")
        return ""

# Function to initialize database
def init_db():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to add credentials
def add_credentials(service, username, password, key):
    encrypted_password = encrypt(password, key)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("INSERT INTO credentials (service, username, password) VALUES (?, ?, ?)", 
              (service, username, encrypted_password))
    conn.commit()
    conn.close()
    print("Credentials stored securely!")

# Function to retrieve credentials
def get_credentials(service, key):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT username, password FROM credentials WHERE service = ?", (service,))
    result = c.fetchone()
    conn.close()
    if result:
        username, encrypted_password = result
        decrypted_password = decrypt(encrypted_password, key)
        if decrypted_password:
            print(f"Service: {service}\nUsername: {username}\nPassword: {decrypted_password}")
    else:
        print("No credentials found.")

# Function to list all saved services
def list_services():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT DISTINCT service FROM credentials")
    services = c.fetchall()
    conn.close()
    if services:
        print("Saved Services:")
        for service in services:
            print(f"- {service[0]}")
    else:
        print("No services found.")

# Function to delete a credential entry
def delete_credentials(service):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("DELETE FROM credentials WHERE service = ?", (service,))
    conn.commit()
    conn.close()
    print("Credential deleted successfully!")

# Main logic
def main():
    init_db()
    master_password = getpass("Enter master password: ")
    key = derive_key(master_password)
    
    while True:
        print("\n1. Add Credentials")
        print("2. Retrieve Credentials")
        print("3. List All Services")
        print("4. Delete Credentials")
        print("5. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            add_credentials(service, username, password, key)
        elif choice == "2":
            service = input("Enter service name to retrieve: ")
            get_credentials(service, key)
        elif choice == "3":
            list_services()
        elif choice == "4":
            service = input("Enter service name to delete: ")
            delete_credentials(service)
        elif choice == "5":
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
