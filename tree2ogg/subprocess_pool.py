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

import subprocess
import multiprocessing
import signal
import logging

class SubprocessPool:
    def __init__(self, max_jobs):
        self.max_jobs = max_jobs
        if self.max_jobs <= 0:
            try:
                self.max_jobs = multiprocessing.cpu_count()
            except NotImplementedError:
                self.max_jobs = 1

        self.jobs = set()
        signal.signal(signal.SIGCHLD, self._sigchld)

    def _sigchld(self, signum, frame):
        logging.debug("SIGCHLD")
        done_jobs = set()
        for p in self.jobs:
            if p.poll() != None:
                done_jobs.add(p)

        self.jobs.difference_update(done_jobs)

    def popen(self, *args, **kwrds):
        while len(self.jobs) >= self.max_jobs:
            # If we have jobs than we allow, we wait for a signal until
            # a job finishes.
            signal.pause()
        self.jobs.add(subprocess.Popen(*args, **kwrds))

    def wait(self):
        """Wait for all the jobs to terminate"""
        while len(self.jobs) > 0:
            signal.pause()
