import os

class Config:
    # Kunci rahasia untuk keamanan aplikasi Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci_rahasia_yang_anda_pilih'
