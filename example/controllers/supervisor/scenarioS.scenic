from scenic.simulators.webots.model import WebotsObject

import numpy as np

class Lead(WebotsObject):
    webotsName: "LEAD"

class Follower(WebotsObject):
    webotsName: "FOLLOWER"

class Obstacle(WebotsObject):
    webotsName: "OBSTACLE"
    color: Options([[0.0, 0.0, 0.0],
                    [0.5, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 0.5, 0.0],
                    [0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.5],
                    [0.0, 0.0, 1.0],
                    [0.5, 0.5, 0.5],
                    [1.0, 1.0, 1.0]])

class OilBarrel1(WebotsObject):
    webotsName: "OIL_BARREL_1"

class OilBarrel2(WebotsObject):
    webotsName: "OIL_BARREL_2"

class OilBarrel3(WebotsObject):
    webotsName: "OIL_BARREL_3"

class Scenario(WebotsObject):
    webotsName: "SCENARIO"
    ind: "S"

s = Scenario

x_space = list(np.linspace(35.5, 38.5, num=50)) + list(np.linspace(51.5, 54.5, num=50))
y_space = list(np.linspace(-25.5, -10.5, num=100))
obstacle = Obstacle at Uniform(*x_space) @ Uniform(*y_space)

lead = Lead at Range(-56.5, -52.5) @ Range(-106, -104), facing Range(-5.0, 5.0) deg
ego = Follower at Range(-66.5, -62.5) @ Range(-106, -104), facing Range(-5.0, 5.0) deg
