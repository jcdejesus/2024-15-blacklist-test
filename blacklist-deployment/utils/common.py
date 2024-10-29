import re

UUID_REG_EXP = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"

def isUUID(id):
    try:
        return re.search(UUID_REG_EXP, id) is not None
    except ValueError:
        return False