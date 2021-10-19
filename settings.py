# settings.py
from dotenv import load_dotenv, find_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True, override=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
# env_path = Path('.') / '.env'
# print(env_path)
# load_dotenv(dotenv_path=env_path)
load_dotenv(find_dotenv())
print(find_dotenv())