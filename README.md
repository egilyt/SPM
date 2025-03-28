# SPM
Python script to plot AFM data. The script processes every `.gwy`-file in its folder, and saves the images in a sub-folder.

## Work flow
1. For each `.spm`-file (or similar format) in your folder:
   1. Open the files in [Gwyddion](https://gwyddion.net/download.php), and do the
      necessary data processing (i.e. level topography data by mean plane substraction, align rows, etc.).
   2. Save as a new file with the `.gwy` file extension.
2. Run `plot_spm_folder.py` in the same folder as the data.
3. Voilà.

---

For more advanced functionality, check out [Ruben's WallPY repo](https://github.com/RubenDragland/WallPY/tree/main).
