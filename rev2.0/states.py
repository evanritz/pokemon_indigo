
import enum

class AppStates(enum.Enum):
    start = 1
    text = 2
    battle = 3
    game = 4
    trans = 5

class DirStates(enum.Enum):
    up = 1
    down = 2
    left = 3
    right = 4
    none = 5

