from scenic.simulators.webots.model import WebotsObject

import numpy as np

class Lead(WebotsObject):
    webotsName: "LEAD"

class Follower(WebotsObject):
    webotsName: "FOLLOWER"

class Obstacle(WebotsObject):
    webotsName: "OBSTACLE"

class OilBarrel1(WebotsObject):
    webotsName: "OIL_BARREL_1"

class OilBarrel2(WebotsObject):
    webotsName: "OIL_BARREL_2"

class OilBarrel3(WebotsObject):
    webotsName: "OIL_BARREL_3"

# scenario Subscenario1():
#     setup:
#         print("Subscenario1")
#     compose:
#         while True:
#             wait

# scenario Subscenario2():
#     setup:
#         print("Subscenario2")
#     compose:
#         while True:
#             wait

# scenario Subscenario3():
#     setup:
#         print("Subscenario3")
#     compose:
#         while True:
#             wait

# scenario Main():
#     setup:
#         x_space = list(np.linspace(-4.5, 25.5, num=100))
#         y_space = list(np.linspace(-54.5, -51.5, num=50)) + list(np.linspace(-38.5, -35.5, num=50))
#         obstacle = Obstacle at Uniform(*x_space) @ Uniform(*y_space)
#         oil_barrel_1 = OilBarrel1 at Range(-30.0, -10.0) @ Range(-115.0, -95.0)
#         oil_barrel_2 = OilBarrel2 at Range(-10.0, 10.0) @ Range(-115.0, -95.0)
#         oil_barrel_3 = OilBarrel3 at Range(10.0, 30.0) @ Range(-115.0, -95.0)
#         lead = Lead at -54.5 @ -105, facing 0 deg, with controller 'lead'
#         ego = Follower at -64.5 @ -105, facing 0 deg, with controller 'follower'
#     compose:
#         do Subscenario1() until ego.y > -64.5
#         do Subscenario2() until ego.x < 25.5
#         do Subscenario3() until ego.y > -4.5


x_space = list(np.linspace(10.5, 25.5, num=100))
y_space = list(np.linspace(-54.5, -51.5, num=50)) + list(np.linspace(-38.5, -35.5, num=50))
obstacle = Obstacle at Uniform(*x_space) @ Uniform(*y_space)
oil_barrel_1 = OilBarrel1 at Range(-30.0, -10.0) @ Range(-115.0, -95.0)
oil_barrel_2 = OilBarrel2 at Range(-10.0, 10.0) @ Range(-115.0, -95.0)
oil_barrel_3 = OilBarrel3 at Range(10.0, 30.0) @ Range(-115.0, -95.0)
lead = Lead at -54.5 @ -105, facing 0 deg
ego = Follower at -64.5 @ -105, facing 0 deg

# terminate when (distance from lead to ego) > 11 or (angle from lead to ego) > 100 deg

# terminate when (angle from lead to ego) > 100 deg


