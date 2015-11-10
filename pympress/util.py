#       util.py
#
#       Copyright 2009, 2010 Thomas Jost <thomas.jost@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

"""
:mod:`pympress.util` -- various utility functions
-------------------------------------------------
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Poppler
import pkg_resources
import configparser
import os, os.path, sys

def load_icons():
    """
    Load pympress icons from the pixmaps directory (usually
    :file:`/usr/share/pixmaps` or something similar).

    :return: loaded icons
    :rtype: list of :class:`GdkPixbuf.Pixbuf`
    """

    req = pkg_resources.Requirement.parse("pympress")
    icon_names = pkg_resources.resource_listdir(req, "share/pixmaps")
    icons = []
    for icon_name in icon_names:
        if os.path.splitext(icon_name)[1].lower() != ".png": continue
        icon_fn = pkg_resources.resource_filename(req, "share/pixmaps/" + icon_name)
        try:
            icon_pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_fn)
            icons.append(icon_pixbuf)
        except Exception as e:
            print(e)

    return icons


def poppler_links_available():
    """Check if hyperlinks are supported in python-Poppler.

    :return: ``True`` if python-poppler is recent enough to support hyperlinks,
       ``False`` otherwise
    :rtype: boolean
    """

    try:
        type(Poppler.ActionGotoDest)
    except AttributeError:
        return False
    else:
        return True

def path_to_config():
    if os.name == 'posix':
        conf_dir=os.path.expanduser("~/.config")
        conf_file_nodir=os.path.expanduser("~/.pympress")
        conf_file_indir=os.path.expanduser("~/.config/pympress")

        if os.path.isfile(conf_file_indir):
            return conf_file_indir
        elif os.path.isfile(conf_file_nodir):
            return conf_file_nodir

        elif os.path.isdir(conf_dir):
            return conf_file_indir
        else:
            return conf_file_nodir
    else:
        return os.path.expandvars("%APPDATA%/pympress")

def load_config():
    config = configparser.ConfigParser()
    config.add_section('presentation')
    config.add_section('controller')
    config.add_section('cache')

    config.read(path_to_config())

    return config

def save_config(config):
    with open(path_to_config(), 'w') as configfile:
        config.write(configfile)

##
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 4
# fill-column: 80
# end:
