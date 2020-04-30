import pyglet
import math


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

CAR_IMAGE = pyglet.image.load('car_v2.png')
CAR_IMAGE.anchor_x = round(CAR_IMAGE.width * 0.65)
CAR_IMAGE.anchor_y = CAR_IMAGE.height // 2

MAP_IMAGE = pyglet.image.load('track.png')
MAP_IMAGE.anchor_x = 0#SCREEN_WIDTH
MAP_IMAGE.anchor_y = 0#SCREEN_HEIGHT


class Map:
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(MAP_IMAGE)

    def draw(self):
        self.sprite.draw()


class Car:
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(CAR_IMAGE)
        self.sprite.scale = 0.1

        self.sprite.x = SCREEN_WIDTH // 2
        self.sprite.y = SCREEN_HEIGHT // 2

        self.velocity = 0

        self.steering_speed = 120

    def calculate_unit_vector(self):

        direction_radians = math.radians(self.sprite.rotation + 180)

        x = math.cos(direction_radians)
        y = -math.sin(direction_radians)

        return x, y

    def draw(self):
        self.sprite.draw()

    def rotate(self, dt, direction):
        x = self.velocity
        if self.velocity <= 20:
            m = -1/12
            rotational_change = (51.83 * (m * x) ** 3) + (129.6 * ((m * x) ** 2))
        else:
            rotational_change = 120

        rotational_change *= direction * dt

        self.sprite.rotation += rotational_change

        self.calculate_unit_vector()

    def accelerate(self, forwards=True):
        if forwards:
            self.velocity += 0.5
        else:
            self.velocity *= 0.99

    def move(self, dt):
        x, y = self.calculate_unit_vector()
        self.sprite.x += self.velocity * x * dt
        self.sprite.y += self.velocity * y * dt

    def ambient_deceleration(self, dt):
        self.velocity *= 0.7 ** dt


class Game:
    def __init__(self):
        self.window = pyglet.window.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, caption='Driving Game')

        self.car = Car()
        self.map = Map()

        self.pressed_keys = []

    def on_draw(self):
        self.window.clear()

        self.map.draw()
        self.car.draw()

    def on_key_press(self, button, modifiers):
        self.pressed_keys.append(button)

    def on_key_release(self, button, modifiers):
        index = self.pressed_keys.index(button)
        del self.pressed_keys[index]

    def on_mouse_press(self, x, y, button, modifiers):
        self.car.sprite.x = x
        self.car.sprite.y = y

    def update(self, dt):
        if pyglet.window.key.A in self.pressed_keys:
            self.car.rotate(dt, -1)
        if pyglet.window.key.D in self.pressed_keys:
            self.car.rotate(dt, 1)
        if pyglet.window.key.W in self.pressed_keys:
            self.car.accelerate()
        if pyglet.window.key.S in self.pressed_keys:
            self.car.accelerate(forwards=False)

        self.car.move(dt)
        self.car.ambient_deceleration(dt)

    def main(self):
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)
        self.window.event(self.on_mouse_press)

        pyglet.clock.schedule(self.update)

        pyglet.app.run()


if __name__ == '__main__':
    game = Game()
    game.main()
