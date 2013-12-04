import os
import sys
import fnmatch
import subprocess
import multiprocessing
import signal
import argparse



def main(args):
    pool = SubprocessPool(args.jobs)

    for root, dirs, files in os.walk(args.src_dir):
        flac_files = fnmatch.filter(files, "*.flac")

        if not flac_files:
            continue

        rel_dir = os.path.relpath(root, args.src_dir)
        target_dir = os.path.join(args.dst_dir, rel_dir)

        try:
            os.makedirs(target_dir)
        except OSError, e:
            if e.errno != 17: # File exists
                raise

        for name in flac_files:
            name_wo_ext = os.path.splitext(name)[0]
            target_name = name_wo_ext + '.ogg'
        
            target_file = os.path.join(args.dst_dir, rel_dir, target_name)
            src_file = os.path.join(root, name)
            ogg_enc(pool, src_file, target_file)

        pool.wait()


def ogg_enc(pool, src_file, dst_file):
    args = ['oggenc', '--quality', '5', '--output', dst_file, src_file]

    pool.popen(args)


class SubprocessPool:
    def __init__(self, max_jobs):
        self.max_jobs = max_jobs
        self.jobs = set()
        signal.signal(signal.SIGCHLD, self._sigchld)

    def _sigchld(self, signum, frame):
        done_jobs = set()
        for p in self.jobs:
            if p.poll() != None:
                done_jobs.add(p)

        self.jobs.difference_update(done_jobs)

    def popen(self, *args, **kwrds):
        while len(self.jobs) >= self.max_jobs:
            signal.pause()
        self.jobs.add(subprocess.Popen(*args, **kwrds))

    def wait(self):
        """Wait for all the jobs to terminate"""
        while len(self.jobs) > 0:
            signal.pause()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("src_dir", help="source directory to transcode")
    parser.add_argument("dst_dir", help="destination directory")

    parser.add_argument("-j", "--jobs", help="number of simultaneous encoding"
                        "process to spawn", default=0, type=int)
    args = parser.parse_args()

    if args.jobs <= 0:
        try:
            args.jobs = multiprocessing.cpu_count()
        except NotImplementedError:
            args.jobs = 1


    main(args)
