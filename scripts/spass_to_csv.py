#!/usr/bin/env python3
"""Decrypt a Samsung Pass .spass file to CSV."""
import csv, sys, os, base64, hashlib, getpass
os.environ['TK_SILENCE_DEPRECATION'] = '1'
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

ITERATION_COUNT = 70000
KEY_LENGTH = 32
SALT_BYTES = 20
BLOCK_SIZE = 16

def pkcs7_unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def decrypt_spass(filepath, password):
    """Decrypt a .spass file and return the plaintext bytes."""
    with open(filepath, 'rb') as f:
        data_b64 = f.read()
    data = base64.b64decode(data_b64)
    salt = data[:SALT_BYTES]
    iv = data[SALT_BYTES:SALT_BYTES + BLOCK_SIZE]
    encrypted = data[SALT_BYTES + BLOCK_SIZE:]
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, ITERATION_COUNT, dklen=KEY_LENGTH)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    return pkcs7_unpad(decrypted)

def spass_to_csv(spass_path, csv_path, password):
    """Decrypt a .spass file and write passwords to CSV."""
    plaintext = decrypt_spass(spass_path, password).decode('utf-8')
    lines = plaintext.split('\r\n')

    header = lines[4].split(';')
    data_lines = [l for l in lines[5:] if l.strip()]

    rows = []
    for line in data_lines:
        fields = line.split(';')
        decoded = []
        for f in fields:
            try:
                decoded.append(base64.b64decode(f).decode('utf-8'))
            except:
                decoded.append('')
        record = dict(zip(header, decoded))
        pwd = record.get('password_value', '')
        if not pwd or pwd == '&&&NULL&&&':
            continue
        title = record.get('title', '')
        url = record.get('origin_url', '')
        user = record.get('username_value', '')
        notes = record.get('credential_memo', '')
        otp = record.get('otp', '')
        if notes == '&&&NULL&&&':
            notes = ''
        if otp == '&&&NULL&&&':
            otp = ''
        rows.append({'Title': title, 'URL': url, 'Username': user, 'Password': pwd, 'Notes': notes, 'OTPAuth': otp})

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['Title', 'URL', 'Username', 'Password', 'Notes', 'OTPAuth'])
        w.writeheader()
        w.writerows(rows)

    print(f"\n  Done! {len(rows)} passwords decrypted.")
    print(f"  Output: {csv_path}\n")

def open_file_dialog(title, filetypes):
    """Open a native file picker dialog. Returns path or empty string."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
        return path
    except:
        return ''

def save_file_dialog(title, filetypes, defaultext, initialfile=''):
    """Open a native save file dialog. Returns path or empty string."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.asksaveasfilename(title=title, filetypes=filetypes, defaultextension=defaultext, initialfile=initialfile)
        root.destroy()
        return path
    except:
        return ''

def find_spass_files():
    """Find .spass files in the project root directory."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return sorted(f for f in os.listdir(root_dir) if f.endswith('.spass'))

def main():
    print("")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   Samsung Pass (.spass) → CSV Converter   ║")
    print("  ╚══════════════════════════════════════════════╝")
    print("")

    if len(sys.argv) >= 3:
        spass_path, csv_path = sys.argv[1], sys.argv[2]
    else:
        spass_files = find_spass_files()
        if len(spass_files) == 1:
            spass_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), spass_files[0])
            print(f"  Found: {spass_files[0]}")
            use = input("  Use this file? (Y/n): ").strip().lower()
            if use and use != 'y':
                spass_path = open_file_dialog("Select .spass file", [("Samsung Pass", "*.spass"), ("All files", "*.*")])
                if not spass_path:
                    spass_path = input("\n  .spass file path: ").strip().strip("'\"")
        elif len(spass_files) > 1:
            print("  Found multiple .spass files:\n")
            for i, f in enumerate(spass_files, 1):
                print(f"     {i}. {f}")
            print(f"     {len(spass_files)+1}. Browse for a different file...")
            choice = input(f"\n  Select (1-{len(spass_files)+1}): ").strip()
            idx = int(choice) if choice.isdigit() else 0
            if idx == len(spass_files) + 1:
                spass_path = open_file_dialog("Select .spass file", [("Samsung Pass", "*.spass"), ("All files", "*.*")])
                if not spass_path:
                    spass_path = input("\n  .spass file path: ").strip().strip("'\"")
            elif 1 <= idx <= len(spass_files):
                spass_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), spass_files[idx - 1])
            else:
                print("\n  Invalid selection.")
                sys.exit(1)
        else:
            print("  No .spass files found in this folder.")
            spass_path = open_file_dialog("Select .spass file", [("Samsung Pass", "*.spass"), ("All files", "*.*")])
            if not spass_path:
                spass_path = input("  .spass file path: ").strip().strip("'\"")

        default_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'passwords.csv')
        print(f"\n  Default output: {default_csv}")
        print(f"    1. Save here (press Enter)")
        print(f"    2. Choose a different location")
        choice = input("  Select [1]: ").strip()
        if choice == '2':
            csv_path = save_file_dialog("Save CSV file", [("CSV", "*.csv")], ".csv", "passwords.csv")
            if not csv_path:
                csv_path = input("  Output CSV path: ").strip().strip("'\"")
        else:
            csv_path = default_csv

    if not os.path.isfile(spass_path):
        print(f"\n  File not found: {spass_path}")
        sys.exit(1)

    if len(sys.argv) >= 4:
        password = sys.argv[3]
    else:
        password = getpass.getpass("  Decryption password: ")

    if not password:
        print("\n  Password cannot be empty.")
        sys.exit(1)

    print("\n  Decrypting...")
    try:
        spass_to_csv(spass_path, csv_path, password)
    except Exception:
        print("\n  Wrong password or corrupted file.")
        sys.exit(1)

if __name__ == '__main__':
    main()
