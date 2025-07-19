import os
import dotenv

dotenv.load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")
if not SECRET_TOKEN:
    raise ValueError("SECRET_TOKEN must be set in the .env file")
