import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init
import sys
import time

# Initialize color support
init(autoreset=True)

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
# SYSTEM LOGGER
# ==============================

logger = logging.getLogger("NEMU")
logger.setLevel(logging.DEBUG)

if logger.handlers:
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | [%(filename)s:%(lineno)d] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("NEMU logging system initialized")

# ==============================
# CONVERSATION LOGGER
# ==============================

conversation_logger = logging.getLogger("NEMU_CONVERSATION")
conversation_logger.setLevel(logging.INFO)
conversation_logger.addHandler(file_handler)
conversation_logger.propagate = False


# ==============================
# CONVERSATION DISPLAY
# ==============================

def log_user(message: str):

    print(
        Fore.GREEN + "\n--------------------------------------------------"
    )
    print(
        Fore.GREEN + Style.BRIGHT + f"USER : {message}"
    )

    conversation_logger.info(f"USER : {message}")


def log_nemu(message: str):

    print(
        Fore.CYAN + Style.BRIGHT + f"NEMU : {message}"
    )
    print(
        Fore.CYAN + "--------------------------------------------------\n"
    )

    conversation_logger.info(f"NEMU : {message}")


# ==============================
# THINKING INDICATOR
# ==============================

def nemu_thinking():

    sys.stdout.write(Fore.YELLOW + "NEMU : Thinking")
    sys.stdout.flush()

    for _ in range(3):
        time.sleep(0.4)
        sys.stdout.write(".")
        sys.stdout.flush()

    print("\n")