import pygame

pygame.init()
width, height = 950, 650
screen = pygame.display.set_mode((width, height))


def start_screen():
    title = pygame.image.load('data/title.png')
    screen.blit(title, (250, 0))
    start_screen_text = ["Начать", "",
                         "Настройки", "",
                         "Выход"]

    font = pygame.font.Font(None, 50)
    text_coord = 200
    for string in start_screen_text:
        line_rendered = font.render(string, 1, pygame.Color('yellow'))
        intro_rect = line_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - line_rendered.get_width() // 2
        text_coord += intro_rect.height
        screen.blit(line_rendered, intro_rect)

running = True
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    start_screen()
    pygame.display.flip()
pygame.quit()
