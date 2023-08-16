import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

#
import requests
from configs.celery import app

from core.dataclasses.user_dataclass import UserDataClass
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.currencies.models import CurrenciesModel
from apps.currencies.serializers import CurrenciesSerializer
from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_NAME'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost/api/activate/{token}'
        cls.__send_email.delay(user.email, 'register.html', {'name': user.profile.name, 'url': url}, 'Register')

    @classmethod
    def change_password(cls, user: UserDataClass):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost/api/recovery/{token}'
        cls.__send_email.delay(user.email, 'change_password.html', {'name': user.profile.name, 'url': url},
                               'Change Password')


@app.task
def get_courses():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    data = requests.get(url).json()
    currency = CurrenciesModel.objects.all()
    num_for_id = 0
    if currency.count() >= 2:
        currency.delete()
    for item in data:
        data_for_serializer = {
            "name": f"{item['ccy']}",
            "base_ccy": f"{item['base_ccy']}",
            "buy": float(item['buy']),
            "sale": float(item['sale'])
        }
        serializer = CurrenciesSerializer(data=data_for_serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save(id=(num_for_id + 1))
        num_for_id += 1
