import pytest
import numpy as np
import PatternFinder 
import FixedPoints as FPts
import CloudPoints as CPts

# maximum error tolerance set for unit tests is 2mm for 2D lidar pose estimation 
pos_abs_tol = 0.002 #meters 
angle_abs_tol = 0.02 #degrees
finder = PatternFinder.PatternFinder(FPts.known_distances(), 0.02)



def test_all_fixed_no_obstacle_1():
    # Robot origin is at x~0.5, y~1.5, theta ~32.06° left
    # no other obstacles, approximated lidar reading from geogebra
    lidar2table = finder.find_pattern(CPts.get_distances(CPts.amalgame_sample_1))

    # verify position
    lidar_pos = PatternFinder.Triangulate.lidar_pos_wrt_table(
        lidar2table, CPts.amalgame_sample_1, FPts.known_points())
    expected_lidar_pos = np.array([0.5, 1.5]).reshape(2, 1)
    assert np.allclose(lidar_pos, expected_lidar_pos, atol=pos_abs_tol)

    # verify angle
    lidar_angle = PatternFinder.Triangulate.lidar_angle_wrt_table(
        lidar_pos, lidar2table, CPts.amalgame_sample_1, FPts.known_points())
    expected_lidar_angle = 32.06
    assert np.isclose(lidar_angle, expected_lidar_angle, angle_abs_tol)

def test_partial_fixed_no_obstacle_1(): 
    #expected values :
    expected_lidar_pos = np.array([0.5, 1.5]).reshape(2, 1)
    expected_lidar_angle = 32.06

    #test amalgame_sample_1 with 4 points :
    first_four_amalgames = CPts.amalgame_sample_1[:4]
    lidar2table = finder.find_pattern(CPts.get_distances(first_four_amalgames))

    # verify position
    lidar_pos = PatternFinder.Triangulate.lidar_pos_wrt_table(
        lidar2table, first_four_amalgames, FPts.known_points())
    assert np.allclose(lidar_pos, expected_lidar_pos, atol=pos_abs_tol)

    # verify angle
    lidar_angle = PatternFinder.Triangulate.lidar_angle_wrt_table(
        lidar_pos, lidar2table, first_four_amalgames, FPts.known_points())
    assert np.isclose(lidar_angle, expected_lidar_angle, angle_abs_tol)

    #test amalgame_sample_1 with 3 points:
    first_three_amalgames = CPts.amalgame_sample_1[:3]
    lidar2table = finder.find_pattern(CPts.get_distances(first_three_amalgames))

    # verify position
    lidar_pos = PatternFinder.Triangulate.lidar_pos_wrt_table(
        lidar2table, first_three_amalgames, FPts.known_points())
    assert np.allclose(lidar_pos, expected_lidar_pos, atol=pos_abs_tol)

    # verify angle
    lidar_angle = PatternFinder.Triangulate.lidar_angle_wrt_table(
        lidar_pos, lidar2table, first_three_amalgames, FPts.known_points())
    assert np.isclose(lidar_angle, expected_lidar_angle, angle_abs_tol)

    #test amalgame_sample_1 with 2 points:
    first_two_amalgames = CPts.amalgame_sample_1[:2]
    with pytest.raises(ValueError):
        lidar2table = finder.find_pattern(CPts.get_distances(first_two_amalgames))

#TODO : check function lidar_angle_wrt_table with origin of robot aligned x or y axis to the beacon


#def test_cloud_points():
    #assert all get_distances()
if __name__ == "__main__":
    pytest.main(["-x", ".\\loca_lidar\\launch_tests.py"])

