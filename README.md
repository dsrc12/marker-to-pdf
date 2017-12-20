# **marker-to-pdf**
### **Overview**
Script used to generate pdf documents, populated with April Tag markers, for quick printing.
Contains:
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
### **The Script: Input**
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
