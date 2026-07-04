#!/usr/bin/env python3
"""创建认证验厂合成图"""
from PIL import Image, ImageDraw, ImageFont
import os

# 配置
OUTPUT_DIR = '/home/tangguo/yingjian-website/images/competence/'
LOGO_DIR = OUTPUT_DIR + 'logos/'
SIZE = (400, 280)

# 认证名称
certifications = [
    ('smeta', 'SMETA', (65, 105, 225)),      # 蓝色
    ('sedex', 'Sedex', (0, 128, 128)),      # 青色
    ('bsci', 'BSCI', (255, 140, 0)),        # 橙色
    ('slcp', 'SLCP', (50, 205, 50)),        # 绿色
    ('walmart', 'Walmart', (0, 100, 180)),   # 深蓝
    ('disney', 'Disney', (25, 25, 112)),    # 藏蓝
    ('fsc', 'FSC', (34, 139, 34)),          # 森林绿
    ('grs', 'GRS', (0, 128, 0)),            # 绿色
    ('iso', 'ISO', (220, 20, 60)),          # 红色
]

# 背景颜色配置（模拟不同工业场景）
bg_colors = [
    ((120, 150, 170), (90, 120, 140)),  # 1. 工厂外景-灰蓝
    ((160, 160, 170), (130, 130, 140)), # 2. 工厂内景-不锈钢灰
    ((100, 130, 100), (70, 100, 70)),   # 3. 工业车间-绿色地砖
    ((140, 145, 150), (110, 115, 120)), # 4. 金属表面
    ((130, 120, 100), (100, 90, 80)),   # 5. 仓储/物流
    ((150, 140, 160), (120, 110, 130)), # 6. 商业/零售
    ((80, 120, 80), (60, 100, 60)),     # 7. 森林/自然
    ((160, 140, 130), (130, 110, 100)), # 8. 纺织/面料
    ((180, 160, 140), (150, 130, 110)), # 9. 食品加工
]

def create_gradient_bg(color1, color2, size):
    """创建渐变背景"""
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    w, h = size
    for y in range(h):
        ratio = y / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def add_industrial_details(img, bg_idx):
    """添加工业场景细节"""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # 根据背景类型添加不同细节
    if bg_idx == 0:  # 工厂外景 - 添加窗户/玻璃效果
        for i in range(3):
            for j in range(4):
                x = 50 + i * 100
                y = 80 + j * 50
                draw.rectangle([x, y, x+60, y+35], outline=(200,220,240), width=2)
    elif bg_idx == 1:  # 工厂内景 - 不锈钢货架
        for i in range(5):
            draw.line([(60+i*70, 40), (60+i*70, 280)], fill=(180,180,190), width=3)
            draw.line([(40, 80+i*50), (380, 80+i*50)], fill=(170,170,180), width=2)
    elif bg_idx == 2:  # 工业车间 - 机械设备
        for i in range(4):
            x = 30 + i * 95
            draw.ellipse([x, 150, x+70, 220], outline=(60,80,60), width=3)
            draw.rectangle([x+20, 100, x+50, 150], fill=(80,100,80))
    elif bg_idx == 3:  # 金属表面 - 反光条纹
        for i in range(20):
            y = i * 14
            draw.line([(0, y), (400, y+5)], fill=(180,185,190), width=1)
    elif bg_idx == 4:  # 仓储 - 货架
        for i in range(6):
            draw.line([(40+i*60, 20), (40+i*60, 280)], fill=(120,100,80), width=4)
            draw.line([(20, 60+i*40), (380, 60+i*40)], fill=(110,90,70), width=3)
    elif bg_idx == 5:  # 商业 - 展示架
        for i in range(3):
            draw.rectangle([50+i*120, 180, 140+i*120, 280], outline=(180,170,190), width=2)
            draw.rectangle([60+i*120, 120, 130+i*120, 170], outline=(180,170,190), width=2)
    elif bg_idx == 6:  # 森林 - 树木
        for i in range(5):
            x = 40 + i * 80
            draw.polygon([(x, 280), (x+30, 150), (x+60, 280)], fill=(50,100,50))
    elif bg_idx == 7:  # 纺织 - 线条纹理
        for i in range(30):
            y = i * 10
            draw.line([(0, y), (400, y)], fill=(140,120,110), width=1)
    elif bg_idx == 8:  # 食品 - 圆形元素
        import random
        random.seed(42)
        for _ in range(15):
            x = random.randint(20, 380)
            y = random.randint(100, 270)
            r = random.randint(15, 40)
            draw.ellipse([x-r, y-r, x+r, y+r], outline=(160,130,100), width=2)
    
    return img

