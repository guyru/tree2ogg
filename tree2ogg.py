import os
import sys
import fnmatch
import subprocess
import multiprocessing


def main(src_path, dst_path):

    pool = multiprocessing.Pool(processes=6)

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
            print target_name
        
            target_file = os.path.join(dst_path, rel_dir, target_name)
            src_file = os.path.join(root, name)
            pool.apply_async(ogg_enc, [src_file, target_file])

    pool.close()
    pool.join()

def ogg_enc(src_file, dst_file):
    args = ['oggenc', '--quality', '5', '--output', dst_file, src_file]
    subprocess.call(args)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
