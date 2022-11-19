from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation, fuzzy

from resources.models import Resource, ResourceLimit

User = get_user_model()


class ResourceFactory(DjangoModelFactory):

    title = Faker("name")
    content = Faker("name")
    creator = factory.Iterator(User.objects.all())
    modifier = factory.Iterator(User.objects.all())

    class Meta:
        model = Resource


class ResourceLimitFactory(DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    is_limited = fuzzy.FuzzyChoice(choices=[True, False])
    max_limit = fuzzy.FuzzyInteger(low=1)
    creator = factory.Iterator(User.objects.all())
    modifier = factory.Iterator(User.objects.all())

    class Meta:
        model = ResourceLimit
