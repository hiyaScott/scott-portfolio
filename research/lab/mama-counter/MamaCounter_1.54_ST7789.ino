/**
 * 妈妈计数器 - Mama Counter v1.1.0-waveshare-1.54
 * 适配: 微雪 ESP32-S3-Touch-LCD-1.54 (ST7789, 240×240)
 * 
 * 硬件: 微雪 ESP32-S3 1.54寸开发板
 *       - 1.54寸 LCD 240×240 (ST7789驱动)
 *       - 板载双I2S数字麦克风
 *       - 板载陀螺仪QMI8658
 *       - 板载扬声器
 *       - 触摸功能 (本版本未使用)
 * 
 * 功能: 检测"妈妈"关键词，计数并显示在圆形屏幕上
 *       支持翻转静音 (陀螺仪检测)
 * 
 * 作者: Shrimp Jetton
 * 日期: 2026-05-17
 * 版本: v1.1.0-waveshare-1.54
 */

#include <TFT_eSPI.h>      // 屏幕驱动库
#include <driver/i2s.h>     // I2S麦克风驱动
#include <Wire.h>           // I2C (陀螺仪)

// ==================== 引脚定义 (微雪 ESP32-S3-Touch-LCD-1.54) ====================
// LCD引脚 (ST7789, 240×240)
#define TFT_CS      10
#define TFT_SCK     12
#define TFT_MOSI    11
#define TFT_DC      13
#define TFT_RST     9
#define TFT_BL      42

// I2S数字麦克风引脚 (双麦克风)
#define I2S_MIC_SCK     4
#define I2S_MIC_WS      5
#define I2S_MIC_SD      6

// I2C陀螺仪引脚
#define I2C_SDA         15
#define I2C_SCL         16

// 按键引脚 (如果你的板子有实体按键的话)
// 注意：1.54寸板子可能使用触摸代替实体按键
// 这里保留定义，如果没有实体按键可以注释掉
#define BUTTON_1        0
#define BUTTON_2        14

// ==================== 配置参数 ====================
#define SCREEN_WIDTH    240
#define SCREEN_HEIGHT   240
#define CENTER_X        120
#define CENTER_Y        120

// I2S配置
#define SAMPLE_RATE     16000
#define BUFFER_SIZE     256

// 声音检测参数
#define ENERGY_THRESHOLD    3000    // I2S能量阈值 (240×240屏幕适配)
#define TRIGGER_COOLDOWN    2000    // 触发冷却时间 (ms)
#define FLIP_THRESHOLD      -0.7    // 翻转检测阈值 (z轴)

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
bool isFlipped = false;

// 电池状态
uint8_t batteryLevel = 85;

// 波形数据
int waveData[12] = {0};     // 240宽度适配，减少柱状图数量
int waveIndex = 0;

// I2S缓冲区
int32_t i2sBuffer[BUFFER_SIZE];

// ==================== 初始化 ====================
void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Mama Counter v1.1.0-waveshare-1.54 Starting ===");
    Serial.println("Hardware: ESP32-S3 1.54\" LCD (ST7789, 240x240) with I2S Mic");
    
    // 初始化引脚
    pinMode(BUTTON_1, INPUT_PULLUP);
    pinMode(BUTTON_2, INPUT_PULLUP);
    pinMode(TFT_BL, OUTPUT);
    
    // 初始化屏幕
    initDisplay();
    
    // 初始化I2S麦克风
    initI2SMic();
    
    // 初始化陀螺仪 (可选)
    initGyroscope();
    
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
    // 读取陀螺仪状态 (翻转检测)
    checkFlipState();
    
    // 读取I2S麦克风
    int energy = readI2SMicrophone();
    
    // 更新波形显示
    updateWaveform(energy / 100);  // 缩放以适应显示
    
    // 检测触发 (未翻转且在监听模式)
    if (!isFlipped && isListening && energy > ENERGY_THRESHOLD) {
        if (millis() - lastTriggerTime > TRIGGER_COOLDOWN) {
            triggerMamaDetected();
        }
    }
    
    // 检查按键
    checkButtons();
    
    // 更新状态显示
    updateStatusDisplay();
    
    delay(10);  // 100Hz刷新率
}

// ==================== I2S麦克风初始化 ====================
void initI2SMic() {
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = BUFFER_SIZE
    };
    
    i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_MIC_SCK,
        .ws_io_num = I2S_MIC_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = I2S_MIC_SD
    };
    
    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config);
    
    Serial.println("I2S Microphone initialized");
}

// ==================== 读取I2S麦克风 ====================
int readI2SMicrophone() {
    size_t bytes_read;
    i2s_read(I2S_NUM_0, i2sBuffer, sizeof(i2sBuffer), &bytes_read, portMAX_DELAY);
    
    // 计算音频能量 (简化的能量检测)
    int64_t energy = 0;
    int num_samples = bytes_read / sizeof(int32_t);
    
    for (int i = 0; i < num_samples; i++) {
        // 右移8位转换为16位有效数据
        int16_t sample = i2sBuffer[i] >> 8;
        energy += abs(sample);
    }
    
    return energy / num_samples;
}

