import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# ==============================
# LOG DIRECTORY
# ==============================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_DIR,
    f"nemu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

# ==============================
# LOGGER
# ==============================

logger = logging.getLogger("NEMU")
logger.setLevel(logging.DEBUG)

if logger.handlers:
    logger.handlers.clear()

# ==============================
# FORMATTERS
# ==============================

detailed_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | [%(filename)s:%(lineno)d] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

clean_formatter = logging.Formatter("%(message)s")

# ==============================
# FILE HANDLER
# ==============================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

# ==============================
# CONSOLE HANDLER
# ==============================

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(detailed_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("NEMU logging system initialized")

# ==============================
# CONVERSATION LOGGER
# ==============================

convo_logger = logging.getLogger("CONVERSATION")
convo_logger.setLevel(logging.INFO)
convo_logger.propagate = False

convo_console = logging.StreamHandler()
convo_console.setLevel(logging.INFO)
convo_console.setFormatter(clean_formatter)

convo_file = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
convo_file.setLevel(logging.INFO)
convo_file.setFormatter(detailed_formatter)

convo_logger.addHandler(convo_console)
convo_logger.addHandler(convo_file)

# ==============================
# CONVERSATION LOG HELPERS
# ==============================

def log_user(message: str):
    convo_logger.info(f"USER : {message}")


def log_nemu(message: str):
    convo_logger.info(f"NEMU : {message}")
