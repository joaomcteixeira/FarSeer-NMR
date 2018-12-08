
import os

if os.path.exists('farseernmr.log'):
    os.remove('farseernmr.log')

if os.path.exists('debug.log'):
    os.remove('debug.log')

import numpy as np

from core.fslibs.plotting.templates.BarExtendedHorizontal import BarExtendedHorizontal
from core.fslibs.plotting.templates.BarCompacted import BarCompacted

if __name__ == "__main__":
    
    ######################################################################## 1
    ############ Short data set
    
    values = np.full((7,15), 0.2)
    labels = np.arange(1, len(values[0])+1).astype(str)
    
    plot1 = BarExtendedHorizontal(values, labels)
    c = {"figure_path": "bar_extended_horizontal_1_short.pdf"}
    plot1.set_config(c)
    plot1.plot()
    
    plot2 = BarCompacted(values)
    c = {"figure_path": "bar_compacted_1_short.pdf"}
    plot2.set_config(c)
    plot2.plot()
    
    ######################################################################## 2
    ############ Large data set
    
    values = np.full((2,765), 0.2)
    labels = np.arange(1, len(values[0])+1).astype(str)
    
    c = {"figure_path": "bar_extended_horizontal_2_large.pdf"}
    plot1 = BarExtendedHorizontal(values, labels, config=c)
    plot1.plot()
    
    c = {"figure_path": "bar_compacted_2_large.pdf"}
    plot2 = BarCompacted(values, labels, config=c)
    plot2.plot()
    
    ######################################################################## 2
    ############ Mark details
    
    values = np.random.random((3,100)) - 0.5
    labels = np.arange(1, len(values[0])+1).astype(str)
    aa = ['P','A']
    letter = np.random.choice(aa, values.shape[1], p=[0.1,0.9])
    mask = np.where(letter=='P')
    values[:,mask] = np.nan
    
    dd = ['None','foo','bar','boo']
    details = np.random.choice(dd, values.shape[1])
    details = np.stack([details, details, details], axis=0)
    details[:, mask] = "None"
    
    c = {
        "y_lims":(-1,1),
        "figure_path": "bar_extended_horizontal_3_mark.pdf",
        "mark_prolines_flag": True,
        "mark_user_details_flag": True,
        "color_user_details_flag": True,
        "user_marks_dict": {
            "foo": "f",
            "bar": "b",
            "boo": "o"
        },
        "user_bar_colors_dict": {
            "foo": "green",
            "bar": "yellow",
            "boo": "magenta"
        },
            }
    
    plot1 = BarExtendedHorizontal(
        values, labels, config=c, letter_code=letter, details=details)
    plot1.plot()
    
    plot2 = BarCompacted(
        values, labels, config=c, letter_code=letter, details=details)
    c = {"figure_path": "bar_compacted_3_mark.pdf"}
    plot2.set_config(c)
    plot2.plot()
    
