// wifi_portal.ino
// WiFi配网AP模式示例代码
// 需要在主程序中集成

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

WebServer server(80);
bool portalRunning = false;

// 启动配网AP
void startWiFiPortal() {
    Serial.println("启动WiFi配网模式...");
    
    WiFi.mode(WIFI_AP);
    String apName = "MamaCounter-" + String(device_id).substring(3, 7);
    WiFi.softAP(apName.c_str(), "12345678");  // 默认密码
    
    Serial.print("AP名称: ");
    Serial.println(apName);
    Serial.print("AP地址: ");
    Serial.println(WiFi.softAPIP());
    
    // 设置路由
    server.on("/", HTTP_GET, handleRoot);
    server.on("/scan", HTTP_GET, handleScan);
    server.on("/connect", HTTP_POST, handleConnect);
    server.on("/status", HTTP_GET, handleStatus);
    
    server.begin();
    portalRunning = true;
    
    Serial.println("配网服务器已启动，访问 http://192.168.4.1");
}

// 处理配网页面
void handleRoot() {
    String html = R"(
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>妈妈计数器 - WiFi配置</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 400px;
            width: 100%;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo-icon {
            font-size: 60px;
            margin-bottom: 10px;
        }
        .logo h1 {
            font-size: 24px;
            color: #39ff14;
        }
        .logo p {
            color: rgba(255,255,255,0.5);
            font-size: 14px;
            margin-top: 5px;
        }
        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .card h2 {
            font-size: 16px;
            margin-bottom: 20px;
            color: #00ffff;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-size: 13px;
            color: rgba(255,255,255,0.6);
            margin-bottom: 8px;
        }
        select, input {
            width: 100%;
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #39ff14;
        }
        .btn {
            width: 100%;
            padding: 14px;
            background: #39ff14;
            color: #000;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn:hover {
            box-shadow: 0 0 20px #39ff14;
        }
        .btn:disabled {
            background: rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.3);
            cursor: not-allowed;
            box-shadow: none;
        }
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
        .status.success {
            background: rgba(0,255,136,0.15);
            color: #39ff14;
            display: block;
        }
        .status.error {
            background: rgba(255,100,100,0.15);
            color: #ff6464;
            display: block;
        }
        .status.loading {
            background: rgba(0,170,255,0.15);
            color: #00aaff;
            display: block;
        }
        .network-list {
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 15px;
        }
        .network-item {
            padding: 12px;
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            margin-bottom: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s;
        }
        .network-item:hover {
            background: rgba(0,255,136,0.1);
        }
        .network-item.selected {
            background: rgba(0,255,136,0.2);
            border: 1px solid #39ff14;
        }
        .signal {
            margin-left: auto;
            font-size: 12px;
        }
        .refresh-btn {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.3);
            color: #fff;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            margin-bottom: 15px;
        }
        .refresh-btn:hover {
            border-color: #39ff14;
            color: #39ff14;
        }
        .device-info {
            text-align: center;
            padding: 15px;
            background: rgba(0,255,136,0.05);
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .device-id {
            font-family: monospace;
            font-size: 18px;
            color: #39ff14;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <div class="logo-icon">👩‍👧</div>
            <h1>妈妈计数器</h1>
            <p>WiFi网络配置</p>
        </div>
        
        <div class="device-info">
            <div style="font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 5px;">设备ID</div>
            <div class="device-id">)" + String(device_id) + R"(</div>
        </div>
        
        <div class="card">
            <h2>📶 选择WiFi网络</h2>
            
            <button class="refresh-btn" onclick="scanNetworks()">🔄 刷新列表</button>
            
            <div class="network-list" id="networkList">
                <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px;">
                    点击刷新按钮扫描网络...
                </div>
            </div>
            
            <div class="form-group">
                <label>WiFi密码</label>
                <input type="password" id="password" placeholder="输入WiFi密码">
            </div>
            
            <button class="btn" id="connectBtn" onclick="connectWiFi()">连接网络</button>
            
            <div class="status" id="status"></div>
        </div>
        
        <div style="text-align: center; color: rgba(255,255,255,0.4); font-size: 12px;">
            配置完成后设备将自动重启
        </div>
    </div>
    
    <script>
        let selectedSSID = '';
        
        function scanNetworks() {
            const list = document.getElementById('networkList');
            list.innerHTML = '<div style="text-align: center; padding: 20px; color: #00aaff;">扫描中...</div>';
            
            fetch('/scan')
                .then(r => r.json())
                .then(data => {
                    list.innerHTML = '';
                    data.networks.forEach(net => {
                        const div = document.createElement('div');
                        div.className = 'network-item';
                        div.onclick = () => selectNetwork(net.ssid, div);
                        
                        const signal = net.rssi > -60 ? '●●●' : net.rssi > -70 ? '●●○' : '●○○';
                        const lock = net.encrypted ? '🔒 ' : '';
                        
                        div.innerHTML = `
                            <span>${lock}${net.ssid}</span>
                            <span class="signal">${signal}</span>
                        `;
                        list.appendChild(div);
                    });
                })
                .catch(err => {
                    list.innerHTML = '<div style="text-align: center; color: #ff6464;">扫描失败</div>';
                });
        }
        
        function selectNetwork(ssid, element) {
            selectedSSID = ssid;
            document.querySelectorAll('.network-item').forEach(el => el.classList.remove('selected'));
            element.classList.add('selected');
        }
        
        function connectWiFi() {
            if (!selectedSSID) {
                showStatus('请先选择一个WiFi网络', 'error');
                return;
            }
            
            const password = document.getElementById('password').value;
            const btn = document.getElementById('connectBtn');
            
            btn.disabled = true;
            showStatus('正在连接...', 'loading');
            
            fetch('/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ssid: selectedSSID, password: password })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showStatus('连接成功! 设备将在3秒后重启...', 'success');
                    setTimeout(() => location.reload(), 3000);
                } else {
                    showStatus('连接失败: ' + data.message, 'error');
                    btn.disabled = false;
                }
            })
            .catch(err => {
                showStatus('请求失败', 'error');
                btn.disabled = false;
            });
        }
        
        function showStatus(msg, type) {
            const status = document.getElementById('status');
            status.textContent = msg;
            status.className = 'status ' + type;
        }
        
        // 页面加载时自动扫描
        window.onload = scanNetworks;
    </script>
