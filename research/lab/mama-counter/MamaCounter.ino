/**
 * 妈妈计数器 - Mama Counter
 * 基于 ESP32-Display (1.28寸圆形LCD, GC9A01驱动)
 * 
 * 硬件: ESP32-C3 + 1.28寸圆形LCD + 麦克风模块
 * 功能: 检测"妈妈"关键词，计数并显示在圆形屏幕上
 * 
 * 作者: Shrimp Jetton
 * 日期: 2026-03-21
 */

#include <TFT_eSPI.h>  // 屏幕驱动库
#include <SPI.h>

// ==================== 引脚定义 ====================
// ESP32-C3-Display 默认引脚 (1.28寸圆形LCD)
// LCD_SPI_CS     10
// LCD_SPI_SCK    6
// LCD_SPI_MOSI   7
// LCD_SPI_DC     2
// LCD_SPI_RST    -1 (内部复位)
// LCD_BACKLIGHT  3

// 麦克风模块 (MAX9814)
#define MIC_PIN         0       // 麦克风模拟输入引脚 (ADC)
#define MIC_DIGITAL_PIN 1       // 麦克风数字输出引脚 (可选)

// 按键
#define BUTTON_PIN      4       // 功能按键

// ==================== 配置参数 ====================
#define SCREEN_WIDTH    240
#define SCREEN_HEIGHT   240
#define CENTER_X        120
#define CENTER_Y        120

// 声音检测参数
#define SOUND_THRESHOLD     500     // 声音阈值 (0-4095)
#define TRIGGER_COOLDOWN    2000    // 触发冷却时间 (ms)
#define SAMPLE_WINDOW       50      // 采样窗口 (ms)

// 显示颜色
#define COLOR_BG        TFT_BLACK
#define COLOR_PRIMARY   0x07E0      // 绿色
#define COLOR_SECONDARY 0xFFE0      // 黄色
#define COLOR_ACCENT    0xF800      // 红色
#define COLOR_TEXT      TFT_WHITE
#define COLOR_GRAY      0x8410      // 灰色

// ==================== 全局变量 ====================
TFT_eSPI tft = TFT_eSPI();

// 计数器状态
uint32_t mamaCount = 0;
uint32_t lastTriggerTime = 0;
bool isListening = true;

// 电池状态
uint8_t batteryLevel = 85;

// 波形数据
int waveData[12] = {0};
int waveIndex = 0;

// ==================== 初始化 ====================
void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Mama Counter Starting ===");
    
    // 初始化引脚
    pinMode(MIC_PIN, INPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    
    // 初始化屏幕
    initDisplay();
    
    // 显示启动画面
    showBootScreen();
    delay(2000);
    
    // 清空屏幕
    tft.fillScreen(COLOR_BG);
    
    // 绘制静态UI元素
    drawStaticUI();
    
    Serial.println("System Ready!");
}

// ==================== 主循环 ====================
void loop() {
    // 读取麦克风
    int soundLevel = readMicrophone();
    
    // 更新波形显示
    updateWaveform(soundLevel);
    
    // 检测触发
    if (isListening && soundLevel > SOUND_THRESHOLD) {
        if (millis() - lastTriggerTime > TRIGGER_COOLDOWN) {
            triggerMamaDetected();
        }
    }
    
    // 检查按键
    if (digitalRead(BUTTON_PIN) == LOW) {
        delay(50); // 消抖
        if (digitalRead(BUTTON_PIN) == LOW) {
            handleButtonPress();
            while (digitalRead(BUTTON_PIN) == LOW); // 等待释放
        }
    }
    
    // 更新状态显示
    updateStatusDisplay();
    
    delay(20); // 50Hz刷新率
}

// ==================== 显示初始化 ====================
void initDisplay() {
    tft.init();
    tft.setRotation(0);  // 圆形屏幕无需旋转
    tft.fillScreen(COLOR_BG);
    tft.setTextFont(2);
}

