import math
import time


class RenderingObject():
    def __init__(self, position: list, texture: str):
        """Renderable object

        Args:
            position (list): Position in the frame
            texture (str): Texture of the object
        """
        self.position = position
        self.texture = texture

    def set_position(self, position: list):
        """Sets the object current position

        Args:
            position (list): New position
        """
        self.position = position


class Renderer():
    def __init__(self, viewport_size: list):
        """Class that processes rendering objects

        Args:
            viewport_size (list): Size of the viewport
        """
        self.objects = []
        self.viewport_size = viewport_size
        self.last_frame = []
        self.frames_without_clear = 0

    def add_object(self, obj: RenderingObject):
        """Adds an object to the renderer

        Args:
            obj (RenderingObject): Object to be added
        """
        self.objects.append(obj)

    def remove_object(self, obj: RenderingObject):
        """Removes an object from the renderer

        Args:
            obj (RenderingObject): Object to be removed
        """
        self.objects.remove(obj)

    def render_frame(self):
        """Renders and prints all objects
        """
        viewport_vector = [[' ' for _ in range(
            self.viewport_size[0])] for _ in range(self.viewport_size[1])]
        for obj in self.objects:
            for row_i, row in enumerate(map(list, obj.texture.split("\n"))):
                for column_i, column in enumerate(row):
                    if 0 <= int(row_i + obj.position[1]) <= self.viewport_size[1] - 1 and 0 <= int(column_i + obj.position[0]) <= self.viewport_size[0] - 1:
                        viewport_vector[int(
                            row_i + obj.position[1])][int(column_i + obj.position[0])] = column

        if viewport_vector != self.last_frame:
            self.last_frame = viewport_vector
            self.frames_without_clear += 1
            if self.frames_without_clear == 20:
                self.frames_without_clear = 0
                print("\033c\033[3J")
            else:
                print("\033[2J\033[1;1H", end="")
            for row in viewport_vector:
                row_str = ""
                for column in row:
                    if column:
                        row_str += column

                print(row_str)
