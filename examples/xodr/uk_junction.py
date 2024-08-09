"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright (c) 2022 The scenariogeneration Authors.


    Example of how to create a highway entry using CommonJunctionCreator

    Some features used:

    - create_road

    - add_successor/add_predecessor with and without the lane_offset option, and the direct_junction input

    - CommonJunctionCreator
"""

import os
from scenariogeneration import xodr, prettyprint, ScenarioGenerator
import numpy as np
import random
import math


class Scenario(ScenarioGenerator):
    def __init__(self):
        super().__init__()

    def road(self, **kwargs):
        # initalize the junction creator
        junction_id = 100
        junction_creator = xodr.DirectJunctionCreator(
            id=junction_id, name="my direct junction"
        )

        roads = []

        # Road 1
        rm_solid = xodr.RoadMark("solid")
        rm_broken = xodr.RoadMark("broken")

        road_1_geo = xodr.Line(100.0)
        road_1_pv = xodr.PlanView(x_start=0.0, y_start=0.0, h_start=0.0)
        road_1_pv.add_geometry(road_1_geo)

        road_1_left_lane_3 = xodr.Lane(a=15.0, lane_type="shoulder")
        road_1_left_lane_2 = xodr.Lane(a=3.0)
        road_1_left_lane_2.add_roadmark(rm_solid)
        road_1_left_lane_1 = xodr.Lane(a=3.0)
        road_1_left_lane_1.add_roadmark(rm_broken)
        road_1_right_lane_1 = xodr.Lane(a=3.0)
        road_1_right_lane_1.add_roadmark(rm_broken)
        road_1_right_lane_2 = xodr.Lane(a=3.0)
        road_1_right_lane_2.add_roadmark(rm_solid)
        road_1_right_lane_3 = xodr.Lane(a=16.5, lane_type="shoulder")
        road_1_right_lane_4 = xodr.Lane(a=60.0, lane_type="driving")
        road_1_center_lane = xodr.Lane()
        road_1_center_lane.add_roadmark(rm_solid)

        road_1_lanes = xodr.Lanes()
        road_1_lane_section = xodr.LaneSection(0.0, road_1_center_lane)
        road_1_lane_section.add_left_lane(road_1_left_lane_1)
        road_1_lane_section.add_left_lane(road_1_left_lane_2)
        road_1_lane_section.add_left_lane(road_1_left_lane_3)
        road_1_lane_section.add_right_lane(road_1_right_lane_1)
        road_1_lane_section.add_right_lane(road_1_right_lane_2)
        road_1_lane_section.add_right_lane(road_1_right_lane_3)
        road_1_lane_section.add_right_lane(road_1_right_lane_4)
        road_1_lanes.add_lanesection(road_1_lane_section)
        road1 = xodr.Road(road_id=1, planview=road_1_pv, lanes=road_1_lanes)

        # Road

        # create 3 roads, and add the successor/predecessor junction
        #road1 = xodr.create_road(xodr.Line(100), id=1, left_lanes=3, right_lanes=2)
        road2 = xodr.create_road(xodr.Line(100), id=2, left_lanes=1, right_lanes=1)
        road3 = xodr.create_road(xodr.Line(100), id=3, left_lanes=2, right_lanes=2)

        roads.append(road1)
        roads.append(road2)
        roads.append(road3)

        # create direct junction connection to all common lanes between the main roads

        junctions = []
        junction_creator = xodr.CommonJunctionCreator(id=100, name="my_junction")

        junction100 = junction_creator.add_incoming_road_cartesian_geometry(
            road1, x=0, y=0, heading=0, road_connection="successor"
        )

        junction101 = junction_creator.add_incoming_road_cartesian_geometry(
            road2, x=50, y=50, heading=3.1415 * 3 / 2, road_connection="predecessor"
        )

        junction102 = junction_creator.add_incoming_road_cartesian_geometry(
            road3, x=100, y=0, heading=-3.1415, road_connection="predecessor"
        )

        # OBJECTS
        # Add some random trees
        points = generate_points(10, 100, -15, -100, 6, 16, 10, 20)
        for x, y, height in points:
            roads[1].add_object(
                xodr.Object(name="tree", s=x, t=y, height=height, Type="tree")
            )

        for j in range(0, 200, 20):
            roads[0].add_object(
                xodr.Object(name="UK house 1", s=j, t=15, hdg=0, zOffset=-0.1, Type="residential", height="4.5", width="4.5", length="4.5")
            )
            roads[1].add_object(
                xodr.Object(name="UK house 1", s=j, t=15, hdg=0, zOffset=-0.1, Type="residential", height="4.5", width="4.5", length="4.5")
            )
            roads[2].add_object(
                xodr.Object(name="UK house 1", s=j, t=15, hdg=0, zOffset=-0.1, Type="residential", height="4.5", width="4.5", length="4.5")
            )

        for k in range(0, 200, 40):
            roads[0].add_object(
                xodr.Object(name="lamp post", s=k, t=7, hdg=0)
            )

        roads[0].add_object(
            xodr.Object(name="supermarket", s=100, t=-50, hdg=-1.57, height="4", width="4", length="4", Type="commercial")
        )

        # create the opendrive
        odr = xodr.OpenDrive("my_road")

        # add the roads
        junction_creator.add_connection(road_one_id=1, road_two_id=3)
        junction_creator.add_connection(
            road_one_id=1, road_two_id=2, lane_one_id=2, lane_two_id=1
        )
        junction_creator.add_connection(
            road_one_id=2, road_two_id=3, lane_one_id=-1, lane_two_id=2
        )

        junctions = junction_creator.get_connecting_roads()

        # Add stuff to junctions

        junctions[1].add_object(xodr.Object(name="UK house 1", s=40, t=15, hdg=0, zOffset=-0.1, Type="residential", height="4.5", width="4.5", length="4.5"))

        odr.add_road(road1)
        odr.add_road(road2)
        odr.add_road(road3)

        # add the junction creator
        odr.add_junction_creator(junction_creator)

        # adjust the roads and lanes
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
    #sce.generate(".")
    sce.generate(r"D:\wmg3xdsimulatorue5.3\Plugins\OpenDRIVE\Content\OpenX\GenerationTesting")

    # uncomment the following lines to display the scenario using esmini
    # from scenariogeneration import esmini
    # esmini(sce,os.path.join('esmini'))
