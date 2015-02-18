"""
Converts a pidgin smilies theme to a phpbb version 3.0.X pak file.
Expects to be placed in a directory with the theme file and its images

theme file must be named "theme"
outputs "converted.pak" and "log.txt"

upload converted.pak and matching images to your <phpbb root>/images/smilies/
then install the smiley through the forum admin control panel keep in mind
that phpbb3 places a hard limit of 1000 on installed smilies by default you
can mod this if you need to.

Only preserves the first emote code as phpbb doesn't support multiple per image.
Maybe someday I'll implement an interactive mode that asks which to keep.
"""


# TODO:
# 1. Interactive mode ???
#
# Reminders:
# pak line format is 
# filename, width, height, visible, name, emote code
# 'thumbsup3d.gif', '15', '15', '0', 'Thumbs Up', ':yes:',
# the visible attribute controls whether a smiley is visible on the posting page 1=yes, 0=no
# you most likely don't want this to be 1 for the bulk of them because it will make post forms
# scroll too much vertically
# PIL.Image.size is a (width, height) tuple

from __future__ import print_function
from PIL import Image
import os
import argh
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('theme2pak')


def convert_theme(input_path, output_path, verbose=False):
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("Converting {} -> {}".format(input_path, output_path))
    logger.debug("in convert_theme with input_path={}, output_path={}".format(repr(input_path), repr(output_path)))
    input_path = os.path.join(os.getcwd(), input_path)
    output_path = os.path.join(os.getcwd(), output_path)
    base_path = os.path.split(input_path)[:-1][0]

    try:
        with open(input_path, 'r') as theme_file, open(output_path, 'w') as output_file:
            for line in theme_file:
                logger.debug("Read: {}".format(repr(line)))
                if line:
                    pak_line = get_pak_line_from_theme_line(line, base_path)
                    if pak_line:
                        logger.debug("Output: {}".format(repr(pak_line)))
                        output_file.write(pak_line)
                        print('.', end='')
            print('\nDone!\n')
    except Exception as e:
        logger.error(e)


def get_pak_line_from_theme_line(line, base_path):
    logger.debug("in get_pak_line_from_theme_line with line={}, base_path={}".format(repr(line), repr(base_path)))

    if line is not None and line[0] == '!':
        emote_filename = line.split()[1]
        emote_bbcode = line.split()[2]
        emote_size = get_emote_image_dimensions(os.path.join(base_path, emote_filename))

        if emote_size:
            emote_width, emote_height = get_emote_image_dimensions(os.path.join(base_path, emote_filename))
            return "'{0}', '{1}', '{2}', '0', '{3}', '{4}',\n".format(emote_filename, emote_width,
                                                                      emote_height, emote_filename.split('.')[0],
                                                                      emote_bbcode)
        else:
            return None


def get_emote_image_dimensions(path):
    logger.debug("in get_emote_image_dimensions with path={}".format(repr(path)))
    try:
        with Image.open(path) as emote_image:
            return emote_image.size
    except IOError as e:
        logger.error("Problem reading image {}".format(repr(path)))
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    argh.dispatch_command(convert_theme)