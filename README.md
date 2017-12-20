# marker-to-pdf

Script used to generate pdf documents, populated with April Tag markers, for quick printing.
Contains:
- TagResizer.py
-- The python script which takes the markers in Tags and scales and prints them according to the required page size, tag size, resolution, etc. It can take CSV files or the required tags can be typed in as a comma-separated list (follow the instructions on the command-line).
- PrintSomeTags.bat
-- A batch file which pip installs the non-standard modules required (pygame, fpdf, and pathlib) and then runs TagResizer.py.
- Tags
-- A folder which contains a heap of numbered png images of the markers, taken directly from the AprilTags site (https://april.eecs.umich.edu/software/apriltag.html) of the 36h11 tag family.
- OpenSans-Regular.ttf
-- The font used for printing in the pdf.
- LICENSE
-- The MIT license for the code herein.
- README.md
-- ...this document.
