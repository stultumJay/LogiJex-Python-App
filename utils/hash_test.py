# hash_test.py
#
# This script is a utility for generating and verifying password hashes.
# It is used for testing and ensuring consistency with the hashing mechanisms
# (SHA-256 and MD5 for legacy) used in the DatabaseManager for user authentication.
#
# Usage: Run directly (python utils/hash_test.py) to see hash outputs.
#
# Helper modules: Uses hashlib for hash generation.

import hashlib

def main():
    # This function demonstrates the hashing process for predefined passwords.
    # It prints SHA-256 and MD5 hashes for 'admin' and 'password'.
    # It also compares these generated hashes with known hardcoded values
    # to verify the hashing logic.
    
    # Test admin password
    admin_pw = "admin"  # Define the admin password string.
    admin_hash_sha256 = hashlib.sha256(admin_pw.encode()).hexdigest()  # Generate SHA-256 hash.
    admin_hash_md5 = hashlib.md5(admin_pw.encode()).hexdigest()      # Generate MD5 hash.
    print(f"admin SHA-256 hash: {admin_hash_sha256}")  # Output the SHA-256 hash.
    print(f"admin MD5 hash: {admin_hash_md5}")          # Output the MD5 hash.
    
    # Test manager and retailer passwords (using a common example password 'password')
    password = "password"  # Define a common test password string.
    password_hash_sha256 = hashlib.sha256(password.encode()).hexdigest()  # Generate SHA-256 hash.
    password_hash_md5 = hashlib.md5(password.encode()).hexdigest()      # Generate MD5 hash.
    print(f"'password' SHA-256 hash: {password_hash_sha256}")  # Output the SHA-256 hash.
    print(f"'password' MD5 hash: {password_hash_md5}")          # Output the MD5 hash.
    
    # Compare with hardcoded values (these should match the DatabaseManager's default user hashes if generated with the same logic)
    # This section helps verify that the hashing logic is consistent.
    admin_hardcoded = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # Expected SHA-256 for 'admin'.
    password_hardcoded = "5f4dcc3b5aa765d61d8327deb882cf99"  # Expected MD5 for 'password' (example of legacy hash).
    
    print(f"Admin SHA-256 hash match: {admin_hash_sha256 == admin_hardcoded}")  # Check if generated admin SHA-256 matches hardcoded.
    print(f"Password MD5 hash match: {password_hash_md5 == password_hardcoded}")    # Check if generated 'password' MD5 matches hardcoded.

if __name__ == "__main__":
    # This ensures main() is called only when the script is executed directly.
    main() 