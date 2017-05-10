import sys
### Paths to somewhere:
spectra_path = sys.argv[1]  # where spectra peaklists .csv files are stored - relative path
logfile_name = 'file.log' #  the name of the log file
####################################

### Input Data Setup
applyFASTA = True  # complete the sequence with a FASTA file?
FASTAstart = 1  # Residue number for the first residue in the FASTA file?
#
perform_cs_correction = False  # Aligns peaklists to a specific residue in the reference spectra
cs_correction_res_ref = 76  # To which residue?
#
has_sidechains = False  # Are there sidechain entries in the peaklists?
use_sidechains = False  # Do you want to analyse those sidechains?
#
expand_lost_yy = False  # Considers lost residue over yy references and xx reference
expand_lost_zz = False  # Considers lost residue over zz references and xx reference
####################################

### Calculations Setup
do_cond1 = True  # Analyse data in the first titration condition (dimension)
do_cond2 = False  # Analyse data in the second titration condition (dimension)
do_cond3 = False  # Analyse data in the thrid titration condition (dimension)
#
perform_comparisons = False  # Compares data obtained for condition experiment.
#
csp_alpha4res = 0.14  # General alpha normalization factor for CSP
csp_res_exceptions = {'G': 0.2}  # exceptions for the normalization factor
cs_lost = 'prev'  # how to represent the lost residues in CSPs [prev/full]
#
perform_resevo_fit = True  # Fit parameter evolution over titration experiment
#
titration_x_values = [0, 125, 250, 500, 1000, 2000, 2500] # values for the x axis in the fitting procedure (ex. Ligand concentration)
#
## Perform PRE analysis
apply_PRE_analysis = False
apply_smooth=True
gaussian_stddev=1
gauss_x_size=7
pre_color='green'  # theoretical PRE line color
pre_lw=1  # theoretical PRE line width
tag_color='blue'
tag_lw=0.8
tag_ls='-'
#####################################
#
#
### Data Representation Setup
#
chimera_att_select_format = ':'  # format to select residues in Chimera
#
# Restrains to Plot:
plots_PosF1_delta = False # Plot nuclei 1 shift perturbation data
plots_PosF2_delta = False # Plot nuclei 2 shift perturbation data
plots_CSP = True  # Plot combined chemical shift perturbation data
plots_Height_ratio = False  # Plot Height ratio data
plots_Volume_ratio = False  # Plot Volume ratio data
#
# Ploting Templates
plots_extended_bar = False  # Represent data in Extended Bar Plot style
plots_compacted_bar = True  # Represent data in Compacted Bar Plot style
plots_vertical_bar = False # Represent data in Vertical Bar Plot style
plots_residue_evolution = False  # Represent Data Evolution per Residue style
plots_cs_scatter = False  # Represent chemical shift scatter data
#
# Y Axis Label for each restraint
yy_label_PosF1_delta = 'ppm'  # y axis label for nuclei 1
yy_label_PosF2_delta = 'ppm'  # y axis label for nuclei 2
yy_label_CSP = 'CSPs (ppm)'  # y axis label for combined chemical shift
yy_label_Height_ratio = 'Hi/H0'  # y axis label for height ratio
yy_label_Volume_ratio = 'Vi/V0'  # y axis label for volume ratio
#
# Restraint column name for the output
calccol_name_PosF1_delta = 'H1_delta'  # column name for nuclei 1
calccol_name_PosF2_delta = 'N15_delta'  # column name for nuclei 2
calccol_name_CSP = 'CSP'  # column name for combined chemical shift perturbation data
calccol_name_Height_ratio = 'Height_ratio'  # column name for Height Ratio data
calccol_name_Volume_ratio = 'Vol_ratio'  # column name for Volume Ratio data
#
# Y axis scale for each calculated restraint
yy_scale_PosF1_delta = 0.1  # y axis sacle for nuclei 1
yy_scale_PosF2_delta = 0.25  # y axis scale for nuclei 2
yy_scale_CSP = 0.3  # y axis sacle for combined chemical shift
yy_scale_Height_ratio = 1.5 # y axis scale for height ratio
yy_scale_Volume_ratio = 1.5 # y axis scale for volume ratio
yy_scale_nbins=5  # adjusted number of ticks
#####################################
#
#### Plot configuration variables
### General Titration Plots Variables
tplot_subtitle_fn= 'Arial'  # font type for the subplot titles.
tplot_subtitle_fs= 8  # font size for the subplot titles.
tplot_subtitle_pad= 0.99  # subplot title separation from y
tplot_subtitle_weight= 'normal'  # subplot title font weight: bold, italic, etc...
tplot_x_label_fn= 'Arial'  # x-label font
tplot_x_label_fs= 8  # x-label font size
tplot_x_label_pad= 2  # x-label separation from axis
tplot_x_label_weight= 'bold'  #x_label font weight: bold, italic, etc...
tplot_y_label_fn= 'Arial'  # y-label font
tplot_y_label_fs= 8  # y-label font size
tplot_y_label_pad=3  # y-label separation from ayis
tplot_y_label_weight= 'bold'  #y_label font weight: bold, italic, etc...
tplot_x_ticks_pad=2  # x ticks pad
tplot_x_ticks_len=2  # length of xticks
tplot_y_ticks_fn='Arial'  # y-tick font name
tplot_y_ticks_fs=5  # y-tick font size
tplot_y_ticks_rot=0
tplot_y_ticks_pad=1  # y-tick separati
tplot_y_ticks_weight= 'normal'  #x_label font weight: bold, italic, etc...on
tplot_y_ticks_len=2  # length of y ticks
tplot_y_grid_flag=True  # ON/OFF horizontal grid
tplot_y_grid_color='lightgrey'  # grid color
tplot_y_grid_linestyle='-'  # style of grid line
tplot_y_grid_linewidth=0.2  # grid line width
tplot_y_grid_alpha=0.8  # grid transparency
tplot_vspace=0.5 # vertical spacing between plots
#
## General Bar Plots Variables
bar_measured_color= 'black'  # bar color for measured peaks
bar_status_color_flag= True  # applies color to the 'lost' residues
bar_lost_color= 'red'  # bar color for the lost residues
bar_unassigned_color= 'lightgrey'  # xticks and shade color for unassigned residues.
bar_width= 0.6  # bar width
bar_alpha= 1  # 0 is full transparency, 1 full opacity
bar_linewidth= 0  # bar border line width, 0 to desable
bar_threshold_flag= True  # applies stdev thresold
bar_threshold_color= 'red'  # threshold color
bar_threshold_linewidth= 0.5  # threshold line width
bar_threshold_alpha= 0.8  # threshold transparency
bar_mark_fontsize=3  # user defined marks fontsize
bar_mark_prolines_flag=True  # mark prolines ON/OFF
bar_mark_prolines_symbol='P'  # symbol to mark prolines
bar_mark_user_details_flag=True  # mark user details ON/OFF
bar_color_user_details_flag=True  # color bars according to user detail marks ON/OFF
bar_user_marks_dict = {
    'H0': 'H',
    'V0': 'V',
    'low':'L',
    'p1':'1',
    'p2':'2',
    'p3':'3',
    'p4':'4',
    'p5':'5',
    'p6':'6',
    'p7':'7',
    'p8':'8',
    'p9':'9',
    'p10':'10',
    'z':'z',
    'Z':'z',
    'MTSL':'M'
}  # keys: the string in 'Details' column in input data, value: the character to be drawn
bar_user_bar_colors_dict = {
    'H0': 'khaki',
    'V0': 'khaki',
    'low':'khaki'}  # keys: the string in 'Details' column in input data, value: the character to be drawn

