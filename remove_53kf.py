#!/usr/bin/env python3
"""
Line-based removal of 53KF chat widget (ft-chat*) from HTML files.
More robust than regex for multi-line HTML structures.
"""
import re
import os
import glob

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original = ''.join(lines)
    new_lines = []
    i = 0
    in_chat_popup_div = False
    in_ftChatBtn_div = False
    removed_something = False
    
    while i < len(lines):
        line = lines[i]
        
        # Detect start of ftChatPopup div block
        if '<div' in line and 'ft-chat-popup' in line and 'ftChatPopup' in line and 'id=' in line:
            in_chat_popup_div = True
            removed_something = True
            i += 1
            continue
        
        # If we're inside the chat popup div, skip until we find closing </div>
        if in_chat_popup_div:
            if '</div>' in line:
                in_chat_popup_div = False
            i += 1
            continue
        
        # Detect ftChatBtn div in toolbar (multi-line)
        if '<div' in line and 'tool-item' in line and 'ftChatBtn' in line and 'id=' in line:
            in_ftChatBtn_div = True
            removed_something = True
            i += 1
            continue
        
        if in_ftChatBtn_div:
            if '</div>' in line:
                in_ftChatBtn_div = False
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    content = ''.join(new_lines)
    
    # Remove body onload auto-show for ftChatPopup
    content = re.sub(
        r'<body\s+onload="[^"]*ftChatPopup[^"]*"',
        '<body',
        content
    )
    
    # Remove CSS: .ft-chat-popup block and all .ft-chat-* rules  
    # Remove "/* Chat Popup */" block up to "/* Phone Popup */"
    content = re.sub(
        r'/\* Chat Popup \*/[^\n]*\n[\s\S]*?(?=\s*/\* Phone Popup \*/)',
        '/* Phone Popup */\n',
        content
    )
    # Remove remaining ft-chat CSS rules
    content = re.sub(
        r'\n?\.ft-chat-[a-zA-Z\-]+\s*\{[^}]*\}\s*',
        '',
        content
    )
    content = re.sub(
        r'\n?#ftChat(?:SendBtn|Text|Msgs)[^}]*\}\s*',
        '',
        content
    )
    
    # Remove ftChatBtn from JS var declaration (single-line HTML case)
    content = re.sub(
        r'<div\s+class="tool-item"\s+id="ftChatBtn"[^>]*>.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove JS: chatBtn and chatPop references  
    content = re.sub(
        r'var\s+chatBtn\s*=\s*\$\('+"'ftChatBtn'"+r'\),\s*',
        'var ',
        content
    )
    content = re.sub(
        r',\s*chatBtn\s*=\s*\$\('+"'ftChatBtn'"+r'\)',
        '',
        content
    )
    content = re.sub(
        r',\s*chatPop\s*=\s*\$\('+"'ftChatPopup'"+r'\)',
        '',
        content
    )
    content = re.sub(
        r'var\s+chatPop\s*=\s*\$\('+"'ftChatPopup'"+r'\)\s*,\s*',
        'var ',
        content
    )
    content = re.sub(
        r'var\s+chatPop\s*=\s*\$\('+"'ftChatPopup'"+r'\)\s*;?\s*',
        '',
        content
    )
    content = re.sub(
        r'allPops\s*=\s*\[\s*chatPop\s*,?\s*',
        'allPops=[',
        content
    )
    content = re.sub(
        r'if\s*\(\s*chatBtn\s*\)\s*chatBtn\s*\.\s*addEventListener\s*\([^)]+\);\s*',
        '',
        content
    )
    
    # Remove /* Chat send */ IIFE block
    content = re.sub(
        r'/\*\s*Chat send\s*\*/[\s\S]*?\}\)\s*\(\s*\)\s*;?\s*(?=\n\s*(?:/\* Tab|</script))',
        '',
        content
    )
    
    # Clean up double blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    os.chdir('/home/tangguo/yingjian-website')
    html_files = glob.glob('*.html')
    html_files = [f for f in html_files if '.bak' not in f]
    
    print(f"Found {len(html_files)} HTML files to process")
    
    modified = []
    unchanged = []
    
    for filepath in sorted(html_files):
        changed = process_file(filepath)
        if changed:
            modified.append(filepath)
        else:
            unchanged.append(filepath)
    
    print(f"\nModified {len(modified)} files:")
    for f in modified:
        print(f"  + {f}")
    
    if unchanged:
        print(f"\nUnchanged {len(unchanged)} files:")
        for f in unchanged:
            print(f"  - {f}")

if __name__ == '__main__':
    main()