// ==================== 启动画面 ====================
void showBootScreen() {
    tft.fillScreen(COLOR_BG);
    
    // 外圈
    tft.drawCircle(CENTER_X, CENTER_Y, 110, COLOR_PRIMARY);
    tft.drawCircle(CENTER_X, CENTER_Y, 108, COLOR_PRIMARY);
    
    // 标题
    tft.setTextColor(COLOR_PRIMARY);
    tft.setTextSize(2);
    tft.setTextDatum(MC_DATUM);
    tft.drawString("MAMA COUNTER", CENTER_X, CENTER_Y - 30);
    
    // 版本
    tft.setTextColor(COLOR_GRAY);
    tft.setTextSize(1);
    tft.drawString("v1.0 | ESP32-Display", CENTER_X, CENTER_Y);
    
    // 加载动画
    for (int i = 0; i < 360; i += 10) {
        int x1 = CENTER_X + 80 * cos(i * PI / 180);
        int y1 = CENTER_Y + 80 * sin(i * PI / 180);
        int x2 = CENTER_X + 80 * cos((i + 10) * PI / 180);
        int y2 = CENTER_Y + 80 * sin((i + 10) * PI / 180);
        tft.drawLine(x1, y1, x2, y2, COLOR_PRIMARY);
        delay(10);
    }
}

// ==================== 绘制静态UI ====================
void drawStaticUI() {
    // 外圈装饰
    tft.drawCircle(CENTER_X, CENTER_Y, 118, COLOR_GRAY);
    tft.drawCircle(CENTER_X, CENTER_Y, 116, COLOR_GRAY);
    
    // 标题
    tft.setTextColor(COLOR_GRAY);
    tft.setTextSize(1);
    tft.setTextDatum(TC_DATUM);
    tft.drawString("MAMA COUNT", CENTER_X, 40);
    
    // 单位
    tft.setTextDatum(BC_DATUM);
    tft.drawString("times", CENTER_X, 180);
}

// ==================== 读取麦克风 ====================
int readMicrophone() {
    // 简单的峰值检测
    int maxVal = 0;
    int minVal = 4095;
    
    for (int i = 0; i < 20; i++) {
        int val = analogRead(MIC_PIN);
        if (val > maxVal) maxVal = val;
        if (val < minVal) minVal = val;
        delayMicroseconds(100);
    }
    
    // 计算峰峰值
    int peakToPeak = maxVal - minVal;
    
    // 映射到显示范围 (0-100)
    return map(peakToPeak, 0, 1000, 0, 100);
}

// ==================== 更新波形 ====================
void updateWaveform(int level) {
    // 更新波形数据
    waveData[waveIndex] = level;
    waveIndex = (waveIndex + 1) % 12;
    
    // 绘制波形 (底部半圆区域)
    int barWidth = 8;
    int barGap = 4;
    int startX = CENTER_X - (12 * (barWidth + barGap)) / 2 + barGap;
    int baseY = 200;
    
    for (int i = 0; i < 12; i++) {
        int idx = (waveIndex + i) % 12;
        int height = map(waveData[idx], 0, 100, 2, 25);
        int x = startX + i * (barWidth + barGap);
        
        // 清除旧条
        tft.fillRect(x, baseY - 30, barWidth, 30, COLOR_BG);
        
        // 绘制新条
        uint16_t color = (i == 11) ? COLOR_PRIMARY : COLOR_GRAY;
        tft.fillRect(x, baseY - height, barWidth, height, color);
    }
}

// ==================== 触发检测 ====================
void triggerMamaDetected() {
    lastTriggerTime = millis();
    mamaCount++;
    
    Serial.print("Mama detected! Count: ");
    Serial.println(mamaCount);
    
    // 视觉反馈
    drawCountDisplay(true);
    
    // 屏幕闪烁效果
    for (int i = 0; i < 3; i++) {
        tft.fillCircle(CENTER_X, CENTER_Y, 100, COLOR_PRIMARY);
        delay(50);
        tft.fillCircle(CENTER_X, CENTER_Y, 100, COLOR_BG);
        drawStaticUI();  // 重绘静态元素
        delay(50);
    }
    
    // 更新显示
    drawCountDisplay(false);
}

