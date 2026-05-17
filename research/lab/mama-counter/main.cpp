/**
 * 妈妈计数器 - Mama Counter v1.1.0-waveshare-1.54
 * 适配: 微雪 ESP32-S3-Touch-LCD-1.54 (ST7789, 240×240)
 */

#include <TFT_eSPI.h>
#include <driver/i2s.h>
#include <Wire.h>

#define TFT_CS      10
#define TFT_SCK     12
#define TFT_MOSI    11
#define TFT_DC      13
#define TFT_RST     9
#define TFT_BL      42
#define I2S_MIC_SCK     4
#define I2S_MIC_WS      5
#define I2S_MIC_SD      6
#define I2C_SDA         15
#define I2C_SCL         16
#define BUTTON_1        0
#define BUTTON_2        14

#define SCREEN_WIDTH    240
#define SCREEN_HEIGHT   240
#define CENTER_X        120
#define CENTER_Y        120
#define SAMPLE_RATE     16000
#define BUFFER_SIZE     256
#define ENERGY_THRESHOLD    3000
#define TRIGGER_COOLDOWN    2000
#define FLIP_THRESHOLD      -0.7

#define COLOR_BG        TFT_BLACK
#define COLOR_PRIMARY   0x07E0
#define COLOR_SECONDARY 0xFFE0
#define COLOR_ACCENT    0xF800
#define COLOR_TEXT      TFT_WHITE
#define COLOR_GRAY      0x8410

TFT_eSPI tft = TFT_eSPI();

uint32_t mamaCount = 0;
uint32_t lastTriggerTime = 0;
bool isListening = true;
bool isFlipped = false;
uint8_t batteryLevel = 85;
int waveData[12] = {0};
int waveIndex = 0;
int32_t i2sBuffer[BUFFER_SIZE];

// ===== 前向声明 (解决编译顺序问题) =====
void initDisplay();
void initI2SMic();
int readI2SMicrophone();
void initGyroscope();
void checkFlipState();
void showBootScreen();
void drawStaticUI();
void updateWaveform(int level);
void triggerMamaDetected();
void drawCountDisplay(bool highlight);
void updateStatusDisplay();
void updateModeIndicator();
void checkButtons();
void resetCounter();
void toggleListening();
void enterDeepSleep(uint32_t sleepTimeMs);
uint8_t readBatteryLevel();

// ===== 函数实现 =====

void initDisplay() {
    tft.init();
    tft.setRotation(0);
    tft.fillScreen(COLOR_BG);
    tft.setTextFont(2);
    analogWrite(TFT_BL, 255);
}

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

int readI2SMicrophone() {
    size_t bytes_read;
    i2s_read(I2S_NUM_0, i2sBuffer, sizeof(i2sBuffer), &bytes_read, portMAX_DELAY);
    int64_t energy = 0;
    int num_samples = bytes_read / sizeof(int32_t);
    for (int i = 0; i < num_samples; i++) {
        int16_t sample = i2sBuffer[i] >> 8;
        energy += abs(sample);
    }
    return energy / num_samples;
}

void initGyroscope() {
    Wire.begin(I2C_SDA, I2C_SCL);
    Wire.beginTransmission(0x6B);
    Wire.write(0x60);
    Wire.write(0x05);
    Wire.endTransmission();
    Serial.println("Gyroscope initialized");
}

void checkFlipState() {
    Wire.beginTransmission(0x6B);
    Wire.write(0x35);
    Wire.endTransmission(false);
    Wire.requestFrom(0x6B, 2);
    if (Wire.available() >= 2) {
        int16_t az = (Wire.read() << 8) | Wire.read();
        float az_g = az / 16384.0;
        bool newFlipState = (az_g < FLIP_THRESHOLD);
        if (newFlipState != isFlipped) {
            isFlipped = newFlipState;
            updateModeIndicator();
        }
    }
}

void showBootScreen() {
    tft.fillScreen(COLOR_BG);
    tft.drawCircle(CENTER_X, CENTER_Y, 115, COLOR_PRIMARY);
    tft.drawCircle(CENTER_X, CENTER_Y, 113, COLOR_PRIMARY);
    tft.setTextColor(COLOR_PRIMARY);
    tft.setTextSize(2);
    tft.setTextDatum(MC_DATUM);
    tft.drawString("MAMA", CENTER_X, CENTER_Y - 35);
    tft.drawString("COUNTER", CENTER_X, CENTER_Y - 5);
    tft.setTextColor(COLOR_GRAY);
    tft.setTextSize(1);
    tft.drawString("v1.1.0", CENTER_X, CENTER_Y + 25);
    for (int i = 0; i < 360; i += 5) {
        int x1 = CENTER_X + 90 * cos(i * PI / 180);
        int y1 = CENTER_Y + 90 * sin(i * PI / 180);
        int x2 = CENTER_X + 90 * cos((i + 5) * PI / 180);
        int y2 = CENTER_Y + 90 * sin((i + 5) * PI / 180);
        tft.drawLine(x1, y1, x2, y2, COLOR_PRIMARY);
        delay(5);
    }
}

