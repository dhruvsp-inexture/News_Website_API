import re


# function for validating name
def validate_name(name):
    if name.isalpha() and len(name) < 25:
        return True
    else:
        return False

# function for validating email id.
def validate_email(email):
    return re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)


# function for validating password
def validate_password(passwd):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,18}$"

    if re.fullmatch(reg, passwd):
        return True
    else:
        return False
