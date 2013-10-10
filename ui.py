import pygame


class Grid(object):
    """
    A grid object for organizing and displaying pygame data.
    Attributes:
        width, height: int
        x, y: int
        cell_width, cell_height: int
        x_spacing, y_xpacing: int
        x_scale, y_scale: int
        color: tuple or list (of ints)
        border: int
        items: pygame.sprite.Group
        field: list (of lists)

    Methods:
        get_cell((x, y))
        set_cell((x, y), value)
        get_loc((x, y))
        get_pos((x, y))
        add_sprite(sprite, (x, y))
        draw(surface)
    """
    def __init__(self, width, height, x=0, y=0, cell_width=50,
            cell_height=50, x_spacing=0, y_spacing=0,
            color=(0, 0, 0), border=0):
        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.x_spacing = x_spacing
        self.y_spacing = y_spacing

        self.x_scale = cell_width + x_spacing
        self.y_scale = cell_width + y_spacing

        self.color = color

        self.border = border

        # Create a sprite group to hold the grid's sprites
        self.items = pygame.sprite.Group()

        # Create a list of length height lists with length width Nones
        self.field = [[None for j in range(self.width)]
                for i in range(self.height)]

    def get_cell(self, (x, y)):
        """
        (x, y): tuple or list (of ints)
        Returns the value of the cell at field[y][x].
        Note: A row (y) is a list of cells, while a column (x) is a value.
        Returns an object or None.
        """
        return self.field[y][x]

    def set_cell(self, (x, y), value):
        """
        (x, y): tuple or list (of ints)
        value: any object (usually int, None, or pygame.sprite.Sprite)
        Sets the value of the cell at field[y][x] to the given value.
        Note: A row(y) is a list of cells, while a column (x) is a value.
        """
        self.field[y][x] = value

    def get_loc(self, (x, y)):
        """
        (x, y): tuple or list (of ints)
        Returns a tuple of grid coordinates that correspond to position (x, y).
        Returns None if the coordinates are not in the grid.
        Returns a tuple or None.
        """
        if x < self.x or y < self.y:
            return None

        x_max = self.x + self.width * self.x_scale
        y_max = self.y + self.height * self.y_scale

        if x >= x_max or y >= y_max:
            return None

        # Subtract grid starting position to get correct alignment
        grid_x = x - self.x
        grid_y = y - self.y

        # Round to the nearest grid cell to the left of the position
        grid_x /= self.x_scale
        grid_y /= self.y_scale

        # Lists of pixels that that overlap with the nearest cell to the left
        x_range = range(self.x + grid_x * self.x_scale,
                self.x + grid_x * self.x_scale + self.cell_width)
        y_range = range(self.y + grid_y * self.y_scale,
                self.y + grid_y * self.y_scale + self.cell_height)

        if x not in x_range or y not in y_range:
            return None

        return (grid_x, grid_y)

    def get_pos(self, (x, y)):
        """
        (x, y): tuple or list (of ints)
        Takes a set of grid coordinates and returns their pixel position.
        Returns a tuple.
        """
        x = self.x + x * self.x_scale
        y = self.y + y * self.y_scale

        return (x, y)

    def add_sprite(self, sprite, (x, y)):
        """
        sprite: pygame.sprite.Sprite
        (x, y): tuple or list (of ints)
        Adds a sprite to the items group and sets its Rect position.
        Only works if the cell is empty (set to None).
        Puts the cell in the field list.
        """
        if self.get_cell((x, y)) is None:
            self.set_cell((x, y), sprite)

            sprite.rect.left = self.get_pos((x, y))[0]
            sprite.rect.top = self.get_pos((x, y))[1]

            self.items.add(sprite)

    def draw(self, surface):
        """
        surface: pygame.Surface object
        Draws each of the sprites in the items group.
        Draws grid to the specified surface using a Rect object.
        """
        self.items.draw(surface)

        cell = pygame.Rect(self.x, self.y, self.cell_width, self.cell_height)

        for row in range(self.height):
            for column in range(self.width):
                pygame.draw.rect(surface, self.color, cell, self.border)

                # Move cell to next grid location in row
                cell = cell.move(self.x_scale, 0)

            # Move cell back to left edge of grid and down one row
            cell = cell.move(-self.width * self.x_scale, self.y_scale)


