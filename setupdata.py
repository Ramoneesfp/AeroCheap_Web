import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

DATABASE_USER=os.getenv("DATABASE_USER")