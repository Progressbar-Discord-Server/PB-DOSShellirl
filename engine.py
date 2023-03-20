from rendering import Renderer, RenderingObject
import time
import copy


class Node():
    def __init__(self, position: list, texture: str, collision_box: str | None = None):
        """Programmable node with collision

        Args:
            position (list): Node of position
            texture (str): Texture of the node
            collision_box (str | None, optional): Collision box coordinates. Defaults to None.
        """
        self.position = position
        self.texture = texture
        self.collision_box = collision_box
        self.renderobject = RenderingObject(self.position, texture)

    def _process(self, scene: Scene, delta: int):
        """This callback is ran once in a frame.

        Args:
            scene (Scene): The current scene
            delta (int): Interval between the start of the last frame and the current one
        """

    def _ready(self, scene: Scene):
        """This callback is ran when the node is added to the scene.

        Args:
            scene (Scene): The current scene
        """

    def _on_collision(self, scene: Scene, collider: Node):
        """This callback is ran when the node collides with another one

        Args:
            scene (Scene): The current scene
            collider (Node): Colliding node
        """


class Scene():
    def __init__(self, manager: SceneManager, name: str):
        """Group of nodes.

        Args:
            manager (SceneManager): Scene manager
            name (str): Name of the scene
        """
        self.nodes = []
        self.temp_nodes = []
        self.renderer = Renderer([60, 30])
        self.stop_flag = True
        self.manager = manager
        self.manager.scenes[name] = self

    def start(self):
        """Starts the scene
        """
        loop_start_time = 0
        delta = 0

        self.renderer = Renderer([60, 30])

        self.temp_nodes = list(map(copy.deepcopy, self.nodes))
        for temp_node in self.temp_nodes:
            temp_node._ready(self)
            self.renderer.add_object(temp_node.renderobject)
        self.stop_flag = False
        while not self.stop_flag:
            collision_boxes = []
            for node in self.temp_nodes:
                node._process(self, delta)
                if node.collision_box:
                    for collision_box in collision_boxes:
                        position_cb = [[axis + collision_box[0].position[i]
                                        for i, axis in enumerate(coord)] for coord in collision_box[1]]
                        node_position_cb = [
                            [axis + node.position[i] for i, axis in enumerate(coord)] for coord in node.collision_box]
                        if (min(position_cb[1][0], node_position_cb[1][0]) > max(position_cb[0][0], node_position_cb[0][0])) and (min(position_cb[1][1], node_position_cb[1][1]) > max(position_cb[0][1], node_position_cb[0][1])):
                            node._on_collision(self, collision_box[0])
                            collision_box[0]._on_collision(self, node)
                    collision_boxes.append([node, node.collision_box])
            self.renderer.render_frame()
            delta = time.time() - loop_start_time
            loop_start_time = time.time()

    def stop(self):
        """Stops the scene
        """
        self.stop_flag = True

    def add_node(self, node: Node):
        """Adds a node to the scene

        Args:
            node (Node): Node to be added
        """
        if self.stop_flag:
            self.nodes.append(node)
        else:
            self.temp_nodes.append(node)
            self.renderer.add_object(node.renderobject)
            node._ready(self)

    def get_node(self, id: int):
        """Gets a node by using its id

        Args:
            id (int): Node index

        Returns:
            Node: The node object
        """
        return self.temp_nodes[id]

    def remove_node(self, node: Node):
        """Removes a node from the scene

        Args:
            node (Node): Node to remove
        """
        self.temp_nodes.remove(node)
        self.renderer.remove_object(node.renderobject)


class SceneManager():
    def __init__(self):
        """Manages the scenes
        """
        self.scenes = {}
        self.current_scene = None

    def change_current_scene(self, new_scene: str):
        """Changes the scene

        Args:
            new_scene (str): Scene to start
        """
        if self.current_scene:
            self.current_scene.stop()
        self.current_scene = self.scenes[new_scene]
        self.scenes[new_scene].start()
