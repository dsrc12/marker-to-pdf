import pygame, os
from pathlib import Path
from fpdf import FPDF
# Requires pygame, pathlib and fpdf
# For page drawing, path compatibility on different systems, and pdf generation, respectively
pygame.init()

# paths for the tag images and font used
loadtagpath = str(Path("Tags") / "tag36_11_") # Filename may have to be changed if tags replaced to different spec
fontpath = "OpenSans-Regular.ttf" # Nice opensource font... also used by SR

# Dictionary of the dimensions of the different print formats, in mm
papertypes = {"A4": (297, 210), "A3": (420, 297), "SQUARE": (100, 100)}

# Dictionary of the different print presets, showing
#   The name (in CAPS), as it appears in selection, as the key
#   A list of values containing
#     A short description, shown in selection
#     The pixels-per-mm value
#     The page type used
#     The marker size used, as side length in cm (this includes its white border)
presets = {"LARGE": ["A3 page with 25cm marker", 5, "A3", 25],
           "SMALL": ["A4 page with 10cm marker", 5, "A4", 10],
           "SQUARE": ["Just markers (does not produce PDF)", 5, "SQUARE", 10]}
presetnames = list(presets.keys())

# Each set of marker images printed (and the document collating them) go in a numbered folder designated by this number
pageset = 0

# Instructions for preset input
presettext = "Select preset from list below:\n{}\nCUSTOM - Select the parameters separately\n>> "
presettext = presettext.format("\n".join(["{} - {}".format(i, presets[i][0]) for i in presetnames]))
# Instructions for paper type input
papertypetext = "Paper type\nOne from: {}\n>> ".format(", ".join(list(papertypes.keys())))

