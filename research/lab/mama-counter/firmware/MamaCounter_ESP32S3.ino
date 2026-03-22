// MamaCounter_ESP32S3.ino
// 妈妈计数器 ESP32-S3 固件 v2.0
// 适配: 微雪 ESP32-S3 1.85寸 圆形LCD开发板
// 功能: 声音检测 + 实体按键 + WiFi同步 + 屏幕显示

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Preferences.h>

// ========== 硬件引脚定义 (微雪 ESP32-S3 1.85寸) ==========
#define PIN_LCD_CS      10
#define PIN_LCD_DC      9
#define PIN_LCD_RST     8
#define PIN_KEY1        0    // 左侧按键
#define PIN_KEY2        1    // 右侧按键
#define PIN_I2S_WS      4    // 麦克风 WS
#define PIN_I2S_SD      5    // 麦克风 SD
#define PIN_I2S_SCK     6    // 麦克风 SCK

// ========== 配置常量 ==========
const char* FIRMWARE_VERSION = "2.0.0";
const char* DEVICE_MODEL = "MC-ESP32S3-185";

// 默认WiFi配置 (首次使用需要配置)
char wifi_ssid[64] = "";
char wifi_password[64] = "";

// 服务器配置
const char* API_BASE_URL = "https://your-api-server.com/api";  // 部署后修改
const int SYNC_INTERVAL_MS = 300000;  // 5分钟同步一次

// 设备唯一ID (首次启动生成，存储在Flash)
char device_id[32] = "";

// ========== 状态变量 ==========
struct DeviceState {
    uint32_t today_count;
    uint32_t total_count;
    uint8_t current_mode;      // 0=计数, 1=今日, 2=本周, 3=电池
    bool in_settings_menu;
    uint8_t selected_menu_item;
    bool wifi_connected;
    uint8_t battery_percent;
    bool is_listening;
    bool is_flipped;           // 翻转静音状态
    
    // 时段统计
    uint16_t morning_count;
    uint16_t forenoon_count;
    uint16_t afternoon_count;
    uint16_t evening_count;
} state;

// 按键状态
struct ButtonState {
    bool key1_pressed;
    bool key2_pressed;
    uint32_t key1_press_time;
    uint32_t key2_press_time;
    bool key1_long_triggered;
    bool key2_long_triggered;
} buttons;

// 时间记录
uint32_t last_sync_time = 0;
uint32_t last_display_update = 0;
String current_date = "";

// 存储对象
Preferences prefs;

// ========== 函数声明 ==========
void setupHardware();
void setupWiFi();
void generateDeviceID();
void loadConfig();
void saveConfig();
void loadDailyData();
void saveDailyData();
void handleButtons();
void handleKey1(bool shortPress);
void handleKey2(bool shortPress);
void detectAudio();
void updateDisplay();
void drawCountMode();
void drawTodayMode();
void drawWeekMode();
void drawBatteryMode();
void drawSettingsMenu();
void syncToCloud();
void enterDeepSleep();
void checkFlipMute();
String getCurrentDate();
int getCurrentHour();
void resetDailyCount();

// ========== 初始化 ==========
void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("\n========================================");
    Serial.println("  妈妈计数器 ESP32-S3 固件 v2.0");
    Serial.println("  MamaCounter Firmware");
    Serial.println("========================================\n");
    
    // 初始化存储
    prefs.begin("mama_counter", false);
    
    // 加载或生成设备ID
    loadConfig();
    if (strlen(device_id) == 0) {
        generateDeviceID();
        saveConfig();
    }
    
    Serial.print("设备ID: ");
    Serial.println(device_id);
    
    // 初始化硬件
    setupHardware();
    
    // 初始化状态
    state.today_count = 0;
    state.total_count = 0;
    state.current_mode = 0;
    state.in_settings_menu = false;
    state.selected_menu_item = 0;
    state.wifi_connected = false;
    state.battery_percent = 78;
    state.is_listening = true;
    state.is_flipped = false;
    state.morning_count = 0;
    state.forenoon_count = 0;
    state.afternoon_count = 0;
    state.evening_count = 0;
    
    buttons.key1_pressed = false;
    buttons.key2_pressed = false;
    buttons.key1_long_triggered = false;
    buttons.key2_long_triggered = false;
    
    // 加载今日数据
    loadDailyData();
    current_date = getCurrentDate();
    
    // 尝试连接WiFi
    if (strlen(wifi_ssid) > 0) {
        setupWiFi();
    }
    
    Serial.println("初始化完成，开始运行...");
    Serial.println("提示: 使用Web配置页面设置WiFi");
}

