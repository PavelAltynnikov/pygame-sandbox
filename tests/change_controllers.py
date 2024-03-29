import pygame

import setup  # noqa
from sandbox.controllers import (
    Controller, PygameKeyboard, PygameIntermittentKeyboard,
    PygameGamepad, PygameIntermittentGamepad
)
from sandbox.settings import ControllerSettings, Setting

pygame.init()


class Text:
    def __init__(self, screen, font, color: tuple[int, int, int]):
        self._screen = screen
        self._font = font
        self._color = color

    def render(self, value: str, location: tuple[int, int]):
        self._screen.blit(
            self._font.render(value, False, self._color),
            location
        )


class Test:
    def __init__(self):
        settings = ControllerSettings(
            right=Setting(1073741903),
            left=Setting(1073741904),
            up=Setting(1073741906),
            down=Setting(1073741905),
        )
        self._controllers: list[Controller] = [
            PygameKeyboard(settings),
            PygameGamepad(),
            PygameIntermittentKeyboard(settings),
            PygameIntermittentGamepad(),
        ]
        self._controller_index = 0
        self._controller = self._controllers[self._controller_index]

    def _render_labels(self, text):
        text.render("For change controller press \"accept\" on a keyboard", (10, 10))
        text.render(f"current controller: {self._controller}", (10, 35))
        text.render(f"up={self._controller.move_up._activated}", (10, 60))
        text.render(f"right={self._controller.move_right._activated}", (10, 85))
        text.render(f"down={self._controller.move_down._activated}", (10, 110))
        text.render(f"left={self._controller.move_left._activated}", (10, 135))
        text.render(f"accept={self._controller.accept._activated}", (10, 160))
        text.render(f"quit={self._controller.quit._activated}", (10, 185))

    def _quit_button_is_pressed(self, event):
        return (
            event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, ))
        )

    def _change_controller(self) -> None:
        if self._controller.accept.activated:
            self._controller_index += 1
            if self._controller_index == len(self._controllers):
                self._controller_index = 0
            self._controller = self._controllers[self._controller_index]

    def _start_loop(self, screen, color):
        close_window = False
        clock = pygame.time.Clock()
        fps = 30

        font = pygame.font.SysFont('Consolas', 25)
        black_color = (0, 0, 0)
        text = Text(screen, font, black_color)

        while not close_window:
            events = pygame.event.get()
            self._controller.conduct_survey_of_controls(events)
            if self._controller.quit.activated:
                return
            self._change_controller()

            screen.fill(color)
            self._render_labels(text)

            pygame.display.update()

            self._controller.deactivate_all_controls()
            clock.tick(fps)

    def start(self):
        SCREEN_SIZE = (1000, 500)

        pygame.init()
        pygame.joystick.init()

        pygame.key.set_repeat(500)
        screen = pygame.display.set_mode(SCREEN_SIZE)
        blue = (0, 49, 83)

        self._start_loop(screen, blue)


if __name__ == '__main__':
    t = Test()
    t.start()
