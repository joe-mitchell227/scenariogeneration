"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright (c) 2022 The scenariogeneration Authors.

    Example of how to create a junction but adding signals to the junction


"""

# Same approach to creating a junction as "full_junction.py" but with signals for each incoming road.
import numpy as np
import random
import math
import os
from scenariogeneration import xodr, prettyprint, ScenarioGenerator

class Scenario(ScenarioGenerator):
    def __init__(self):
        super().__init__()

    def road(self, **kwargs):
        roads = []
        incoming_roads = 4
        nlanes = 1
        # setup junction creator
        junction_creator = xodr.CommonJunctionCreator(100, "my junction")

        # create roads and connections
        for i in range(incoming_roads):
            roads.append(
                xodr.create_road(
                    [xodr.Line(600)],
                    i,
                    center_road_mark=xodr.STD_ROADMARK_BROKEN,
                    left_lanes=nlanes,
                    right_lanes=nlanes,
                    lane_width=4.5
                )
            )
            # roads[-1].add_signal(
            #     xodr.Signal(name="test", s=100, t=-4, country="USA", Type="R1", subtype="1")
            # )

            # Add some random trees
            points = generate_points(10, 600, 15, 600, 6, 16, 10, 250)
            for x, y, height in points:
                roads[-1].add_object(
                        xodr.Object(name="tree", s=x, t=y, height=height, Type="tree")
                    )

            # Add some lamp posts
            for j in range(10, 600, 50):
                roads[-1].add_object(
                    xodr.Object(name="lamp post", s=j, t=6.5, hdg=0)
                )
                roads[-1].add_object(
                    xodr.Object(name="lamp post", s=j, t=-6.5, hdg=3.14)
                )

            # add road to junciton
            junction_creator.add_incoming_road_circular_geometry(
                roads[i], 20, i * 2 * np.pi / incoming_roads, "successor"
            )

            # add connection to all previous roads
            for j in range(i):
                junction_creator.add_connection(j, i)

        odr = xodr.OpenDrive("myroad")

        for r in roads:
            odr.add_road(r)
        odr.add_junction_creator(junction_creator)

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
            x = random.uniform(s_min, s_max)
            y = random.uniform(t_min, t_max)
            h = random.uniform(h_min, h_max)
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