while True:
    # Allows case insensitive selection of input type (anything not CSV interpreted as MANUAL)
    inputtype = input("Select tag input type from list below:\n"
                      "MANUAL - Input the tag numbers, sizes, etc by hand\n"
                      "CSV - Input a path to a csv, containing tag names, tag numbers and tag sizes\n>> ").upper()
    
    if inputtype == "CSV":
        # Pixels per mm... kept as 5 for simplicity here
        mmscale = 5
        # Paper type input (case insensitive)
        papertype = input(papertypetext).upper()
        # Obtains the dimensions of the page according to the input format
        dims = papertypes[papertype]
        # The width and height of the page in pixels
        w = dims[0] * mmscale
        h = dims[1] * mmscale
        csvpath = input("Input csv path\n>> ")
        # Takes in all the data from the csv to data
        csvfile = os.open(csvpath, os.O_RDONLY)
        data = ""
        buffer = "x"
        # When nothing is returned in the buffer, file has been read
        while len(buffer) > 0:
            buffer = str(os.read(csvfile, 4096))[2:-1] # Slice strips out leading b' and trailing '
            data += buffer # Appends read data to total data
        # The rows of data, each split into columns
        rows = [row.split(",") for row in data.split("\\n")]
        # Generates the font and pdf (not required for squares format)
        if papertype != "SQUARE":
            textfont = pygame.font.Font(fontpath, 15 * mmscale)
            pdf = FPDF(orientation="L", format=papertype)
        # Increments set counter until it finds an unused set, then makes said folder
        while os.path.exists("Set{:03d}".format(pageset)):
            pageset += 1
        # Path for the folder in which the printed pngs and pdf are saved
        setpath = "Set{:03d}".format(pageset)
        print("Tags will be saved as {}".format(setpath))
        os.makedirs(setpath, exist_ok=True)
        
        for i in range(len(rows)):
            row = rows[i]
            print("Row {} read: {}".format(i + 1, ", ".join(row)))
            try:
                tagname, tagno, tagedge = row
                
                tagno = int(tagno)
                # Tagedge is the edge length of the tag in pixels (includes white border)
                tagedge = int(tagedge) * mmscale * 10
                if papertype == "SQUARE":
                    w = tagedge
                    h = tagedge
                # Page on which the tag will be drawn
                page = pygame.Surface((w, h))
                # Generates the correct tag, scaled to the right size
                tag = pygame.transform.scale(pygame.image.load_extended(loadtagpath + ("{:05d}.png".format(int(tagno)))),
                                             (tagedge, tagedge))
    
                # The corners of the tags, including the white border, on the page (ensures central tag)
                lft = int((w - tagedge) / 2)
                top = int((h - tagedge) / 2)
                rgt = int((w + tagedge) / 2)
                btm = int((h + tagedge) / 2)
    
                # Prints tag pages to png files
                page.fill((255, 255, 255))  # White background
                page.blit(tag, (lft, top))  # The central tag
                # Draws left and right lines around tag's white border
                if w != tagedge:
                    pygame.draw.line(page, 0, (lft, top), (lft, btm))
                    pygame.draw.line(page, 0, (rgt, top), (rgt, btm))
                # And the top and bottom ones
                if h != tagedge:
                    pygame.draw.line(page, 0, (lft, top), (rgt, top))
                    pygame.draw.line(page, 0, (lft, btm), (rgt, btm))
                # Renders and inserts a number if possible
                if papertype != "SQUARE":
                    number = textfont.render("- {} -".format(tagno), 0, (0, 0, 0))
                    page.blit(number, ((w - number.get_width()) / 2, btm))
                # Saves the page as a png
                savetagpath = str(Path(setpath) / ("{}(Tag{}).png".format(i, tagno)))
                pygame.image.save(page, savetagpath)
                print("{} - Saved Tag {}".format(i, tagno))
                # Adds the page to the pdf (except for squares)
                if papertype != "SQUARE":
                    pdf.add_page()  # Adds page
                    pdf.image(savetagpath, 0, 0, dims[0], dims[1])  # Prints image on it
            except:
                print("Row {} skipped".format(i + 1))
        if papertype != "SQUARE":
            pdf.output(str(Path(setpath) / "Tags.pdf"), "F")
            print("Saved pdf\n")
    else:
        while True:
            # Shows the list of presets for selection and takes a choice (case insensitive) for input
            preset = input(presettext).upper()
            
            # Anything not in the list is interpreted as "CUSTOM"
            if preset not in list(presets.keys()):
                # Takes custom values for those in each value of presets above
                mmscale = int(input("Scale (Pixels per mm)\n>> "))  # Higher number basically means higher resolution
                # Paper type input (case insensitive)
                papertype = input(papertypetext).upper()
                dims = papertypes[papertype]
                # The width and height of the page in pixels
                w = dims[0] * mmscale
                h = dims[1] * mmscale
                # Tagedge is the edge length of the tag in pixels (includes white border)
                tagedge = int(float(input("Side length of Tag, in cm\n>> ")) * mmscale * 10)
                if papertype == "SQUARE":
                    # The square format takes the marker to the edge of the image
                    w = tagedge
                    h = tagedge
            else:
                # All values in preset calculated from template in presets
                preset = presets[preset]
                mmscale = preset[1]
                papertype = preset[2]
                dims = papertypes[papertype]
                w = dims[0] * mmscale
                h = dims[1] * mmscale
                tagedge = int(preset[3] * mmscale * 10)
            
            # The square format has no marker number, so needs no font to be loaded
            if papertype != "SQUARE":
                # Loads up the font for the marker number
                textfont = pygame.font.Font(fontpath, 15 * mmscale)
            
            # The pygame Surface for the page to be printed
            page = pygame.Surface((w, h))
            
            # Enter the main loop for tag choices
            while True:
                # Takes comma-separated string of tags or ranges of tags
                taginput = input("Input Tag Numbers\n"
                                 "Comma-separated single numbers or inclusive ranges of form a-b\n"
                                 "Press enter without typing anything to return to the menu\n>> ")
                # Exits to menu if no tags chosen
                if taginput == "":
                    break
                # breaks aforementioned string up into a list
                tagnos = [i for i in taginput.split(",")]
                
                # Creates a pdf to add the tag pages to (unless square tags printed)
                if papertype != "SQUARE":
                    pdf = FPDF(orientation="L", format=papertype)
    
                # The corners of the tags, including the white border, on the page (ensures central tag)
                lft = int((w - tagedge) / 2)
                top = int((h - tagedge) / 2)
                rgt = int((w + tagedge) / 2)
                btm = int((h + tagedge) / 2)
    
                # Increments set counter until it finds an unused set, then makes said folder
                while os.path.exists("Set{:03d}".format(pageset)):
                    pageset += 1
                # Path for the folder in which the printed pngs and pdf are saved
                setpath = "Set{:03d}".format(pageset)
                print("Tags will be saved as {}".format(setpath))
                os.makedirs(setpath, exist_ok=True)
        
                # indicator of position in list of strings representing tag numbers or ranges
                # a simpler for loop is not used to allow coping with ranges
                i = 0
                while i < len(tagnos):
                    # gets a string representing a single tag or range
                    tagno = tagnos[i]
                    if "-" in tagno:
                        # If it's a range, sorts it so it's just numbers
                        # Gets the beginning and end points (inclusive)
                        fromno, tono = tagno.split("-")
                        # Makes a list of tag numbers
                        nos = [j for j in range(int(fromno), int(tono) + 1)]
                        # Shoves them into the list of tag numbers in place of the representative string
                        nos.reverse() # Bakwards, so they end up forwards
                        tagnos.remove(tagno)
                        for no in nos:
                            tagnos.insert(i, str(no)) # Put in as strings for consistency
                        # Doesn't increment i, so the first of the range is printed in the next pass of the loop
                    else:
                        # Generates the correct tag, scaled to the right size
                        tag = pygame.transform.scale(pygame.image.load_extended(loadtagpath +
                                                                                ("{:05d}.png".format(int(tagno)))),
                                                     (tagedge, tagedge))
                        # Prints tag pages to png files
                        page.fill((255, 255, 255))  # White background
                        page.blit(tag, (lft, top))  # The central tag
                        # Draws left and right lines around tag's white border
                        if w != tagedge:
                            pygame.draw.line(page, 0, (lft, top), (lft, btm))
                            pygame.draw.line(page, 0, (rgt, top), (rgt, btm))
                        # And the top and bottom ones
                        if h != tagedge:
                            pygame.draw.line(page, 0, (lft, top), (rgt, top))
                            pygame.draw.line(page, 0, (lft, btm), (rgt, btm))
                        # Renders and inserts a number if possible
                        if papertype != "SQUARE":
                            number = textfont.render("- {} -".format(tagnos[i]), 0, (0, 0, 0))
                            page.blit(number, ((w - number.get_width()) / 2, btm))
                        # Saves the page as a png
                        savetagpath = str(Path(setpath) / ("{}(Tag{}).png".format(i, tagnos[i])))
                        pygame.image.save(page, savetagpath)
                        print("{} - Saved Tag {}".format(i, tagnos[i]))
                        # Adds the page to the pdf (except for squares)
                        if papertype != "SQUARE":
                            pdf.add_page()  # Adds page
                            pdf.image(savetagpath, 0, 0, dims[0], dims[1])  # Prints image on it
                        i += 1
                # And saves the pdf (if one has been created)
                if papertype != "SQUARE":
                    pdf.output(str(Path(setpath) / "Tags.pdf"), "F")
                    print("Saved pdf\n")
                pageset += 1
