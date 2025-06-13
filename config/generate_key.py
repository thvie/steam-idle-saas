from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open(".fernet.key", "wb") as f:
        f.write(key)
    print("Key generated")

if __name__ == "__main__":
    generate_key()