void drawStaticUI() {
    tft.drawCircle(CENTER_X, CENTER_Y, 118, COLOR_GRAY);
    tft.drawCircle(CENTER_X, CENTER_Y, 116, COLOR_GRAY);
    tft.setTextColor(COLOR_GRAY);
    tft.setTextSize(1);
    tft.setTextDatum(TC_DATUM);
    tft.drawString("MAMA COUNT", CENTER_X, 40);
    tft.setTextDatum(BC_DATUM);
    tft.drawString("times", CENTER_X, 200);
}

void updateWaveform(int level) {
    level = constrain(level, 0, 100);
    waveData[waveIndex] = level;
    waveIndex = (waveIndex + 1) % 12;
    int barWidth = 8;
    int barGap = 4;
    int startX = CENTER_X - (12 * (barWidth + barGap)) / 2 + barGap;
    int baseY = 220;
    for (int i = 0; i < 12; i++) {
        int idx = (waveIndex + i) % 12;
        int height = map(waveData[idx], 0, 100, 2, 30);
        int x = startX + i * (barWidth + barGap);
        tft.fillRect(x, baseY - 35, barWidth, 35, COLOR_BG);
        uint16_t color = (i == 11) ? COLOR_PRIMARY : COLOR_GRAY;
        tft.fillRect(x, baseY - height, barWidth, height, color);
    }
}

void triggerMamaDetected() {
    lastTriggerTime = millis();
    mamaCount++;
    Serial.print("Mama detected! Count: ");
    Serial.println(mamaCount);
    drawCountDisplay(true);
    for (int i = 0; i < 3; i++) {
        tft.fillCircle(CENTER_X, CENTER_Y, 100, COLOR_PRIMARY);
        delay(50);
        tft.fillCircle(CENTER_X, CENTER_Y, 100, COLOR_BG);
        drawStaticUI();
        delay(50);
    }
    drawCountDisplay(false);
}

void drawCountDisplay(bool highlight) {
    tft.fillCircle(CENTER_X, CENTER_Y, 95, COLOR_BG);
    tft.setTextDatum(MC_DATUM);
    if (highlight) tft.setTextColor(COLOR_PRIMARY);
    else tft.setTextColor(COLOR_TEXT);
    String countStr = String(mamaCount);
    if (countStr.length() <= 2) tft.setTextSize(5);
    else if (countStr.length() == 3) tft.setTextSize(4);
    else tft.setTextSize(3);
    tft.drawString(countStr, CENTER_X, CENTER_Y + 15);
}

void updateStatusDisplay() {
    int batX = 185;
    int batY = 20;
    tft.fillRect(batX, batY, 35, 16, COLOR_BG);
    tft.drawRect(batX, batY, 30, 12, COLOR_GRAY);
    tft.fillRect(batX + 30, batY + 3, 3, 6, COLOR_GRAY);
    int fillWidth = map(batteryLevel, 0, 100, 0, 24);
    uint16_t batColor = (batteryLevel > 20) ? COLOR_PRIMARY : COLOR_ACCENT;
    tft.fillRect(batX + 2, batY + 2, fillWidth, 8, batColor);
    static uint32_t lastUpdate = 0;
    if (millis() - lastUpdate > 1000) {
        drawCountDisplay(false);
        lastUpdate = millis();
    }
}

void updateModeIndicator() {
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
                resetCounter();
                buttonPressed = false;
                delay(500);
            }
        }
    } else {
        if (buttonPressed) {
            uint32_t pressDuration = millis() - pressStartTime;
            if (pressDuration < 2000) {
                toggleListening();
            }
            buttonPressed = false;
        }
    }
}

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

void toggleListening() {
    isListening = !isListening;
    updateModeIndicator();
    Serial.println(isListening ? "Listening resumed" : "Listening paused");
}

void enterDeepSleep(uint32_t sleepTimeMs) {
    Serial.println("Entering deep sleep...");
    digitalWrite(TFT_BL, LOW);
    i2s_stop(I2S_NUM_0);
    esp_sleep_enable_timer_wakeup(sleepTimeMs * 1000);
    esp_deep_sleep_start();
}

uint8_t readBatteryLevel() {
    int raw = analogRead(17);
    float voltage = raw * 3.3 / 4095.0 * 2.0;
    int percentage = map((int)(voltage * 100), 330, 420, 0, 100);
    return constrain(percentage, 0, 100);
}

// ===== setup() 和 loop() =====

void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Mama Counter v1.1.0-waveshare-1.54 Starting ===");
    pinMode(BUTTON_1, INPUT_PULLUP);
    pinMode(BUTTON_2, INPUT_PULLUP);
    pinMode(TFT_BL, OUTPUT);
    initDisplay();
    initI2SMic();
    initGyroscope();
    showBootScreen();
    delay(2000);
    tft.fillScreen(COLOR_BG);
    drawStaticUI();
    Serial.println("System Ready!");
}

void loop() {
    checkFlipState();
    int energy = readI2SMicrophone();
    updateWaveform(energy / 100);
    if (!isFlipped && isListening && energy > ENERGY_THRESHOLD) {
        if (millis() - lastTriggerTime > TRIGGER_COOLDOWN) {
            triggerMamaDetected();
        }
    }
    checkButtons();
    updateStatusDisplay();
    delay(10);
}