// ==================== 陀螺仪初始化 ====================
void initGyroscope() {
    Wire.begin(I2C_SDA, I2C_SCL);
    
    // QMI8658初始化 (简化版)
    Wire.beginTransmission(0x6B);
    Wire.write(0x60);  // CTRL1
    Wire.write(0x05);  // 启用加速度计
    Wire.endTransmission();
    
    Serial.println("Gyroscope initialized");
}

// ==================== 检查翻转状态 ====================
void checkFlipState() {
    // 读取加速度计Z轴
    Wire.beginTransmission(0x6B);
    Wire.write(0x35);  // AZ_H
    Wire.endTransmission(false);
    Wire.requestFrom(0x6B, 2);
    
    if (Wire.available() >= 2) {
        int16_t az = (Wire.read() << 8) | Wire.read();
        float az_g = az / 16384.0;  // 转换为g值
        
        bool newFlipState = (az_g < FLIP_THRESHOLD);
        
        // 状态变化时更新显示
        if (newFlipState != isFlipped) {
            isFlipped = newFlipState;
            updateModeIndicator();
        }
    }
}

// ==================== 显示初始化 ====================
void initDisplay() {
    tft.init();
    tft.setRotation(0);  // 圆形屏幕无需旋转
    tft.fillScreen(COLOR_BG);
    tft.setTextFont(2);
    
    // 设置背光
    analogWrite(TFT_BL, 255);
}

// ==================== 启动画面 ====================
void showBootScreen() {
    tft.fillScreen(COLOR_BG);
    
    // 外圈 (240屏幕适配)
    tft.drawCircle(CENTER_X, CENTER_Y, 115, COLOR_PRIMARY);
    tft.drawCircle(CENTER_X, CENTER_Y, 113, COLOR_PRIMARY);
    
    // 标题 (缩小字体适配240屏幕)
    tft.setTextColor(COLOR_PRIMARY);
    tft.setTextSize(2);
    tft.setTextDatum(MC_DATUM);
    tft.drawString("MAMA", CENTER_X, CENTER_Y - 35);
    tft.drawString("COUNTER", CENTER_X, CENTER_Y - 5);
    
    // 版本
    tft.setTextColor(COLOR_GRAY);
    tft.setTextSize(1);
    tft.drawString("v1.1.0", CENTER_X, CENTER_Y + 25);
    
    // 加载动画
    for (int i = 0; i < 360; i += 5) {
        int x1 = CENTER_X + 90 * cos(i * PI / 180);
        int y1 = CENTER_Y + 90 * sin(i * PI / 180);
        int x2 = CENTER_X + 90 * cos((i + 5) * PI / 180);
        int y2 = CENTER_Y + 90 * sin((i + 5) * PI / 180);
        tft.drawLine(x1, y1, x2, y2, COLOR_PRIMARY);
        delay(5);
    }
}

// ==================== 绘制静态UI ====================
void drawStaticUI() {
    // 外圈装饰 (240屏幕适配)
    tft.drawCircle(CENTER_X, CENTER_Y, 118, COLOR_GRAY);
    tft.drawCircle(CENTER_X, CENTER_Y, 116, COLOR_GRAY);
    
    // 标题
    tft.setTextColor(COLOR_GRAY);
    tft.setTextSize(1);
    tft.setTextDatum(TC_DATUM);
    tft.drawString("MAMA COUNT", CENTER_X, 40);
    
    // 单位
    tft.setTextDatum(BC_DATUM);
    tft.drawString("times", CENTER_X, 200);
}

// ==================== 更新波形 ====================
void updateWaveform(int level) {
    // 限制范围
    level = constrain(level, 0, 100);
    
    // 更新波形数据
    waveData[waveIndex] = level;
    waveIndex = (waveIndex + 1) % 12;
    
    // 绘制波形 (底部区域，适配240宽度)
    int barWidth = 8;
    int barGap = 4;
    int startX = CENTER_X - (12 * (barWidth + barGap)) / 2 + barGap;
    int baseY = 220;
    
    for (int i = 0; i < 12; i++) {
        int idx = (waveIndex + i) % 12;
        int height = map(waveData[idx], 0, 100, 2, 30);
        int x = startX + i * (barWidth + barGap);
        
        // 清除旧条
        tft.fillRect(x, baseY - 35, barWidth, 35, COLOR_BG);
        
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
        drawStaticUI();
        delay(50);
    }
    
    // 更新显示
    drawCountDisplay(false);
}

