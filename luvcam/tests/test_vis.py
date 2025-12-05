import pytest
from luvcam.vis import find_visible_stars, ra_dec_to_quaternion

def test_sun70():
    TLE = (
        "GRBBeta",
        "1 60237U 24128C   25308.26896397  .00005441  00000+0  39123-3 0  9997",
        "2 60237  61.9902 284.0803 0057066  88.4364 272.3263 15.04176770 72405,"
    )
    obs = "2025/11/05 12:49:25"  # UTC
    visible = find_visible_stars(TLE, obs, sun_avoid_deg=70, limb_avoid_deg=5) # One test for each argument to the public function
    assert(visible[0]['name'] == 'Moon')
    assert(visible[1]['name'] == 'Vega')


def test_sun20():
    TLE = (
        "GRBBeta",
        "1 60237U 24128C   25308.26896397  .00005441  00000+0  39123-3 0  9997",
        "2 60237  61.9902 284.0803 0057066  88.4364 272.3263 15.04176770 72405,"
    )
    obs = "2025/11/05 12:49:25"  # UTC
    visible = find_visible_stars(TLE, obs, sun_avoid_deg=20, limb_avoid_deg=5) # One test for each argument to the public function
    assert(visible[0]['name'] == 'Moon')
    assert(visible[1]['name'] == 'Arcturus')


def test_quat():
    x, y, z, w = ra_dec_to_quaternion(40.31, 19.43)
    assert(x == -0.35216305275061904)
    assert(y == 0.6131730459481766)
    assert(z == 0.695400773377592)
    assert(w == -0.1281318242508355)
