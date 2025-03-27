import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import gwyfile as gwy
import os

# Update global matplotlib parameters for consistent styling
plt.rcParams.update({
    'font.size': 12,  # Set font size for all text elements
    'font.family': 'serif',  # Use serif fonts
    "text.usetex": True, # Use LaTeX for text rendering
    'text.latex.preamble': # Add custom LaTeX preamble for font selection
        r"""
        \usepackage{libertine}
        \usepackage[libertine]{newtxmath}
        """,
})


def add_cbar(im, ax, data, label, **kwargs):
    """
    Adds a customized colorbar to the plot.
    
    Parameters:
        im: The image plot object for which the colorbar is added.
        ax: The axis object of the plot.
        data: The numerical data used for the image plot.
        label: Label for the colorbar.
        **kwargs: Additional keyword arguments for the colorbar.

    Returns:
        cbar: The colorbar object added to the plot.
    """
    cbar = plt.colorbar(im, ax=ax, shrink=0.5, aspect=12, pad=0.03, **kwargs)  # Add colorbar
    cbar.ax.axis('off')  # Hide colorbar axis

    sep = 0.07  # Separation between the colorbar and the labels
    # Add min and max value labels
    cbar.ax.text(0.5, 0-sep, f"{data.min():.3g}", va='center', ha='center', transform=cbar.ax.transAxes)
    cbar.ax.text(0.5, 1+sep, f"{data.max():.3g}", va='center', ha='center', transform=cbar.ax.transAxes)
    # Add vertical colorbar label
    cbar.ax.text(2.25, 0.5, label, va='center', ha='center', transform=cbar.ax.transAxes, rotation=-90)

    return cbar


def add_scalebar(ax, **kwargs):
    """
    Adds a scale bar to the plot.
    
    Parameters:
        ax: The axis object of the plot.
        **kwargs: Additional keyword arguments for the scalebar.

    Returns:
        scalebar: The scalebar object added to the plot.
    """
    scalebar = ScaleBar(
        1, "m", length_fraction=0.3, location="lower left", scale_loc='top',
        frameon=False, border_pad=1.5, width_fraction=0.012,
        color='white', **kwargs
    )  # Customize scalebar properties
    ax.add_artist(scalebar)  # Add the scalebar to the axis

    return scalebar


# Parameters for different AFM channels and their visualization settings
params = {
    'ZSensor': {
        'cmap': 'afmhot',
        'datascale': 1e9,
        'label': 'Height [nm]',
    },
    'Peak Force Error': {
        'cmap': 'gray',
        'datascale': 1e3,
        'label': 'Peak Force [mV]',
    },
    'Potential': { # KPFM potential
        'cmap': 'inferno', 
        'datascale': 1, 
        'label': 'Potential [V]',
    },
}


def process_gwy_files():
    """
    Processes all `.gwy` files in the current directory, extracts AFM data,
    and saves the plots with scalebars and colorbars.
    """
    # Get all .gwy files in the current folder
    files = [f for f in os.listdir(os.getcwd()) if f.endswith('.gwy')]
    
    if not files:  # Check if there are no .gwy files
        print("No .gwy files found in the folder.")
        return
    
    # Create an output folder for processed images
    output_folder = os.path.join(os.getcwd(), "processed_images")
    os.makedirs(output_folder, exist_ok=True)

    # Process each .gwy file
    for file in files:
        try:
            channels = gwy.util.get_datafields(gwy.load(file))
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue

        # Iterate over data channels in the .gwy file
        for key, channel in channels.items():
            # Skip channels that are not in the `params` dictionary
            if key not in params.keys():
                continue
            
            # Scale the data for visualization
            data = channel.data * params[key]['datascale']

            # Set lowest value to zero for height data
            if key == 'ZSensor':
                data -= data.min()

            # Create a figure and axis for plotting
            fig, ax = plt.subplots(layout='constrained')
            im = ax.imshow(
                data, interpolation='none', origin='upper', 
                extent=(0, channel.xreal, 0, channel.yreal), cmap=params[key]['cmap']
            )  # Plot the data
            
            ax.axis('off')  # Turn off axes for clean visualization
            add_cbar(im, ax, data, params[key]['label'])
            add_scalebar(ax)  

            # Define the output file path
            output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.{key}.png")
            # Save the figure as an image file
            fig.savefig(output_path, dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    process_gwy_files()
