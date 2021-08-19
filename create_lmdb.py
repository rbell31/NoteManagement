import argparse
import pickle
import cv2
import os
import lmdb
from path import Path
from icecream import ic


ic.enable()

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=Path, required=True)
    parser.add_argument('--type', type=str)
    args = parser.parse_args()
    return args

def set_database(args):
    # 2GB is enough for IAM dataset
    name = args.data_dir.split('\\')
    name = name[-1]
    ic(name)
    assert not (args.data_dir.parent / 'lmdb'+'_'+name).exists()
    map_size = get_size(args.data_dir)*10
    env = lmdb.open(str(args.data_dir.parent / 'lmdb'+'_'+name), map_size=map_size)
    return env

def png(args, env):
    # go over all png files
    fn_imgs = list((args.data_dir / 'img').walkfiles('*.png'))
    
    # and put the imgs into lmdb as pickled grayscale imgs
    with env.begin(write=True) as txn:
        for i, fn_img in enumerate(fn_imgs):
            print(i, len(fn_imgs))
            img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)
            basename = fn_img.basename()
            txn.put(basename.encode("ascii"), pickle.dumps(img))
    
    env.close()

def file(args, env):
    # go over all png files
    fn_files = list(args.data_dir.walkfiles('*'))
    
    # and put the files into lmdb as pickled json
    with env.begin(write=True) as txn:
        for i, fn_file in enumerate(fn_files):
            print(i, len(fn_files))
            lines = []
            with open(fn_file, 'r') as f:
                for line in f:
                    lines.append(line)
            lines = "".join(lines)
            lines = lines.replace("\n", "")
            lines = {'data': lines}
            basename = fn_file.basename()
            txn.put(basename.encode("ascii"), pickle.dumps(lines))
    
    env.close()


if __name__ == '__main__':
    args = parse()
    env = set_database(args)

    if args.type == 'img':
        png(args, env)
    else:
        file(args, env)


