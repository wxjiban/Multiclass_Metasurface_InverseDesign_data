import pandas as pd
import json
import os
import random
import shutil

# 输入路径
labels_except_phys_path = 'Dataset_gray/labels_except_phys.csv'
labels_phys_path = 'Dataset_gray/labels_phys.csv'
image_dir = 'Dataset_gray/images/'

# 读取 CSV 数据（光谱数据和物理量）
df_spectra = pd.read_csv(labels_except_phys_path)
df_phys = pd.read_csv(labels_phys_path)

# 输出 JSON Lines 文件路径
output_train_jsonl_path = 'train_vlm_8_data.jsonl'
output_eval_jsonl_path = 'eval_vlm_8_data.jsonl'

# 用来存储生成的 JSON 数据
train_dataset = []
eval_dataset = []

# 创建目标文件夹（训练集和测试集）
train_image_dir = 'Dataset_gray/train_images/'
eval_image_dir = 'Dataset_gray/eval_images/'
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(eval_image_dir, exist_ok=True)

# 获取总样本数
total_samples = len(df_spectra)

# 随机选择 16000 个训练集索引
train_indices = random.sample(range(total_samples), 16000)

# 遍历每一行数据
for i, (spectra_row, phys_row) in enumerate(zip(df_spectra.iterrows(), df_phys.iterrows())):
    # 光谱数据（前 800 列，按每 100 个采样一次）
    values = spectra_row[1].iloc[:800].values[::100]

    # 获取物理量（Plasma, Thickness, Index），处理 NaN 情况
    plasma = phys_row[1].get('Plasma', 0)  # 如果没有 Plasma 列，默认为 0
    thickness = phys_row[1].get('Thickness', 0)
    index = phys_row[1].get('Index', 0)

    # 生成 "assistant" 的 content（光谱数据）
    assistant_content = " ".join(map(str, values))

    # 根据 Plasma 和 Thickness 生成 "user" 的 content
    if plasma != 0:
        user_content = f"3.2*3.2um2的MIM结构，金属层Plasma= {plasma} 介质层Thickness= {thickness * 100}nm 请输出4-12um波长的结果"
    else:
        user_content = f"7.5*7.5um2的DM结构，介质层Index= {index} 介质层Thickness= {thickness} 请输出4-12um波长的结果"

    # 获取图片路径（假设图片名为 00001.png, 00002.png 等）
    img_filename = f"{i + 1:05d}.png"
    # img_path = os.path.join(image_dir, img_filename)
    img_path = img_filename
    # 根据是否在训练集索引中决定将图片移动到哪个文件夹
    if i in train_indices:
        # 将图片复制到训练集文件夹
        # shutil.copy(img_path, os.path.join(train_image_dir, img_filename))
        # image_dir_for_json = os.path.join(train_image_dir, img_filename)

        # 生成训练集的 JSON 数据
        entry = {
            "conversations": [
                {
                    "role": "user",
                    "content": f"{user_content}\n<image>"
                },
                {
                    "role": "assistant",
                    "content": assistant_content  # 光谱数据描述
                }
            ],
            "image": img_filename
        }
        train_dataset.append(entry)

    else:
        # 将图片复制到测试集文件夹
        # shutil.copy(img_path, os.path.join(eval_image_dir, img_filename))
        # image_dir_for_json = os.path.join(eval_image_dir, img_filename)

        # 生成测试集的 JSON 数据
        entry = {
            "conversations": [
                {
                    "role": "user",
                    "content": f"{user_content}\n<image>"
                },
                {
                    "role": "assistant",
                    "content": assistant_content  # 光谱数据描述
                }
            ],
            "image": img_filename
        }
        eval_dataset.append(entry)

# 将训练集数据写入 JSONL 文件
with open(output_train_jsonl_path, 'w', encoding='utf-8') as f:
    for entry in train_dataset:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")  # 每个对象结束后加一个换行符

# 将测试集数据写入 JSONL 文件
with open(output_eval_jsonl_path, 'w', encoding='utf-8') as f:
    for entry in eval_dataset:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")  # 每个对象结束后加一个换行符

print(f"✅ 训练集 JSONL 数据集已生成并保存在 {output_train_jsonl_path}")
print(f"✅ 测试集 JSONL 数据集已生成并保存在 {output_eval_jsonl_path}")
print(f"✅ 训练集图片已移动到 {train_image_dir}")
print(f"✅ 测试集图片已移动到 {eval_image_dir}")
