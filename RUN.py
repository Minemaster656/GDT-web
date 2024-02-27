import os

import Data

os.system(f"uvicorn main:app --reload --port {Data.PORT}")