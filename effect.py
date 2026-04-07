import pygame
from dataclasses import dataclass
import math

@dataclass
class Wave():
    origin_x: float
    amp: float
    freq: float
    speed: float
    decay: float
    age: float = 0.0

    def is_alive(self):
        return self.amp > 0.01

    def update(self, dt: float):
        self.age += 2*dt
        self.amp *=  (1 - self.decay) ** dt # so hight decay = faster

    def y_at(self, x:int, spread):
        # return self.amp/(abs(self.origin_x - x)+1)//1 * math.sin(self.freq * abs(x - self.origin_x ) + self.age * self.speed)
        return (self.amp * math.sin(self.freq * abs(x - self.origin_x ) + self.age * self.speed))/(abs(self.origin_x - x)/spread+1)#//1
    
class Lines():
    """Draws a line on the screen at baseline_y and from the x coords in span_x. .trigger() takes an int for the x coord along the line where the wave starts"""
    def __init__(self, baseline_y: int, span_x: tuple, amp: float = 20, freq: float = 0.1, speed: float = 3, decay: float = 0.5, spread: float = 5, depth: int = 0):
        self.baseline_y = baseline_y
        self.span_x = span_x
        self.amp = amp
        self.freq = freq / (self.span_x[1] - self.span_x[0])
        self.speed = speed
        self.decay = decay
        self.waves = []
        self.spread = spread
        self.depth = depth

    def trigger(self, x: int, amp = None):
        """Parameter amp can be overridden here e.g. for larger wave based on collision velocity"""
        if amp == None:
            amp = self.amp
        wave = Wave(x, amp, self.freq, self.speed, self.decay)
        self.waves.append(wave)
    
    def update(self, dt: float):
        for w in self.waves:
            w.update(dt)
        self.waves = [w for w in self.waves if w.is_alive()]
    
    def draw(self, screen: pygame.Surface, colour: tuple = (0, 100, 150)):
        num_points = 10
        step = max(1, (self.span_x[1] - self.span_x[0]) // num_points)
        points_list = [(x, sum(w.y_at(x, self.spread) for w in self.waves) + self.baseline_y) for x in range(self.span_x[0], self.span_x[1]+step, step)] # 100 works here
        polygon_points = points_list + [(self.span_x[1], self.baseline_y + self.depth), (self.span_x[0], self.baseline_y + self.depth)]
        if len(self.waves) >= 1:
            pygame.draw.polygon(screen, colour, polygon_points)
            pygame.draw.aalines(screen, (200, 200, 200), False, points=points_list)
        else:
            pygame.draw.polygon(screen, colour, polygon_points)
            pygame.draw.line(screen, (200, 200, 200), (self.span_x[0], self.baseline_y), (self.span_x[1], self.baseline_y))
