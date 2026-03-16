// 按需监控模式 v5.25
// 基本概念：认知负载是用户需要时才关心的数据

const MonitorMode = {
    IDLE: 'idle',
    MONITORING: 'monitoring'
};

let currentMode = MonitorMode.IDLE;
let monitorTimer = null;
let countdownTimer = null;
let remainingSeconds = 0;
let lastDataTimestamp = null;

const API_URL = 'http://101.126.54.134/api/cognitive/status';

async function fetchWithTimeout(url, timeout = 3000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    try {
        const response = await fetch(url, {
            signal: controller.signal,
            headers: { 'Accept': 'application/json' }
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
}

async function fetchData() {
    try {
        const cacheBuster = `?t=${Date.now()}`;
        const response = await fetchWithTimeout(API_URL + cacheBuster, 3000);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        lastDataTimestamp = data.timestamp;
        updateUI(data);
        updateStatusDisplay();
    } catch (e) {
        console.error('[Cognitive Monitor] 获取失败:', e.message);
        showError('⚠️ 连接失败');
    }
}

function showError(msg) {
    document.getElementById('radioStatusText').textContent = msg;
    document.getElementById('radioStatusText').style.color = '#ef4444';
}

function updateStatusDisplay() {
    const modeEl = document.getElementById('monitorMode');
    const timeEl = document.getElementById('monitorTime');
    const btnEl = document.getElementById('monitorBtn');
    
    if (!modeEl || !timeEl || !btnEl) return;
    
    if (currentMode === MonitorMode.MONITORING) {
        const mins = Math.floor(remainingSeconds / 60);
        const secs = remainingSeconds % 60;
        modeEl.textContent = '🔴 监控中';
        modeEl.style.color = '#ef4444';
        timeEl.textContent = `${mins}:${secs.toString().padStart(2, '0')} 后停止`;
        btnEl.textContent = '停止监控';
        btnEl.classList.add('active');
    } else {
        modeEl.textContent = '🟢 静止模式';
        modeEl.style.color = '#4ade80';
        const timeStr = lastDataTimestamp 
            ? new Date(lastDataTimestamp).toLocaleTimeString('zh-CN')
            : '--:--:--';
        timeEl.textContent = `更新于 ${timeStr}`;
        btnEl.textContent = '▶ 5分钟监控';
        btnEl.classList.remove('active');
    }
}

function toggleMonitor() {
    if (currentMode === MonitorMode.IDLE) {
        startMonitoring();
    } else {
        stopMonitoring();
    }
}

function startMonitoring() {
    currentMode = MonitorMode.MONITORING;
    remainingSeconds = 300;
    fetchData();
    monitorTimer = setInterval(() => fetchData(), 15000);
    countdownTimer = setInterval(() => {
        remainingSeconds--;
        if (remainingSeconds <= 0) stopMonitoring();
        updateStatusDisplay();
    }, 1000);
    updateStatusDisplay();
}

function stopMonitoring() {
    currentMode = MonitorMode.IDLE;
    if (monitorTimer) { clearInterval(monitorTimer); monitorTimer = null; }
    if (countdownTimer) { clearInterval(countdownTimer); countdownTimer = null; }
    remainingSeconds = 0;
    updateStatusDisplay();
}

function manualRefresh() {
    fetchData();
}

function updateUI(data) {
    const score = data.cognitive_score || 0;
    const timeStr = new Date().toLocaleTimeString('zh-CN', {hour12: false});
    document.getElementById('lastHeartbeat').textContent = timeStr;
    
    const cpuEl = document.getElementById('cpuValue');
    const memEl = document.getElementById('memoryValue');
    if (cpuEl) cpuEl.textContent = (data.cpu_percent || 0) + '%';
    if (memEl) memEl.textContent = (data.memory_percent || 0) + '%';
    
    const connStatus = score >= 65 ? '高负载' : score >= 45 ? '中等' : score >= 25 ? '轻负载' : '空闲';
    const connColor = score >= 65 ? 'high' : score >= 45 ? 'busy' : 'online';
    const connEl = document.getElementById('connectionValue');
    if (connEl) {
        connEl.textContent = connStatus;
        connEl.className = 'compact-status-value ' + connColor;
    }
    
    const agentStatusEl = document.getElementById('agentStatusValue');
    if (agentStatusEl) {
        agentStatusEl.textContent = data.pending_count > 0 ? 'busy' : 'active';
        agentStatusEl.className = 'compact-status-value ' + (data.pending_count > 0 ? 'busy' : 'online');
    }
    
    const radioPercent = document.getElementById('radioPercent');
    const radioPointer = document.getElementById('radioPointer');
    const radioStatusText = document.getElementById('radioStatusText');
    const zones = [document.getElementById('zoneIdle'), document.getElementById('zoneLow'), 
                   document.getElementById('zoneMedium'), document.getElementById('zoneHigh')];
    zones.forEach(z => z && z.classList.remove('active'));
    
    if (radioPercent && radioPointer) {
        const numSpan = radioPercent.querySelector('.percent-number');
        if (numSpan) numSpan.textContent = score;
        radioPointer.style.left = score + '%';
        
        let statusText = '🟢 空闲 - 立即响应', pointerClass = 'idle', percentClass = 'idle', activeZone = zones[0], statusColor = '#4ade80';
        if (score >= 65) {
            statusText = '🔴 高负载 - 建议等待'; pointerClass = 'high'; percentClass = 'high'; activeZone = zones[3]; statusColor = '#ef4444';
        } else if (score >= 45) {
            statusText = '🟡 中等负载 - 简单任务'; pointerClass = 'medium'; percentClass = 'medium'; activeZone = zones[2]; statusColor = '#eab308';
        } else if (score >= 25) {
            statusText = '🔵 轻负载 - 30秒内响应'; pointerClass = 'low'; percentClass = 'low'; activeZone = zones[1]; statusColor = '#60a5fa';
        }
        
        radioPointer.className = 'pointer ' + pointerClass;
        radioPercent.className = 'percent-number ' + percentClass;
        radioStatusText.textContent = statusText;
        radioStatusText.style.color = statusColor;
        if (activeZone) activeZone.classList.add('active');
    }
    
    document.getElementById('sessionsValue').textContent = data.active_sessions || 0;
    document.getElementById('pendingValue').textContent = data.pending_count || 0;
    document.getElementById('processingValue').textContent = data.processing_count || 0;
    document.getElementById('tokensValue').textContent = (data.total_tokens || 0) > 1000 
        ? ((data.total_tokens / 1000).toFixed(1) + 'k') : (data.total_tokens || 0);
    document.getElementById('suggestionValue').textContent = data.suggestion || '可立即响应';
    
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

// 初始加载
fetchData();
updateStatusDisplay();
