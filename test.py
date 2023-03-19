from engine import Scene, Node
import keyboard
import random
import colorama
import os

os.system('mode con: cols=60 lines=31')

colorama.init()


class Progressbar(Node):
    def __init__(self, position):
        super().__init__(position,
                         "████████████████████████\n██                    ██\n████████████████████████", [[2, 1], [22, 2]])
        self.segments = []

    def _process(self, scene, delta):
        self.position[1] += delta * 6 * \
            (keyboard.is_pressed("s") - keyboard.is_pressed("w"))
        self.position[0] += delta * 12 * \
            (keyboard.is_pressed("d") - keyboard.is_pressed("a"))

    def _on_collision(self, scene, collider):
        if isinstance(collider, BlueSegment):
            if all(map(lambda x: x in ["-"], self.segments)):
                self.segments = ["░"]
                self.collision_box[0][0] = 3
            else:
                self.segments.append("░")
                self.collision_box[0][0] += 1
                if len(self.segments) == 20:
                    scene.stop()
        if isinstance(collider, CyanSegment):
            if all(map(lambda x: x in ["-"], self.segments)):
                self.segments = ["░"] * collider.multiplier
                self.collision_box[0][0] = 3
            else:
                self.segments.extend(["░"] * collider.multiplier)
                self.collision_box[0][0] += 1
                if len(self.segments) == 20:
                    scene.stop()
        if isinstance(collider, YellowSegment):
            if all(map(lambda x: x in ["-"], self.segments)):
                self.segments = ["▓"]
                self.collision_box[0][0] = 3
            else:
                self.segments.append("░")
                self.collision_box[0][0] += 1
                if len(self.segments) == 20:
                    scene.stop()
        elif isinstance(collider, PinkSegment):
            if all(map(lambda x: x == "-", self.segments)):
                self.segments.append("-")
                self.collision_box[0][0] += 1
            else:
                self.segments.pop()
                self.collision_box[0][0] -= 1
        elif isinstance(collider, RedSegment):
            raise Exception("You lost!")
        elif isinstance(collider, GreenSegment):
            self.segments = ["░"] * 20
            scene.stop()
        self.renderobject.texture = f"████████████████████████\n██{''.join(self.segments)}{' ' * (20 - len(self.segments))}██\n████████████████████████"


class Segment(Node):
    def __init__(self, position, texture, speed, wobbling_speed):
        super().__init__(position, texture, [[0, 0], [1, 1]])
        self.speed = speed
        self.wobbling_speed = wobbling_speed
        self.ticks = 0
        self.wobbling_direction = 1

    def _process(self, scene, delta):
        self.position[1] += self.speed * delta
        self.position[0] += self.wobbling_speed * \
            self.wobbling_direction * delta
        self.ticks += 1
        if self.ticks == 1000:
            self.wobbling_direction *= -1
            self.ticks = 0

    def _on_collision(self, scene, collider):
        scene.remove_node(self)
        del self

class BlueSegment(Segment):
    def __init__(self, position, speed, wobbling_speed):
        super().__init__(position, "░", speed, wobbling_speed)

class YellowSegment(Segment):
    def __init__(self, position, speed, wobbling_speed):
        super().__init__(position, "▓", speed, wobbling_speed)

class CyanSegment(Segment):
    def __init__(self, position, speed, wobbling_speed, multiplier):
        super().__init__(position, f"▒x{multiplier}", speed, wobbling_speed)
        self.multiplier = multiplier

class PinkSegment(Segment):
    def __init__(self, position, speed, wobbling_speed):
        super().__init__(position, "-", speed, wobbling_speed)

class RedSegment(Segment):
    def __init__(self, position, speed, wobbling_speed):
        super().__init__(position, "!", speed, wobbling_speed)

class NullSegment(Segment):
    def __init__(self, position, speed, wobbling_speed):
        super().__init__(position, "0", speed, wobbling_speed)

class GreenSegment(Segment):
    def __init__(self, position, speed, wobbling_speed):
        super().__init__(position, "✓", speed, wobbling_speed)

class SegmentGen(Node):
    def __init__(self):
        super().__init__([0, 0], "")
        self.ticks = 0

    def _process(self, scene, delta):
        self.ticks += 1
        if self.ticks == 10000:
            scene.add_node(random.choice([BlueSegment([random.randint(0, 60), 0], 4, 4), PinkSegment([random.randint(
                0, 60), 0], 4, 4), RedSegment([random.randint(0, 60), 0], 4, 4), YellowSegment([random.randint(0, 60), 0], 4, 4),
                NullSegment([random.randint(0, 60), 0], 4, 4), GreenSegment([random.randint(0, 60), 0], 4, 4),
                CyanSegment([random.randint(0, 60), 0], 4, 4, random.randint(2, 3))]))
            self.ticks = 0


class WinningScreen(Node):
    def __init__(self):
        super().__init__([16, 3], "╔═════════════════════════╗\n║        You win!         ║\n╠═════════════════════════╣\n║                         ║\n║                         ║\n║    Congratulations!     ║\n║                         ║\n║                         ║\n║      ╔═══════════╗      ║\n║      ║    O K    ║      ║\n║      ╚═══════════╝      ║\n╚═════════════════════════╝")

    def _process(self, scene, delta):
        if keyboard.is_pressed("space"):
            scene.stop()


progressbar = Progressbar([6, 0])

segmentgen = SegmentGen()

scene = Scene()

scene.add_node(progressbar)

scene.add_node(segmentgen)

confirm = input(
    "WARNING: Flashing lights, please do not play if you're sensitive (Y)")

if confirm.upper() == "Y":
    scene.start()

    winning = Scene()

    winning_popup = WinningScreen()
    winning.add_node(winning_popup)

    winning.start()
