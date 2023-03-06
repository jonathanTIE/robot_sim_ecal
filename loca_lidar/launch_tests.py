import pytest
import numpy as np
import PatternFinder 
import FixedPoints as fp
import CloudPoints as cp
from  PointsDataStruct import PolarPts

######### Test amalgame discovery from cloud points ############

def test_one_amalgame():
    # Amalgame between 10° & 20°
    # Check if amalgame is detected if only the amalgame is detected by lidar and nothing else (except dummy points)
    pts_test = np.array([
        (0.01, 0),
        (0.01, 1),
        (0.01, 2),
        (0.01, 3),
        (0.01, 4),
        (0.01, 5),
        (0.01, 6),
        (0.01, 7),
        (0.01, 8),
        (0.01, 9),
        (1.0, 10), #expected size : 0.18
        (1.0, 11), #expected center : (1, 15)
        (1.0, 12),
        (1.0, 13),
        (1.0, 14),
        (1.0, 15),
        (1.0, 16),
        (1.0, 17),
        (1.0, 18),
        (1.0, 19),
        (1.0, 20),
        (0.01, 21),
        (0.01, 22),
        (0.01, 23),
        (0.01, 24),
        (0.01, 25),
        (0.01, 26),
        (0.01, 27),
    ], dtype=PolarPts)

    pts_filtered = np.array([
        (1.0, 10), #expected size : 0.18
        (1.0, 11), #expected center : (1, 15)
        (1.0, 12),
        (1.0, 13),
        (1.0, 14),
        (1.0, 15),
        (1.0, 16),
        (1.0, 17),
        (1.0, 18),
        (1.0, 19),
        (1.0, 20),
    ], dtype=PolarPts)
    basic_filtered = cp.basic_filter_pts(pts_test)
    assert np.array_equal(basic_filtered, pts_filtered)
    cp.amalgames_from_cloud(basic_filtered)

######### Test finding pattern from amalgames
# maximum error tolerance set for unit tests is 2mm for 2D lidar pose estimation 
pos_abs_tol = 0.002 #meters 
angle_abs_tol = 0.02 #degrees
finder = PatternFinder.PatternFinder(fp.known_distances(), 0.02)


def test_all_fixed_no_obstacle_1():
    # Robot origin is at x~0.5, y~1.5, theta ~32.06° left
    # no other obstacles, approximated lidar reading from geogebra
    lidar2table = finder.find_pattern(cp.get_distances(cp.amalgame_sample_1))

    # verify position
    lidar_pos = PatternFinder.Triangulate.lidar_pos_wrt_table(
        lidar2table, cp.amalgame_sample_1, fp.known_points())
    expected_lidar_pos = np.array([0.5, 1.5]).reshape(2, 1)
    assert np.allclose(lidar_pos, expected_lidar_pos, atol=pos_abs_tol)

    # verify angle
    lidar_angle = PatternFinder.Triangulate.lidar_angle_wrt_table(
        lidar_pos, lidar2table, cp.amalgame_sample_1, fp.known_points())
    expected_lidar_angle = 32.06
    assert np.isclose(lidar_angle, expected_lidar_angle, angle_abs_tol)

def test_partial_fixed_no_obstacle_1(): 
    #expected values :
    expected_lidar_pos = np.array([0.5, 1.5]).reshape(2, 1)
    expected_lidar_angle = 32.06

    #test amalgame_sample_1 with 4 points :
    first_four_amalgames = cp.amalgame_sample_1[:4]
    lidar2table = finder.find_pattern(cp.get_distances(first_four_amalgames))

    # verify position
    lidar_pos = PatternFinder.Triangulate.lidar_pos_wrt_table(
        lidar2table, first_four_amalgames, fp.known_points())
    assert np.allclose(lidar_pos, expected_lidar_pos, atol=pos_abs_tol)

    # verify angle
    lidar_angle = PatternFinder.Triangulate.lidar_angle_wrt_table(
        lidar_pos, lidar2table, first_four_amalgames, fp.known_points())
    assert np.isclose(lidar_angle, expected_lidar_angle, angle_abs_tol)

    #test amalgame_sample_1 with 3 points:
    first_three_amalgames = cp.amalgame_sample_1[:3]
    lidar2table = finder.find_pattern(cp.get_distances(first_three_amalgames))

    # verify position
    lidar_pos = PatternFinder.Triangulate.lidar_pos_wrt_table(
        lidar2table, first_three_amalgames, fp.known_points())
    assert np.allclose(lidar_pos, expected_lidar_pos, atol=pos_abs_tol)

    # verify angle
    lidar_angle = PatternFinder.Triangulate.lidar_angle_wrt_table(
        lidar_pos, lidar2table, first_three_amalgames, fp.known_points())
    assert np.isclose(lidar_angle, expected_lidar_angle, angle_abs_tol)

    #test amalgame_sample_1 with 2 points:
    first_two_amalgames = cp.amalgame_sample_1[:2]
    with pytest.raises(ValueError):
        lidar2table = finder.find_pattern(cp.get_distances(first_two_amalgames))

#TODO : check function lidar_angle_wrt_table with origin of robot aligned x or y axis to the beacon

#Test case : 2 perfect with geogebra (bottom right, top right pointing bottom left)
# take one of these and add false obstacles inside & outside 
# robot is outside 
#obstacles that make a valid positionning
#cloud points that are not valid


#def test_cloud_points():
    #assert all get_distances()
if __name__ == "__main__":
    pytest.main(["-x", ".\\loca_lidar\\launch_tests.py"])

