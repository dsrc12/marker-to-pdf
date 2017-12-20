# **marker-to-pdf**
### **Overview of the files**
This repo contains:
* TagResizer.py
  * The python script which takes the markers in Tags and scales and prints them according to the required page size, tag size, resolution, etc. It can take CSV files or the required tags can be typed in as a comma-separated list (follow the instructions on the command-line).
* PrintSomeTags.bat
  * A batch file which pip installs the non-standard modules required (pygame, fpdf, and pathlib) and then runs TagResizer.py.
* Tags
  * A folder which contains a heap of numbered png images of the markers, taken directly from the AprilTags site (https://april.eecs.umich.edu/software/apriltag.html) of the 36h11 tag family.
* OpenSans-Regular.ttf
  * The font used for printing in the pdf.
* LICENSE
  * The MIT license for the code herein.
* README.md
  * ...this document.
### **The Script: using TagResizer.py**
TagResizer.py codes for a commandline interface which allows the user to print out markers of various sizes to an easily printable PDF or a series of PNG images for insertion into other media, where attempting to resize and format the original images from the AprilTags website could be time-consuming or irritating.
As aforementioned, TagResizer.py can take CSV files or comma-separated input.
CSV files should be formatted with the name of the tag in the first column (to be printed above the tag on the page), the tag's code in the second (to be printed below the tag on the page), and the tag's side length in cm (including the white border) in the third. Any headers or malformed rows will be omitted (visible in the terminal output).
For example:

|TagName | TagCode | TagSize | << Header, ignored.
|------- | ------- | ------- | ------------------
|NorthPillar | 4 | 25 | << The first tag in the document, 25cm x 25cm (standard wall marker size), representing a 4.
|EastPillar | 8 | 25 | << The second tag in the document, 25cm x 25cm, representing an 8.
|PoisonToken | 13 | 10 | << The third tag in the document, 10cm x 10cm (standard token size), representing a 13.
|BrToken | Yes | 9 | << This tag would be the fourth tag, 9cm x 9cm, but has a malformed number code, so is omitted.
|  | 0 | 5 | << The fourth tag in the document, 5cm x 5cm (very small), representing a 0. This tag will be unnamed.

If the tag numbers are input manually on the command line, they are required in the form of a comma-separated list, but the individual elements can be single numbers or ranges of numbers of the form a-b, which print all of the tags representing numbers from a to b, inclusive, in order.

```python
1,2,3,4,5       # Would produce tags representing 1, 2, 3, 4 and 5
1, 2, 3, 4, 5   # This would do likewise
1-5             # As would this
1,1-3,5,8,1-10  # Would print tags 1, 1, 2, 3, 5, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9 and 10. In that order.
```

Manually input tag numbers do not give opportunity for printing tag names.

TagResizer.py gives two forms of output: a series of PNG images of the printed pages, and a PDF document with them all collated for printing. (TODO: clarify this further?) The commandline interface gives options for the format of printing, permitting manual customisation or use of presets for standard marker formats.

The available presets are:
* LARGE
  * Produces an A3 page with a 25cm x 25cm marker in the centre.
* SMALL
  * Produces an A4 page with a 10cm x 10cm marker in the centre.
* SQUARE
  * Produces a square page, entirely filled by the marker (including its white border).
  * This preset will not produce a PDF.

In CUSTOM format creation, you can select:
* Scale
  * Essentially the clarity of the image. Takes a value for the number of pixels per mm the image is rendered with.
  * The standard value is 5px per mm. This value is used in the presets and for CSV input, for simplicity.
* Paper type
  * One from A4, A3 or SQUARE.
    * A4 and A3 formats produce series of PNG images and a PDF of all the markers on pages of their respective paper size, all with the marker in the centre, code underneath and name above.
    * SQUARE format does not produce a PDF, only a series of marker PNGs with no number or label.
* Tag size
  * The side length of the tag printed, in cm.
  * Tags are printed in the centre of the page, with the code underneath and name above, except in the case of the SQUARE page type, where they determine the size of the image.
  * If you select a size of 0, no tag will be printed but a blank page will be inserted into the PDF or, if the SQUARE page type is selected, a PNG with nothing in it will be produced for that marker.
 
