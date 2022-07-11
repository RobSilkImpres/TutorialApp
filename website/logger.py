import logging
import os

if not os.path.isdir(os.environ.get('LOG_PATH', 'log')):
    os.mkdir(os.environ.get('LOG_PATH', 'log'))

# Configure logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

debug_file_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/debug.log')
info_file_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/info.log')
error_file_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/error.log')

debug_file_handler.setLevel(logging.DEBUG)
info_file_handler.setLevel(logging.INFO)
error_file_handler.setLevel(logging.ERROR)

debug_file_handler.setFormatter(formatter)
info_file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

logger.addHandler(debug_file_handler)
logger.addHandler(info_file_handler)
logger.addHandler(error_file_handler)