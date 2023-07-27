import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean windows system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from itertools import cycle
from libs.transform import *
from shapes.planet import *

# ------------  Viewer class & windows management ------------------------------


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
        GL.glClearColor(0, 0, 0, 0.1)
        # GL.glEnable(GL.GL_CULL_FACE)   # enable backface culling (Exercise 1)
        # GL.glFrontFace(GL.GL_CCW) # GL_CCW: default

        GL.glEnable(GL.GL_DEPTH_TEST)  # enable depth test (Exercise 1)
        GL.glDepthFunc(GL.GL_LESS)   # GL_LESS: default

        # initially empty list of object t draw
        self.drawables = []

    def run(self):
        earth_orbit = 0
        earth_orbit_sun = 0
        moon_orbit = 0
        moon_orbit_earth = 0
        sun_orbit_itself = 0
        while not glfw.window_should_close(self.win):
            # clear draw buffer
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(win_size)

            earth_to_sun = translate(50.0, 0, 0)
            sun_to_earth = translate(-50.0, 0, 0)
            earth_rotate = rotate(axis=(0, 0, 1), angle=earth_orbit)
            earth_rotate = earth_to_sun @ earth_rotate @ sun_to_earth
            earth_rotate_sun = rotate(axis=(0, 0, 1), angle=earth_orbit_sun)
            earth_rotate = earth_rotate_sun @ earth_rotate
            earth_orbit += 0.0075 * (360 / 24)
            earth_orbit_sun += 0.1 * (360 / 8764)

            moon_to_sun = translate(55.0, 0, 0)
            sun_to_moon = translate(-55.0, 0, 0)
            moon_rotate = rotate(axis=(0, 0, 1), angle=moon_orbit)
            moon_rotate = moon_to_sun @ moon_rotate @ sun_to_moon
            moon_rotate_earth = rotate(axis=(0, 0, 1), angle=moon_orbit_earth)
            moon_rotate_earth = earth_to_sun @ moon_rotate_earth @ sun_to_earth
            moon_rotate = earth_rotate_sun @ (moon_rotate_earth @ moon_rotate)
            moon_orbit_earth += 0.075 * (360 / (24 * 27.3))

            sun_rotate = rotate(axis=(0, 0, 1), angle=sun_orbit_itself)
            sun_orbit_itself += 0.0025
            moon_orbit += 0.0075 * (360 / (24 * 29.5))

            for i in range(len(self.drawables)):
                if i == 0:
                    self.drawables[i].draw(
                        projection, view, earth_rotate, None)
                elif i == 1:
                    self.drawables[i].draw(projection, view, moon_rotate, None)
                else:
                    self.drawables[i].draw(projection, view, sun_rotate, None)

            glfw.swap_buffers(self.win)

            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this windows """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            if key == glfw.KEY_W:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))

            for drawable in self.drawables:
                if hasattr(drawable, 'key_handler'):
                    drawable.key_handler(key)

    def on_mouse_move(self, win, xpos, ypos):
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.trackball.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.trackball.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        self.trackball.zoom(deltay, glfw.get_window_size(win)[1])


def main():
    viewer = Viewer()

    earth = Planet("resources/shaders/phongtex.vert",
                   "resources/shaders/phongtex.frag", [50.0, 0.0, 0.0], 2.0, 50, 50, 0).setup()
    moon = Planet("resources/shaders/phongtex.vert",
                  "resources/shaders/phongtex.frag", [55.0, 0.0, 0.0], 0.5, 50, 50, 1).setup()
    sun = Planet("resources/shaders/phongtex.vert",
                 "resources/shaders/phongtex.frag", [0.0, 0.0, 0.0], 10.0, 50, 50, 2).setup()
    viewer.add(earth)
    viewer.add(moon)
    viewer.add(sun)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize windows system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
