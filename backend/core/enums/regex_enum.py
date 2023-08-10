from enum import Enum


class RegExEnum(Enum):
    BRAND = (
        r'^[А-ЯЁІЇЄҐ][А-яёЁіІєЄїЇґҐ]{1,49}|[A-Z][a-zA-Z\d]{1,49}$',
        'First letter uppercase min 2 max 25 ch'
    )
    PASSWORD = (
        r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=(?:.*[`~!@#$%^&*()\-_+=\\\|\'\"\;\:\/?.>,<\[\]\{\}]){2,})'
        r'[a-zA-Z\d`~!@#$%^&*()\-_+=\\\|\'\"\;\:\/?.>,<\[\]\{\}]{8,30}',
        [
            'min 1 lowercase ch',
            'min 1 uppercase ch',
            'min 1 digit',
            'min 2 special character',
            'length 8-30'
        ]
    )
    NAME = (
        r'^[А-ЯЁІЇЄҐ][А-яёЁіІєЄїЇґҐ]{1,49}|[A-Z][a-zA-Z\d]{1,49}$',
        [
            'only letters, without special characters',
            'First letter uppercase',
            'min 2 max 50 ch'
        ]
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
