import logging
from colorama import Fore, Style, init
import sys
import time

# Initialize color support
init(autoreset=True)

# ==============================
# SYSTEM LOGGER
# ==============================

logger = logging.getLogger("NEMU")
logger.setLevel(logging.INFO)

if logger.handlers:
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | [%(filename)s:%(lineno)d] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logger.info("NEMU logging system initialized")


# ==============================
# CONVERSATION DISPLAY
# ==============================

def log_user(message: str):
    sys.stdout.write(Fore.GREEN + "\n--------------------------------------------------\n")
    sys.stdout.write(Fore.GREEN + Style.BRIGHT + f"USER : {message}\n")
    sys.stdout.flush()


def log_nemu(message: str):
    sys.stdout.write(Fore.CYAN + Style.BRIGHT + f"NEMU : {message}\n")
    sys.stdout.write(Fore.CYAN + "--------------------------------------------------\n\n")
    sys.stdout.flush()


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