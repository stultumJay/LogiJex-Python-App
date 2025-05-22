import hashlib

def main():
    # Test admin password
    admin_pw = "admin"
    admin_hash_sha256 = hashlib.sha256(admin_pw.encode()).hexdigest()
    admin_hash_md5 = hashlib.md5(admin_pw.encode()).hexdigest()
    print(f"admin SHA-256 hash: {admin_hash_sha256}")
    print(f"admin MD5 hash: {admin_hash_md5}")
    
    # Test manager and retailer passwords
    password = "password"
    password_hash_sha256 = hashlib.sha256(password.encode()).hexdigest()
    password_hash_md5 = hashlib.md5(password.encode()).hexdigest()
    print(f"'password' SHA-256 hash: {password_hash_sha256}")
    print(f"'password' MD5 hash: {password_hash_md5}")
    
    # Compare with hardcoded values
    admin_hardcoded = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
    password_hardcoded = "5f4dcc3b5aa765d61d8327deb882cf99"
    
    print(f"Admin SHA-256 hash match: {admin_hash_sha256 == admin_hardcoded}")
    print(f"Password MD5 hash match: {password_hash_md5 == password_hardcoded}")

if __name__ == "__main__":
    main() 