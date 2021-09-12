import sys, argparse, logging


import pandas as pd
import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt

from adjustText import adjust_text

color_map_green_yellow_red = matplotlib.colors.LinearSegmentedColormap.from_list("", ["green","yellow","red"])

def gradient_image(ax, extent, direction=0.3, cmap=color_map_green_yellow_red, cmap_range=(0, 1), interpolation='bicubic', **kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* kwarg.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, interpolation=interpolation,
                   vmin=0, vmax=0.9, cmap=cmap, **kwargs)
    return im

def scatter_and_annotate_risk_data_points():
    #https://stackoverflow.com/questions/14432557/matplotlib-scatter-plot-with-different-text-at-each-data-point
    #https://stackoverflow.com/questions/19073683/matplotlib-overlapping-annotations-text
    return im

def decorate_axes(ax, graph_font):
    ax.set_xlabel('Impact', **graph_font)
    im = ax.set_ylabel('Likelihood', **graph_font)
    ax.tick_params(axis='both', labelsize=8)
    return im

def decorate_figure(ax, graph_font):
    im = ax.set_title('Risk Matrix Graph', **graph_font)
    return im

def calculate_simple_risk(df):
    # the risk is impact * likelihood^T
    return df['impact']*df['likelihood']

def main(csv_filename, graph_filename):
    # load the data files
    logging.debug("Parcing CSV file: {}".format(csv_filename))
    df = pd.read_csv(csv_filename)
    print(df.to_string())
    
    # calculate risk
    r = calculate_simple_risk(df)
    
    # generate the graph
    xmin, xmax = xlim = -1, 6
    ymin, ymax = ylim = -1, 6

    min_impact, max_impact = impact_lim = 0, 5
    min_likelihood, max_likelihood = likelihood_lim = 0, 5
    fig, ax = plt.subplots()
    
    im = gradient_image(ax, direction=0.5, extent=(min_impact, xmax, min_likelihood, ymax),
                        cmap_range=(0, 1), interpolation='bicubic')

    ax.set(xlim=(min_impact, xmax),ylim=(min_likelihood, ymax), autoscale_on=False)
    ax.set_aspect('equal')
    
    ax.scatter(x=df['impact'], y=df['likelihood'], s=r*2, c='black',alpha=0.2)
    
    graph_font = {'fontname':'Helvetica', 'fontsize': 8}
                  
    # annotate
    texts = []
    for index,id in enumerate(df['id']):
        texts.append(
            ax.annotate(str(df['id'][index]), (df['impact'][index], df['likelihood'][index]),
                            bbox=dict(boxstyle="round,pad=0.1", fc='w', alpha=0.4, ec="black", lw=0.5),
                            **graph_font
            )
        )
    
    # adjust text
    adjust_text(texts, ax=ax, 
                expand_text=(1.5, 1.3), 
                expand_points=(1.3, 1.3), 
                expand_objects=(1.3, 1.3),
                force_text=(1.55, 1.35), force_points=(1.15, 1.3), force_objects=(1.3, 1.3),
                only_move=dict(points='xy', text='xy', object='xy'),
                va='center', ha='left', precision=0.1,
                arrowprops=dict(arrowstyle="-", color='black', lw=0.5), 
                lim=2000)
    
    decorate_axes(ax, graph_font)
    decorate_figure(ax, graph_font)
    
    plt.savefig(graph_filename)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser( 
                        description = "Takes a csv risk matrix with a header and generates a risk matrix graph",
                        epilog = "",
                        fromfile_prefix_chars = '@' )
    parser.add_argument(
                        "csv_filename",
                        help = "Path to the .csv file containing the risk matrix",
                        metavar = "CSV_FILENAME")
    parser.add_argument(
                        "graph_filename",
                        help = "Path to the .png output file",
                        metavar = "PNG_FILENAME")
    parser.add_argument(
                        "-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
  
    # Setup logging
    loglevel = logging.INFO    
    if args.verbose:
        loglevel = logging.DEBUG
    
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
        
    main(args.csv_filename, args.graph_filename)
