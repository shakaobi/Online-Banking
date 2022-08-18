"""
    Manages the usernames, passwords, and balances in data.csv
    Author: Samuels, Goods,Pearson,and Garber
    Class: CMSC 495-6981
    Date Created: 2022-05-02
    Last Updated: 2022-08-10
"""

import socket
from datetime import datetime
from passlib.hash import sha256_crypt as crypt

CREDENTIALS_FILE = "data.txt"
UNSECURE_FILE = "CommonPasswords.txt"
LOG_FILE = "log.txt"

#Password requirements
LENGTH = 4
LOWER = True
UPPER = False
NUMBER = False
SPECIAL = False

def __secure_check(password):
    """Verify that candidate password meets all criteria"""

    #Check against list of unsecure passwords
    with open(UNSECURE_FILE, encoding="UTF-8") as file:
        if password in file.read():
            return "Password is a known unsecure password."

    #Password length
    if len(password) < LENGTH:
        return "Password must be at least 12 characters long."

    lower = not LOWER
    upper = not UPPER
    number = not NUMBER
    special = not SPECIAL

    #Determine if each character is lower, upper, numeric, or special
    for char in password:
        ascii_val = ord(char)
        if 96 < ascii_val < 123:
            lower = True
        elif 64 < ascii_val < 91:
            upper = True
        elif 47 < ascii_val < 58:
            number = True
        else:
            special = True

    if not (lower and upper and number and special):
        error_string1 = "Password must contain at least one lowercase, uppercase, "
        return error_string1 + "numeric, and special characters."

    return None

def verify(username, password):
    """Verifys that the correct username-hash pair exists in the credentials file"""

    #Check each row for username-hash pair
    with open(CREDENTIALS_FILE, encoding="UTF-8") as file:
        for line in file:
            if line.split()[0] == username:
                if crypt.verify(password, line.split()[1]):
                    return float(line.split()[2])

    #Log failed login attempt
    with open(LOG_FILE, "a", encoding="UTF-8") as file:
        ip = socket.gethostbyname(socket.gethostname())
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M%p")
        file.write(f"user={username}, timestamp={timestamp}, ip={ip}\n")

    return -1

def create(username, password):
    """Create new username-hash pair if username is unique and password is valid"""

    #Verify that username is not blank
    if len(username) == 0:
        return "Username cannot be blank."

    #Verify that username has no spaces
    if " " in username:
        return "Username cannot contains spaces."

    #Check if username already exists
    with open(CREDENTIALS_FILE, encoding="UTF-8") as file:
        for line in file:
            if line.split(' ')[0] == username:
                return "Username already exists."

    #Check password
    secure = __secure_check(password)
    if secure:
        return secure

    #Create new username-hash pair
    hashed = crypt.hash(password)

    with open(CREDENTIALS_FILE, "a", encoding="UTF-8") as file:
        file.write(f"{username} {hashed} 0\n")

    return None

def change(username, password):
    """Allows user to change their password"""

    #Check password
    secure = __secure_check(password)
    if secure:
        return secure

    #Update password
    hashed = crypt.hash(password)

    #Read in credentials list
    pairs = []
    with open(CREDENTIALS_FILE, encoding="UTF-8") as file:
        for line in file:
            pairs.append(line.split())

    #Rewrite crendtials file with new password
    with open(CREDENTIALS_FILE, "w", encoding="UTF-8") as file:
        for pair in pairs:
            if pair[0] == username:
                pair[1] = hashed

            file.write(f"{pair[0]} {pair[1]} {pair[2]}\n")

    return None

def update_balance(username, balance):
    """Updates user balance in data.txt"""

    #Read in credentials list
    pairs = []
    with open(CREDENTIALS_FILE, encoding="UTF-8") as file:
        for line in file:
            pairs.append(line.split())

    #Rewrite crendtials file with new password
    with open(CREDENTIALS_FILE, "w", encoding="UTF-8") as file:
        for pair in pairs:
            if pair[0] == username:
                pair[2] = "{:.2f}".format(balance)

            file.write(f"{pair[0]} {pair[1]} {pair[2]}\n")

    return None