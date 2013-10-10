import pygame
import buildings
import ui


class Game(object):
    """
    Main game object.
    Attributes:
        black, white, grey
        screen, screen_width, screen_height, screen_pos
        clock
        mouse_sprite
        background
        grid, palette, status_bar
        game_started, start_loc

    Methods:
        draw_mouse()
        draw_text(text)
        add_building(grid, sprite, pos, status=None)
        check_for_new_buildings()
        process_click(pos)
        process_grid_click(pos)
        process_palette_click(sprite)
        start_game()
        end_game()
        update_income()
        main()
    """
    def __init__(self):
        # Define colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (25, 25, 25)

        # Set icon
        icon = buildings.load_image('solarsystem.png')
        pygame.display.set_icon(icon)

        # Set screen
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height)
                )
        self.screen_pos = (0, 0)

        # Set title
        pygame.display.set_caption("A solar system")

        # Set framerate object
        self.clock = pygame.time.Clock()

        # Set object for drawing sprites on the mouse
        self.mouse_sprite = pygame.sprite.GroupSingle()

        # Set background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()
        self.background.fill(self.black)

        # Create Grid for the playing field
        self.grid = ui.Grid(10, 10, x=100, color=self.grey, border=1)

        # Set start of game conditions
        self.game_started = False

        starting_panel = buildings.SolarPanel()
        self.start_loc = (4, 5)

        self.grid.add_sprite(starting_panel, self.start_loc)

        self.grid.draw(self.background)

        # Create Grid for the palette
        self.palette = ui.Grid(1, 6, x=25, y=25, y_spacing=25,
                color=self.grey, border=1)

        self.palette.draw(self.background)

        # Create StatusBar for displaying messages
        self.status_bar = ui.StatusBar(None, self.white)
        self.status_bar.change_power(starting_panel.get_power())

        # Draw background onto the screen
        self.screen.blit(self.background, self.screen_pos)
        pygame.display.update()

        # Draw initial status
        self.status_bar.set_status(
                "You stumble upon an abandoned solar panel - "
                       "maybe you can turn it on?"
                )
        self.draw_text(self.status_bar.status)

    def draw_mouse(self):
        """
        Draws the mouse sprite on the cursor.
        Covers the old position with the background image.
        Uses dirty rect animation to only update the parts of the
            screen that the mouse moves through.
        """
        sprite = self.mouse_sprite.sprite

        mouse_rects = []
        mouse_rects.append(sprite.rect.copy())

        self.screen.blit(self.background, sprite.rect, sprite.rect)

        pos = pygame.mouse.get_pos()
        sprite.rect.center = pos

        mouse_rects.append(sprite.rect)

        self.mouse_sprite.draw(self.screen)
        pygame.display.update(mouse_rects)

    def draw_text(self, text):
        """
        Draws the given status objects to the screen.
        Covers the old position with black filler.
        Uses dirty rect animation to only update the parts of the
            screen that contain the text.
        """
        old_pos = text.get_old_pos()
        pos = text.get_pos()

        rects = []
        rects.append(old_pos)

        filler = pygame.Surface((self.screen_width, self.screen_height))
        filler.fill(self.black)

        self.background.blit(filler, old_pos, old_pos)

        rects.append(pos)

        self.background.blit(text.get_text(), pos)
        self.screen.blit(self.background, self.screen_pos)

        pygame.display.update(rects)

    def add_building(self, grid, sprite, pos, status=None):
        """
        Adds a sprite to a grid.
        Draws the sprite and the grid it's inside.
        Uses dirty rect animation to only update the part of the
            screen that contains the sprite and its grid cell.
        Draws a status message to the screen (if one is provided).
        """
        rects = []
        rects.append(sprite.rect.copy())

        grid.add_sprite(sprite, pos)

        rects.append(sprite.rect)

        grid.draw(self.background)
        self.screen.blit(self.background, self.screen_pos)

        pygame.display.update(rects)

        if status is not None:
            self.status_bar.set_status(status)
            self.draw_text(self.status_bar.status)

    def check_for_new_buildings(self):
        """
        Checks to see whether more buildings should be added to the palette.
        If so, add them.
        New buildings are added based on the income accumulated so far and
            what buildings are already in the palette.
        A status message is provided when the building is added.
        """
        income = self.status_bar.get_income()
        n = len(self.palette.items)

        if n == 1 and income >= 100:
            self.add_building(self.palette, buildings.SolarPanel(), (0, 1),
                    status="You have learned to build solar panels!")

        if n == 2 and income >= 500:
            self.add_building(self.palette, buildings.Factory(), (0, 2),
                    status="You can now power factories!")

        if n == 3 and income >= 10000:
            self.add_building(self.palette, buildings.SolarFarm(), (0, 3),
                    status="You have learned to build solar farms!")

        if n == 4 and income >= 50000:
            self.add_building(self.palette, buildings.Corporation(), (0, 4),
                    status="You can now power corporations!")

        if n == 5 and income >= 1000000:
            self.add_building(self.palette, buildings.Sun(), (0, 5),
                    status="You have learned to harvest the Sun!")

    def process_click(self, pos):
        """
        Decides what to do when the mouse is clicked.
        If no sprite is on the cursor:
            Check if the game has started and start it if not.
            Check if there was a click on the palette and process it if so.
        If there is a sprite on the cursor:
            Check if there was a click on the grid and process it if so.
        """
        if len(self.mouse_sprite) == 0:
            if not self.game_started:
                loc = self.grid.get_loc(pos)

                if loc == self.start_loc:
                    self.start_game()

            else:
                loc = self.palette.get_loc(pos)

                if loc is not None:
                    sprite = self.palette.get_cell(loc)
                    self.process_palette_click(sprite)

        elif len(self.mouse_sprite) == 1:
            loc = self.grid.get_loc(pos)

            if loc is not None:
                self.process_grid_click(loc)

    def process_grid_click(self, pos):
        """
        Determines whether to place the mouse sprite onto the grid.
        If the cell at the provided position is empty:
            Add the building to the grid.
            Use the sprite's name and type to send a status message
                about the new addition.
            Empty the mouse_sprite object.
        """
        if self.grid.get_cell(pos) is None:
            sprite = self.mouse_sprite.sprite

            name = sprite.name.lower()

            if sprite.get_building_type() == 1:
                if name == "sun":
                    status = "You have harnessed the power of the Sun!"
                else:
                    status = "You built a " + str(name) + "!"

            else:
                status = "You powered a " + str(name) + "!"

            self.add_building(self.grid, sprite, pos, status)

            self.mouse_sprite.empty()

    def process_palette_click(self, sprite):
        """
        Determines whether to add a palette sprite to the cursor.
        If there was no sprite provided, do nothing.
        If the building is a power generator (type 1):
            If there is enough income to cover the cost of the building:
                Subtract the cost from the total income.
                Increase the power pool by the amount the building generates.
                Add the sprite to the mouse_sprite object.
            If there is not enough income to cover the cost:
                Set the status to inform the user.
        If the sprite is an income generator (not type 1):
            If there is sufficient power to power the building:
                Subtract the power cost from the power pool.
            If there is insufficient power:
                Set the status to inform the user.
        """
        if sprite is None:
            return

        sprite = type(sprite)()

        if sprite.building_type == 1:
            if self.status_bar.get_income() >= sprite.cost:
                self.status_bar.change_income(-sprite.cost)
                self.draw_text(self.status_bar.income)

                self.status_bar.change_power(sprite.power)
                self.draw_text(self.status_bar.power)

                self.mouse_sprite.add(sprite)

            else:
                self.status_bar.set_status("You cannot afford that!")
                self.draw_text(self.status_bar.status)

        else:
            if self.status_bar.get_power() >= sprite.power:
                self.status_bar.change_power(-sprite.power)
                self.draw_text(self.status_bar.power)

                self.mouse_sprite.add(sprite)

            else:
                self.status_bar.set_status("You don't have the power!")
                self.draw_text(self.status_bar.status)

    def start_game(self):
        """
        Starts the game when the initial solar panel is clicked.
        Adds a House object to the palette and draws the status bar
            to the screen. Updates the entire display.
        """
        self.game_started = True

        house = buildings.House()
        self.add_building(self.palette, house, (0, 0),
                status="You can now power houses!")

        self.status_bar.draw_labels(self.background)
        self.screen.blit(self.background, self.screen_pos)

        self.draw_text(self.status_bar.power)

        self.status_bar.change_income(0)
        self.draw_text(self.status_bar.income)

        pygame.display.update()

    def end_game(self):
        """
        Ends the game when all grid objects are full.
        Displays a final message in the 'game over' portion
            of the screen depending on how much income has been
            accumulated so far.
        """
        if self.status_bar.get_income() >= 1000000:
            end_text = "You're rich!"

        else:
            end_text = "Game over."

        self.status_bar.set_game_over(end_text)

        self.draw_text(self.status_bar.game_over)

    def update_income(self):
        """
        Gets the sum of the income from all of the buildings
            that generate income and increases the total income
            by that amount.
        """
        income = 0

        for building in self.grid.items:
            if building.get_building_type() != 1:
                income += building.income

        self.status_bar.change_income(income)
        self.draw_text(self.status_bar.income)

    def main(self):
        """
        Main game loop.
        Ends when the window is closed.
        Determines what should be done when the left mouse
            button is pressed down.
        Draws the mouse if there is an object in the mouse group.
        Updates the income and checks for new buildings every
            5 seconds (20 fps means 100 ticks per 5 seconds).
        Ends the game once the grid is full of buildings.
        """
        done = False
        count = 20

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if len(self.grid.items) < 100:
                        pos = pygame.mouse.get_pos()
                        self.process_click(pos)

            count += 1

            if len(self.mouse_sprite) == 1:
                self.draw_mouse()

            if len(self.grid.items) > 1 and count % 100 == 0:
                self.update_income()
                self.check_for_new_buildings()

            if len(self.grid.items) == 100:
                self.end_game()

            self.clock.tick(20)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.main()
    pygame.quit()
