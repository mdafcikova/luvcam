.. _usage:

**************
Using LUVCam
**************

To find the set of visible stars in the field of LUVCam, one will first need to retrieve the TLE of LUVCam's 
current position. LUVCam's TLE is provided by Celestrak: https://celestrak.org/NORAD/elements/gp.php?CATNR=60237. 
Each line of the TLE can be entered as the element of a list to be passed into find_visible_stars():
::

    >>> import luvcam
    >>> from luvcam.vis import find_visible_stars
    >>> TLE = (
        "GRBBeta",
        "1 60237U 24128C   25308.26896397  .00005441  00000+0  39123-3 0  9997",
        "2 60237  61.9902 284.0803 0057066  88.4364 272.3263 15.04176770 72405,"
        )
    >>> obs = "2025/11/05 12:49:25"  # UTC
    >>> visible = find_visible_stars(TLE, obs, sun_avoid_deg=70, limb_avoid_deg=5)
    >>> for star in visible:
    >>>     print(star)
    {'name': 'Moon', 'magnitude': -12.78, 'sun_sep_deg': 176.36669122952148, 'limb_clearance_deg': -19, 'RA': 40.3107, 'Dec': 19.4385}
    {'name': 'Vega', 'magnitude': 0.03, 'sun_sep_deg': 77.29, 'limb_clearance_deg': 61.65, 'RA': 279.4494, 'Dec': 38.8107}
    {'name': 'Altair', 'magnitude': 0.76, 'sun_sep_deg': 80.23, 'limb_clearance_deg': 77.6, 'RA': 298.0095, 'Dec': 8.9387}
    {'name': 'Fomalhaut', 'magnitude': 1.17, 'sun_sep_deg': 109.4, 'limb_clearance_deg': 20.16, 'RA': 344.7732, 'Dec': -29.4861}
    ...
    {'name': 'Sheliak', 'magnitude': 3.52, 'sun_sep_deg': 76.79, 'limb_clearance_deg': 67.44, 'RA': 282.755, 'Dec': 33.3956}
    {'name': 'Thuban', 'magnitude': 3.67, 'sun_sep_deg': 80.44, 'limb_clearance_deg': 16.72, 'RA': 211.2652, 'Dec': 64.2507}
    {'name': 'Alshain', 'magnitude': 3.71, 'sun_sep_deg': 80.56, 'limb_clearance_deg': 75.87, 'RA': 299.1444, 'Dec': 6.4732}
    {'name': 'Alcor', 'magnitude': 3.99, 'sun_sep_deg': 72.59, 'limb_clearance_deg': 12.46, 'RA': 201.5594, 'Dec': 54.8517}


Another small function is provided for converting targets to quaternion coordinates, ra_dec_to_quaternion():
::
    >>> import luvcam
    >>> from luvcam.vis import ra_dec_to_quaternion
    >>> ra_deg = 40.31
    >>> dec_deg = 19.43
    >>> x, y, z, w = ra_dec_to_quaternion(ra_deg, dec_deg)
    >>> print(x)
    >>> print(y)
    >>> print(z)
    >>> print(w)
    -0.35216305275061904
    0.6131730459481766
    0.695400773377592
    -0.1281318242508355