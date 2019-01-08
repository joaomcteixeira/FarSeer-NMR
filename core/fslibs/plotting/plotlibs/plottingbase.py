import core.fslibs.Logger as Logger
from core.fslibs.WetHandler import WetHandler

logger = Logger.FarseerLogger(__name__).setup_log()

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
        "hex":[self._RGB_to_hex(RGB) for RGB in gradient],
        "r":[RGB[0] for RGB in gradient],
        "g":[RGB[1] for RGB in gradient],
        "b":[RGB[2] for RGB in gradient]
        }
    
    return d

def linear_gradient(finish_hex="#FFFFFF", n=10):
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
    s = _hex_to_RGB(start_hex)
    f = _hex_to_RGB(finish_hex)
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
    
    return _color_dict(RGB_list)


def draw_figure(num_subplots, rows_page, cols_page, fig_height, fig_width):
    """
    Draws the figure architecture.
    
    Defines the size of the figure and subplots based
    on the data to plot.
    
    Parameters:
    
        - num_subplots:
        - cols_page:
        - fig_height:
        - fig_width:
    
    Returns:
        - matplotlib Figure, Axes
    """
    
    numrows = _calc_num_rows(
        num_subplots,
        cols_page,
        )
    
    real_fig_height = _calc_real_fig_height(
        rows_page, 
        numrows,
        fig_height,
        )
    
    # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
    figure, axs = plt.subplots(
        nrows=numrows,
        ncols=cols_page,
        figsize=(fig_width, real_fig_height),
        )
    
    self.axs = self.axs.ravel()
    
    plt.tight_layout(
        rect=[0.01,0.01,0.995,0.995]
        )
    
    logger.debug("Figure drawn: OKAY")
    
    return figure, axs


def adjust_subplots(figure, hspace, wspace):
    
    figure.subplots_adjust(
        hspace=hspace,
        wspace=wspace,
        )
    
    return

def clean_subplots(axs, num_subplots):
    """ Removes unsed subplots."""
    
    len_axs = len(axs)
    
    logger.debug(f"Length Axes: {len_axs}")
    
    for i in range(num_subplots, len_axs):
        axs[i].remove()
    
    return


def save_figure(
        figure,
        file_path,
        header="",
        header_fs=5,
        dpi=300,
        ):
    """Saves figure to path"""
    
    figure.text(
        0.01,
        0.01,
        header,
        fontsize=header_fs,
        )
    
    figure.savefig(file_path, dpi=dpi)
    
    logger.info(f"**Saved plot figure** {file_path}")
    
    return