# Specific details for Extended Bar Plot
## use a combination of cols_page and rows_page to achieve desired figure ratio
ext_bar_cols_page = 1  # number of columns of subplots per page
ext_bar_rows_page = 6  # number of rows of subplots per page
ext_bar_x_ticks_fn = 'monospace'  # x ticks font type
ext_bar_x_ticks_fs = 6  # x ticks font size
ext_bar_x_ticks_rot = 90  # x ticks rotation
ext_bar_x_ticks_weight = 'normal'  # x ticks rotation
ext_bar_x_ticks_color_flag=True
#
# Specific details for Compacted Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
comp_bar_cols_page = 3  # number of columns of subplots per page
comp_bar_rows_page = 5  # number of rows of subplots per page
comp_bar_x_ticks_fn='Arial'  # x ticks font type
comp_bar_x_ticks_fs=6  # x ticks font size
comp_bar_x_ticks_rot=0  # x ticks rotation
comp_bar_x_ticks_weight='normal'  # x ticks pad
comp_bar_unassigned_shade=True  # displays shade for unassigned residues
comp_bar_unassigned_shade_alpha=0.5  # unassigned residues shade transparency.
#
# Specific details for Vertical Bar plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
vert_bar_cols_page = 5  # number of columns of subplots per page
vert_bar_rows_page = 2  # number of rows of subplots per page
#
# Specific details for DELTA PRE oscilations Plot
dpre_osci_rows=10
dpre_osci_width=3  # scale factor for the width of the plot
dpre_osci_y_label = r'$\Delta$PRE$_(rc-exp)$'
dpre_osci_y_label_fs=5
dpre_osci_dpre_ms=2  # DELTA_PRE circle marker size
dpre_osci_ymax=0.8
dpre_osci_dpre_alpha=0.5  # DELTA_PRE alpha
dpre_osci_smooth_lw=1  # smooted DPRE line width
dpre_osci_ref_color='black'  # color for the reference data
dpre_osci_color_init='#ff00ff'  # initial color for data points color gradient
dpre_osci_color_end='#0000ff'  # final color for data points color gradient
dpre_osci_x_ticks_fn='Arial'  # xticks font
dpre_osci_x_ticks_fs=5  # x ticks font size
dpre_osci_x_ticks_pad = 0.5
dpre_osci_x_ticks_weight = 'normal'
dpre_osci_grid_color='grey'  # grid color
dpre_osci_shade = False  # applies shade to regions
dpre_osci_shade_regions = [(23,37),(0,0),(0,0)]  # defines shade regions
dpre_osci_res_highlight=True  # flags residue highlight
dpre_osci_res_hl_list=[25,32,54,64,66,47]  # residues to highlight (res, shade width)
dpre_osci_rh_fs=4  # font size for residue highlight
dpre_osci_rh_y=0.9  # y position for residue 1-letter representation
#
## General Variables for Evolution per Residue
revo_subtitle_fn='Arial'  # subplot title font
revo_subtitle_fs=8  # subplot title font size
revo_subtitle_pad=0.98  # subplot title pad
revo_subtitle_weight='normal'
revo_x_label_fn='Arial'  # x label font
revo_x_label_fs=6  # x label font size
revo_x_label_pad=2  # x label pad
revo_x_label_weight='normal'  # x label weight
revo_y_label_fn='Arial'  # y label font
revo_y_label_fs=6  # y label font size
revo_y_label_pad=2  # y label pad
revo_y_label_weight='normal'  # y label weight
revo_x_ticks_fn='Arial'  # x ticks font
revo_x_ticks_fs=5  # x ticks font size
revo_x_ticks_pad=1  # x ticks pad
revo_x_ticks_weight=1  # x ticks font style
revo_x_ticks_rot=30  # ticks label rotation
revo_y_ticks_fn='Arial'  # x ticks font
revo_y_ticks_fs=5  # x ticks font size
revo_y_ticks_pad=1  # x ticks pad
revo_y_ticks_weight=1  # x ticks font style
revo_y_ticks_rot=0
#
# Specific details for Residue Evolution Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
res_evo_cols_page = 5  # number of columns of subplots per page
res_evo_rows_page = 8  # number of rows of subplots per page 
res_evo_set_x_values=True  # use user defined x values? Necessary for titration fitting.
res_evo_x_ticks_nbins=5  #adjust number of ticks
res_evo_x_label='[RNF125]'  # x label
res_evo_line_style='-'  # data line style
res_evo_line_width=1  # data line width
res_evo_line_color='r'  # data line color
res_evo_marker_style='o'  # data marker style
res_evo_marker_color='darkred'  # data marker color
res_evo_marker_size=3  # data marker size
res_evo_fill_between=True  # draw data shade
res_evo_fill_color='pink'  # shade color
res_evo_fill_alpha=0.5  # shade transparency (0-1)
res_evo_fit_line_color = 'black'  # fit line color
res_evo_fit_line_width = 1  # fit line width
res_evo_fit_line_style = '-'
#
# Specific details for Chemical Shift Scatter Plot
cs_scatter_cols_page = 5  # number of columns of subplots per page
cs_scatter_rows_page = 7  # number of rows of subplots per page
cs_scatter_x_label='1H (ppm)'
cs_scatter_y_label='15N (ppm)'
cs_scatter_mksize=20  # marker size
cs_scatter_scale=0.01  # scale representation
cs_scatter_mk_type='color' # 'color' or 'shape'
cs_scatter_mk_start_color='#cdcdcd' # start color for gradient [in hex notation] - color style
cs_scatter_mk_end_color='#000000' # end color for gradient [in hex notation] - color style
cs_scatter_markers=['^','>','v','<','s','p','h','8','*','D']  # sequencial markers
cs_scatter_mk_color=['none']  # marker inside color for shape style - SHOULD BE LIST
cs_scatter_mk_edgecolors=['black']  # marker edge color for shape style - SHOULD BE LIST
cs_scatter_mk_lost_color='red'  # color for lost data points - color style
#
### DELTA PRE Heat Maps
heat_map_rows = 20
heat_map_vmin=0.2
heat_map_vmax=0.7
heat_map_x_ticks_fn='Arial'
heat_map_x_ticks_fs=6
heat_map_x_ticks_pad=1
heat_map_x_ticks_weight='normal'
heat_map_x_ticks_rot=0
heat_map_y_label_fn='Arial'
heat_map_y_label_fs=3
heat_map_y_label_pad=2
heat_map_y_label_weight='bold'
heat_map_right_margin=0.2
heat_map_bottom_margin=0.5
heat_map_top_margin=0.9
heat_map_cbar_font_size=4
########################################

#
### Figure Details
fig_width = 8.69  # Figure width in inches
fig_height = 11.69  # Figure height in inches
fig_file_type = 'pdf'  # Figure file type
fig_dpi = 300  # Figure resolution
#s

import farseermain