// ========== 主循环 ==========
void loop() {
    // 检查日期变更
    String newDate = getCurrentDate();
    if (newDate != current_date) {
        saveDailyData();  // 保存旧日期数据
        current_date = newDate;
        resetDailyCount();  // 重置新日期计数
        loadDailyData();
    }
    
    // 处理按键
    handleButtons();
    
    // 音频检测 (如果启用)
    if (state.is_listening && !state.is_flipped) {
        detectAudio();
    }
    
    // 检查翻转静音
    checkFlipMute();
    
    // 更新显示 (限制刷新率)
    if (millis() - last_display_update > 100) {
        updateDisplay();
        last_display_update = millis();
    }
    
    // WiFi同步
    if (state.wifi_connected && millis() - last_sync_time > SYNC_INTERVAL_MS) {
        syncToCloud();
        last_sync_time = millis();
    }
    
    delay(10);  // 短暂延时降低功耗
}

// ========== 硬件初始化 ==========
void setupHardware() {
    // 初始化按键
    pinMode(PIN_KEY1, INPUT_PULLUP);
    pinMode(PIN_KEY2, INPUT_PULLUP);
    
    // TODO: 初始化LCD屏幕
    // TODO: 初始化I2S麦克风
    // TODO: 初始化陀螺仪
    
    Serial.println("硬件初始化完成");
}

// ========== WiFi设置 ==========
void setupWiFi() {
    Serial.print("连接WiFi: ");
    Serial.println(wifi_ssid);
    
    WiFi.begin(wifi_ssid, wifi_password);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        state.wifi_connected = true;
        Serial.println("\nWiFi已连接!");
        Serial.print("IP地址: ");
        Serial.println(WiFi.localIP());
    } else {
        state.wifi_connected = false;
        Serial.println("\nWiFi连接失败");
    }
}

// ========== 生成设备唯一ID ==========
void generateDeviceID() {
    uint64_t chipid = ESP.getEfuseMac();
    snprintf(device_id, sizeof(device_id), "MC-%04X%08X", 
             (uint32_t)(chipid >> 32), (uint32_t)chipid);
}

// ========== 加载配置 ==========
void loadConfig() {
    prefs.getString("device_id", device_id, sizeof(device_id));
    prefs.getString("wifi_ssid", wifi_ssid, sizeof(wifi_ssid));
    prefs.getString("wifi_pass", wifi_password, sizeof(wifi_password));
}

// ========== 保存配置 ==========
void saveConfig() {
    prefs.putString("device_id", device_id);
    prefs.putString("wifi_ssid", wifi_ssid);
    prefs.putString("wifi_pass", wifi_password);
}

// ========== 加载今日数据 ==========
void loadDailyData() {
    String key = "count_" + getCurrentDate();
    state.today_count = prefs.getUInt(key.c_str(), 0);
    state.total_count = prefs.getUInt("total_count", 0);
    
    String periodKey = "period_" + getCurrentDate();
    String periodData = prefs.getString(periodKey.c_str(), "0,0,0,0");
    
    // 解析时段数据
    sscanf(periodData.c_str(), "%hu,%hu,%hu,%hu",
           &state.morning_count, &state.forenoon_count,
           &state.afternoon_count, &state.evening_count);
}

// ========== 保存今日数据 ==========
void saveDailyData() {
    String key = "count_" + getCurrentDate();
    prefs.putUInt(key.c_str(), state.today_count);
    prefs.putUInt("total_count", state.total_count);
    
    String periodKey = "period_" + getCurrentDate();
    char periodData[32];
    snprintf(periodData, sizeof(periodData), "%d,%d,%d,%d",
             state.morning_count, state.forenoon_count,
             state.afternoon_count, state.evening_count);
    prefs.putString(periodKey.c_str(), periodData);
}

