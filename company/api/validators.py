import uuid


def uuid_valid(val: str) -> bool:
    try:
        uuid.UUID(val)
    except ValueError:
        return False
    return True
