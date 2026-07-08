import os


class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASS', 'SQL12345')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'Library')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only-change-in-production')

    LOAN_PERIOD_DAYS = 14          # срок выдачи книги (один для всех ролей)
    RESERVATION_HOLD_DAYS = 3      # сколько дней бронь удерживается за первым в очереди
    FINE_PER_DAY = 0.10            # штраф за каждый день просрочки, BYN


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True