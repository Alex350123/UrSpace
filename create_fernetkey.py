from cryptography.fernet import Fernet
import os


def generate_fernet_key():
    """
    generate a new fernet key
    """
    return Fernet.generate_key().decode()


def write_to_env_file(key, file_path=".env"):
    """
    write the key to a .env file
    """

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
    else:
        lines = []


    key_exists = False
    for i, line in enumerate(lines):
        if line.startswith("FERNET_KEY"):
            lines[i] = f"FERNET_KEY={key}\n"
            key_exists = True
            break


    if not key_exists:
        lines.append(f"FERNET_KEY={key}\n")

    with open(file_path, "w") as file:
        file.writelines(lines)


if __name__ == "__main__":

    fernet_key = generate_fernet_key()
    write_to_env_file(fernet_key)

    print(f"FERNET_KEY generated and written to .env file：{fernet_key}")
