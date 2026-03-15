        // Tab切换
        function switchInfoTab(tabName) {
            document.querySelectorAll('.info-panel').forEach(p => p.classList.remove('active'));
            const selected = document.getElementById('panel-' + tabName);
            if (selected) selected.classList.add('active');
        }
        
        // 指标提示数据
        const metricTips = {
            sessions: {
                title: '📊 活跃会话',
                desc: '最近10分钟内有活动（发送/接收消息）的会话数量。包括群聊、私聊和后台任务。',
                formula: '活跃标准：文件修改时间 < 10分钟。为其他指标提供上下文参考。'
            },
            pending: {
                title: '⏳ 待处理',
                desc: '用户已发送消息但我尚未开始处理的数量。反映等待队列的长度。',
                formula: '参与方式：直接贡献「等待评分」。等待时间越长 → 评分越高。\n0-10s: 20-30% | 10-30s: 30-55% | 30-60s: 55-80% | 60s+: 80-95%'
            },
            processing: {
                title: '🔄 处理中',
                desc: '当前正在执行任务的数量。检测到thinking消息或工具调用视为处理中。',
                formula: '参与方式：每个处理中任务 +3% 评分加成（最多+15%）。\n反映系统正在进行的实际工作量。'
            },
            tokens: {
                title: '🔤 Token负载',
                desc: '当前处理中任务的上下文Token总量。代表AI需要处理的内容复杂度。',
                formula: '参与方式：直接贡献「Token评分」。只统计处理中任务的Tokens。\n10k: 10% | 50k: 30% | 100k: 50% | 200k+: 75-80%'
            },
            estimated: {
                title: '⏱️ 预计响应时间',
                desc: '基于当前处理任务数量和Token量估算的响应时间。让你知道大概要等多久。',
                formula: '计算方式：\n• 每个处理中任务：+30秒基础时间\n• 每50k tokens：+最多30秒\n• 每个排队任务：+15秒\n\n示例：2个处理中任务 + 100k tokens = 约60-90秒'
            }
        };
        
        // 显示指标提示
        function showMetricTip(metricKey) {
            const tip = metricTips[metricKey];
            if (!tip) return;
            
            document.getElementById('tooltipTitle').textContent = tip.title;
            document.getElementById('tooltipDesc').textContent = tip.desc;
            document.getElementById('tooltipFormula').textContent = tip.formula;
            document.getElementById('metricTooltip').classList.add('active');
        }
        
        // 隐藏指标提示
        function hideMetricTip() {
            document.getElementById('metricTooltip').classList.remove('active');
        }
        
        // Redis 直接访问配置（方案 A：快速恢复）
        const config = {
            url: 'https://singular-snake-71209.upstash.io',
            token: 'gQAAAAAAARYpAAIncDE2NmRhOGU0OWFhZWM0N2I4OGZlMGZkNGM5NjdjMTI5NnAxNzEyMDk'
        };
        
        async function fetchData() {
            try {
                const response = await fetch(`${config.url}/get/cognitive.json`, {
                    headers: { 'Authorization': `Bearer ${config.token}` }
                });
                
                if (!response.ok) throw new Error('Fetch failed');
                
                const data = await response.json();
                if (!data.result) return;
                
                const outer = JSON.parse(data.result);
                const metrics = JSON.parse(outer.value);
                
                updateUI(metrics);
            } catch (e) {
                console.error('Error:', e);
                // 显示离线状态
                document.getElementById('radioStatusText').textContent = '⚠️ 连接失败';
                document.getElementById('radioStatusText').style.color = '#ef4444';
            }
        }
        
        function updateUI(data) {
            const score = data.cognitive_score || 0;
            
            // 更新心跳时间
            const now = new Date();
            const timeStr = now.toLocaleTimeString('zh-CN', {hour12: false});
            document.getElementById('lastHeartbeat').textContent = timeStr;
            
            // 更新CPU和内存
            const cpuEl = document.getElementById('cpuValue');
            const memEl = document.getElementById('memoryValue');
            if (cpuEl) cpuEl.textContent = (data.cpu_percent || 0) + '%';
            if (memEl) memEl.textContent = (data.memory_percent || 0) + '%';
            
            // 更新连接状态
            const connStatus = score >= 65 ? '高负载' : score >= 45 ? '中等' : score >= 25 ? '轻负载' : '空闲';
            const connColor = score >= 65 ? 'high' : score >= 45 ? 'busy' : 'online';
            const connEl = document.getElementById('connectionValue');
            if (connEl) {
                connEl.textContent = '实时 (' + connStatus + ')';
                connEl.className = 'compact-status-value ' + connColor;
            }
            
            // 更新agent状态
            const agentStatusEl = document.getElementById('agentStatusValue');
            if (agentStatusEl) {
                agentStatusEl.textContent = data.pending_count > 0 ? 'busy' : 'active';
                agentStatusEl.className = 'compact-status-value ' + (data.pending_count > 0 ? 'busy' : 'online');
            }
            
            // 更新收音机调频仪表盘 - 左边大数字
            const radioPercent = document.getElementById('radioPercent');
            const radioPointer = document.getElementById('radioPointer');
            const radioStatusText = document.getElementById('radioStatusText');
            
            const zoneIdle = document.getElementById('zoneIdle');
            const zoneLow = document.getElementById('zoneLow');
            const zoneMedium = document.getElementById('zoneMedium');
            const zoneHigh = document.getElementById('zoneHigh');
            
            // 清除所有zone的active类
            [zoneIdle, zoneLow, zoneMedium, zoneHigh].forEach(z => {
                if (z) z.classList.remove('active');
            });
            
            if (radioPercent && radioPointer) {
                radioPercent.textContent = score + '%';
                radioPointer.style.left = score + '%';
                
                let statusText = '🟢 空闲 - 立即响应';
                let pointerClass = 'idle';
                let percentClass = 'idle';
                let activeZone = zoneIdle;
                let statusColor = '#4ade80';
                
                if (score >= 65) {
                    statusText = '高负载 - 建议等待';
                    pointerClass = 'high';
                    percentClass = 'high';
                    activeZone = zoneHigh;
                    statusColor = '#f87171';
                } else if (score >= 45) {
                    statusText = '中等负载 - 建议简单任务';
                    pointerClass = 'medium';
                    percentClass = 'medium';
                    activeZone = zoneMedium;
                    statusColor = '#facc15';
                } else if (score >= 25) {
                    statusText = '轻负载 - 30秒内响应';
                    pointerClass = 'low';
                    percentClass = 'low';
                    activeZone = zoneLow;
                    statusColor = '#60a5fa';
                } else {
                    statusText = '空闲 - 立即响应';
                    pointerClass = 'idle';
                    percentClass = 'idle';
                    activeZone = zoneIdle;
                    statusColor = '#4ade80';
                }
                
                radioPointer.className = 'radio-pointer ' + pointerClass;
                radioPercent.className = 'radio-percent ' + percentClass;
                
                if (radioStatusText) {
                    radioStatusText.textContent = statusText;
                    radioStatusText.style.color = statusColor;
                }
                if (activeZone) activeZone.classList.add('active');
            }
            
            // 更新指标 - 5个标签
            document.getElementById('sessionsValue').textContent = data.active_sessions || 0;
            document.getElementById('pendingValue').textContent = data.pending_count || 0;
            document.getElementById('processingValue').textContent = data.processing_count || 0;
            document.getElementById('tokensValue').textContent = data.total_tokens_formatted || '0';
            document.getElementById('estimatedValue').textContent = data.estimated_response_formatted || 'Now';
            
            // 获取历史数据并绘制走势图
            const historyData = data['history_' + currentTimeRange] || [];
            drawStockChart(historyData);
            
            // 更新任务队列 - 显示具体任务描述
            const taskList = document.getElementById('taskList');
            if (data.task_queue && data.task_queue.length > 0) {
                taskList.innerHTML = data.task_queue.map(task => {
                    // 显示具体任务名
                    const displayName = task.label || task.name || '💭 未知任务';
                    const statusText = task.status || '✅ 空闲';
                    
                    // 判断状态样式
                    let statusClass = 'idle';
                    if (statusText.includes('🔄') || statusText.includes('processing')) {
                        statusClass = 'processing';
                    } else if (statusText.includes('⏳') || statusText.includes('wait')) {
                        statusClass = 'waiting';
                    }
                    
                    // 格式化tokens显示
                    const tokens = task.tokens || 0;
                    const tokensText = tokens > 1000 ? `${(tokens/1000).toFixed(1)}k tokens` : `${tokens} tokens`;
                    
                    return `
                        <div class="task-item">
                            <div class="task-info">
                                <span class="task-name">${displayName}</span>
                                <span class="task-detail">${tokensText} · ${task.last_role === 'user' ? '等待中' : task.last_role === 'tool' ? '工具执行' : '已回复'}</span>
                            </div>
                            <span class="task-status ${statusClass}">${statusText}</span>
                        </div>
                    `;
                }).join('');
            } else {
                taskList.innerHTML = '<div class="task-item"><span class="task-name">🟢 无活跃任务 - 系统空闲</span></div>';
            }
            
            document.getElementById('updateTime').textContent = '最后更新: ' + new Date().toLocaleString('zh-CN');
        }
        
        // 当前时间范围
        let currentTimeRange = '5m';
        
        // 切换时间范围
        function switchTimeRange(range) {
            currentTimeRange = range;
            document.querySelectorAll('.time-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.range === range);
            });
            fetchData();
        }
        
        // 绘制平滑曲线走势图
        function drawStockChart(history) {
            const canvas = document.getElementById('stockChartCanvas');
            if (!canvas || !history || history.length < 2) {
                if (canvas) {
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = '#444';
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('暂无数据', canvas.width/2, canvas.height/2);
                }
                document.getElementById('chartStats').textContent = '最高:-- 最低:-- 平均:--';
                return;
            }
            
            // 设置canvas尺寸
            const rect = canvas.parentElement.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            
            const ctx = canvas.getContext('2d');
            const width = canvas.width;
            const height = canvas.height;
            const padding = { top: 20, right: 50, bottom: 30, left: 10 };
            const chartWidth = width - padding.left - padding.right;
            const chartHeight = height - padding.top - padding.bottom;
            
            // 清空画布
            ctx.clearRect(0, 0, width, height);
            
            // 计算范围
            const scores = history.map(h => h.score);
            const minScore = Math.min(...scores, 0);
            const maxScore = Math.max(...scores, 100);
            const avgScore = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
            const range = maxScore - minScore || 100;
            
            // 更新统计
            document.getElementById('chartStats').textContent = `最高:${maxScore}% 最低:${minScore}% 平均:${avgScore}%`;
            
            // 绘制网格线
            ctx.strokeStyle = 'rgba(255,255,255,0.05)';
            ctx.lineWidth = 1;
            for (let i = 0; i <= 4; i++) {
                const y = padding.top + (chartHeight / 4) * i;
                ctx.beginPath();
                ctx.moveTo(padding.left, y);
                ctx.lineTo(width - padding.right, y);
                ctx.stroke();
                
                // Y轴标签
                const scoreLabel = Math.round(maxScore - (range / 4) * i);
                ctx.fillStyle = '#666';
                ctx.font = '10px sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText(scoreLabel + '%', width - padding.right + 5, y + 3);
            }
            
            // 绘制平均线
            const avgY = padding.top + chartHeight - ((avgScore - minScore) / range) * chartHeight;
            ctx.strokeStyle = 'rgba(255,255,255,0.2)';
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(padding.left, avgY);
            ctx.lineTo(width - padding.right, avgY);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 根据评分范围确定线条颜色
            function getScoreColor(score) {
                if (score >= 65) return '#ef4444'; // 红色 - 高负载
                if (score >= 45) return '#eab308'; // 黄色 - 中等
                if (score >= 25) return '#3b82f6'; // 蓝色 - 轻负载
                return '#22c55e'; // 绿色 - 空闲
            }
            
            // 计算点的坐标
            const points = history.map((point, i) => ({
                x: padding.left + (i / (history.length - 1)) * chartWidth,
                y: padding.top + chartHeight - ((point.score - minScore) / range) * chartHeight,
                score: point.score
            }));
            
            // 绘制平滑曲线
            if (points.length >= 2) {
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                
                // 绘制渐变填充区域
                ctx.save();
                ctx.beginPath();
                ctx.moveTo(points[0].x, padding.top + chartHeight);
                for (let i = 0; i < points.length; i++) {
                    if (i === 0) {
                        ctx.lineTo(points[i].x, points[i].y);
                    } else {
                        const prev = points[i - 1];
                        const curr = points[i];
                        const cpX = (prev.x + curr.x) / 2;
                        ctx.bezierCurveTo(cpX, prev.y, cpX, curr.y, curr.x, curr.y);
                    }
                }
                ctx.lineTo(points[points.length - 1].x, padding.top + chartHeight);
                ctx.closePath();
                const gradient = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartHeight);
                gradient.addColorStop(0, 'rgba(0, 255, 255, 0.15)');
                gradient.addColorStop(1, 'rgba(0, 255, 255, 0)');
                ctx.fillStyle = gradient;
                ctx.fill();
                ctx.restore();
                
                // 绘制主曲线（分段着色）
                for (let i = 1; i < points.length; i++) {
                    const prev = points[i - 1];
                    const curr = points[i];
                    const avgScore = (prev.score + curr.score) / 2;
                    
                    ctx.strokeStyle = getScoreColor(avgScore);
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(prev.x, prev.y);
                    const cpX = (prev.x + curr.x) / 2;
                    ctx.bezierCurveTo(cpX, prev.y, cpX, curr.y, curr.x, curr.y);
                    ctx.stroke();
                }
                
                // 绘制当前点高亮
                const lastPoint = points[points.length - 1];
                ctx.fillStyle = getScoreColor(lastPoint.score);
                ctx.beginPath();
                ctx.arc(lastPoint.x, lastPoint.y, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // 绘制当前点数值
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 12px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(lastPoint.score + '%', lastPoint.x, lastPoint.y - 12);
            }
            
            // X轴时间标签（显示首尾）
            if (history.length > 0) {
                ctx.fillStyle = '#666';
                ctx.font = '10px sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText(history[0].timestamp, padding.left, height - 10);
                ctx.textAlign = 'right';
                ctx.fillText(history[history.length - 1].timestamp, width - padding.right, height - 10);
            }
        }
        
        // 初始加载
        fetchData();
        
        // 倒计时刷新
        const UPDATE_INTERVAL = 30;
        let countdown = UPDATE_INTERVAL;
        
        setInterval(() => {
            countdown--;
            if (countdown <= 0) {
                countdown = UPDATE_INTERVAL;
                fetchData();
            }
            const el = document.getElementById('countdownSec');
            if (el) el.textContent = countdown;
        }, 1000);
