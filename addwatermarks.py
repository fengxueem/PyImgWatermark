"""
使用示例：

python addwatermarks.py --in-img-dir /home/gohgih/in_data/ --out-img-dir /home/gohgih/data/ --watermark-txt @foo.bar
"""
from multiprocessing.pool import Pool
from tqdm import tqdm
from argparse import ArgumentParser
import argparse
from itertools import repeat
import os
import glob
import random
import cv2 as cv
import numpy as np

# 定义全局变量
COLOR_LIST = [(210,250,250), (238,238,175), (135,206,250), (147,112,219), (169,169,169), (144 ,128 ,112)] # BGR 顺序
ROTATION_LIST = range(-27, 27, 2)
FONT_LIST = [x / 10.0 for x in range(20, 40, 2)]
ALPHA_LIST = [x / 100.0 for x in range(9, 12, 1)]
NUM_THREADS = min(8, max(1, os.cpu_count() - 2))  # 多线程数量

def ispath(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError('No such directory: ' + path)
    else:
        return path


def draw_text_watermark(ori_img, text, fontsize, alpha, color, rotation):
    ori_img_h, ori_img_w, ori_img_c = ori_img.shape
    font_scale = ori_img_w * ori_img_h / (1920 * 1080)
    # 绘制文字水印图片
    watermark_img = np.zeros((int(ori_img_h * 0.5), int(ori_img_w * 0.5), ori_img_c), dtype=np.uint8)
    watermark_img_h, watermark_img_w = watermark_img.shape[:2]
    text_loc = (int(watermark_img_w / 4), int(watermark_img_h / 2))
    cv.putText(watermark_img, text, text_loc, cv.FONT_HERSHEY_SIMPLEX, fontsize * font_scale, color, 3)
    rotate_matrix = cv.getRotationMatrix2D(text_loc, rotation, 1) # 生成旋转矩阵
    watermark_img_rot = cv.warpAffine(watermark_img, rotate_matrix, (watermark_img.shape[1], watermark_img.shape[0]))
    watermark_img_rot_h, watermark_img_rot_w = watermark_img_rot.shape[:2]#获取旋转后水印的高度、宽度
    # 随机截取原图区域
    ori_watermark_roi_h = random.randint(int(watermark_img_rot_h * 0.2), ori_img_h - watermark_img_rot_h)
    ori_watermark_roi_w = random.randint(int(watermark_img_rot_w * 0.2), ori_img_w - watermark_img_rot_w)
    ori_watermark_roi = ori_img[ori_watermark_roi_h : ori_watermark_roi_h + watermark_img_rot_h, ori_watermark_roi_w : ori_watermark_roi_w + watermark_img_rot_w]
    # 添加水印
    ori_watermark_roi = cv.addWeighted(watermark_img_rot, alpha, ori_watermark_roi,1,0) 
    ori_img[ori_watermark_roi_h : ori_watermark_roi_h + watermark_img_h, ori_watermark_roi_w : ori_watermark_roi_w + watermark_img_w] = ori_watermark_roi
    return ori_img


def drawer(args):
    in_img_path, out_img_path, watermark_txt = args
    # 检查输入图像路径合法性
    if not os.path.exists(in_img_path):
        print(f'Warning: {in_img_path} does not exist! Skipping ...')
        return False
    # 读取原图
    img = cv.imread(in_img_path)
    # 随机次数添加水印
    for _ in range(0, random.randint(1,3)):
        img = draw_text_watermark(img, watermark_txt,
                        random.choice(FONT_LIST), random.choice(ALPHA_LIST), random.choice(COLOR_LIST), random.choice(ROTATION_LIST))
    # 保存图像
    cv.imwrite(out_img_path, img)
    return True


def main(args):
    # 获取目录下的所有图片
    r_str = args.in_img_dir + '/**/*.jpg'
    jpg_list = glob.glob(r_str, recursive=True)
    res_lists = []
    # 生成输出水印图片路径
    print(f'Drawing img with bbox on {args.out_img_dir}')
    watermarked_img_list = [jpg.replace(args.in_img_dir, args.out_img_dir) for jpg in jpg_list]
    # 生成输出图片文件夹
    watermarked_img_dir_dic = {os.path.dirname(img) for img in watermarked_img_list}
    for dir in watermarked_img_dir_dic:
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
    # 多线程画图
    with Pool(NUM_THREADS) as pool:
        pbar = tqdm(pool.imap(drawer, zip(jpg_list, watermarked_img_list, repeat(args.watermark_txt))),
                    total=len(jpg_list))
        # wait for all workers to finish the job by adding results to a list
        for res in pbar:
            res_lists.append(res)
    pbar.close()


if __name__ == '__main__':
    parser = ArgumentParser(description="Add watermark to bunchs of images")
    parser.add_argument(
        '--in-img-dir',
        required=True,
        type=ispath, help="Directory containing original images")
    parser.add_argument(
        '--out-img-dir',
        required=True,
        type=ispath, help="Directory to save watermarked images")
    parser.add_argument(
        '--watermark-txt',
        required=True,
        help="String of watermark content")
    args = parser.parse_args()
    main(args)
