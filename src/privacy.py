from cryptography.fernet import Fernet
import os

class SecurityLayer:
    def __init__(self):
        # In a real app, store this key securely
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_sensitive_data(self, text):
        """Encrypts sensitive log content for secure storage."""
        return self.cipher.encrypt(text.encode()).decode()

    def anonymize_user(self, user_id):
        """Pseudo-anonymization via hashing."""
        import hashlib
        return hashlib.sha256(user_id.encode()).hexdigest()