def create_banner(img, color, name_short):
    """创建白色横幅并添加logo和文字"""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # 横幅尺寸
    banner_w = int(w * 0.6)
    banner_h = 90
    banner_x = (w - banner_w) // 2
    banner_y = 30
    
    # 绘制白色圆角横幅
    draw.rounded_rectangle(
        [banner_x, banner_y, banner_x + banner_w, banner_y + banner_h],
        radius=10,
        fill=(255, 255, 255),
        outline=(220, 220, 220),
        width=2
    )
    
    # 尝试加载logo图片
    logo_path = LOGO_DIR + name_short + '.png'
    logo_img = None
    if os.path.exists(logo_path) and os.path.getsize(logo_path) > 1000:
        try:
            logo_img = Image.open(logo_path)
            logo_img = logo_img.convert('RGBA')
        except:
            logo_img = None
    
    # 绘制logo或文字
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
        font_sub = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    if logo_img:
        # 调整logo大小
        logo_w, logo_h = logo_img.size
        max_logo_w = 120
        max_logo_h = 50
        ratio = min(max_logo_w / logo_w, max_logo_h / logo_h)
        new_w = int(logo_w * ratio)
        new_h = int(logo_h * ratio)
        logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS)
        
        # 放置logo
        logo_x = (w - new_w) // 2
        logo_y = banner_y + 10
        img.paste(logo_img, (logo_x, logo_y), logo_img)
        
        # "验厂"文字
        text = "验厂"
        bbox = draw.textbbox((0, 0), text, font=font_sub)
        text_w = bbox[2] - bbox[0]
        text_x = (w - text_w) // 2
        text_y = banner_y + 65
        draw.text((text_x, text_y), text, fill=(80, 80, 80), font=font_sub)
    else:
        # 无logo时绘制首字母
        letter = name_short[:2].upper() if len(name_short) > 2 else name_short.upper()
        
        # 绘制认证缩写
        bbox = draw.textbbox((0, 0), letter, font=font_title)
        letter_w = bbox[2] - bbox[0]
        letter_h = bbox[3] - bbox[1]
        letter_x = (w - letter_w) // 2
        letter_y = banner_y + 8
        
        # 绘制字母
        draw.text((letter_x, letter_y), letter, fill=color, font=font_title)
        
        # "验厂"文字
        text = "验厂"
        bbox = draw.textbbox((0, 0), text, font=font_sub)
        text_w = bbox[2] - bbox[0]
        text_x = (w - text_w) // 2
        text_y = banner_y + 60
        draw.text((text_x, text_y), text, fill=(80, 80, 80), font=font_sub)
    
    return img

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOGO_DIR, exist_ok=True)
    
    for i, (name_short, name_full, color) in enumerate(certifications):
        print(f"创建 {name_short}_yanchang.jpg...")
        
        # 创建背景
        bg_color1, bg_color2 = bg_colors[i]
        img = create_gradient_bg(bg_color1, bg_color2, SIZE)
        
        # 添加工业细节
        img = add_industrial_details(img, i)
        
        # 添加白色横幅和文字
        img = create_banner(img, color, name_short)
        
        # 保存
        output_path = OUTPUT_DIR + name_short + '_yanchang.jpg'
        img.save(output_path, 'JPEG', quality=90)
        print(f"  保存到: {output_path}")
    
    print("\n完成！所有9张验厂图片已创建。")

if __name__ == '__main__':
    main()