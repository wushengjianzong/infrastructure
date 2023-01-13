#!python3

import sys
import argparse
import subprocess
from typing import List


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src', dest='src', type=str, required=True)
    parser.add_argument('-d', '--dst', dest='dst', type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    src_image: str = args.src
    dst_image: str = args.dst

    src_split: List[str] = src_image.split('/')
    if len(src_split) == 1:
        src_split = ['docker.io', 'library'] + src_split
    elif '.' not in src_split[0]:
        src_split = ['docker.io'] + src_split
    # print('---src split:', src_split)

    dst_split: List[str] = dst_image.split('/')
    if len(dst_split) > 1:
        dst_split.append(src_split[-1])
    else:
        dst_split.extend(src_split[1:])
    # print('---dst split:', dst_split)

    src_image = '/'.join(src_split)
    dst_image = '/'.join(dst_split)
    # print(src_image, dst_image)

    # subprocess.call(f'docker pull {src_image}', shell=True)
    subprocess.call(f"docker tag {src_image} {dst_image}", shell=True)
    subprocess.call(f"docker push {dst_image}", shell=True)
    subprocess.call(f"docker rmi {dst_image}", shell=True)

