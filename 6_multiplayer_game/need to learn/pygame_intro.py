"""pygame tutorial"""
import sys

import pygame as pg

pg.init()

#### Screen ##
SCREEN_WIDTH, SCREEN_HIGHT = 600, 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
pg.display.set_caption("~~Pygame Tutorial~~")


#### Def vars ####
## const ##
ROUND_TIME = 25
FPS = 30


## VArs ##
clock = pg.time.Clock()


## Colors ##
BLACK = pg.Color(15, 15, 15)
TRUE_BLACK = pg.Color(0,0,0)
WHITE = pg.Color(255, 255, 255)
PLAYER_COLOR = pg.Color(125, 55, 200)


## Font ##
FONT = pg.font.SysFont("gabriola", 28)


### Def class ####


class Player:
    """A player class that the user can control"""

    def __init__(
        self, x: int, y: int, size: int, color: pg.Color = PLAYER_COLOR
    ) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color

        # Init player values
        self.dx, self.dy = 0, 0
        self.coord = (self.x, self.y, self.size, self.size)

    def update(self):
        """Update the players cords, gravity, sprite"""

        # Get a list of all the pressed keys
        keys = pg.key.get_pressed()

        # Create player rect
        player_rect = pg.draw.rect(screen, self.color, self.coord)

        # Move the player
        if keys[pg.K_UP] and player_rect.top > 0:
            self.dx, self.dy = 0, -self.size
        elif keys[pg.K_DOWN] and player_rect.bottom < SCREEN_HIGHT:
            self.dx, self.dy = 0, self.size
        elif keys[pg.K_LEFT] and player_rect.left > 0:
            self.dx, self.dy = -self.size, 0
        elif keys[pg.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            self.dx, self.dy = self.size, 0
        else:
            self.dx, self.dy = 0, 0

        # Update player coords
        self.x += self.dx
        self.y += self.dy
        self.coord = (self.x, self.y, self.size, self.size)


class Game:
    """A class to control game play"""

    def __init__(self, player: Player) -> None:
        self.player = player

        # State vars
        self.frame_count = 0  # Help determine how long one second is
        self.round_time = ROUND_TIME  # Current round time

    def draw(self):
        """Draw the sprites to screen"""

        # draw the player
        player.update()

        # Create the round time text and draw
        time_text = FONT.render(f"Time: {self.round_time}", True, WHITE)
        time_rect = time_text.get_rect()

        time_rect.center = (SCREEN_WIDTH // 2, 15)
        screen.blit(time_text, time_rect)

    def update(self):
        """Update the game, advance the clock, update player"""

        # Advance the timer
        self.frame_count += 1

        if self.frame_count % FPS == 0:
            self.round_time -= 1

        # Update player
        self.player.update()


#### Def funcs ####

#### Create objects ####
player = Player(300, 300, 25)
game = Game(player)

while True:
    screen.fill(BLACK)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Update and draw classes
    game.draw()
    game.update()

    pg.display.flip()
    clock.tick(FPS)
