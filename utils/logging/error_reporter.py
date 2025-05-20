import logging
import traceback
import smtplib
from email.mime.text import MIMEText
import os

ERROR_LOG = os.path.join(os.path.dirname(__file__), '../../logs/error.log')

class ErrorReporter:
    @staticmethod
    def log_error(exc: Exception, context: str = ""):
        with open(ERROR_LOG, 'a', encoding='utf-8') as f:
            f.write(f"\n---\nContext: {context}\n{traceback.format_exc()}\n")
        logging.error(f"Error in {context}: {exc}")

    @staticmethod
    def send_error_report(exc: Exception, context: str = "", email: str = None):
        if not email:
            return
        msg = MIMEText(f"Context: {context}\n\n{traceback.format_exc()}")
        msg['Subject'] = f'CryptoQuantFactory Error Report'
        msg['From'] = email
        msg['To'] = email
        try:
            with smtplib.SMTP('localhost') as server:
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Failed to send error report: {e}")
