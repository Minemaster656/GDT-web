import os
import config

os.system(f"uvicorn main:app --reload --port {config.PORT}")