// ========== 重置每日计数 ==========
void resetDailyCount() {
    state.today_count = 0;
    state.morning_count = 0;
    state.forenoon_count = 0;
    state.afternoon_count = 0;
    state.evening_count = 0;
}

// ========== 按键处理 ==========
void handleButtons() {
    // KEY1 状态检测
    bool key1_state = !digitalRead(PIN_KEY1);  // 低电平有效
    if (key1_state && !buttons.key1_pressed) {
        // 按键按下
        buttons.key1_pressed = true;
        buttons.key1_press_time = millis();
        buttons.key1_long_triggered = false;
    } else if (!key1_state && buttons.key1_pressed) {
        // 按键释放
        buttons.key1_pressed = false;
        uint32_t pressDuration = millis() - buttons.key1_press_time;
        if (pressDuration < 3000) {
            handleKey1(true);  // 短按
        }
    } else if (key1_state && buttons.key1_pressed && !buttons.key1_long_triggered) {
        // 长按检测
        if (millis() - buttons.key1_press_time >= 3000) {
            buttons.key1_long_triggered = true;
            handleKey1(false);  // 长按
        }
    }
    
    // KEY2 状态检测
    bool key2_state = !digitalRead(PIN_KEY2);
    if (key2_state && !buttons.key2_pressed) {
        buttons.key2_pressed = true;
        buttons.key2_press_time = millis();
        buttons.key2_long_triggered = false;
    } else if (!key2_state && buttons.key2_pressed) {
        buttons.key2_pressed = false;
        uint32_t pressDuration = millis() - buttons.key2_press_time;
        if (pressDuration < 5000) {
            handleKey2(true);
        }
    } else if (key2_state && buttons.key2_pressed && !buttons.key2_long_triggered) {
        if (millis() - buttons.key2_press_time >= 5000) {
            buttons.key2_long_triggered = true;
            handleKey2(false);
        }
    }
}

// ========== KEY1 处理 ==========
void handleKey1(bool shortPress) {
    if (shortPress) {
        if (state.in_settings_menu) {
            // 菜单中: 循环选择
            state.selected_menu_item = (state.selected_menu_item + 1) % 6;
        } else {
            // 正常模式: 切换显示模式
            state.current_mode = (state.current_mode + 1) % 4;
        }
    } else {
        // 长按
        if (state.in_settings_menu) {
            state.in_settings_menu = false;
        } else {
            state.in_settings_menu = true;
            state.selected_menu_item = 0;
        }
    }
}

// ========== KEY2 处理 ==========
void handleKey2(bool shortPress) {
    if (shortPress) {
        if (state.in_settings_menu) {
            // 执行选中菜单项
            switch (state.selected_menu_item) {
                case 0:  // 声纹录制
                    // TODO: 进入声纹录制模式
                    Serial.println("进入声纹录制...");
                    break;
                case 1:  // WiFi配置
                    // TODO: 启动AP模式，提供Web配置
                    Serial.println("启动WiFi配置...");
                    break;
                case 2:  // 灵敏度
                    // TODO: 调节灵敏度
                    break;
                case 3:  // 设备ID
                    // 显示设备ID
                    break;
                case 4:  // 恢复出厂
                    // TODO: 确认后清除数据
                    break;
                case 5:  // 返回
                    state.in_settings_menu = false;
                    break;
            }
        }
    } else {
        // 长按: 开关机
        Serial.println("关机确认...");
        // TODO: 显示确认对话框
        // enterDeepSleep();
    }
}

// ========== 音频检测 ==========
void detectAudio() {
    // TODO: 实现I2S音频采集和"妈妈"关键词检测
    // 这里使用模拟数据演示
    
    static uint32_t lastTrigger = 0;
    if (millis() - lastTrigger > 5000) {  // 每5秒模拟一次触发
        // 模拟检测到"妈妈"
        // 实际实现需要使用ESP-SR库或自定义算法
        
        // 更新计数
        state.today_count++;
        state.total_count++;
        
        // 更新时段统计
        int hour = getCurrentHour();
        if (hour < 9) state.morning_count++;
        else if (hour < 12) state.forenoon_count++;
        else if (hour < 18) state.afternoon_count++;
        else state.evening_count++;
        
        // 保存数据
        saveDailyData();
        
        Serial.print("检测到'妈妈'! 今日: ");
        Serial.println(state.today_count);
        
        lastTrigger = millis();
    }
}

