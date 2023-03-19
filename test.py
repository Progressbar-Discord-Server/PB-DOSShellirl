from engine import Scene, Node, SceneManager
import keyboard
import random
import colorama
import os
import string

os.system('mode con: cols=60 lines=31')

colorama.init()


class Desktop(Node):
    def __init__(self):
        super().__init__([0, 0], "Begin (B)")

    def _process(self, scene, delta):
        if keyboard.is_pressed("B"):
            scene.manager.change_current_scene("level")


current_level = 1


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
        if isinstance(collider, CyanSegment):
            if all(map(lambda x: x in ["-"], self.segments)):
                self.segments = ["░"] * collider.multiplier
                self.collision_box[0][0] = 3
            else:
                self.segments.extend(["░"] * collider.multiplier)
                self.collision_box[0][0] += 1
        if isinstance(collider, YellowSegment):
            if all(map(lambda x: x in ["-"], self.segments)):
                self.segments = ["▓"]
                self.collision_box[0][0] = 3
            else:
                self.segments.append("▓")
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
        if len(self.segments) == 20:
            scene.manager.change_current_scene("winning")


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

        if self.ticks == 20000:
            scene.remove_node(self)
            del self

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
    def __init__(self, position, speed, wobbling_speed):
        self.multiplier = random.randint(2, 3)
        super().__init__(position, f"▒x{self.multiplier}", speed, wobbling_speed)


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


class Clippy(Node):
    def __init__(self, position):
        self.key = random.choice(string.ascii_letters)
        super().__init__(position,
                         f"╔═╗╔════════════╗\n00║╠════════════╣\n╚╝║║ close  ({self.key}) ║\n╚═╝╚════════════╝")

    def _process(self, scene, delta):
        if keyboard.is_pressed(self.key):
            scene.remove_node(self)
            del self
        else:
            progressbar_pos = scene.get_node(0).position
            try:
                direction = [(progressbar_pos[i]-self.position[i]) /
                             abs(progressbar_pos[i]-self.position[i]) for i in range(2)]
                self.position[0] += direction[0] * 4 * delta
                self.position[1] += direction[1] * 4 * delta
            except ZeroDivisionError:
                pass


class ObjectGen(Node):
    def __init__(self):
        super().__init__([0, 0], "")
        self.ticks = 0
        self.wobbling_speed = min(current_level * 2, 20)
        self.speed = 2 + min(current_level * 2, 20)
        self.needed_ticks = min(40000/current_level, 2500)

    def _process(self, scene, delta):
        self.ticks += 1
        if self.ticks == self.needed_ticks:
            scene.add_node(random.choices([BlueSegment, CyanSegment, YellowSegment, PinkSegment,
                           RedSegment, NullSegment, GreenSegment], [0.3, 0.14, 0.01, 0.14, 0.3, 0.01, 0.1])[0]([random.randint(0, 60), 0], self.speed, self.wobbling_speed))
            scene.add_node(random.choice([Clippy([random.randint(0, 60),
                                                  random.randint(0, 30)])]))
            self.ticks = 0


class WinningScreen(Node):
    def __init__(self):
        global current_level
        super().__init__([16, 3], "╔═════════════════════════╗\n║        You win!         ║\n╠═════════════════════════╣\n║                         ║\n║                         ║\n║    Congratulations!     ║\n║                         ║\n║                         ║\n║      ╔═══════════╗      ║\n║      ║    O K    ║      ║\n║      ╚═══════════╝      ║\n╚═════════════════════════╝")
        current_level += 1

    def _process(self, scene, delta):
        if keyboard.is_pressed("space"):
            scene.manager.change_current_scene("desktop")


confirm = input(
    "WARNING: Flashing lights, please do not play if you're sensitive (Y)")

if confirm.upper() == "Y":
    try:
        manager = SceneManager()

        desktop = Desktop()

        desktopscene = Scene(manager, "desktop")

        desktopscene.add_node(desktop)

        progressbar = Progressbar([6, 0])

        objectgen = ObjectGen()

        scene = Scene(manager, "level")

        scene.add_node(progressbar)

        scene.add_node(objectgen)

        winning = Scene(manager, "winning")

        winning_popup = WinningScreen()

        winning.add_node(winning_popup)

        manager.change_current_scene("desktop")
    except Exception as e:
        print(e)
        input()
