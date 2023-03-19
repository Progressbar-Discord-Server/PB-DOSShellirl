from engine import Scene, Node
import keyboard
import random
import colorama
import os

os.system('mode con: cols=60 lines=31')

colorama.init()

class Progressbar(Node):
    def __init__(self, position):
        super().__init__(position, "████████████████████████\n██                    ██\n████████████████████████", [[2, 1], [22, 2]])
        self.segments = 0
    def _process(self, scene, delta):
        self.position[1] += delta * 6 * (keyboard.is_pressed("s") - keyboard.is_pressed("w"))
        self.position[0] += delta * 12 * (keyboard.is_pressed("d") - keyboard.is_pressed("a"))
    def _on_collision(self, scene, collider):
        if isinstance(collider, BlueSegment):
            self.segments += 1
            self.collision_box[0][0] += 1
            if self.segments == 20:
                scene.stop()
        elif isinstance(collider, PinkSegment):
            self.segments -= 1
            self.collision_box[0][0] -= 1
        self.renderobject.texture = f"████████████████████████\n██{'▓' * self.segments}{' ' * (20 - self.segments)}██\n████████████████████████"

class BlueSegment(Node):
    def __init__(self, position):
        super().__init__(position, "▓", [[0, 0], [1, 1]])
    def _process(self, scene, delta):
        self.position[1] += 4 * delta
    def _on_collision(self, scene, collider):
        scene.remove_node(self)
        del self

class PinkSegment(Node):
    def __init__(self, position):
        super().__init__(position, "-", [[0, 0], [1, 1]])
    def _process(self, scene, delta):
        self.position[1] += 4 * delta
    def _on_collision(self, scene, collider):
        scene.remove_node(self)
        del self
    
class RedSegment(Node):
    def __init__(self, position):
        super().__init__(position, "!", [[0, 0], [1, 1]])
    def _process(self, scene, delta):
        self.position[1] += 0.01
    def _on_collision(self, scene, collider):
        scene.remove_node(self)
        del self

class SegmentGen(Node):
    def __init__(self):
        super().__init__([0, 0], "")
        self.ticks = 0
    def _process(self, scene, delta):
        self.ticks += 1
        if self.ticks == 10000:
            scene.add_node(random.choice([BlueSegment([random.randint(0, 60), 0]), PinkSegment([random.randint(0, 60), 0])]))
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

confirm = input("WARNING: Flashing lights, please do not play if you're sensitive (Y)")

if confirm.upper() == "Y":
    scene.start()

    winning = Scene()

    winning_popup = WinningScreen()
    winning.add_node(winning_popup)

    winning.start()