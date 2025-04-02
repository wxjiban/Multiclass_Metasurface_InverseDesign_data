import os
import pandas as pd
import shutil
import cv2
from matplotlib.image import imread

# 输入路径
original_csv = 'Dataset/labels.csv'  # 前面生成的标签 CSV（包含 filename + 所有值）
original_img_dir = 'Dataset/images/'

# 输出路径
out_img_dir = 'Dataset_gray/images/'
out_all_csv = 'Dataset_gray/labels_all.csv'
out_phys_csv = 'Dataset_gray/labels_phys.csv'
out_except_phys_csv = 'Dataset_gray/labels_except_phys.csv'

# 创建输出文件夹
os.makedirs(out_img_dir, exist_ok=True)

# 读取原始 CSV
df = pd.read_csv(original_csv)

# 分列
df_all = df.copy()
df_phys = df.iloc[:, -3:].copy()
df_except_phys = df.iloc[:, 1:-3].copy()

# 保存 CSVs
df_all.to_csv(out_all_csv, index=False)
df_phys.to_csv(out_phys_csv, index=False)
df_except_phys.to_csv(out_except_phys_csv, index=False)

# 转换图像为灰度图
for i, row in df.iterrows():
    filename = row['filename']
    src_path = os.path.join(original_img_dir, filename)
    dst_path = os.path.join(out_img_dir, filename)

    if not os.path.exists(src_path) or filename == "MISSING.png":
        print(f"⚠️ 跳过缺失图片：{filename}")
        continue

    # 使用 matplotlib 读图再转灰度（避免透明通道）
    img = imread(src_path)
    img = (img[:, :, :3] * 255).astype('uint8')  # 确保是 RGB
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(dst_path, gray)

print("✅ 新数据集构建完成！")
print(f"📂 灰度图目录：{out_img_dir}")
print(f"📄 全部标签：{out_all_csv}")
print(f"📄 光谱部分：{out_except_phys_csv}")
print(f"📄 物理量部分：{out_phys_csv}")
