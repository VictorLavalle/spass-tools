# Example Files

These are dummy test files with fake credentials for testing the tools.

## Files

| File | Description | Password |
|------|-------------|----------|
| `sample_passwords.csv` | Sample CSV with 5 fake passwords (use as input for encryption) | — |
| `sample_passwords.spass` | Encrypted `.spass` file (use as input for decryption) | `Test1234!` |

## Testing

### Decrypt the .spass file
```bash
python3 spass_to_csv.py examples/sample_passwords.spass output.csv "Test1234!"
```

### Encrypt the CSV file
```bash
python3 csv_to_spass.py examples/sample_passwords.csv output.spass "Test1234!"
```
