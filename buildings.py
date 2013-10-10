import pygame
import os


class Building(pygame.sprite.Sprite):
    """
    A generic building sprite.
    Attributes:
        name: string
        building_type: int
        cost: int
        income: int
        power: int

    Methods:
        get_name()
        get_building_type()
        get_cost()
        get_income()
        get_power()
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = None

        self.building_type = 0
        self.cost = 0
        self.income = 0
        self.power = 0

    def get_name(self):
        """
        Returns the object's name.
        Returns a string.
        """
        return self.name

    def get_building_type(self):
        """
        Returns the object's building type.
        Returns an int.
        """
        return self.building_type

    def get_cost(self):
        """
        Returns the object's cost.
        Returns an int.
        """
        return self.cost

    def get_income(self):
        """
        Returns the object's income.
        Returns an int.
        """
        return self.income

    def get_power(self):
        """
        Returns the object's power.
        Returns an int.
        """
        return self.power


class SolarPanel(Building):
    """A solar panel with cost 25 and power 10."""
    def __init__(self):
        Building.__init__(self)

        self.image = load_image('solarpanel.png')
        self.rect = self.image.get_rect()

        self.name = "Solar Panel"

        self.building_type = 1
        self.cost = 25
        self.power = 10


class House(Building):
    """A house with income 10 and power drain 1."""
    def __init__(self):
        Building.__init__(self)

        self.image = load_image('house.png')
        self.rect = self.image.get_rect()

        self.name = "House"

        self.building_type = 2
        self.income = 10
        self.power = 1


class Factory(Building):
    """A building with income 500 and power drain 20."""
    def __init__(self):
        Building.__init__(self)

        self.image = load_image('factory.png')
        self.rect = self.image.get_rect()

        self.name = "Factory"

        self.building_type = 2
        self.income = 500
        self.power = 20


class SolarFarm(Building):
    """A solar farm with cost 200 and power 100."""
    def __init__(self):
        Building.__init__(self)

        self.image = load_image('solarfarm.png')
        self.rect = self.image.get_rect()

        self.name = "Solar Farm"

        self.building_type = 1
        self.cost = 200
        self.power = 100


class Corporation(Building):
    """A corporation with income 10000 and power drain 200."""
    def __init__(self):
        Building.__init__(self)

        self.image = load_image('corporation.png')
        self.rect = self.image.get_rect()

        self.name = "Corporation"

        self.building_type = 2
        self.income = 10000
        self.power = 100


class Sun(Building):
    """The Sun! It has power 20000 and cost 0!"""
    def __init__(self):
        Building.__init__(self)

        self.image = load_image('sun.png')
        self.rect = self.image.get_rect()

        self.name = "Sun"

        self.building_type = 1
        self.cost = 0
        self.power = 20000


def load_image(filename):
    """
    filename: string
    Load the image located at 'data/filename'.
    Returns a pygame.Surface object.
    """
    location = os.path.join('data', filename)
    image = pygame.image.load(location)

    if __name__ != '__main__':
        return image

    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image
