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

"""
usage: tree2ogg [-h] [-j JOBS] [-v] [--version] src dst_dir

Convert a directory tree of FLAC files to Ogg.

positional arguments:
  src                   source directory/playlist
  dst_dir               destination directory

optional arguments:
  -h, --help            show this help message and exit
  -j JOBS, --jobs JOBS  number of simultaneous encoding process to spawn
  -v, --verbose         increase output verbosity
  --version             show program's version number and exit
"""

import os
import fnmatch
import logging
import urllib
from subprocess_pool import SubprocessPool

__version__ = '0.2.0'

class Tree2Ogg:
    def __init__(self, args):
        for attr in ['src', 'dst_dir', 'skip', 'force']:
            setattr(self, attr, getattr(args, attr))

        self._pool = SubprocessPool(args.jobs)

        self._oggenc_args = ['oggenc', '--quality', '5']
        if logging.getLogger().level > logging.INFO:
            self._oggenc_args.append('--quiet')

        self._oggenc_args += args.oggenc_args

    def run(self):

        generator = self._generator_file
        if os.path.isdir(self.src):
            generator = self._generator_dir

        for src_file in generator():
            self._create_directories(src_file)
            self._encode_file(src_file)

        self._pool.wait()

    def _create_directories(self, filepath):
        """Create the target directories needed for converting a given file."""
        dirname = os.path.dirname(filepath)
        relative_dirname = os.path.relpath(dirname, self.src)
        relative_dirname = os.path.normpath('/' + relative_dirname)[1:]
        dst_dirname = os.path.join(self.dst_dir, relative_dirname)

        if not os.path.isdir(dst_dirname):
            logging.debug("Creating directory: %s", dst_dirname)
            os.makedirs(dst_dirname)

    def _encode_file(self, filepath):
        """Encode a flac file to ogg."""
        dirname, filename = os.path.split(filepath)
        name_wo_ext = os.path.splitext(filename)[0]
        target_name = name_wo_ext + '.ogg'

        rel_dir = os.path.relpath(dirname, self.src)
        # nice trick to prevent directory traversal
        rel_dir = os.path.normpath('/' + rel_dir).lstrip('/')
        target_file = os.path.join(self.dst_dir, rel_dir, target_name)

        if os.path.exists(target_file) and self.skip == True:
            logging.warning('Skipping file: %s', filepath)
            return False
        elif os.path.exists(target_file) and self.force == False:
            # We should check the timestamp of the target and compare it with
            # the source.
            if os.path.getmtime(target_file) > os.path.getmtime(filepath):
                # target is probably up-to-date.
                logging.warning('Skipping file: %s', filepath)
                return False


        args = self._oggenc_args + ['--output', target_file, filepath]

        self._pool.popen(args)
        return True

    def _generator_dir(self):
        for root, _, files in os.walk(self.src):
            flac_files = fnmatch.filter(files, "*.flac")

            if not flac_files:
                continue

            for name in flac_files:
                src_file = os.path.join(root, name)
                yield src_file

    def _generator_file(self):
        first_line = True
        m3u_playlist = False
        for line in open(self.src, 'rb'):
            line = line.rstrip('\n')
            if first_line:
                m3u_playlist = line.startswith('#EXTM3U')
                first_line = False
            if m3u_playlist:
                if line.startswith('#'):
                    continue
                if line.startswith('file://'):
                    line = line[len('file://'):]
                line = urllib.unquote(line)
            if not line.startswith('/'):
                # path is relative
                line = os.path.join(os.path.dirname(self.src), line)
            yield line
