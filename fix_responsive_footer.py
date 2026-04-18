import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 找到响应式 CSS 部分并替换为更精细的版本
old_responsive = '''        /* Responsive */
        @media (max-width: 1024px) {
            .games-grid { grid-template-columns: repeat(2, 1fr); }
            .games-text { letter-spacing: -4px; }
        }
        
        @media (max-width: 768px) {
            .games-grid { grid-template-columns: repeat(2, 1fr); }
            .footer-inner {
                flex-direction: column;
                gap: 16px;
                text-align: center;
            }
        }
        
        @media (max-width: 640px) {
            .header-inner { padding: 0 20px; }
            .nav-desktop { display: none; }
            .nav-social { display: none; }
            .menu-btn { 
                display: flex; 
                align-items: center; 
                justify-content: center;
            }
            .games-mask-container { padding: 40px 20px 30px; }
            .cards-wrapper { padding: 0 20px 60px; }
            .games-grid { grid-template-columns: 1fr; gap: 16px; }
            .footer { 
                padding: 20px;
                padding-bottom: calc(40px + env(safe-area-inset-bottom, 0px));
            }
        }'''

new_responsive = '''        /* Responsive - Fine-tuned for different devices */
        
        /* Tablet and small desktop */
        @media (max-width: 1024px) {
            .games-grid { grid-template-columns: repeat(2, 1fr); }
            .games-text { letter-spacing: -4px; }
        }
        
        /* Phone landscape - critical for short screens */
        @media (max-height: 500px) and (orientation: landscape) {
            .footer { 
                padding: 15px;
                padding-bottom: calc(30px + env(safe-area-inset-bottom, 0px));
            }
            .footer-inner {
                flex-direction: row;
                gap: 12px;
            }
            .footer-nav { gap: 12px; }
            .footer-nav a { font-size: 11px; }
            .footer-copyright { font-size: 11px; }
            .footer-social { gap: 10px; }
        }
        
        /* Phone portrait - normal phones */
        @media (max-width: 768px) {
            .games-grid { grid-template-columns: repeat(2, 1fr); }
            .footer-inner {
                flex-direction: column;
                gap: 16px;
                text-align: center;
            }
        }
        
        /* Small phone portrait */
        @media (max-width: 640px) {
            .header-inner { padding: 0 20px; }
            .nav-desktop { display: none; }
            .nav-social { display: none; }
            .menu-btn { 
                display: flex; 
                align-items: center; 
                justify-content: center;
            }
            .games-mask-container { padding: 40px 20px 30px; }
            .cards-wrapper { padding: 0 20px 60px; }
            .games-grid { grid-template-columns: 1fr; gap: 16px; }
            .footer { 
                padding: 20px;
                padding-bottom: calc(40px + env(safe-area-inset-bottom, 0px));
            }
        }
        
        /* Foldable phones - larger screens, need more padding */
        @media (min-width: 700px) and (max-width: 900px) and (min-height: 1000px) {
            .footer {
                padding-bottom: calc(80px + env(safe-area-inset-bottom, 0px));
            }
        }
        
        /* iOS specific - detect iPhone with safe-area */
        @supports (-webkit-touch-callout: none) {
            /* iOS devices */
            @media (max-height: 700px) and (orientation: portrait) {
                .footer {
                    padding-bottom: calc(50px + env(safe-area-inset-bottom, 20px));
                }
            }
        }'''

content = content.replace(old_responsive, new_responsive)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')