# `.spass` Format Reference

## Encryption

| Parameter | Value |
|-----------|-------|
| Algorithm | AES-256-CBC |
| Key derivation | PBKDF2-HMAC-SHA256 |
| Iterations | 70,000 |
| Salt | 20 random bytes |
| IV | 16 random bytes |
| Padding | PKCS7 |
| File encoding | `base64(salt + iv + encrypted_data)` |

## Internal Structure

Line separator: `\r\n` (CRLF)

```
30                                    ← format version
true;false;false;false                ← modules (passwords;cards;addresses;notes)
false                                 ← unknown field (new in v25+)
next_table                            ← section delimiter
_id;origin_url;action_url;...         ← header (35 semicolon-separated fields)
<base64>;<base64>;...                 ← data rows (each field base64-encoded)
```

## Password Record Fields (35 total)

| # | Field | Value |
|---|-------|-------|
| 0 | `_id` | Incremental ID |
| 1 | `origin_url` | Site URL |
| 2 | `action_url` | `&&&NULL&&&` |
| 3 | `username_element` | empty |
| 4 | `username_value` | Username |
| 5 | `id_tz_enc` | `&&&NULL&&&` |
| 6 | `password_element` | empty |
| 7 | `password_value` | Password |
| 8 | `pw_tz_enc` | `&&&NULL&&&` |
| 9 | `host_url` | Same as origin_url |
| 10 | `ssl_valid` | `0` |
| 11 | `preferred` | `0` |
| 12 | `blacklisted_by_user` | `0` |
| 13 | `use_additional_auth` | `1` |
| 14 | `cm_api_support` | `&&&NULL&&&` |
| 15 | `created_time` | Timestamp (ms) |
| 16 | `modified_time` | Timestamp (ms) |
| 17 | `title` | Site/app name |
| 18 | `favicon` | PNG bytes or empty |
| 19 | `source_type` | `2` |
| 20 | `app_name` | App name |
| 21 | `package_name` | Android package or empty |
| 22 | `package_signature` | Package signature or empty |
| 23–30 | `reserved_1`–`reserved_8` | `&&&NULL&&&` (except `reserved_2` = `0`) |
| 31 | `credential_memo` | Notes |
| 32 | `otp` | OTP auth URI |
| 33 | `root_id` | `&&&NULL&&&` |
| 34 | `parent_id` | `&&&NULL&&&` |

> **Note**: Null fields use `&&&NULL&&&` (3 ampersands each side). Fields `username_element` and `password_element` are actual empty strings.
