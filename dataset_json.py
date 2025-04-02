import pandas as pd
import json
import os

# 输入路径
labels_except_phys_path = 'Dataset_gray/labels_except_phys.csv'
labels_phys_path = 'Dataset_gray/labels_phys.csv'
image_dir = 'Dataset_gray/images/'

# 读取 CSV 数据（光谱数据和物理量）
df_spectra = pd.read_csv(labels_except_phys_path)
df_phys = pd.read_csv(labels_phys_path)

# 输出 JSON Lines 文件路径
output_jsonl_path = 'output_dataset_with_corrected_format.jsonl'

# 用来存储生成的 JSON 数据
dataset = []

# 遍历每一行数据
for i, (spectra_row, phys_row) in enumerate(zip(df_spectra.iterrows(), df_phys.iterrows())):
    # 光谱数据（前 800 列）
    values = spectra_row[1].iloc[:800].values[::100]

    # 获取物理量（Plasma, Thickness, Index）
    plasma = phys_row[1]['Plasma']
    thickness = phys_row[1]['Thickness']
    index = phys_row[1]['Index']

    # 生成 "assistant" 的 content（光谱数据）
    assistant_content = " ".join(map(str, values))

    # 根据 Plasma 和 Thickness 生成 "user" 的 content
    if plasma != 0:
        user_content = f"3.2*3.2um2的MIM结构，金属层Plasma= {plasma} 介质层Thickness= {thickness * 100}nm 请输出4-12um波长的结果"
    else:
        user_content = f"7.5*7.5um2的DM结构，介质层Index= {index} 介质层Thickness= {thickness}"

    # 获取图片路径（假设图片名为 00001.png, 00002.png 等）
    img_filename = f"{i + 1:05d}.png"
    # img_path = os.path.join(image_dir, img_filename)
    img_path = img_filename
    # 生成 JSON 数据
    entry = {
        "conversations": [
            {
                "role": "user",
                "content": f"{user_content}\n<image>"  # 图片路径标签
                  # 图片路径
            },
            {
                "role": "assistant",
                "content": assistant_content  # 光谱数据描述
            }
        ],
        "image": img_path
    }
    # 将当前数据写入 JSONL 文件（每行写一个 JSON 对象）
    with open(output_jsonl_path, 'a', encoding='utf-8') as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")  # 每个对象结束后加一个换行符

print(f"✅ JSONL 数据集已生成并保存在 {output_jsonl_path}")
