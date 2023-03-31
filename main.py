# ------------ Package Import ------------

import OpenGL.GL as GL
import glfw
import numpy as np

# ------------ Library Import ------------

from libs.transform import Trackball
from itertools import cycle

# ------------ Shape Import ------------

from shapes.tetrahedron import *
from shapes.cylinder import *
from shapes.cube import *
from shapes.triangle import *
from shapes.pyramid import *
from shapes.cone import *
from shapes.sphere import *
from shapes.mesh import *
from shapes.ellipsoid import *


class Viewer:

    def __init__(self, width=800, height=800):
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

        # version hints: create GL windows with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)
        glfw.window_hint(glfw.DEPTH_BITS, 16)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # initialize trackball
        self.trackball = Trackball()
        self.mouse = (0, 0)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_cursor_pos_callback(self.win, self.on_mouse_move)
        glfw.set_scroll_callback(self.win, self.on_scroll)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.5, 0.5, 0.5, 0.1)
        # GL.glClearColor(0, 0, 0, 1)
        # GL.glEnable(GL.GL_CULL_FACE)   # enable backface culling (Exercise 1)
        # GL.glFrontFace(GL.GL_CCW) # GL_CCW: default

        GL.glEnable(GL.GL_DEPTH_TEST)  # enable depth test (Exercise 1)
        GL.glDepthFunc(GL.GL_LESS)   # GL_LESS: default

        # initially empty list of object to draw
        self.drawables = []

    def run(self):
        """ Main render loop for this OpenGL windows """
        while not glfw.window_should_close(self.win):
            # clear draw buffer
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(win_size)

            # draw our scene objects
            for drawable in self.drawables:
                drawable.draw(projection, view, None)

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this windows """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            if key == glfw.KEY_W:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))

            for drawable in self.drawables:
                if hasattr(drawable, 'key_handler'):
                    drawable.key_handler(key)

    def on_mouse_move(self, win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.trackball.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.trackball.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.trackball.zoom(deltay, glfw.get_window_size(win)[1])


def printUsage():
    print('python main.py Cube Gouraud')
    print('python main.py Tetrahedron Gouraud')
    print('python main.py Cylinder Gouraud')
    print('python main.py Triangle Gouraud')
    print('python main.py Pyramid Gouraud')
    print('python main.py Cone Gouraud')
    print('python main.py Sphere Gouraud')
    print('python main.py Ellipsoid Gouraud')
    print('python main.py Mesh Gouraud')


def main(argv):
    viewer = Viewer()
    if len(argv) < 1:
        printUsage()
        return
    elif argv[0] == 'Cube' and argv[1] == 'Gouraud':
        model = Cube('resources/shaders/gouraud.vert',
                     'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Pyramid' and argv[1] == 'Gouraud':
        model = Pyramid('resources/shaders/gouraud.vert',
                        'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Cylinder' and argv[1] == 'Gouraud':
        model = Cylinder('resources/shaders/gouraud.vert',
                         'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Tetrahedron' and argv[1] == 'Gouraud':
        model = Tetrahedron('resources/shaders/gouraud.vert',
                            'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Cone' and argv[1] == 'Gouraud':
        model = Cone('resources/shaders/gouraud.vert',
                     'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Sphere' and argv[1] == 'Gouraud':
        model = Sphere('resources/shaders/gouraud.vert',
                       'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Ellipsoid' and argv[1] == 'Gouraud':
        model = Ellipsoid('resources/shaders/gouraud.vert',
                          'resources/shaders/gouraud.frag').setup()
    elif argv[0] == 'Mesh' and argv[1] == 'Gouraud':
        model = Mesh('resources/shaders/gouraud.vert',
                     'resources/shaders/gouraud.frag').setup()

    viewer.add(model)
    viewer.run()


if __name__ == '__main__':
    glfw.init()
    main(sys.argv[1:])
    glfw.terminate()
