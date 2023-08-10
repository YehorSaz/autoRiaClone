import os
from uuid import uuid1


def upload_image(instance, file:str) -> str:
    ext = file.split('.')[-1]
    return os.path.join(instance.brand, 'image', f'{uuid1()}.{ext}')
