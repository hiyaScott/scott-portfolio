import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 为卡片添加 data-page 属性，方便分页控制
content = content.replace(
    '<div class="games-grid">',
    '<div class="games-grid" id="gamesGrid">'
)

# 2. 为每个卡片添加页码属性
for i in range(1, 13):
    old_card = '<div class="game-card">'
    page_num = (i - 1) // 9 + 1
    new_card = '<div class="game-card" data-page="' + str(page_num) + '">'
    content = content.replace(old_card, new_card, 1)

# 3. 在卡片容器后添加分页控件
old_wrapper_end = '''</div>
            </div>
            
            <!-- Scroll Indicator -->'''

new_wrapper_end = '''</div>
                
                <!-- Pagination -->
                <div class="pagination" id="pagination">
                    <button class="pagination-btn prev" onclick="changePage(-1)">←</button>
                    <div class="pagination-numbers" id="pageNumbers"></div>
                    <button class="pagination-btn next" onclick="changePage(1)">→</button>
                </div>
            </div>
            
            <!-- Scroll Indicator -->'''

content = content.replace(old_wrapper_end, new_wrapper_end)

# 4. 添加分页样式
pagination_css = '''        /* Pagination */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            margin-top: 40px;
            padding: 20px 0;
        }
        
        .pagination-btn {
            width: 40px;
            height: 40px;
            border: 1px solid #ddd;
            background: #fff;
            color: #333;
            font-size: 14px;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .pagination-btn:hover:not(:disabled) {
            background: #f5f5f5;
            border-color: #999;
        }
        
        .pagination-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        .pagination-numbers {
            display: flex;
            gap: 8px;
        }
        
        .pagination-number {
            width: 40px;
            height: 40px;
            border: 1px solid #ddd;
            background: #fff;
            color: #333;
            font-size: 14px;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        .pagination-number:hover {
            background: #f5f5f5;
            border-color: #999;
        }
        
        .pagination-number.active {
            background: #333;
            color: #fff;
            border-color: #333;
        }
        
        @media (max-width: 640px) {
            .pagination-btn, .pagination-number {
                width: 36px;
                height: 36px;
                font-size: 13px;
            }
        }
        '''

content = content.replace(
    '        /* Footer - Match Homepage EXACTLY */',
    pagination_css + '\n        /* Footer - Match Homepage EXACTLY */'
)

# 5. 添加分页 JavaScript
pagination_js = '''        // Pagination Logic
        const CARDS_PER_PAGE = 9;
        let currentPage = 1;
        
        function initPagination() {
            const cards = document.querySelectorAll('.game-card');
            const totalPages = Math.ceil(cards.length / CARDS_PER_PAGE);
            
            const pageNumbers = document.getElementById('pageNumbers');
            pageNumbers.innerHTML = '';
            for (let i = 1; i <= totalPages; i++) {
                const btn = document.createElement('button');
                btn.className = 'pagination-number' + (i === currentPage ? ' active' : '');
                btn.textContent = i;
                btn.onclick = () => goToPage(i);
                pageNumbers.appendChild(btn);
            }
            
            updateCardsVisibility();
            updatePaginationButtons(totalPages);
        }
        
        function updateCardsVisibility() {
            const cards = document.querySelectorAll('.game-card');
            const start = (currentPage - 1) * CARDS_PER_PAGE;
            const end = start + CARDS_PER_PAGE;
            
            cards.forEach((card, index) => {
                if (index >= start && index < end) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        function updatePaginationButtons(totalPages) {
            const prevBtn = document.querySelector('.pagination-btn.prev');
            const nextBtn = document.querySelector('.pagination-btn.next');
            
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage === totalPages;
            
            document.querySelectorAll('.pagination-number').forEach((btn, index) => {
                btn.classList.toggle('active', index + 1 === currentPage);
            });
        }
        
        function changePage(direction) {
            const cards = document.querySelectorAll('.game-card');
            const totalPages = Math.ceil(cards.length / CARDS_PER_PAGE);
            const newPage = currentPage + direction;
            
            if (newPage >= 1 && newPage <= totalPages) {
                currentPage = newPage;
                updateCardsVisibility();
                updatePaginationButtons(totalPages);
            }
        }
        
        function goToPage(page) {
            currentPage = page;
            updateCardsVisibility();
            const cards = document.querySelectorAll('.game-card');
            const totalPages = Math.ceil(cards.length / CARDS_PER_PAGE);
            updatePaginationButtons(totalPages);
        }
        
        initPagination();
        '''

content = content.replace(
    '        // Resize handler',
    pagination_js + '\n        // Resize handler'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')