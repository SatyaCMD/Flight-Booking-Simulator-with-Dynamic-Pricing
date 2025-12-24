import random
import string

def generate_captcha():
    """Generates a random 6-character alphanumeric captcha string."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
