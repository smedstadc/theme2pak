"""
Converts a pidgin smilies theme to a phpbb version 3.0.X pak file.
Expects to be placed in a directory with the theme file and its images

theme file must be named "theme"
outputs "converted.pak" and "log.txt"

upload converted.pak and matching images to your <phpbb root>/images/smilies/
then install the smiley through the forum softwares admin panel
keep in mind that phpbb3 places a hard limit of 1000 on installed smilies
you can mod this 

Only preserves the first emote code as phpbb doesn't support multiple per image.
In the future I'll implement an interactive mode that asks which to keep.
"""


# TODO:
# 1. Clean up for command line use.
# 2. Interactive mode.
#
# Reminders:
# pak line format is 
# 'thumbsup3d.gif', '15', '15', '1', 'Thumbs Up', ':yes:',
# filename, width, height, visible, name, emote code
# PIL.Image.size is a (width, height) tuple

__author__ = "Corey Smedstad"

from PIL import Image
import os
import sys

# controls whether a smiley is visible on the posting page 1=yes, 0=no
# you most likely don't want this to be 1 for the bulk of them
visible = '0'

def quoted(s):
    """
    Returns a quoted, comma delimited string.
    For example "s" becomes "'s', "

    s: string to surround with quotes.
    """
    leftquote = '\''
    rightquote = '\', '
    return leftquote + s + rightquote

cwd = os.path.dirname(__file__)
filename = os.path.join(cwd, 'theme')
themefile = open(filename, 'r')
count = 0
skipped = 0

try:
    outputfile = open(os.path.join(cwd, 'converted.pak'), 'w')
except IOError:
    print "Error opening output file. Quitting."
    sys.exit()

try:
    logfile = open(os.path.join(cwd, 'log.txt'), 'w')
except IOError:
    print "Error opening log file. Quitting."
    sys.exit()

logfile.write("Script started...\n")
logfile.write("-" * 79 + "\n")

for line in themefile:
    if line[0] == '!':
        s = line.split()
        emotefile = s[1]
        emotecode = s[2]
        try:
            emoteimage = Image.open(os.path.join(cwd, emotefile))
            emotewidth = emoteimage.size[0]
            emoteheight = emoteimage.size[1]
            outputfile.write(quoted(emotefile))
            outputfile.write(quoted(str(emotewidth)))
            outputfile.write(quoted(str(emoteheight)))
            outputfile.write(quoted(str(visible)))
            outputfile.write(quoted(emotefile.split('.')[0]))
            outputfile.write(quoted(emotecode))
            outputfile.write('\n')
            count += 1
        except IOError:
            print "Skipping " + str(emotecode) + " for missing file."
            logfile.write("Could not find file: " + emotefile + " for " + emotecode + "\n")
            skipped += 1

logfile.write("-" * 79 + "\n")
logfile.write("Added " + str(count) + " smilies to converted.pak\n")
logfile.write("Skipped " + str(skipped) + " missing files.\n")
logfile.write("Script finished...\n")
outputfile.close()
logfile.close()
