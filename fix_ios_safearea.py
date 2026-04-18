import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 更新 viewport meta 标签添加 viewport-fit=cover
content = content.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'
)

# 2. 为 footer 添加安全区域边距
old_footer = '''        /* Footer - Match Homepage EXACTLY */
        .footer {
            background: #fff;
            padding: 30px 40px;
            border-top: 1px solid #eee;
            flex-shrink: 0;
        }'''

new_footer = '''        /* Footer - Match Homepage EXACTLY */
        .footer {
            background: #fff;
            padding: 30px 40px;
            padding-bottom: calc(30px + env(safe-area-inset-bottom, 0px));
            border-top: 1px solid #eee;
            flex-shrink: 0;
        }
        
        @media (max-width: 768px) {
            .footer {
                padding: 20px;
                padding-bottom: calc(20px + env(safe-area-inset-bottom, 0px));
            }
        }'''

content = content.replace(old_footer, new_footer)

# 3. 更新 mobile 响应式的 footer padding
old_mobile_footer = '''            .footer { padding: 20px; }'''
new_mobile_footer = '''            .footer { 
                padding: 20px;
                padding-bottom: calc(20px + env(safe-area-inset-bottom, 0px));
            }'''

content = content.replace(old_mobile_footer, new_mobile_footer)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')