import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改颜色为 rgb(250,250,250)
content = content.replace('rgba(200, 200, 200,', 'rgba(250, 250, 250,')

# 2. 修改透明度逻辑：1.00 → 0.8（逐渐变暗）
content = content.replace(
    'const alpha = 0.25 + (this.scale - 1) * 3.75;  // scale 1→1.2, alpha 0.25→1.0',
    'const alpha = 1.0 - (this.scale - 1) * 1.0;  // scale 1→1.2, alpha 1.0→0.8'
)
content = content.replace('// ALPHA: base 0.25 → hover 1.0', '// ALPHA: base 1.0 → hover 0.8')

# 3. 影响范围扩大一倍：200 → 400
content = content.replace('const INFLUENCE_RADIUS = 200;', 'const INFLUENCE_RADIUS = 400;')

# 4. 完全删除光晕代码（而不是注释）
content = content.replace(
    '''                // GLOW on hover (scale > 1.1) - DISABLED
                // if (this.scale > 1.1) {
                //     ctx.shadowColor = 'rgba(255, 255, 255, 0.6)';
                //     ctx.shadowBlur = 20;
                // }
                ''',
    ''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')