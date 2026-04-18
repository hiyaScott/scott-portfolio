import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 找到现有的3张卡片并扩展为12张
old_cards = '''                <div class="games-grid">
                    <div class="game-card">
                        <div class="card-image">🎮
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">PC / Mac</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Grid Dominion</h3>
                            <div class="card-meta">Strategy · 2024</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🌌
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Project Starfield</h3>
                            <div class="card-meta">Exploration · TBA</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🎲
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">Mobile</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Echoes of Silence</h3>
                            <div class="card-meta">Puzzle · 2025</div>
                        </div>
                    </div>
                </div>'''

new_cards = '''                <div class="games-grid">
                    <div class="game-card">
                        <div class="card-image">🎮
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">PC / Mac</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Grid Dominion</h3>
                            <div class="card-meta">Strategy · 2024</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🌌
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Project Starfield</h3>
                            <div class="card-meta">Exploration · TBA</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🎲
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">Mobile</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Echoes of Silence</h3>
                            <div class="card-meta">Puzzle · 2025</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">⚔️
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC / Console</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Blade Chronicles</h3>
                            <div class="card-meta">Action RPG · 2025</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🚀
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">Mobile / PC</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Stellar Drift</h3>
                            <div class="card-meta">Racing · 2024</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🏰
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Castle of Echoes</h3>
                            <div class="card-meta">Adventure · TBA</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🎯
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">Mobile</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Precision Strike</h3>
                            <div class="card-meta">Shooter · 2024</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🌊
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC / Console</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Tidal Forces</h3>
                            <div class="card-meta">Simulation · 2025</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🧩
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">Mobile / PC</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Mind Maze</h3>
                            <div class="card-meta">Puzzle · 2024</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🔥
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Inferno Protocol</h3>
                            <div class="card-meta">Survival · TBA</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">🎨
                            <span class="status-badge">Live</span>
                            <span class="platform-tag">Mobile</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Canvas Odyssey</h3>
                            <div class="card-meta">Creative · 2024</div>
                        </div>
                    </div>
                    
                    <div class="game-card">
                        <div class="card-image">⚡
                            <span class="status-badge beta">Beta</span>
                            <span class="platform-tag">PC / Console</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">Voltage Rush</h3>
                            <div class="card-meta">Arcade · 2025</div>
                        </div>
                    </div>
                </div>'''

content = content.replace(old_cards, new_cards)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done - 12 cards added')