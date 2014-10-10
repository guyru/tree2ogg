###########################################################################
 #   Copyright (C) 2013-2014 by Guy Rutenberg                              #
 #   http://www.guyrutenberg.com/                                          #
 #                                                                         #
 #   This program is free software; you can redistribute it and/or modify  #
 #   it under the terms of the GNU General Public License as published by  #
 #   the Free Software Foundation; either version 2 of the License, or     #
 #   (at your option) any later version.                                   #
 #                                                                         #
 #   This program is distributed in the hope that it will be useful,       #
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
 #   GNU General Public License for more details.                          #
 #                                                                         #
 #   You should have received a copy of the GNU General Public License     #
 #   along with this program; if not, write to the                         #
 #   Free Software Foundation, Inc.,                                       #
 #   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import argparse
import logging
from tree2ogg import Tree2Ogg, __version__

def run():
    description = "Convert a directory tree of FLAC files to Ogg."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("src", help="source directory/playlist")
    parser.add_argument("dst_dir", help="destination directory")
    parser.add_argument(nargs=argparse.REMAINDER, dest="oggenc_args",
                        help="additional arguments to pass to oggenc")

    parser.add_argument("-j", "--jobs", help=("number of simultaneous encoding"
                        " process to spawn"), default=0, type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--force', action='store_true', default=False,
                        help='force overwrite existing files')
    group.add_argument('--skip', action='store_true', default=False,
                        help='always skip existing files')

    parser.add_argument('-v', '--verbose', help="increase output verbosity",
                        action='count', default=0)
    parser.add_argument('--version', action="version",
                        version="%(prog)s " + __version__)
    args = parser.parse_args()

    logging_level = logging.ERROR - args.verbose * 10
    logging.basicConfig(format="%(message)s", level=logging_level)

    Tree2Ogg(args).run()

run()
