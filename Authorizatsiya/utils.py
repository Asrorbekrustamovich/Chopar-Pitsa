import random

def generate_otp():
    """6 xonali tasodifiy OTP kod yaratish"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])
