import os

EXPORT_DIR = "exports"

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

DEFAULT_ENCODING = "utf-8"