</body>
</html>
)";

    server.send(200, "text/html", html);
}

// 扫描WiFi网络
void handleScan() {
    Serial.println("扫描WiFi网络...");
    
    int n = WiFi.scanNetworks();
    
    DynamicJsonDocument doc(2048);
    JsonArray networks = doc.createNestedArray("networks");
    
    for (int i = 0; i < n; i++) {
        JsonObject net = networks.createNestedObject();
        net["ssid"] = WiFi.SSID(i);
        net["rssi"] = WiFi.RSSI(i);
        net["encrypted"] = WiFi.encryptionType(i) != WIFI_AUTH_OPEN;
    }
    
    String response;
    serializeJson(doc, response);
    server.send(200, "application/json", response);
}

// 连接WiFi
void handleConnect() {
    String body = server.arg("plain");
    
    DynamicJsonDocument doc(512);
    deserializeJson(doc, body);
    
    String ssid = doc["ssid"];
    String password = doc["password"];
    
    Serial.print("尝试连接: ");
    Serial.println(ssid);
    
    // 保存配置
    strncpy(wifi_ssid, ssid.c_str(), sizeof(wifi_ssid));
    strncpy(wifi_password, password.c_str(), sizeof(wifi_password));
    saveConfig();
    
    // 尝试连接
    WiFi.begin(wifi_ssid, wifi_password);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        attempts++;
    }
    
    DynamicJsonDocument resp(256);
    if (WiFi.status() == WL_CONNECTED) {
        resp["success"] = true;
        resp["ip"] = WiFi.localIP().toString();
        
        // 停止AP模式
        portalRunning = false;
        server.stop();
        WiFi.softAPdisconnect(true);
        
        state.wifi_connected = true;
        
        // 3秒后重启
        delay(3000);
        ESP.restart();
    } else {
        resp["success"] = false;
        resp["message"] = "无法连接到指定网络，请检查密码";
    }
    
    String response;
    serializeJson(resp, response);
    server.send(200, "application/json", response);
}

// 状态查询
void handleStatus() {
    DynamicJsonDocument doc(512);
    doc["device_id"] = device_id;
    doc["firmware"] = FIRMWARE_VERSION;
    doc["wifi_connected"] = state.wifi_connected;
    if (state.wifi_connected) {
        doc["ip"] = WiFi.localIP().toString();
        doc["rssi"] = WiFi.RSSI();
    }
    
    String response;
    serializeJson(doc, response);
    server.send(200, "application/json", response);
}

// 在loop中调用
void handlePortalClient() {
    if (portalRunning) {
        server.handleClient();
    }
}
