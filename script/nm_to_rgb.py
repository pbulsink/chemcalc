#!/usr/bin/env python
from __future__ import division

def wavelength_to_rgb(wavelength):
    """
    Convert wavelength in nm (380-780) to a RGB value for visualization.
    Returns a list [red, green, blue]
    Based on http://www.physics.sfasu.edu/astro/color/spectra.html
    """

    red = 0.0
    green = 0.0
    blue = 0.0
    intensity = 1
    
    if wavelength < 380:
        pass
    elif wavelength < 440:
        red = -(wavelength-440)/(440-380)
        green = 0
        blue = 1
    elif wavelength < 490:
        red = 0
        green = (wavelength - 440)/(490-440)
        blue = 1
    elif wavelength < 510:
        red = 0
        green = 1
        blue = -(wavelength - 510)/(510-490)
    elif wavelength < 580:
        red = (wavelength-510)/(580-510)
        green = 1
        blue = 0
    elif wavelength < 645:
        red = 1
        green = -(wavelength-645)/(645-580)
        blue = 0
    elif wavelength < 780:
        red = 1
        green = 0
        blue = 0
    else:
        pass

    if wavelength > 380 and wavelength < 420:
        intensity = 0.3 + 0.7*(wavelength - 380)/(420-380)
    elif wavelength > 700 and wavelength <= 780:
        intensity = 0.3 + 0.7*(780 - wavelength)/(780-700)
    
    red = int(red * 255 * intensity)
    green = int(green * 255 * intensity)
    blue = int(blue * 255 * intensity)
    return [red, green, blue]
