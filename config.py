class Config:
    SQLALCHEMY_DATABASE_URI = 'postgres://test:test@localhost:5433/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'this is the secret key'
