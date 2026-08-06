# utils.py

# Terminal color codes
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Icons with color
CRITICAL_ICON = f"{RED}❗{RESET}"
WARNING_ICON  = f"{YELLOW}⚠️{RESET}"
GOOD_ICON     = f"{GREEN}✔️{RESET}"

# Low stock threshold
LOW_STOCK_THRESHOLD = 5


def make_bar_graph(quantity, max_length=20):
    if quantity <= 0:
        filled = 0
    else:
        filled = int((quantity / max_length) * max_length)
        if filled > max_length:
            filled = max_length

    empty = max_length - filled
    return "█" * filled + "░" * empty
