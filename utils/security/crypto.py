from cryptography.fernet import Fernet
import os
import logging

class KeyManager:
    def __init__(self, key_file='key.bin'):
        self.key_file = key_file
        try:
            if not os.path.exists(self.key_file):
                self.key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(self.key)
            else:
                with open(self.key_file, 'rb') as f:
                    self.key = f.read()
            self.fernet = Fernet(self.key)
        except Exception as e:
            logging.error(f'KeyManager init error: {e}')
            raise

    def encrypt(self, data: str) -> bytes:
        try:
            return self.fernet.encrypt(data.encode())
        except Exception as e:
            logging.error(f'KeyManager encrypt error: {e}')
            return b''

    def decrypt(self, token: bytes) -> str:
        try:
            return self.fernet.decrypt(token).decode()
        except Exception as e:
            logging.error(f'KeyManager decrypt error: {e}')
            return ''
