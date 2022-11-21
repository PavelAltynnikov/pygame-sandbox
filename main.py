import pygame

pygame.init()
pygame.key.set_repeat(1)


class Character:
    def __init__(self):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill((250, 50, 50))
        self.rect = self.surface.get_rect()
        self.rect.center = (300, 300)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.rect.x += 1
            self.rect.y -= 1
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.rect.x += 1
            self.rect.y += 1
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.rect.x -= 1
            self.rect.y -= 1
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.rect.x -= 1
            self.rect.y += 1
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 1
        elif keys[pygame.K_LEFT]:
            self.rect.x -= 1
        elif keys[pygame.K_UP]:
            self.rect.y -= 1
        elif keys[pygame.K_DOWN]:
            self.rect.y += 1

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Window:
    def __init__(self, caption, size, character):
        pygame.display.set_caption(caption)
        self._screen = pygame.display.set_mode(size)
        self._character = character

    @staticmethod
    def _is_quit(event):
        return (
            event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q))
        )

    def _event_handler(self):
        events = pygame.event.get()
        for event in events:
            if self._is_quit(event):
                pygame.display.quit()

    def show(self):
        green_color = (30, 89, 89)
        while True:
            self._event_handler()
            self._character.move()

            self._screen.fill(green_color)
            self._character.draw(self._screen)

            pygame.display.update()


if __name__ == '__main__':
    window = Window(
        caption='Controls tests',
        size=(1000, 500),
        character=Character()
    )
    window.show()
