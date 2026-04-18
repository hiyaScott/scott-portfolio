import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改 update() 方法 - 当在中心位置时，强制无旋转、无缩放、无透明度变化
old_update = '''            update() {
                // Calculate distance to mouse
                const dx = this.centerX - mouseX;
                const dy = this.centerY - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                // Calculate rotation based on distance
                if (distance < INFLUENCE_RADIUS) {
                    const influence = 1 - (distance / INFLUENCE_RADIUS);
                    const angle = Math.atan2(dy, dx);
                    this.targetRotation = angle * (180 / Math.PI) * influence * 0.3;
                    this.targetScale = 1 + influence * 0.2;
                } else {
                    this.targetRotation = 0;
                    this.targetScale = 1;
                }
                
                // Smooth interpolation
                this.rotation += (this.targetRotation - this.rotation) * 0.1;
                this.scale += (this.targetScale - this.scale) * 0.1;
            }'''

new_update = '''            update() {
                // Calculate distance to mouse
                const dx = this.centerX - mouseX;
                const dy = this.centerY - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                // Calculate rotation based on distance
                if (distance < INFLUENCE_RADIUS) {
                    const influence = 1 - (distance / INFLUENCE_RADIUS);
                    const angle = Math.atan2(dy, dx);
                    this.targetRotation = angle * (180 / Math.PI) * influence * 0.3;
                    this.targetScale = 1 + influence * 0.2;
                } else {
                    this.targetRotation = 0;
                    this.targetScale = 1;
                }
                
                // Check if mouse is at center (default state)
                const isAtCenter = (mouseX === window.innerWidth / 2 && mouseY === window.innerHeight / 2);
                
                // Smooth interpolation
                this.rotation += (this.targetRotation - this.rotation) * 0.1;
                this.scale += (this.targetScale - this.scale) * 0.1;
                
                // Force reset to default when at center
                if (isAtCenter) {
                    this.rotation = 0;
                    this.scale = 1;
                }
            }'''

content = content.replace(old_update, new_update)

# 2. 进一步减小卡片容器初始位置 - 从 120px 改为 100px
content = content.replace(
    'margin-top: 120px; /* 紧贴 GAMES 标题下方 */',
    'margin-top: 100px; /* 紧贴 GAMES 标题下方 */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')