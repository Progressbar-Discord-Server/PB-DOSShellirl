from rendering import Renderer, RenderingObject
import time

class Node():
    def __init__(self, position, texture, collision_box = None):
        self.position = position
        self.texture = texture
        self.collision_box = collision_box
        self.renderobject = RenderingObject(position, texture)
    def _process(self, scene, delta):
        pass
    def _on_collision(self, scene, collider):
        pass

class Scene():
    def __init__(self):
        self.nodes = []
        self.renderer = Renderer([60, 30])
        self.stop_flag = False

    def start(self):
        loop_start_time = 0
        delta = 0
        while not self.stop_flag:
            collision_boxes = []
            for node in self.nodes:
                node._process(self, delta)
                if node.collision_box:
                    for collision_box in collision_boxes:
                        position_cb = [[axis + collision_box[0].position[i] for i, axis in enumerate(coord)] for coord in collision_box[1]]
                        node_position_cb = [[axis + node.position[i] for i, axis in enumerate(coord)] for coord in node.collision_box]
                        if (min(position_cb[1][0], node_position_cb[1][0]) > max(position_cb[0][0], node_position_cb[0][0])) and (min(position_cb[1][1], node_position_cb[1][1]) > max(position_cb[0][1], node_position_cb[0][1])):
                            node._on_collision(self, collision_box[0])
                            collision_box[0]._on_collision(self, node)
                    collision_boxes.append([node, node.collision_box])
            self.renderer.render_frame()
            delta = time.time() - loop_start_time
            loop_start_time = time.time() 
    
    def stop(self):
        self.stop_flag = True
            
    def add_node(self, node: Node):
        self.nodes.append(node)
        self.renderer.add_object(node.renderobject)

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        self.renderer.remove_object(node.renderobject)