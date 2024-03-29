class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y


class Character:
    def __init__(self, start_point: Point):
        self._location = start_point

    @property
    def location(self) -> Point:
        return self._location

    def move_to(self, point: Point) -> None:
        self._location = point
