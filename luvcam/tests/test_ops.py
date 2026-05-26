import pytest
from luvcam.ops import _string_to_hex, _get_luvcam_expose_data, create_op_plan_science_img, create_op_plan_calibration_img

expected_output_plan = '''
TBD
'''


def test_string_to_hex():
    decoded_string = _string_to_hex(s="luvcam expose 26d17a.raw")
    assert(decoded_string == "6C 75 76 63 61 6D 20 65 78 70 6F 73 65 20 32 36 64 31 37 61 2E 72 61 77")

def test_get_luvcam_expose_data_filename_format1():
    data = _get_luvcam_expose_data(img_filename='26d17a',img_exp=30000,img_x_offset=1808,img_y_offset=1119,img_xs=512,img_ys=512)
    assert(data == "6C 75 76 63 61 6D 20 65 78 70 6F 73 65 20 32 36 64 31 37 61 2E 72 61 77 20 33 30 30 30 30 20 30 20 31 38 30 38 20 31 31 31 39 20 35 31 32 20 35 31 32 00")

def test_get_luvcam_expose_data_filename_format2():
    data = _get_luvcam_expose_data(img_filename='26d17a.raw',img_exp=30000,img_x_offset=1808,img_y_offset=1119,img_xs=512,img_ys=512)
    assert(data == "6C 75 76 63 61 6D 20 65 78 70 6F 73 65 20 32 36 64 31 37 61 2E 72 61 77 20 33 30 30 30 30 20 30 20 31 38 30 38 20 31 31 31 39 20 35 31 32 20 35 31 32 00")

def test_create_plan():
    plan = create_op_plan_science_img(img_time_utc='2026-04-10 23:55:00',
                              target_ra=(3,47,24),target_dec=(24,7,0),target_name='Pleiades',
                              img_filename='26d10a',img_exp=3000)
    """TBD"""
    
def test_create_plan_cal():
    plan = create_op_plan_calibration_img(img_time_utc='2026-04-17 17:50:00',
                                          img_filename='26d17a',img_exp=30000)
    """TBD"""
    
