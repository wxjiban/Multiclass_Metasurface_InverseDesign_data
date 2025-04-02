import matplotlib.image as mpimg
import numpy as np
import os


def analyze_structure_image(img_path, pmax=4.0, tmax=10.0, emax=5.0, threshold=0.2):
    img = mpimg.imread(img_path)

    if img.max() > 1.0:
        img = img / 255.0  # 归一化

    im_size = img.shape[0]
    psum = pnum = 0.0
    tsum = tnum = 0.0
    esum = enum = 0.0

    for row in range(im_size):
        for col in range(im_size):
            r = img[row][col][0]
            g = img[row][col][1]
            b = img[row][col][2]
            if r > threshold or g > threshold:
                if r > g:
                    psum += r
                    pnum += 1
                else:
                    esum += g
                    enum += 1
            else:
                tsum += b
                tnum += 1

    pAvg = psum / pnum if pnum > 0 else 0.0
    eAvg = esum / enum if enum > 0 else 0.0
    tAvg = tsum / tnum if tnum > 0 else 0.0

    pfake = pAvg * pmax
    efake = eAvg * emax
    tfake = tAvg * tmax

    structure_type = "MIM (plasmonic)" if pnum > enum else "DM (dielectric)"

    print(f"Image: {os.path.basename(img_path)}")
    print(f"  Plasma Index (Fake):     {pfake:.3f}")
    print(f"  Dielectric Index (Fake): {efake:.3f}")
    print(f"  Thickness (Fake):        {tfake:.3f}")
    print(f"  Dominant Structure Type: {structure_type}")
    print("")

    return pfake, efake, tfake


# 用你的图片路径替换下方的路径
image_paths = [
    "sweep_vl900w800alpha80theta80-Al-colorprops.png",
    "sweep_vl900w800alpha80theta80-colorprops.png",
    "sweep_bowtiel1new1170l2new1404theta10-Ge-colorprops.png",
    "sweep_ellipsel2500w1500rot30-Al-colorprops.png",
    "sweep_l800w800-(100nmDielec)-colorprops.png"
]

for path in image_paths:
    analyze_structure_image(path)
    print()
