#!/usr/bin/env python3
"""Samsung Pass (.spass) converter - encrypt and decrypt passwords."""
import sys, os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

def main():
    print("")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         Samsung Pass (.spass) Tools          ║")
    print("  ╚══════════════════════════════════════════════╝")
    print("")
    print("  What would you like to do?")
    print("")
    print("    1. Decrypt .spass to CSV")
    print("    2. Encrypt CSV to .spass")
    print("")
    choice = input("  Select (1-2): ").strip()

    if choice == '1':
        from spass_to_csv import main as decrypt_main
        decrypt_main()
    elif choice == '2':
        from csv_to_spass import main as encrypt_main
        encrypt_main()
    else:
        print("\n  Invalid selection.")
        sys.exit(1)

if __name__ == '__main__':
    main()
