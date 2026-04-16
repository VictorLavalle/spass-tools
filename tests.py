"""Unit tests for spass-tools."""
import csv, io, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from csv_to_spass import encrypt_spass, validate_password, build_password_row, csv_to_spass, b64e
from spass_to_csv import decrypt_spass, spass_to_csv


class TestEncryptDecryptRoundtrip(unittest.TestCase):
    """Test that encrypt then decrypt returns original data."""

    def test_roundtrip_bytes(self):
        plaintext = b'hello world test data'
        password = 'Test1234!'
        encrypted = encrypt_spass(plaintext, password)
        with tempfile.NamedTemporaryFile(suffix='.spass', delete=False) as f:
            f.write(encrypted)
            path = f.name
        try:
            decrypted = decrypt_spass(path, password)
            self.assertEqual(decrypted, plaintext)
        finally:
            os.unlink(path)

    def test_roundtrip_csv(self):
        csv_content = 'Title,URL,Username,Password,Notes,OTPAuth\nTest,https://example.com/,user,REPLACE_ME,,\n'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            csv_path = f.name
        spass_path = csv_path + '.spass'
        out_csv = csv_path + '.out.csv'
        try:
            csv_to_spass(csv_path, spass_path, 'Test1234!')
            spass_to_csv(spass_path, out_csv, 'Test1234!')
            with open(out_csv, encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['Title'], 'Test')
            self.assertEqual(rows[0]['URL'], 'https://example.com/')
            self.assertEqual(rows[0]['Username'], 'user')
            self.assertEqual(rows[0]['Password'], 'REPLACE_ME')
        finally:
            for p in (csv_path, spass_path, out_csv):
                if os.path.exists(p):
                    os.unlink(p)

    def test_wrong_password_raises(self):
        plaintext = b'secret data'
        encrypted = encrypt_spass(plaintext, 'Test1234!')
        with tempfile.NamedTemporaryFile(suffix='.spass', delete=False) as f:
            f.write(encrypted)
            path = f.name
        try:
            with self.assertRaises(Exception):
                decrypt_spass(path, 'WrongPass1!')
        finally:
            os.unlink(path)


class TestColumnDetection(unittest.TestCase):
    """Test CSV column auto-detection for each password manager format."""

    def _roundtrip(self, csv_content):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            csv_path = f.name
        spass_path = csv_path + '.spass'
        out_csv = csv_path + '.out.csv'
        try:
            csv_to_spass(csv_path, spass_path, 'Test1234!')
            spass_to_csv(spass_path, out_csv, 'Test1234!')
            with open(out_csv, encoding='utf-8') as f:
                return list(csv.DictReader(f))
        finally:
            for p in (csv_path, spass_path, out_csv):
                if os.path.exists(p):
                    os.unlink(p)

    def test_apple_format(self):
        rows = self._roundtrip('Title,URL,Username,Password,Notes,OTPAuth\nSite,https://example.com/,user,REPLACE_ME,note,\n')
        self.assertEqual(rows[0]['Title'], 'Site')
        self.assertEqual(rows[0]['Username'], 'user')
        self.assertEqual(rows[0]['Notes'], 'note')

    def test_google_format(self):
        rows = self._roundtrip('name,url,username,password,note\nSite,https://example.com/,user,REPLACE_ME,note\n')
        self.assertEqual(rows[0]['Title'], 'Site')
        self.assertEqual(rows[0]['Username'], 'user')

    def test_lastpass_format(self):
        rows = self._roundtrip('url,username,password,extra,name,grouping,fav\nhttps://example.com/,user,REPLACE_ME,mynote,Site,Group,0\n')
        self.assertEqual(rows[0]['Title'], 'Site')
        self.assertEqual(rows[0]['URL'], 'https://example.com/')
        self.assertEqual(rows[0]['Notes'], 'mynote')

    def test_bitwarden_format(self):
        rows = self._roundtrip('folder,favorite,type,name,notes,fields,reprompt,login_uri,login_username,login_password,login_totp\nFolder,,login,Site,mynote,,0,https://example.com/,user,REPLACE_ME,\n')
        self.assertEqual(rows[0]['Title'], 'Site')
        self.assertEqual(rows[0]['URL'], 'https://example.com/')
        self.assertEqual(rows[0]['Username'], 'user')

    def test_1password_format(self):
        rows = self._roundtrip('Title,Url,Username,Password,Notes,Type\nSite,https://example.com/,user,REPLACE_ME,,Login\n')
        self.assertEqual(rows[0]['Title'], 'Site')
        self.assertEqual(rows[0]['URL'], 'https://example.com/')


class TestPasswordValidation(unittest.TestCase):
    """Test Samsung Pass password requirements."""

    def test_valid_password(self):
        valid, _ = validate_password('Test1234!')
        self.assertTrue(valid)

    def test_too_short(self):
        valid, msg = validate_password('Te1!')
        self.assertFalse(valid)
        self.assertIn('8 characters', msg)

    def test_missing_categories(self):
        valid, msg = validate_password('alllowercase')
        self.assertFalse(valid)
        self.assertIn('3 of', msg)

    def test_two_categories_fails(self):
        valid, _ = validate_password('testtest1')
        self.assertFalse(valid)

    def test_three_categories_passes(self):
        valid, _ = validate_password('Testtest1')
        self.assertTrue(valid)

    def test_special_chars_only_accepted(self):
        valid, _ = validate_password('!!@@##$$%%')
        self.assertFalse(valid)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_empty_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write('Title,URL,Username,Password,Notes\n')
            csv_path = f.name
        spass_path = csv_path + '.spass'
        try:
            with self.assertRaises(SystemExit):
                csv_to_spass(csv_path, spass_path, 'Test1234!')
        finally:
            for p in (csv_path, spass_path):
                if os.path.exists(p):
                    os.unlink(p)

    def test_build_row_has_35_fields(self):
        row = build_password_row(1, 'https://example.com/', 'user', 'pass', 'title', 'notes', 'otp')
        self.assertEqual(len(row.split(';')), 35)

    def test_b64e_roundtrip(self):
        import base64
        original = 'hello world'
        encoded = b64e(original)
        decoded = base64.b64decode(encoded).decode('utf-8')
        self.assertEqual(decoded, original)

    def test_sample_spass_file(self):
        """Test decryption of the included sample file."""
        sample = os.path.join(os.path.dirname(__file__), 'examples', 'sample_passwords.spass')
        if os.path.exists(sample):
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
                out = f.name
            try:
                spass_to_csv(sample, out, 'Test1234!')
                with open(out, encoding='utf-8') as f:
                    rows = list(csv.DictReader(f))
                self.assertEqual(len(rows), 5)
            finally:
                os.unlink(out)


if __name__ == '__main__':
    unittest.main()
