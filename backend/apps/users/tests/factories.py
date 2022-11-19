from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation

from users.models import Org


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(extra_kwargs={})
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class OrgFactory(DjangoModelFactory):

    name = factory.Faker('name')
    code = factory.Sequence(lambda n: "test info {}".format(n))

    class Meta:
        model = Org
