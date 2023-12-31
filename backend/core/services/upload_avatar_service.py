import os
from uuid import uuid1


def upload_avatar(instance, file: str) -> str:
    ext = file.split('.')[-1]
    return os.path.join(instance.surname, 'avatar', f'{uuid1()}.{ext}')
