from django.db import models


class RegionChoices(models.TextChoices):
    Vinnytsia = "Вінницька",
    Volyn = "Волинська",
    Dnipropetrovsk = "Дніпропетровська",
    Donetsk = "Донецька",
    Zhytomyr = "Житомирська",
    Zakarpattia = "Закарпатська",
    Zaporizhia = "Запорізька",
    Ivano_Frankivsk = "Івано - Франківська",
    Kyiv = "Київська",
    Kirovohrad = "Кіровоградська",
    Luhansk = "Луганська",
    Lviv = "Львівська",
    Mykolaiv = "Миколаївська",
    Odessa = "Одеська",
    Poltava = "Полтавська",
    Rivne = "Рівненська",
    Sumy = "Сумська",
    Ternopil = "Тернопільська",
    Kharkiv = "Харківська",
    Kherson = "Херсонська",
    Khmelnytskyi = "Хмельницька",
    Cherkasy = "Черкаська",
    Chernivtsi = "Чернівецька",
    Chernihiv = "Чернігівська"