// ========== 更新显示 ==========
void updateDisplay() {
    if (state.in_settings_menu) {
        drawSettingsMenu();
    } else {
        switch (state.current_mode) {
            case 0: drawCountMode(); break;
            case 1: drawTodayMode(); break;
            case 2: drawWeekMode(); break;
            case 3: drawBatteryMode(); break;
        }
    }
}

// ========== 显示模式: 计数 ==========
void drawCountMode() {
    // TODO: 实现LCD绘制
    // 显示大数字: 今日已喊妈妈 XX次
    Serial.print("[显示] 计数模式 - 今日: ");
    Serial.println(state.today_count);
}

// ========== 显示模式: 今日统计 ==========
void drawTodayMode() {
    // TODO: 绘制时段分布柱状图
    Serial.println("[显示] 今日统计模式");
}

// ========== 显示模式: 本周趋势 ==========
void drawWeekMode() {
    // TODO: 绘制7天折线图
    Serial.println("[显示] 本周趋势模式");
}

// ========== 显示模式: 电池状态 ==========
void drawBatteryMode() {
    // TODO: 显示电池信息和系统状态
    Serial.print("[显示] 电池模式 - ");
    Serial.print(state.battery_percent);
    Serial.println("%");
}

// ========== 设置菜单 ==========
void drawSettingsMenu() {
    const char* menuItems[] = {
        "1. 声纹录制",
        "2. WiFi配置",
        "3. 灵敏度调节",
        "4. 查看设备ID",
        "5. 恢复出厂",
        "6. 返回"
    };
    
    Serial.println("\n===== 设置菜单 =====");
    for (int i = 0; i < 6; i++) {
        if (i == state.selected_menu_item) {
            Serial.print("> ");
        } else {
            Serial.print("  ");
        }
        Serial.println(menuItems[i]);
    }
    Serial.println("====================\n");
}

// ========== 同步到云端 ==========
void syncToCloud() {
    if (!state.wifi_connected) return;
    
    HTTPClient http;
    String url = String(API_BASE_URL) + "/devices/" + device_id + "/sync";
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    // 构建JSON数据
    StaticJsonDocument<512> doc;
    doc["device_id"] = device_id;
    doc["firmware_version"] = FIRMWARE_VERSION;
    doc["timestamp"] = millis();
    doc["today_count"] = state.today_count;
    doc["total_count"] = state.total_count;
    doc["battery"] = state.battery_percent;
    
    JsonObject periods = doc.createNestedObject("periods");
    periods["morning"] = state.morning_count;
    periods["forenoon"] = state.forenoon_count;
    periods["afternoon"] = state.afternoon_count;
    periods["evening"] = state.evening_count;
    
    String payload;
    serializeJson(doc, payload);
    
    int httpCode = http.POST(payload);
    
    if (httpCode == 200) {
        String response = http.getString();
        Serial.println("数据同步成功");
        
        // 解析服务器响应 (可能包含配置更新)
        StaticJsonDocument<256> respDoc;
        deserializeJson(respDoc, response);
        
        // TODO: 处理服务器返回的配置
    } else {
        Serial.print("同步失败: ");
        Serial.println(httpCode);
    }
    
    http.end();
}

// ========== 进入深度睡眠 ==========
void enterDeepSleep() {
    Serial.println("进入深度睡眠...");
    saveDailyData();
    
    // 配置唤醒源 (按键唤醒)
    esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_KEY1, 0);
    esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_KEY2, 0);
    
    esp_deep_sleep_start();
}

// ========== 检查翻转静音 ==========
void checkFlipMute() {
    // TODO: 读取陀螺仪数据，检测设备是否翻转
    // 如果翻转超过阈值，设置 state.is_flipped = true
}

// ========== 获取当前日期 ==========
String getCurrentDate() {
    // TODO: 使用NTP获取真实时间
    // 临时返回模拟日期
    return "2026-03-22";
}

// ========== 获取当前小时 ==========
int getCurrentHour() {
    // TODO: 使用NTP获取真实时间
    return 14;  // 临时返回下午2点
}
