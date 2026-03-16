// 认知监控 v5.25 - 纯手动模式
// 只在用户点击时获取数据，零后台消耗

const API_URL = 'http://101.126.54.134/api/cognitive/status';

async function fetchData() {
    try {
        // 显示加载状态
        document.getElementById('lastHeartbeat').textContent = '获取中...';
        
        const cacheBuster = `?t=${Date.now()}`;
        const response = await fetch(API_URL + cacheBuster, {
            headers: { 'Accept': 'application/json' }
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        
        updateUI(data);
        updateTimeDisplay(data.timestamp);
        
    } catch (e) {
        console.error('[Cognitive Monitor] 获取失败:', e.message);
        document.getElementById('radioStatusText').textContent = '⚠️ 连接失败';
        document.getElementById('radioStatusText').style.color = '#ef4444';
        document.getElementById('lastHeartbeat').textContent = '失败';
    }
}

function updateTimeDisplay(timestamp) {
    const timeEl = document.getElementById('lastHeartbeat');
    const updateEl = document.getElementById('updateTime');
    
    if (timestamp) {
        const date = new Date(timestamp);
        const timeStr = date.toLocaleTimeString('zh-CN', {hour12: false});
        timeEl.textContent = timeStr;
        updateEl.textContent = '数据时间: ' + date.toLocaleString('zh-CN');
    }
}

function updateUI(data) {
    const score = data.cognitive_score || 0;
    
    // 更新 CPU/内存
    document.getElementById('cpuValue').textContent = (data.cpu_percent || 0) + '%';
    document.getElementById('memoryValue').textContent = (data.memory_percent || 0) + '%';
    
    // 更新连接状态
    const connStatus = score >= 65 ? '高负载' : score >= 45 ? '中等' : score >= 25 ? '轻负载' : '空闲';
    const connColor = score >= 65 ? 'high' : score >= 45 ? 'busy' : 'online';
    document.getElementById('connectionValue').textContent = connStatus;
    document.getElementById('connectionValue').className = 'compact-status-value ' + connColor;
    
    // 更新 Agent 状态
    const agentEl = document.getElementById('agentStatusValue');
    if (agentEl) {
        agentEl.textContent = data.pending_count > 0 ? 'busy' : 'active';
        agentEl.className = 'compact-status-value ' + (data.pending_count > 0 ? 'busy' : 'online');
    }
    
    // 更新仪表盘
    const radioPercent = document.getElementById('radioPercent');
    const radioPointer = document.getElementById('radioPointer');
    const radioStatusText = document.getElementById('radioStatusText');
    const zones = ['zoneIdle', 'zoneLow', 'zoneMedium', 'zoneHigh'].map(id => document.getElementById(id));
    zones.forEach(z => z && z.classList.remove('active'));
    
    if (radioPercent && radioPointer) {
        const numSpan = radioPercent.querySelector('.percent-number');
        if (numSpan) numSpan.textContent = score;
        radioPointer.style.left = score + '%';
        
        let statusText = '🟢 空闲 - 立即响应';
        let pointerClass = 'idle';
        let percentClass = 'idle';
        let activeZone = zones[0];
        let statusColor = '#4ade80';
        
        if (score >= 65) {
            statusText = '🔴 高负载 - 建议等待';
            pointerClass = 'high';
            percentClass = 'high';
            activeZone = zones[3];
            statusColor = '#ef4444';
        } else if (score >= 45) {
            statusText = '🟡 中等负载 - 简单任务';
            pointerClass = 'medium';
            percentClass = 'medium';
            activeZone = zones[2];
            statusColor = '#eab308';
        } else if (score >= 25) {
            statusText = '🔵 轻负载 - 30秒内响应';
            pointerClass = 'low';
            percentClass = 'low';
            activeZone = zones[1];
            statusColor = '#60a5fa';
        }
        
        radioPointer.className = 'pointer ' + pointerClass;
        radioPercent.className = 'percent-number ' + percentClass;
        radioStatusText.textContent = statusText;
        radioStatusText.style.color = statusColor;
        if (activeZone) activeZone.classList.add('active');
    }
    
    // 更新指标
    document.getElementById('sessionsValue').textContent = data.active_sessions || 0;
    document.getElementById('pendingValue').textContent = data.pending_count || 0;
    document.getElementById('processingValue').textContent = data.processing_count || 0;
    document.getElementById('tokensValue').textContent = (data.total_tokens || 0) > 1000 
        ? ((data.total_tokens / 1000).toFixed(1) + 'k') : (data.total_tokens || 0);
    document.getElementById('suggestionValue').textContent = data.suggestion || '可立即响应';
    
    // 更新任务列表
    const taskList = document.getElementById('taskList');
    if (data.task_queue && data.task_queue.length > 0) {
        taskList.innerHTML = data.task_queue.map(task => {
            const isWaiting = task.status === 'waiting';
            const statusClass = isWaiting ? 'status-pending' : task.status === 'processing' ? 'status-processing' : 'status-replied';
            const statusText = isWaiting ? '等待中' : task.status === 'processing' ? '处理中' : '已回复';
            const displayName = task.name || '未知任务';
            let detailText = task.channel || '';
            if (task.tokens > 0) {
                detailText = task.tokens > 1000 ? `${(task.tokens/1000).toFixed(1)}k tokens` : `${task.tokens} tokens`;
            }
            return `<div class="task-item"><div class="task-info"><span class="task-name">${displayName}</span><span class="task-detail">${detailText}</span></div><span class="task-status ${statusClass}">${statusText}</span></div>`;
        }).join('');
    } else {
        taskList.innerHTML = '<div class="task-item"><span class="task-name">🟢 无活跃任务 - 系统空闲</span></div>';
    }
}

// v5.25 - 纯手动模式，无自动加载
// 用户点击「刷新数据」按钮时才调用 fetchData()
console.log('[Cognitive Monitor] 手动模式已启用，点击按钮获取数据');
