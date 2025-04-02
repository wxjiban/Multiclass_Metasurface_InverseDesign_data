import os
import shutil
import pandas as pd
import re

# === 路径配置 ===
csv_path = 'absorptionData_HybridGAN.csv'
img_dir = 'Images/'
output_img_dir = 'Dataset/images/'
output_csv_path = 'Dataset/labels.csv'

# 创建输出目录
os.makedirs(output_img_dir, exist_ok=True)

# 读取 CSV
df = pd.read_csv(csv_path)
new_filenames = []
not_found = []


# 工具函数：只去除括号内的下划线
def replace_in_brackets(s):
    return re.sub(r'\((.*?)\)', lambda m: f"({m.group(1).replace('_', '')})", s)


# 遍历行匹配图片
for i, row in df.iterrows():
    original_name = row[0]
    struct_name = original_name.replace("-Excel.mat", "")

    # 构造图片名候选项
    candidates = [
        f"{struct_name}-colorprops.png",
        f"{replace_in_brackets(struct_name)}-colorprops.png",
    ]

    found = False
    for cand in candidates:
        candidate_path = os.path.join(img_dir, cand)
        if os.path.exists(candidate_path):
            new_name = f"{i + 1:05d}.png"
            shutil.copy(candidate_path, os.path.join(output_img_dir, new_name))
            new_filenames.append(new_name)
            found = True
            break

    if not found:
        print(f"⚠️ 图片未找到：{struct_name}")
        new_filenames.append("MISSING.png")
        not_found.append(struct_name)

# 更新并保存 CSV
df['filename'] = new_filenames
df = df.drop(columns=df.columns[0])
df = df[['filename'] + [col for col in df.columns if col != 'filename']]
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
df.to_csv(output_csv_path, index=False)

print("\n✅ 数据整理完成！")
print(f"✅ 图片路径：{output_img_dir}")
print(f"✅ CSV标签表：{output_csv_path}")
if not_found:
    print(f"⚠️ 共 {len(not_found)} 张图片未找到，请检查：")
    for name in not_found:
        print(f"  - {name}")
