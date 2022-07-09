from re import S
import pygame as pg
import sys
import math

# Global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
FPS = 60
RES = SCREEN_WIDTH, SCREEN_HEIGHT
MAP_SIZE = 8
TILE_SIZE = (SCREEN_WIDTH // 2) // MAP_SIZE
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 240
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = MAP_SIZE * TILE_SIZE
SCALE = (SCREEN_WIDTH // 2) // CASTED_RAYS

# Global Variables
player_x = (SCREEN_WIDTH // 2) // 2
player_y = (SCREEN_WIDTH // 2) // 2
player_angle = math.pi

MAP = ('########'
       '#  #   #'
       '#  #   #'
       '#      #'
       '#    ###'
       '# ##   #'
       '#  #   #'
       '########')

# init pygame and create window
pg.init()
win = pg.display.set_mode(RES)
pg.display.set_caption("Raycasting Tutorial")
clock = pg.time.Clock()


# draw map
def draw_map():
    # loop over rows
    for row in range(MAP_SIZE):
        # loop over columns
        for col in range(MAP_SIZE):
            # calculate index
            square = row * MAP_SIZE + col
            # draw map in pg widow
            pg.draw.rect(
                win,
                (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)

            )
    # draw Player on map
    pg.draw.circle(win, (200, 0, 0), (player_x, player_y), 8)
    # draw Player direction
    pg.draw.line(win, (0, 255, 0), (player_x, player_y),
                 (player_x - math.sin(player_angle) * 50,
                  player_y + math.cos(player_angle) * 50),
                 3)
    # draw player fov
    pg.draw.line(win, (0, 255, 255), (player_x, player_y),
                 (player_x - math.sin(player_angle - HALF_FOV) * 50,
                  player_y + math.cos(player_angle - HALF_FOV) * 50),
                 3)
    pg.draw.line(win, (0, 255, 255), (player_x, player_y),
                 (player_x - math.sin(player_angle + HALF_FOV) * 50,
                  player_y + math.cos(player_angle + HALF_FOV) * 50),
                 3)


# Raycating algorithm
def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            row = target_y // TILE_SIZE
            col = target_x // TILE_SIZE

            square = int(row * MAP_SIZE + col)
            if MAP[square] == '#':
                pg.draw.rect(win, (0, 0, 255),
                             (col * TILE_SIZE,
                              row * TILE_SIZE,
                              TILE_SIZE - 2,
                              TILE_SIZE - 2))
                # pg.draw.line(win, (255, 255, 0), (player_x,
                #              player_y), (target_x, target_y))

                # wall shading
                color = 255 / (1 + depth * depth * 0.0001)

                # fix fish eye effect
                depth *= math.cos(player_angle - start_angle)

                # calculate wall height
                wall_height = 21000 / (depth + 0.0001)

                # fix stuck at the wall
                if wall_height > SCREEN_HEIGHT:
                    wall_height = SCREEN_HEIGHT

                # draw 3D projection (rectangle by rectangle...)
                pg.draw.rect(win, (color, color, color), (
                    SCREEN_HEIGHT + ray * SCALE,
                    (SCREEN_HEIGHT / 2) - wall_height / 2,
                    SCALE, wall_height))
                break

        start_angle += STEP_ANGLE


forward = True

while True:
    # escape conditions
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    square = row * MAP_SIZE + col
    if MAP[square] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    # draw map
    pg.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    pg.draw.rect(win, (0, 200, 10),
                 (SCREEN_HEIGHT,
                 SCREEN_HEIGHT/2,
                 SCREEN_HEIGHT,
                 SCREEN_HEIGHT))
    pg.draw.rect(win, (0, 150, 150),
                 (SCREEN_HEIGHT,
                  -SCREEN_HEIGHT/2,
                  SCREEN_HEIGHT,
                  SCREEN_HEIGHT))

    draw_map()

    cast_rays()
    # get user input
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player_angle -= 0.1
    if keys[pg.K_RIGHT]:
        player_angle += 0.1
    if keys[pg.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pg.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

     # set FPS
    clock.tick(FPS)

    # display FPS
    fps = str(int(clock.get_fps()))

    # pick up the font
    font = pg.font.SysFont('Monospace Regular', 50)

    # create font surface
    fps_surface = font.render(fps, False, (255, 0, 0))

    # print FPS to screen
    win.blit(fps_surface, (480, 0))

    # update display
    pg.display.flip()
