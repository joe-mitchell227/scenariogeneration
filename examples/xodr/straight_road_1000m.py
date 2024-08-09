"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright (c) 2022 The scenariogeneration Authors.

    Fundamental example how to build up a road from scratch, but also with objects.

    This example should be seen as a developer example how roads are built up from the very basic classes in OpenDRIVE
    create_road will take care of this and much more, so a user is recommended to use that generator instead.

    Some features used:

    - Object

    - create_road

    - (Object).repeat
"""

import numpy as np
import random
import math
import os
from scenariogeneration import xodr, prettyprint, ScenarioGenerator

class Scenario(ScenarioGenerator):
    def __init__(self):
        super().__init__()

    def road(self, **kwargs):
        # create a road
        road = xodr.create_road([xodr.Line(1000)], 0, 1, 1, lane_width=4.5)

        # Add some random trees
        points = generate_points(10, 1000, 17, 200, 6, 16, 10, 250)
        for x, y, height in points:
            road.add_object(
                xodr.Object(name="tree", s=x, t=y, height=height, Type="tree")
            )
            road.add_object(
                xodr.Object(name="tree", s=x, t=-y, height=height, Type="tree")
            )

        # Add some lamp posts
        for j in range(10, 1000, 50):
            road.add_object(
                xodr.Object(name="lamp post", s=j, t=6.5, hdg=0)
            )
            road.add_object(
                xodr.Object(name="lamp post", s=j, t=-6.5, hdg=3.14)
            )

        ## Create the OpenDrive class (Master class)
        odr = xodr.OpenDrive("straight_road_1000m")

        ## Finally add roads to Opendrive
        odr.add_road(road)

        # Adjust initial positions of the roads looking at succ-pred logic
        odr.adjust_roads_and_lanes()

        return odr

def is_valid_point(x, y, points, min_dist):
    """
    Check if a point (x, y) is at least `min_dist` away from all points in `points`.
    """
    for px, py, ph in points:
        if math.sqrt((x - px) ** 2 + (y - py) ** 2) < min_dist:
            return False
    return True


def generate_points(s_min, s_max, t_min, t_max, h_min, h_max, min_dist, num_objects):

    points = []

    for _ in range(num_objects):
        attempts = 0
        while attempts < 1000:  # Limit the number of attempts to avoid infinite loops
            x = round(random.uniform(s_min, s_max))
            y = round(random.uniform(t_min, t_max))
            h = round(random.uniform(h_min, h_max))
            if is_valid_point(x, y, points, min_dist):
                points.append((x, y, h))
                break
            attempts += 1
        else:
            raise ValueError("Unable to place all points with the required spacing.")

    return points

if __name__ == "__main__":
    sce = Scenario()
    # Print the resulting xml
    prettyprint(sce.road().get_element())

    # write the OpenDRIVE file as xosc using current script name
    sce.generate(".")

    # uncomment the following lines to display the scenario using esmini
    # from scenariogeneration import esmini
    # esmini(sce,os.path.join('esmini'))
