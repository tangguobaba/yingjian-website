#!/usr/bin/env python3
"""清理ft-chat CSS残留，批量处理多个文件"""
import re, os

CHAT_CSS_BLOCK = """        /* Chat dialog popup */
        .ft-chat-popup.show {
            transform: translateY(-50%) translateX(0);
        }
        .ft-chat-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .ft-chat-win-btn:hover { opacity: 1; }
        .ft-chat-header .ft-popup-close {
            top: 50%;
            right: 10px;
            transform: translateY(-50%);
            position: static;
            transform: none;
            font-size: 18px;
            line-height: 1;
        }
        .ft-chat-body .red {
            color: #e60012;
            font-weight: bold;
        }
        .ft-chat-msg-agent .ft-chat-msg-user .ft-chat-textarea-wrap textarea {
            width: 100%;
            height: 100%;
            padding: 6px 60px 6px 10px;
            border: 1px solid #cce0f5;
            border-radius: 4px;
            font-size: 12px;
            font-family: inherit;
            line-height: 1.5;
            resize: none;
            outline: none;
            background: #eaf3fc;
            box-sizing: border-box;
            overflow: hidden;
            word-wrap: break-word;
        }
        .ft-chat-textarea-wrap textarea:focus {
            border-color: #1e6bd6;
        }
        .ft-chat-textarea-wrap .ft-chat-textarea-wrap .ft-chat-icon-btn:hover { color: #1e6bd6; }

        /* Chat callback bar (回电栏) */
        .ft-chat-callback input {
            flex: 1 1 auto;
            padding: 5px 10px;
            border: 1px solid #cce0f5;
            border-radius: 4px;
            font-size: 12px;
            outline: none;
            background: #eaf3fc;
            min-width: 0;
        }
        .ft-chat-callback input:focus { border-color: #1e6bd6; }
        .ft-chat-callback-btn:hover { background: #e55a00; }

        /* Navigation */"""

files = ['aeo_test.html','index_0602.html','index_0701.html','index_0701_v2.html',
         'index_0901.html','index_1202.html','index_61503.html','khal.html',
         'lsgyl.html','lxwm.html','spzx.html']

os.chdir('/home/tangguo/yingjian-website')
cleaned = 0
for f in files:
    if not os.path.exists(f):
        print(f"跳过: {f} 不存在")
        continue
    with open(f) as fp:
        c = fp.read()
    orig = c
    c = c.replace(CHAT_CSS_BLOCK, "        /* Navigation */")
    # 删HTML残留
    c = re.sub(r'<div\s+class="ft-chat-header[^"]*"[^>]*>.*?</div>\s*</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-body[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-msgs[^"]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div\s+class="ft-chat-msg[^\s]*"[^>]*>.*?</div>', '', c, flags=re.DOTALL)
    if c != orig:
        with open(f, 'w') as fp:
            fp.write(c)
        cleaned += 1
        print(f"cleaned: {f}")
    if 'ft-chat' in c:
        print(f"  STILL DIRTY: {f}")

print(f"\n修改了{cleaned}个文件")

# 验证
os.system('cd /home/tangguo/yingjian-website && grep -l "ft-chat" *.html | grep -v ".bak" | grep -v "aeo_test.html"')
