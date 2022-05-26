from django_faker import Faker

from models import Note


def get_fake_data():
    populator = Faker.getPopulator()

    populator.addEntity(Note, 5)