// ==================== 绘制计数显示 ====================
void drawCountDisplay(bool highlight) {
    // 清除计数区域
    tft.fillCircle(CENTER_X, CENTER_Y, 90, COLOR_BG);
    
    // 数字
    tft.setTextDatum(MC_DATUM);
    if (highlight) {
        tft.setTextColor(COLOR_PRIMARY);
        tft.setTextSize(4);
    } else {
        tft.setTextColor(COLOR_TEXT);
        tft.setTextSize(4);
    }
    
    String countStr = String(mamaCount);
    tft.drawString(countStr, CENTER_X, CENTER_Y + 10);
}

// ==================== 更新状态显示 ====================
void updateStatusDisplay() {
    // 电池图标 (右上角)
    int batX = 180;
    int batY = 20;
    
    // 清除旧图标
    tft.fillRect(batX, batY, 30, 15, COLOR_BG);
    
    // 绘制电池外框
    tft.drawRect(batX, batY, 25, 12, COLOR_GRAY);
    tft.fillRect(batX + 25, batY + 3, 3, 6, COLOR_GRAY);
    
    // 填充电量
    int fillWidth = map(batteryLevel, 0, 100, 0, 21);
    uint16_t batColor = (batteryLevel > 20) ? COLOR_PRIMARY : COLOR_ACCENT;
    tft.fillRect(batX + 2, batY + 2, fillWidth, 8, batColor);
    
    // 定期更新计数显示 (避免闪烁)
    static uint32_t lastUpdate = 0;
    if (millis() - lastUpdate > 1000) {
        drawCountDisplay(false);
        lastUpdate = millis();
    }
}

// ==================== 按键处理 ====================
void handleButtonPress() {
    static uint32_t pressStartTime = 0;
    
    if (pressStartTime == 0) {
        pressStartTime = millis();
    } else {
        uint32_t pressDuration = millis() - pressStartTime;
        
        if (pressDuration > 2000) {
            // 长按2秒 - 重置计数
            mamaCount = 0;
            tft.fillScreen(COLOR_BG);
            drawStaticUI();
            drawCountDisplay(false);
            
            tft.setTextColor(COLOR_ACCENT);
            tft.setTextDatum(MC_DATUM);
            tft.drawString("RESET", CENTER_X, CENTER_Y - 50);
            delay(1000);
            
            tft.fillScreen(COLOR_BG);
            drawStaticUI();
            drawCountDisplay(false);
            
            Serial.println("Counter reset!");
        } else {
            // 短按 - 切换监听模式
            isListening = !isListening;
            
            tft.setTextColor(isListening ? COLOR_PRIMARY : COLOR_ACCENT);
            tft.setTextDatum(MC_DATUM);
            tft.drawString(isListening ? "LISTENING" : "PAUSED", CENTER_X, CENTER_Y - 50);
            delay(500);
            
            // 清除提示
            tft.fillCircle(CENTER_X, CENTER_Y - 50, 50, COLOR_BG);
            drawCountDisplay(false);
            
            Serial.println(isListening ? "Listening resumed" : "Listening paused");
        }
        
        pressStartTime = 0;
    }
}

// ==================== 低功耗模式 ====================
void enterDeepSleep(uint32_t sleepTimeMs) {
    Serial.println("Entering deep sleep...");
    
    // 关闭屏幕背光
    // digitalWrite(LCD_BACKLIGHT, LOW);
    
    // 配置定时唤醒
    esp_sleep_enable_timer_wakeup(sleepTimeMs * 1000);
    
    // 进入Deep Sleep
    esp_deep_sleep_start();
}

// ==================== 电池检测 ====================
uint8_t readBatteryLevel() {
    // 读取电池电压 (假设使用分压电阻连接到ADC)
    int raw = analogRead(1);  // 电池检测引脚
    float voltage = raw * 3.3 / 4095.0 * 2.0;  // 根据分压比调整
    
    // 映射到百分比 (3.3V-4.2V)
    int percentage = map((int)(voltage * 100), 330, 420, 0, 100);
    return constrain(percentage, 0, 100);
}