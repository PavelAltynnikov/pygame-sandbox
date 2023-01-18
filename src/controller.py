from abc import ABC, abstractmethod
from enum import Enum

import pygame

import model
import settings


class Control:
    """Представляет один элемент управления на каком либо устройстве ввода.
    Это может быть клавиатура, геймпад, дойстик и т.д.
    """
    def __init__(self, key_number: int):
        self._key_number = key_number
        self._activated = False
        self._value = 0

    @property
    def key_number(self) -> int:
        return self._key_number

    @property
    def activated(self) -> bool:
        return self._activated

    @property
    def value(self) -> float:
        return self._value

    def update_key_number(self, key_number: int) -> None:
        self._key_number = key_number

    def activate(self, value: float = 1):
        """Должен вызываться при нажатии на реальный элемент управления контроллера.

        Args:
            value: Величина с которой произошло нажатие.
            Если не нужно учитывать величину нажатия, то по умолчанию значение 1.
        """
        self._activated = True
        self._value = value

    def deactivate(self):
        """Должен вызываться при отжатии реального элемента управления контроллера.
        """
        self._activated = False
        self._value = 0


class Controller(ABC):
    """Представляет физическое устройство ввода команд."""
    def __init__(self):
        self._move_up = Control(0)
        self._move_right = Control(0)
        self._move_down = Control(0)
        self._move_left = Control(0)

    @property
    def move_right(self):
        return self._move_right

    @move_right.setter
    def move_right(self, value: Control):
        self._move_right = value

    @property
    def move_left(self):
        return self._move_left

    @move_left.setter
    def move_left(self, value: Control):
        self._move_left = value

    @property
    def move_up(self):
        return self._move_up

    @move_up.setter
    def move_up(self, value: Control):
        self._move_up = value

    @property
    def move_down(self):
        return self._move_down

    @move_down.setter
    def move_down(self, value: Control):
        self._move_down = value

    @abstractmethod
    def conduct_survey_of_controls(self) -> None:
        '''Метод который нужно вызывать при каждой итерации игрового цикла
        чтобы понять какие котролы на контроллере были активированы.
        '''
        ...

    def deactivate_all_controls(self):
        self._move_right.deactivate()
        self._move_left.deactivate()
        self._move_up.deactivate()
        self._move_down.deactivate()


class Mover:
    def __init__(self, controller: Controller):
        self._controller = controller

    def move_character(self, character: model.Character):
        speed = 0
        character.move_to(
            model.Point(
                x=self._get_new_x(character.location.x, speed),
                y=self._get_new_y(character.location.y, speed)
            )
        )

    def _get_new_x(self, start_x: float, speed: float) -> float:
        if self._controller.move_right.activated:
            return start_x + self._controller.move_right.value + speed
        if self._controller.move_left.activated:
            return start_x - abs(self._controller.move_left.value) - speed
        return start_x

    def _get_new_y(self, start_y: float, speed: float) -> float:
        if self._controller.move_up.activated:
            return start_y - abs(self._controller.move_up.value) - speed
        if self._controller.move_down.activated:
            return start_y + self._controller.move_down.value + speed
        return start_y


class PygameKeyboardController(Controller):
    def __init__(self, settings: settings.ControlSettings):
        self._settings = settings
        self._move_right = Control(settings.right.value)
        self._move_up = Control(settings.up.value)
        self._move_left = Control(settings.left.value)
        self._move_down = Control(settings.down.value)

    def conduct_survey_of_controls(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[self._move_right.key_number]:
            self._move_right.activate()
        if keys[self._move_left.key_number]:
            self._move_left.activate()
        if keys[self._move_up.key_number]:
            self._move_up.activate()
        if keys[self._move_down.key_number]:
            self._move_down.activate()


class GamePadAxe(Enum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    LEFT_TRIGGER = 4
    RIGHT_TRIGGER = 5


class GamePadButton(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    # элемента с номером 6 на моём геймпаде не оказалось
    START = 7


class PygameGamepadController(Controller):
    def __init__(self):
        # Конструктор должен принимать геймпад, потому что играть можно на нескольких
        # геймпадах одновременно.
        self._game_pad = [
            pygame.joystick.Joystick(x)
            for x
            in range(pygame.joystick.get_count())
        ][0]
        self._dead_zone = 0.05
        self._move_up = Control(GamePadAxe.LEFT_STICK_Y.value)
        self._move_right = Control(GamePadAxe.LEFT_STICK_X.value)
        self._move_down = Control(GamePadAxe.LEFT_STICK_Y.value)
        self._move_left = Control(GamePadAxe.LEFT_STICK_X.value)

    def conduct_survey_of_controls(self) -> None:
        if value := self._game_pad.get_axis(GamePadAxe.LEFT_STICK_X.value):
            if abs(value) > self._dead_zone:
                if value > 0:
                    self._move_right.activate(value)
                else:
                    self._move_left.activate(value)
        if value := self._game_pad.get_axis(GamePadAxe.LEFT_STICK_Y.value):
            if abs(value) > self._dead_zone:
                if value < 0:
                    self._move_up.activate(value)
                else:
                    self._move_down.activate(value)
