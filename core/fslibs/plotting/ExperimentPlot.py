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
import collections
import numpy as np
from matplotlib import pyplot as plt

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.WetHandler import WetHandler as fsw

class ExperimentPlot(PlottingBase):
    """
    Defines a class for plots where each subplot represents each experimental
    datapoint, where X axes are the Residue numbers (labels)
    and Y axes the NMR parameter/observable to be represented.
    
    Not functional on its own.
    
    OPTIONAL PARAMETERS:
    
        Optional parameters can be used to improve plots functionalities.
        
        - subtitles (iterable type of strings): titles of each subplot,
            length must be equal to values.shape[0].
        
        - letter_code (sequence type): 1-letter code of the protein sequence,
            should have length equal to <labels>.
        
        - peak_status (np.array shape (y,x), dtype=str):
            Peak status information according to core.utils.peak_status
            dictionary.
        
        - details (np.array shape (y,x), dtype=str): Details information.
        
        - theo_pre (np.array shape (y,x), dtype=str):
            information of theoretical PRE data.
        
        - tag_position (np.array shape (y,x), dtype=str):
            empty strings were tag not present, and "*" denotes the presence
            of the paramagnetic tag.
        
        - threshold (float): the Y value of the threshold line.
    
    """
    
    _default_config = {
        "plot_theoretical_pre":False,
        "theo_pre_color": "red",
        "theo_pre_lw": 1.0,
        "tag_id":"*",
        
        "tag_cartoon_color": "black",
        "tag_cartoon_ls": "-",
        "tag_cartoon_lw": 1.0
        }
    
    def __init__(
            self,
            config={},
            details=None,
            letter_code=None,
            peak_status=None,
            subtitles=None,
            tag_position=None,
            theo_pre=None,
            threshold=None,
            **kwargs
            ):
        
        # initializes logger
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ExperimentPlot initialized")
        # sets config
        self._config = ExperimentPlot._default_config.copy()
        self._config.update(config)
        #self.logger.debug("Config updated: {}".format(self._config))
        
        # check optional params
        self.letter_code = self._check_letter_code(letter_code)
        self.peak_status = self._check_parameter(peak_status, "peak_status")
        self.details = self._check_parameter(details, "details")
        self.theo_pre = self._check_parameter(theo_pre, "theo_pre")
        self.tag_position = self._check_parameter(tag_position, "tag position")
        self.logger.debug("All parameters **seem** OKAY")
        
        # creates subtitles
        self.subtitles = \
            subtitles or [str(i) for i in range(self.values.shape[0])]
        self.logger.debug("Set subtitles to: {}".format(self.subtitles))
        
        # initiates other attributes
        self._calc_num_subplots()
        
        super().__init__(config=self._config.copy(), **kwargs)
        
        return
    
    def _check_letter_code(self, lc):
        self.logger.debug("Checking integrity for <letter_code>:")
        
        if self._check_exists(lc):
            
            if self._check_instance(collections.Iterator, lc) \
                    or self._check_instance(np.ndarray, lc):
                
                if self._check_equality(len(lc), self.values.shape[1]):
                    self.logger.debug("...everything *seems* OKAY")
                    return lc
        
        self.logger.debug("letter_code is not present or not correct. Set to FALSE")
        return None
    
    def _check_parameter(self, param, name):
        self.logger.debug("Checking integrity for <{}>:".format(name))
        
        if self._check_exists(param):
            
            if self._check_instance(np.ndarray, param):
                
                if self._check_equality(param.shape, self.values.shape):
                    self.logger.debug("...everything *seems* OKAY")
                    return param
        
        self.logger.debug("{} is not present or not correct. Set to FALSE".format(name))
        return None
    
    def _calc_num_subplots(self):
        """
        Calculates the total number of subplots to be plotted
        based on the user data.
        
        Returns:
            - None
            
        Stores:
            - self.num_subplots (int)
        """
        self.num_subplots = self.values.shape[0]
        self.logger.debug("Number of subplots: {}".format(self.num_subplots))
        
        return

    def _text_marker(
            self,
            ax,
            values_x,
            values_y,
            series,
            d,
            fs=3,
            orientation='horizontal'):
        """
        Places a text mark over the bars of a Bar Plot.
        
        Parameters:
            ax (matplotlib subplot axis): where maker is written.
            
            values_x (np.array): series with X axis information
            
            values_y (np.array): series with Y axis information
            
            series (np.array): series with information source to
                convert to text mark.
            
            d (dict): translates information into marker.
            
            fs (int): font size
            
            orientation (str): {'horizontal', 'vertical'}
                wheter plotting in a vertical or horizontal plot.
                Defaults to 'horizontal'
        """
        self.logger.debug("Text marker series: {}".format(series))
        
        if orientation == 'vertical':
            
            for s, x, y in zip(series, values_x, values_y):
                if str(s) in d.keys():
                    
                    if np.nan_to_num(y) > 0:
                        ha='left'
                        
                    elif np.nan_to_num(y) < 0:
                        ha='right'
                    
                    else:
                        ha='center'
                    
                    ax.text(
                        np.nan_to_num(y),
                        np.nan_to_num(x),
                        d[str(s)],
                        ha=ha,
                        va='center',
                        fontsize=fs
                        )
        
        elif orientation == 'horizontal':
            
            for s, x, y in zip(series, values_x, values_y):
                if str(s) in d.keys():
                    
                    if np.nan_to_num(y) > 0:
                        va='bottom'
                        
                    elif np.nan_to_num(y) < 0:
                        va='top'
                    
                    else:
                        va='bottom'
                    
                    ax.text(
                        np.nan_to_num(x),
                        np.nan_to_num(y),
                        d[str(s)],
                        ha='center',
                        va=va,
                        fontsize=fs
                        )
        
        return
    
    def _set_item_colors(self, items, values, d):
        """
        Colour codes <items> according to conditions in <values>
        as described by <d>.
        
        Parameters:
            items (items obj): either plot bars, ticks, etc...
        
            values (np.array shape (x,)):
                containing the condition information.
        
            d (dict): keys are conditions, and values are colours.
        
        Returns:
            None, series are changed in place.
        """
        
        self.logger.debug("Setting colours: {}".format(values))
        for v, it in zip(values, items):
            if str(v) in d.keys():
                it.set_color(d[str(v)])
            
            else:
                continue
        return
        
    def _finds_para_tag(data, tag_data):
        """
        Finds the bar index where the tag tick should be drawn based
        on an <identifier>.
        
        Parameters:
            
            - data (iterator): data upon which the index will be searched
            
            - tag_data (np.array): contains information where the tag is
        """
        if len(data) != len(tag_data):
            logger.info("*** Data and tag_data size equal: FALSE")
            return False
        
        logger.debug("Tag info: {}".format(tag_data))
        
        where_tag = np.where(tag_data==self._config["tag_id"])
        logger.debug("Tag mask found: {}".format(where_tag))
        
        tag_position = list(range(len(data)))[where_tag[0][0]]
        logger.debug("Tag bar index position: {}".format(tag_position))
        
        return tag_position
    
    def _draw_paramagnetic_tag(
            self,
            ax,
            tag_position,
            y_lim,
            plottype='h'
            ):
        """
        Draws paramagnetic tag tick on functionalized residue.
        
        Parameters:
            axs (matplotlib subplot axis): where values are plot.
            
            tag_position (int): the residue number where the paramagnetic
                tag is placed.
            
            y_lim (float): plot's y axis limit
            
            plottype (str): {'h', 'v', 'hm'}, whether plot of type 
                horizontal, vertical or Heat Map. Defaults: 'h'.
            
            tag_color (str): the colour of the tag cartoon
            
            tag_ls (str): matplotlib linestyle kwarg for the tag tick
            
            tag_lw (float): tag tick line width.
        """
        
        y_lim = y_lim*0.1
        
        if plottype in ['h', 'DPRE_plot']:
            ax.vlines(
                tag_position,
                0,
                y_lim,
                colors=self._config["tag_cartoon_color"],
                linestyle=self._config["tag_cartoon_ls"],
                linewidth=self._config["tag_cartoon_lw"],
                zorder=10
                )
            ax.plot(
                tag_position,
                y_lim,
                'o',
                zorder=10,
                color='red',
                markersize=2
                )
        
        elif plottype == 'v':
            ax.hlines(
                tag_position,
                0,
                y_lim,
                colors=self._config["tag_cartoon_color"],
                linestyle=self._config["tag_cartoon_ls"],
                linewidth=self._config["tag_cartoon_lw"],
                zorder=10
                )
            ax.plot(
                y_lim,
                tag_position,
                'o',
                zorder=10,
                color='red',
                markersize=2
                )
        
        elif plottype == 'heatmap':
            
            tag_line = 2
            
            ax.vlines(
                tag_position,
                0,
                tag_line,
                colors=self._config["tag_cartoon_color"],
                linestyle=self._config["tag_cartoon_ls"],
                linewidth=self._config["tag_cartoon_lw"],
                zorder=10
                )
        return
    
    def _plot_theo_pre(
            self,
            ax,
            values_x,
            values_y,
            plottype='h'
            ):
        """
        Plots theoretical PRE.
        
        Parameters:
            axs (matplotlib subplot axis): where values are plot.
            
            values_x (np.ndarray): X values to plot
            
            values_y (np.adrray): Y values to plot
            
            plottype (str): {'h', 'v'}, whether plot of type 
                horizontal, vertical or Heat Map. Defaults: 'h'.
            
        """
        
        if plottype == 'v':
            ax.plot(
                values_y,
                values_x,
                zorder=9,
                color=self._config["theo_pre_color"],
                lw=self._config["theo_pre_lw"]
                )
        
        elif plottype == 'h':
            ax.plot(
                values_x,
                values_y,
                zorder=9,
                color=self._config["theo_pre_color"],
                lw=self._config["theo_pre_lw"]
                )
        
        return
