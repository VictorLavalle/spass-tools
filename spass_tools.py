#!/usr/bin/env python3
"""Samsung Pass (.spass) converter - encrypt and decrypt passwords."""
import sys, os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

def menu():
    print("")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         Samsung Pass (.spass) Tools          ║")
    print("  ╚══════════════════════════════════════════════╝")
    print("")
    print("  What would you like to do?")
    print("")
    print("    1. Decrypt .spass to CSV")
    print("    2. Encrypt CSV to .spass")
    print("    3. Exit")
    print("")
    return input("  Select (1-3): ").strip()

def main():
    while True:
        choice = menu()
        if choice == '1':
            from spass_to_csv import main as decrypt_main
            decrypt_main()
        elif choice == '2':
            from csv_to_spass import main as encrypt_main
            encrypt_main()
        elif choice == '3':
            print("\n  Goodbye!\n")
            break
        else:
            print("\n  Invalid selection.")

if __name__ == '__main__':
    main()
