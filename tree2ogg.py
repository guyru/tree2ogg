import os
import sys
import fnmatch
import subprocess
import multiprocessing
import signal



def main(src_path, dst_path):
    pool = SubprocessPool(6)

    for root, dirs, files in os.walk(src_path):
        flac_files = fnmatch.filter(files, "*.flac")

        if not flac_files:
            continue

        rel_dir = os.path.relpath(root, src_path)
        target_dir = os.path.join(dst_path, rel_dir)

        try:
            os.makedirs(target_dir)
        except OSError, e:
            if e.errno != 17: # File exists
                raise

        for name in flac_files:
            name_wo_ext = os.path.splitext(name)[0]
            target_name = name_wo_ext + '.ogg'
        
            target_file = os.path.join(dst_path, rel_dir, target_name)
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
    main(sys.argv[1], sys.argv[2])
