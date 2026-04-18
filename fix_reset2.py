import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 修改 update() 方法 - 当 target 在中心时，跳过所有计算直接返回默认值
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

new_update = '''            update() {
                // Check if returning to center (default state)
                const isReturningToCenter = (targetMouseX === window.innerWidth / 2 && targetMouseY === window.innerHeight / 2);
                
                if (isReturningToCenter) {
                    // Instantly reset to default, no interpolation
                    this.rotation = 0;
                    this.scale = 1;
                    this.targetRotation = 0;
                    this.targetScale = 1;
                    return;
                }
                
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

content = content.replace(old_update, new_update)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')