class StatusBar(object):
    """
    A bar for displaying text messages on the screen.
    Specific to "A solar system."
    Attributes:
        status: Font object
        power, power_label: Font objects
        power_total: int
        income, income_label: Font objects
        income_total: int
        game_over: Font object

    Methods:
        set_status(text)
        get_income()
        change_income(x)
        get_power()
        change_power(x)
        set_game_over(text)
        draw_labels(surface)
        draw_text(surface, text)
    """
    def __init__(self, font, font_color):
        self.status = Font(font, 23, font_color, (300, 525))
        self.status.set_text("")

        self.power_label = Font(font, 22, font_color, (25, 550))
        self.power = Font(font, 22, font_color, (25, 575))
        self.power_total = 0

        self.income_label = Font(font, 22, font_color, (575, 550))
        self.income = Font(font, 22, font_color, (575, 575))
        self.income_total = 0

        self.game_over = Font(font, 25, font_color, (300, 560))

    def set_status(self, text):
        """
        text: string
        Set the status to the given text.
        Uses the Font method set_text.
        """
        self.status.set_text(text)

    def get_income(self):
        """
        Returns the total income so far.
        Returns an int.
        """
        return self.income_total

    def change_income(self, x):
        """
        x: int
        Changes the current income total by x (can be negative).
        Uses make_string to add commas
        """
        self.income_total += x
        income = "$" + make_string(self.income_total)
        self.income.set_text(income, align="right")

    def get_power(self):
        """
        Returns the current total power.
        Returns an int.
        """
        return self.power_total

    def change_power(self, x):
        """
        x: int
        Changes the current power total by x (can be negative).
        Uses make_string to add commas.
        """
        self.power_total += x
        power = make_string(self.power_total)
        self.power.set_text(power, align="left")

    def set_game_over(self, text):
        """
        text: string
        Sets the game over message to the given text.
        Uses the Font method set_text.
        """
        self.game_over.set_text(text)

    def draw_labels(self, surface):
        """
        surface: pygame.Surface
        Draws the power and income labels to a surface.
        Uses the Font method set_text.
        """
        self.power_label.set_text("Power", align="left")

        surface.blit(self.power_label.get_text(),  self.power_label.get_pos())

        self.income_label.set_text("Income", align="right")

        surface.blit(self.income_label.get_text(), self.income_label.get_pos())

    def draw_text(self, surface, text):
        """
        surface: pygame.Surface
        text: Font object.
        Draws texts to a surface.
        """
        surface.blit(text.get_text(), text.get_pos())


class Font(object):
    """
    A font object for storing and positioning text.
    Attributes:
        font: pygame.font.Font
        fixed_pos: tuple or list (of ints)
        value: pygame.Surface
        pos: pygame.Rect
        old_pos: pygame.Rect
        color: tuple or list (of ints)
    """
    def __init__(self, font, size, color, pos):
        self.font = pygame.font.Font(font, size)

        self.fixed_pos = pos

        self.value = self.font.render("", True, color)
        self.pos = self.value.get_rect()
        self.old_pos = self.pos

        self.color = color

    def set_text(self, text, align=None):
        """
        text: string
        align: string
        Sets the object's text to the given text and aligns it.
        Alignments:
            left: Rect.midleft
            right: Rect.midright
            all other: Rect.center
        The positions used for alignment are stored in fixed_pos.
        """
        self.old_pos = self.pos
        self.value = self.font.render(text, True, self.color)
        self.pos = self.value.get_rect()

        if align == "left":
            self.pos.midleft = self.fixed_pos

        elif align == "right":
            self.pos.midright = self.fixed_pos

        else:
            self.pos.center = self.fixed_pos

    def get_text(self):
        """
        Returns the value of the object's text.
        Returns a string.
        """
        return self.value

    def get_pos(self):
        """
        Returns the position of the object.
        Returns a pygame.Rect object.
        """
        return self.pos

    def get_old_pos(self):
        """
        Returns the previous position of the object.
        Returns a pygame.Rect object.
        """
        return self.old_pos


def make_string(number):
    """
    number: int or string
    Turns a number into a string with commas for the
        thousands, hundred-thousands, etc.
    Returns a string.
    """
    number = str(number)
    string_number = ""

    offset = len(number) % 3

    for i in range(len(number)):
        string_number += number[i]

        if (1 + i - offset) % 3 == 0 and i != len(number) - 1:
            string_number += ","

    return string_number
