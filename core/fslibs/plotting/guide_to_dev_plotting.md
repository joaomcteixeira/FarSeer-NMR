# The Plotting System

The plotting system can be found in `core/fslibs/plotting`, where the base classes are placed. Inside `templates` are the front-end classes that actualy configure the plotting template. _Base classes_ contain methods that are shared by the different _front-end classes_, and front-end classes should configure *only* the subplot template. Figure properties and subplot organization should be managed by the _base classes_. In this sense, you should choose the base classes inheritance according to the type of plot you wish to generate and design a front-end class (plot template) to configure your subplot.  

Nonetheless, the plotting architecture is such that you can create you own plotting structure independent of the official Farseer-NMR plotting system, as long it is consistent with the Farseer-NMR workflow, however we discourage this methodology.  

## Structure of the plotting base classes.

Class hierarchy of the plotting base classes.

```
| PlottingBase.py
|
|---- ExperimentPlot.py
    | ---- BarPlotBase.py

|---- ResiduePlot.py
|---- SinglePlot.py
```

`PlottingBase` contains those methods commons to every plot, which mostly refer to configuration of the plotting figure, subplot management, and data checks. *Three* types of plots are currently available, _Experiment Plot_, _Residue Plot_ and _Single Plot_; these plot types refer to which data is represented in each subplot. For example:

- in _experiment plot_, each subplot represents a given parameter information for every residue for a given experimental data point; this is normally used for bar plots, where bars represent residues and each subplots contains the information of each experimental titration data point.  
- On the other hand, for _Residue Plots_, each subplot, contains the evolution of a given parameter (or observable) for a single residue along the whole titration series, and the final plot figure contains one subplot for each residue in the protein.  
- Lastly, the _Single Plot_ contains all the information of the series (residues and experiments) in a single subplot.  

Depending on the hierarchy structure, one of the base classes contains a `.plot()` and `.plot_subplots()` methods that, respectively, control the workflow of operation to generate and write the final plotting figure and to send the specific data to each subplot - use `BarPlotBase.py` as an example.

## Plotting templates

Plotting tempates have a `.subplot()` method that actually configures the subplot. Depending on the plot-subplot type, the `.subplot()` method may receive different arguments, in the case of `BarExtendedHorizontal.py` it receives `ax, values, subtitle, i`, repectively:

- ax: the subplot axis where to operate
- values: the Y values array
- subtitle: the subplot title
- i: the index of the subplot

the bar labels where defined during the object instantiation and are stored in `self.labels`.

## Rules of the plotting architecture

If you wish to implement a new plotting template following the Farseer-NMR plotting architecture, you should consider the following rules and guidelines.

### Configuration dictionaries

Plotting parameters are configure by hierarchic (JSON-like) dictionaries and NOT by keyword arguments. In this way, all plotting parameters can be configure inside dictionaries in the Farseer-NMR calculation `config.json` file, as it occurs will all the Farseer-NMR parameters.

Implementation of configuration dictionaries:

- every class in the hierarchy pyramid contains a `_default_config` dictionary attribute with all the parameters that can be configured at that level, therefore the class contains a keyword argument `config={}`
- the default_config dictionary should contain ALL the parameters that are used in that class methods.
    - if methods are general their configuration may rely on arguments instead of the `_config` dictionary
    - `_default_config` can have _items_ referent to parent classes if that provides specificity to the child class.
    - the `_default_config` of the subplot template class (inside `templates` folder) should contain **ALL** items that are used by that template including those from parent classes.
- `config` dictionaries should be pass along the hierarchy and update the parent configuration, see `BarExtendedHorizontal.py` as an example.

```python
class BarExtendedHorizontal(BarPlotBase):
    
    _default_config = {
    # collapsed view
    }
    
    def __init__(
            self,
            values,
            labels,
            config={},
            **kwargs
            ):
        
        # initializes logger
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarExtendedHorizontal initiated")
        
        # sets configuration
        self.logger.debug("Config received: {}".format(config))
        self._config = BarExtendedHorizontal._default_config.copy()
        self._config.update(config)
        self.logger.debug("Config updated: {}".format(self._config))
        
        super().__init__(
            values,
            labels,
            config=self._config.copy(),
            **kwargs
            )
```

- In this way, to change a plot configuration, a configuration dictionary containing only the parameters to be changed can be passed as an argument to the plot to update the default configuration.
- Having a default configuration ensures that the plots are always drawn.
- The method `.set_config()` can be used to update plot's configuration, likewise, `.get_config()` return a dictionary with the current configuration and `.print_confi()` nicely prints the current configuration.

### Additional features

Farseer-NMR plots are feature rich and can be further enriched with any data that desirable to plot or represent. Additional data representation is implemented as such:

Additional data should be pass as a keyword argument defined at the correspondent hierarchy level, for example, if that data would apply to all the _experiment plot_ type it should be configure in the `ExperimentPlot` class.  

These arguments should be, preferencially, np.ndarrays of shape matching the data being plotted and should be stored as a class attributes. Additionally, parameters to flag the representation of this data and configure data representation should be added to the `_default_config` dictionary.
