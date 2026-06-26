#!/usr/bin/env python3
"""
Replace SVG placeholder badges with real images in rzzx.html.
简单策略：找到每个cert-badge-row块，替换SVG img为真实图片路径。
"""
import re, os

HTML = "/home/tangguo/yingjian-website/rzzx.html"
IMG_BASE = "/home/tangguo/yingjian-website/images/rzzx"

FOLDER_TO_CAT = {
    "质量认证":      "ylqx",
    "环境及健康管理": "sp",
    "森林":          "ny",
    "汽车供应链":     "qc",
    "轨道交通":       "qt",
    "医疗服务":       "dz",
    "航天":          "jc",
    "信息安全":       "xxaq",
    "供应链安全":     "fz",
    "二化融合":       "aqeh",
    "知识产权":       "zscq",
}

# 加载图片
folder_images = {}
for folder in os.listdir(IMG_BASE):
    folder_path = os.path.join(IMG_BASE, folder)
    if os.path.isdir(folder_path):
        folder_images[folder] = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ])

cat_info = {}
for folder, cat in FOLDER_TO_CAT.items():
    if folder in folder_images and folder_images[folder]:
        cat_info[cat] = (folder, folder_images[folder])

with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()

# 找到所有data-category的位置（第一次出现）
cat_positions = {}
for cat in cat_info:
    pos = content.find(f'data-category="{cat}"')
    if pos != -1:
        cat_positions[cat] = pos

# 按位置从高到低排序
sorted_cats = sorted(cat_positions.keys(), key=lambda c: cat_positions[c], reverse=True)
print("处理顺序（从后往前）:")
for cat in sorted_cats:
    folder, images = cat_info[cat]
    print(f"  {folder} ({cat}): pos={cat_positions[cat]}, {len(images)}张图片")

svg_pat = re.compile(
    r'<img src="data:image/svg\+xml[^"]*"([^>]*)alt="([^"]*)"([^>]*)style="([^"]*)"'
)

total_rep = 0
for cat in sorted_cats:
    folder, images = cat_info[cat]
    cat_marker = f'data-category="{cat}"'
    cat_pos = cat_positions[cat]

    # 找row div开始：向前找到 <div class="cert-badge-row
    div_start = content.rfind('<div', 0, cat_pos + 10)

    # 找下一个cat的位置（在cat_pos之后）
    next_cat_pos = len(content)
    for next_cat, next_pos in cat_positions.items():
        if next_cat != cat and next_pos > cat_pos and next_pos < next_cat_pos:
            next_cat_pos = next_pos

    # row块：从div_start到next_cat_pos
    # row结束 = 块中最后一个 </div>
    row_chunk = content[div_start:next_cat_pos]
    last_close = row_chunk.rfind('</div>')
    row_end = div_start + last_close + len('</div>')
    row_text = content[div_start:row_end]
    
    svg_count = row_text.count('data:image/svg')
    card_count = row_text.count('cert-img-card')

    # 逐个替换
    new_row = row_text
    replaced = 0
    rep = [0]

    def svg_replacer(m):
        if rep[0] >= len(images):
            return m.group(0)
        img_name = images[rep[0]]
        img_src = f"images/rzzx/{folder}/{img_name}"
        alt = m.group(2)
        style = m.group(4)
        rep[0] += 1
        return f'<img src="{img_src}" {m.group(1)}alt="{alt}" {m.group(3)}style="{style}"'

    new_row = svg_pat.sub(svg_replacer, new_row)
    replaced = rep[0]

    # 写回
    content = content[:div_start] + new_row + content[row_end:]

    # 更新后续cat的位置（因为content长度变了）
    delta = len(new_row) - len(row_text)
    for next_cat in cat_positions:
        if next_cat != cat and cat_positions[next_cat] > cat_pos:
            cat_positions[next_cat] += delta

    total_rep += replaced
    status = "✅" if replaced > 0 else "⚠️ "
    print(f"{status} {folder} ({cat}): {replaced}/{svg_count} 占位符替换（{card_count}卡片）")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n=== 完成：共替换 {total_rep} 张图片 ===")
