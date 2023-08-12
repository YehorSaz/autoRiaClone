from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProfileDataClass:
    id: int
    name: str
    surname: str
    age: int
    phone: int


@dataclass
class CurrencyDataclass:
    name: str
    base_ccy: str
    buy: int
    sale: int


@dataclass
class CarDataclass:
    id: int
    brand: str
    model: str
    price: int
    year: int
    created_at: datetime
    updated_at: datetime
    post: int


@dataclass
class PostsDataclass:
    id: int
    active_status: bool
    region: str
    car: CarDataclass
    created_at: datetime
    updated_at: datetime
    descriptions: str
    user: int
    views_count: int


@dataclass
class UserDataClass:
    id: int
    email: str
    password: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: datetime
    created_at: datetime
    updated_at: datetime
    account_status: str
    profile: ProfileDataClass
    posts: PostsDataclass
