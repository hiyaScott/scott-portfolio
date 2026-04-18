import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改背景色和文字色
content = content.replace('background: #000;', 'background: #fff;')
content = content.replace('color: #fff;', 'color: #333;')
content = content.replace("ctx.fillStyle = '#000';", "ctx.fillStyle = '#fff';")

# 2. 修改 alpha 逻辑 (0.25 → 1.00)
content = content.replace(
    'const alpha = 1.0 - (this.scale - 1) * 2.5;  // scale 1→1.2, alpha 1.0→0.5',
    'const alpha = 0.25 + (this.scale - 1) * 3.75;  // scale 1→1.2, alpha 0.25→1.0'
)
content = content.replace('// ALPHA: base 1.0 → hover 0.5', '// ALPHA: base 0.25 → hover 1.0')

# 3. 注掉光晕效果
content = content.replace(
    '''                // GLOW on hover (scale > 1.1)
                if (this.scale > 1.1) {
                    ctx.shadowColor = 'rgba(255, 255, 255, 0.6)';
                    ctx.shadowBlur = 20;
                }''',
    '''                // GLOW on hover (scale > 1.1) - DISABLED
                // if (this.scale > 1.1) {
                //     ctx.shadowColor = 'rgba(255, 255, 255, 0.6)';
                //     ctx.shadowBlur = 20;
                // }'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')