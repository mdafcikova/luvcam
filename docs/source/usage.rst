.. _usage:

**************
Using LUVCam
**************

To find the set of visible stars in the field of LUVCam, one will first need to retrieve the TLE of LUVCam's 
current position. LUVCam's TLE is provided by Celestrak: https://celestrak.org/NORAD/elements/gp.php?CATNR=60237.
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

For other file formats, a bit more information is needed.  Below, we cover the
basics of :ref:`inspecting files <using_baseband_inspecting>`, :ref:`reading
<using_baseband_reading>` from and :ref:`writing <using_baseband_writing>`
to files, :ref:`converting <using_baseband_converting>` from one format
to another, and :ref:`diagnosing problems <using_baseband_problems>`.
We assume that Baseband as well as numpy_ and the
`astropy.units <https://docs.astropy.org/en/stable/units>`_ module
have been imported::

    >>> import baseband
    >>> import numpy as np
    >>> import astropy.units as u

.. _using_baseband_inspecting:

Inspecting Files
================

Baseband allows you to quickly determine basic properties of a file, including
what format it is, using the `baseband.file_info` function. For instance, it
shows that the sample VDIF file that comes with Baseband is very short (sample
files can all be found in the `baseband.data` module)::

    >>> import baseband.data
    >>> baseband.file_info(baseband.data.SAMPLE_VDIF)
    VDIFStream information:
    start_time = 2014-06-16T05:56:07.000000000
    stop_time = 2014-06-16T05:56:07.001250000
    sample_rate = 32.0 MHz
    shape = (40000, 8)
    format = vdif
    bps = 2
    complex_data = False
    verify = fix
    readable = True
    <BLANKLINE>
    checks:  decodable: True
             continuous: no obvious gaps
    <BLANKLINE>
    VDIFFile information:
    edv = 3
    number_of_frames = 16
    thread_ids = [0, 1, 2, 3, 4, 5, 6, 7]
    number_of_framesets = 2
    frame_rate = 1600.0 Hz
    samples_per_frame = 20000
    sample_shape = (8, 1)

The same function will also tell you when more information is needed. For
instance, for Mark 5B files one needs the number of channels used, as well as
(roughly) when the data were taken::