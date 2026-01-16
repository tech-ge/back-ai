from cryptography.fernet import Fernet
import base64
import hashlib
from config import settings

class EncryptionService:
    """End-to-end encryption for personal vault"""
    
    def __init__(self, key: str = None):
        if key is None:
            key = settings.ENCRYPTION_KEY
        
        # Derive a Fernet key from the provided key using SHA256
        key_hash = hashlib.sha256(key.encode()).digest()
        derived_key = base64.urlsafe_b64encode(key_hash)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext to ciphertext"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        encrypted = self.cipher.encrypt(plaintext)
        return encrypted.decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext to plaintext"""
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode()
        decrypted = self.cipher.decrypt(ciphertext)
        return decrypted.decode()

# Initialize global encryption service
encryption_service = EncryptionService()
