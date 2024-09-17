from dotenv import load_dotenv # type: ignore
import os


load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30