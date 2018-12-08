"""
Copyright © 2017-2018 Farseer-NMR Project

Find us at:

- J. BioMol NMR Publication:
    https://link.springer.com/article/10.1007/s10858-018-0182-5

- GitHub: https://github.com/Farseer-NMR

- Mail list: https://groups.google.com/forum/#!forum/farseer-nmr
    email: farseer-nmr@googlegroups.com

- Research Gate: https://goo.gl/z8dPJU

- Twitter: https://twitter.com/farseer_nmr

This file is part of the Farseer-NMR Project.

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

from math import ceil
from matplotlib import pyplot as plt
import numpy as np
import json

import core.fslibs.Logger as Logger

class PlottingBase:
    """
    Plotting base class with methods common to all plots.
    
    Not functional on its own.
    """
    
    _default_config = {
        "cols_page": 2,
        "rows_page": 2,
        "hspace": 0.5,
        "wspace": 0.5,
        
        "figure_header":"No header provided",
        "header_fontsize":5,
        
        "figure_path":"bar_extended_horizontal.pdf",
        "figure_dpi":300,
        "fig_height": 11.69,
        "fig_width": 8.69
        }
    
    def __init__(self, config={}, **kwargs):
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("PlottingBase initiated")
        
        self.kwargs = kwargs
        self.figure = None
        self.axs = None
        self._config = PlottingBase._default_config.copy()
        self._config.update(config)
        self.logger.debug("Config Updated: {}".format(self._config))
    
    def _check_exists(self, obj):
        """
        Return obj if obj exists, False otherwise.
        name describes the object.
        Writes to logger.
        """
        b = obj is not None
        self.logger.debug("{} exists: {}".format(type(obj), b))
        return b
    
    def _check_instance(self, instance_, obj):
        """
        Check if obj is instance of instance_.
        Returns True or False accordingly.
        """
        b = isinstance(obj, instance_)
        self.logger.debug("... is {} instance of {}: {}".format(type(obj), instance_, b))
        return b
    
    def _check_equality(self, eq1, eq2):
        b = eq1 == eq2
        self.logger.debug("... {} and {} are equal: {}".format(eq1, eq2, b))
        return b
    
    def _check_converter(self, func, var, name):
        try:
            tmp = func(var)
        except ValueError as e:
            msg = "{} can be converted to {}".format(name, func)
            wet = WetHandler(msg=msg, msg_title="ERROR", wet_num=0)
            self.logger.info(wet.wet)
            wet.abort()
        return tmp
    
    def _hex_to_RGB(self, hexx):
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
            self._abort(fsw(msg_title="ERROR", msg=msg, wet_num=27))
        # Pass 16 to the integer function for change of base
        return [int(hexx[i:i+2], 16) for i in range(1,6,2)]

    def _RGB_to_hex(self, RGB):
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
    
    def _color_dict(self, gradient):
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
    
    def _linear_gradient(self, start_hex, finish_hex="#FFFFFF", n=10):
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
        s = self._hex_to_RGB(start_hex)
        f = self._hex_to_RGB(finish_hex)
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
        
        return self._color_dict(RGB_list)
    
    def _calc_real_fig_height(self, rows_page, numrows, fig_hgt):
        """
        Returns real figure height based on the height per page and
        total number of subplots rows.
        
        Paramers:
            - rows_page (int): wanted number of rows per page
            - numrows (int): total number of subplot rows based on
                number of columns
            - fig_hgt (float): height of page
        
        Returns:
            - real_fig_height (float, inches): final figure height
        """

        rows_page = self._check_converter(int, rows_page, "rows_page")
        numrows = self._check_converter(int, numrows, "numrows")
        fig_hgt = self._check_converter(float, fig_hgt, "fig_hgt")
        
        return (fig_hgt/rows_page)*numrows
    
    def _calc_num_rows(self, num_subplots, cols_page):
        """
        Returns the total number of subplot rows calculated based on
        the number of subplots and the columns per page.
        """
        num_subplots = self._check_converter(int, num_subplots, "num_subplots")
        cols_page = self._check_converter(int, cols_page, "cols_page")
        
        return ceil(num_subplots/cols_page) + 1 
    
    def set_config(self, config={}):
        """
        Updates config dictionary
        
        See also .get_config() and .print_config()
        
        Parameters:
            - config (dict)
        """
        
        self.logger.debug("updating config to: {}".\
            format(json.dumps(config, indent=4, sort_keys=True))
            )
        
        self._config.update(config)
        self.logger.debug("updated config: {}".
            format(json.dumps(self._config, indent=4, sort_keys=True))
                )
        
        return
    
    def get_config(self):
        """
        Returns the configuration dictionary
        """
        return self._config
    
    def print_config(self):
        """
        Prints a formatted version of the configuration file.
        """
        print(json.dumps(self._config, indent=4, sort_keys=True))
    
        return
    
    def draw_figure(self):
        """
        Draws the figure architecture.
        
        Defines the size of the figure and subplots based
        on the data to plot.
        
        Returns:
            - None.
        
        Stores :
            - self.figure: Figure object.
            - self.axs: axes of the figure (in case matplotlib is used)
        """
        
        numrows = self._calc_num_rows(
            self.num_subplots,
            self._config["cols_page"]
            )
        
        real_fig_height = self._calc_real_fig_height(
            self._config["rows_page"], 
            numrows,
            self._config["fig_height"]
            )
        
        # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        self.figure, self.axs = plt.subplots(
            nrows=numrows,
            ncols=self._config["cols_page"],
            figsize=(self._config["fig_width"], real_fig_height)
            )        
        self.axs = self.axs.ravel()
        
        plt.tight_layout(
            rect=[0.01,0.01,0.995,0.995]
            )
        
        self.logger.debug("Figure drawn: OKAY")
        
        return
    
    def clean_subplots(self):
        """ Removes unsed subplots."""
        if not self.figure:
            self.logger.info("Figure not yet created")
            return None
        
        len_axs = len(self.axs)
        self.logger.debug("Length Axes: {}".format(len_axs))
        for i in range(self.num_subplots, len_axs):
            self.axs[i].remove()
    
    def adjust_subplots(self):
        if not self.figure:
            self.logger.info("Figure not yet created")
            return None
        
        self.figure.subplots_adjust(
            hspace=self._config["hspace"],
            wspace=self._config["wspace"]
            )
    
    def save_figure(self, path=''):
        """Saves figure to path"""
        if not self.figure:
            self.logger.info("Figure not yet created")
            return None
        
        path = path or self._config["figure_path"]
        
        self.figure.text(
            0.01,
            0.01,
            self._config["figure_header"],
            fontsize=self._config["header_fontsize"]
            )
        
        self.figure.savefig(
            path,
            dpi=self._config["figure_dpi"]
            )
        
        self.logger.info("**Saved plot figure** {}".format(path))
        
        return
    
    
if __name__ == "__main__":
    
    print(__name__)