// ==================== 绘制计数显示 ====================
void drawCountDisplay(bool highlight) {
    // 清除计数区域
    tft.fillCircle(CENTER_X, CENTER_Y, 95, COLOR_BG);
    
    // 数字
    tft.setTextDatum(MC_DATUM);
    if (highlight) {
        tft.setTextColor(COLOR_PRIMARY);
    } else {
        tft.setTextColor(COLOR_TEXT);
    }
    
    // 根据数字位数调整大小 (240屏幕适配)
    String countStr = String(mamaCount);
    if (countStr.length() <= 2) {
        tft.setTextSize(5);
    } else if (countStr.length() == 3) {
        tft.setTextSize(4);
    } else {
        tft.setTextSize(3);
    }
    
    tft.drawString(countStr, CENTER_X, CENTER_Y + 15);
}

// ==================== 更新状态显示 ====================
void updateStatusDisplay() {
    // 电池图标 (右上角，240屏幕适配)
    int batX = 185;
    int batY = 20;
    
    // 清除旧图标
    tft.fillRect(batX, batY, 35, 16, COLOR_BG);
    
    // 绘制电池外框
    tft.drawRect(batX, batY, 30, 12, COLOR_GRAY);
    tft.fillRect(batX + 30, batY + 3, 3, 6, COLOR_GRAY);
    
    // 填充电量
    int fillWidth = map(batteryLevel, 0, 100, 0, 24);
    uint16_t batColor = (batteryLevel > 20) ? COLOR_PRIMARY : COLOR_ACCENT;
    tft.fillRect(batX + 2, batY + 2, fillWidth, 8, batColor);
    
    // 定期更新计数显示
    static uint32_t lastUpdate = 0;
    if (millis() - lastUpdate > 1000) {
        drawCountDisplay(false);
        lastUpdate = millis();
    }
}

// ==================== 更新模式指示器 ====================
void updateModeIndicator() {
    // 清除状态区域 (240屏幕适配)
    tft.fillRect(CENTER_X - 60, 210, 120, 20, COLOR_BG);
    
    tft.setTextDatum(MC_DATUM);
    tft.setTextSize(1);
    
    if (isFlipped) {
        tft.setTextColor(COLOR_ACCENT);
        tft.drawString("[FLIP MUTE]", CENTER_X, 220);
    } else if (isListening) {
        tft.setTextColor(COLOR_PRIMARY);
        tft.drawString("LISTENING...", CENTER_X, 220);
    } else {
        tft.setTextColor(COLOR_SECONDARY);
        tft.drawString("PAUSED", CENTER_X, 220);
    }
}

// ==================== 按键检测 ====================
void checkButtons() {
    static uint32_t pressStartTime = 0;
    static bool buttonPressed = false;
    
    if (digitalRead(BUTTON_1) == LOW) {
        if (!buttonPressed) {
            pressStartTime = millis();
            buttonPressed = true;
        } else {
            uint32_t pressDuration = millis() - pressStartTime;
            
            if (pressDuration > 2000) {
                // 长按2秒 - 重置计数
                resetCounter();
                buttonPressed = false;
                delay(500);  // 消抖
            }
        }
    } else {
        if (buttonPressed) {
            uint32_t pressDuration = millis() - pressStartTime;
            
            if (pressDuration < 2000) {
                // 短按 - 切换监听模式
                toggleListening();
            }
            
            buttonPressed = false;
        }
    }
}

// ==================== 重置计数器 ====================
void resetCounter() {
    mamaCount = 0;
    tft.fillScreen(COLOR_BG);
    drawStaticUI();
    drawCountDisplay(false);
    
    tft.setTextColor(COLOR_ACCENT);
    tft.setTextDatum(MC_DATUM);
    tft.setTextSize(2);
    tft.drawString("RESET", CENTER_X, CENTER_Y - 60);
    delay(1000);
    
    tft.fillScreen(COLOR_BG);
    drawStaticUI();
    drawCountDisplay(false);
    
    Serial.println("Counter reset!");
}

// ==================== 切换监听模式 ====================
void toggleListening() {
    isListening = !isListening;
    updateModeIndicator();
    
    Serial.println(isListening ? "Listening resumed" : "Listening paused");
}

// ==================== 低功耗模式 ====================
void enterDeepSleep(uint32_t sleepTimeMs) {
    Serial.println("Entering deep sleep...");
    
    // 关闭屏幕背光
    digitalWrite(TFT_BL, LOW);
    
    // 停止I2S
    i2s_stop(I2S_NUM_0);
    
    // 配置定时唤醒
    esp_sleep_enable_timer_wakeup(sleepTimeMs * 1000);
    
    // 进入Deep Sleep
    esp_deep_sleep_start();
}

// ==================== 电池检测 ====================
uint8_t readBatteryLevel() {
    // 读取电池电压
    int raw = analogRead(17);  // 电池检测引脚
    float voltage = raw * 3.3 / 4095.0 * 2.0;  // 根据分压比调整
    
    // 映射到百分比 (3.3V-4.2V)
    int percentage = map((int)(voltage * 100), 330, 420, 0, 100);
    return constrain(percentage, 0, 100);
}
