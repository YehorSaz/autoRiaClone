import re

from core.services.censor_service.censor_list import censor_list


def censor(text):
    count = find_censorship(text, censor_list)
    return count


def find_censorship(text_for_censorship, list_for_censorship):
    censor_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in list_for_censorship) + r')\b', re.IGNORECASE)
    matches = censor_pattern.findall(text_for_censorship)
    return len(matches)
