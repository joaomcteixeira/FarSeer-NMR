"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

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
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.WetHandler import WetHandler as fsw

class BarExtended(PlottingBase):
    """Extended Bar plotting template."""
    
    def __init__(self, data, config):
        super.__init__(data, config)
    
    def data_select(self, *args):
        """
        Selects the desired data to plot from the original input data.
        
        This function can be used to fine select the data to the ploted
        or transpose matrix coordinates or any other request that
        faciliates the task of .plot_subplots() method.
        
        Returns:
            - None.
            
        Stores:
            - self.data_to_plot (numpy.array): selected data to plot
        """
        pass
    
    def draw_figure(self, *args):
        """
        Draws the figure architecture.
        
        Defines the size of the figure and subplots based
        on the data to plot.
        
        Returns:
            - None.
        
        Stores :
            - self.figure: Figure object.
            - self.axs: axes of the figure (in case matplotlib is used).
            - self.num_subplots (int): the number of subplots to be used
            - self.len_axs (int): the number of subplots created in the
                figure object.
        """
        pass
    
    def plot_subplots(self, args*):
        """
        Sends the specific data to each subplot.
        
        The way data is sliced from the whole data to plot matrix
        depends on the nature of the subplots.
        
        Returns:
            - None
        """
    
    def subplot(self, args*):
        """The routine that defines each subplot."""

