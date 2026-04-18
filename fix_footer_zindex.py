import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 给 footer 添加 z-index，让它在 GAMES 标题之上
old_footer = '''        /* Footer - Match Homepage EXACTLY */
        .footer {
            background: #fff;
            padding: 30px 40px;
            padding-bottom: calc(30px + env(safe-area-inset-bottom, 0px));
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
            position: relative;
            z-index: 3; /* 在 GAMES 标题 (z-index: 1) 之上 */
        }'''

content = content.replace(old_footer, new_footer)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')