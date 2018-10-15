"""
Copyright © 2017-2018 Farseer-NMR

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""

from core.fslibs.WetHandler import WetHandler
import core.fslibs.Logger as Logger

logger = Logger.FarseerLogger(__name__).setup_log()
logger.debug("Initiated plotting_base module")

def log():
    logger.info("in plotting base")

def hex_to_RGB(hexx):
    """
    This function was taken from:
    Copyright 2017 Ben Southgate
    https://github.com/bsouthga/blog
    
    The MIT License (MIT)
    
    Permission is hereby granted, free of charge,
    to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to
    whom the Software is furnished to do so, subject to the
    following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    "#FFFFFF" -> [255,255,255]
    """
    # if clause not part of the original function, added for the Farseer-NMR Project.
    if not(hexx.startswith("#") and len(hexx) == 7):
        msg = "The input colour is not in HEX format."
        wet = WetHandler(msg_title="ERROR", msg=msg, wet_num=27)
        plotting_base_logger.info(wet.wet)
        wet.abort()
    # Pass 16 to the integer function for change of base
    return [int(hexx[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
    """
    This function was taken verbatim from:
    Copyright 2017 Ben Southgate
    https://github.com/bsouthga/blog
    
    The MIT License (MIT)
    
    Permission is hereby granted, free of charge,
    to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to
    whom the Software is furnished to do so, subject to the
    following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
    
    [255,255,255] -> "#FFFFFF"
    """
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    hexx = "#"+"".join(
        ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB]
        )
    return hexx

def color_dict(gradient):
    """
    This function was taken verbatim from:
    Copyright 2017 Ben Southgate
    https://github.com/bsouthga/blog
    
    The MIT License (MIT)
    
    Permission is hereby granted, free of charge,
    to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to
    whom the Software is furnished to do so, subject to the
    following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
    
    Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on.
    """
    d = {
        "hex":[RGB_to_hex(RGB) for RGB in gradient],
        "r":[RGB[0] for RGB in gradient],
        "g":[RGB[1] for RGB in gradient],
        "b":[RGB[2] for RGB in gradient]
        }
    
    return d


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    """
    This function was taken verbatim from:
    Copyright 2017 Ben Southgate
    https://github.com/bsouthga/blog
    
    The MIT License (MIT)
    
    Permission is hereby granted, free of charge,
    to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to
    whom the Software is furnished to do so, subject to the
    following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
    
    returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF")
    """
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    
    return color_dict(RGB_list)

def clean_subplots(axs, num_subplots):
    """
    Removes unsed subplots.
    
    Parameters:
        - axs (matplotlig figure axes)
        - num_subplots (int): number of used subplots
        - logger (Logger object)
    """
    len_axs = len(axs)
    
    for i in range(num_subplots, len_axs):
        axs[i].remove()
    
    return

def adjust_subplots(figure, hspace, wspace):
    """
    Adjusts figure subplots spacing.
    
    Parameters:
        - figure (matplotlib figure)
        - hspace (float): the height spacing value
        - wspace (float): the width spacing value
    """
    figure.subplots_adjust(
        hspace=hspace,
        wspace=wspace
        )
    
    return

def save_figure(
        figure,
        path='my_plot.pdf',
        header='No header provided',
        fontsize=5,
        dpi=300):
    """
    Saves figure to path.
    
    Parameters:
        - figure (matplotlib figure)
        - path (srt, opt): path to the figure file with extention
        - header (str, opt): informative header
        - fontsize (int, opt): header font size
        - dpi (int, opt): figure resolution
    """
    
    figure.text(
        0.01,
        0.01,
        header,
        fontsize=fontsize
        )
    
    self.figure.savefig(
        path,
        dpi=dpi
        )
    
    return
