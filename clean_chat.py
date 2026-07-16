#!/usr/bin/env python3
import re, os

def clean_file(path):
    with open(path) as f:
        c = f.read()
    orig = c
    # 删除整个ftChatPopup的div块
    c = re.sub(r'<div\s+class="ft-popup ft-chat-popup"[^>]*>.*?</div>\s*</div>\s*(?=<div)', '', c, flags=re.DOTALL)
    # 删除 ft-chat-fab 按钮
    c = re.sub(r'<div\s+class="ft-chat-fab"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    # 删残留的 ft-chat class div
    c = re.sub(r'<div\s+class="ft-chat-header[^"]*"[^>]*>.*?</div>\s*</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-body[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-msgs[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-input[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-msg[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-callback[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-input-main[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-icons[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-textarea-wrap[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    # 删除 JS变量
    c = re.sub(r'var chatBtn[^\n]+\n', '', c)
    c = re.sub(r'var chatPop[^\n]+\n', '', c)
    # 删除 initCustomerChat
    c = re.sub(r',?\s*initCustomerChat\(\)', '', c)
    changed = c != orig
    with open(path, 'w') as f:
        f.write(c)
    return changed, 'ft-chat' in c

os.chdir('/home/tangguo/yingjian-website')
htmls = [f for f in os.listdir('.') if f.endswith('.html') and not f.endswith('.bak')]
cleaned, still_dirty = 0, 0
for h in sorted(htmls):
    changed, dirty = clean_file(h)
    if changed:
        cleaned += 1
    if dirty:
        still_dirty += 1
        print(f"残留: {h}")

print(f"修改了{cleaned}个文件，{still_dirty}个还有残留")
