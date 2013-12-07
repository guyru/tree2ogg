============
``tree2ogg``
============
A script that allows recursively transcode directories/playlists of FLAC files
to Ogg.

Installation
=============
To install ``tree2ogg``, use pip::

  pip install tree2ogg

You can also install the latest development version from github::

   pip install git+https://github.com/guyru/tree2ogg.git#egg=tree2ogg

Synopsis
========
::

  usage: tree2ogg [-h] [-j JOBS] [-v] [--version] src dst_dir ...
  
  Convert a directory tree of FLAC files to Ogg.
  
  positional arguments:
    src                   source directory/playlist
    dst_dir               destination directory
    oggenc_args           additional arguments to pass to oggenc
  
  optional arguments:
    -h, --help            show this help message and exit
    -j JOBS, --jobs JOBS  number of simultaneous encoding process to spawn
    -v, --verbose         increase output verbosity
    --version             show program's version number and exit
