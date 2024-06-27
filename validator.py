from uuid import UUID


def is_valid_uuid(uuid: str) -> bool:
    try:
        uuid_object = UUID(uuid)
    except ValueError:
        return False
    return str(uuid_object) == uuid
