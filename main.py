import pygame
import effect

pygame.init()

screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()


# create instance/s using Lines()
lines = [effect.Lines(400, (0, 800), depth= 500-150)]

running = True

while running:
    screen.fill((0, 0, 0))

    # ---------------------------------------------------------------------------------------------------------------------------------
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pos()[1] < lines[0].baseline_y + 5 and pygame.mouse.get_pos()[1] > lines[0].baseline_y - 5 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            lines[0].trigger(pygame.mouse.get_pos()[0])

    # ---------------------------------------------------------------------------------------------------------------------------------
    # update
    dt = clock.tick()/1000
    for line in lines:
        line.update(dt)

    # ---------------------------------------------------------------------------------------------------------------------------------
    # draw
    for line in lines:
        line.draw(screen)
    
    pygame.display.update()


    

pygame.quit()