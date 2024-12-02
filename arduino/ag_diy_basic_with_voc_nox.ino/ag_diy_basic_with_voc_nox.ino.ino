#include <U8g2lib.h>
#include <AirGradient.h>
#include <WiFiManager.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <SHTSensor.h>
#include <ESP8266WebServer.h>
#include <NOxGasIndexAlgorithm.h>
#include <VOCGasIndexAlgorithm.h>
#include <SensirionI2CSgp41.h>
#include <Wire.h>

//An air quality sensor that outputs a VOC index provides more actionable
//insights. Essentially, the sensor measures VOC levels over a 24-hour period and
//calculates the average value and assigns it VOC Index 100. Once the average is
//calibrated, the sensor can then monitor for changes. Values are measured on a
//range of 0-500. Values between 100 and 500 indicate deterioration, while values
//between 0-100 suggest improvements in air quality.
//
//VOC Index of 100 continuously adapts to any environment. Therefore, conditions
//that were previously interpreted as average (VOC Index = 100) are now
//considered as air quality improvement.
//https://www.pressac.com/insights/what-are-volatile-organic-compounds-vocs-and-why-should-you-be-monitoring-them/

// Webserver setup
ESP8266WebServer server(80);

// AG libs
AirGradient ag = AirGradient();

// Temp/Humid sensor
SHTSensor sht;

// VOC/NOx sensor
SensirionI2CSgp41 sgp41;

// Index algorithms for VOC and NOx
VOCGasIndexAlgorithm voc_algorithm;
NOxGasIndexAlgorithm nox_algorithm;

// time in seconds needed for NOx conditioning
uint16_t conditioning_s = 10;

// Display setup
U8G2_SSD1306_64X48_ER_1_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE); //for DIY BASIC

// CONFIGURATION START

// set to true to switch from Celcius to Fahrenheit
boolean inF = false;

// PM2.5 in US AQI (default ug/m3)
boolean inUSAQI = false;

// set to true if you want to connect to wifi.
boolean connectWIFI=true;

// CONFIGURATION END


unsigned long currentMillis = 0;

const int oledInterval = 5000;
unsigned long previousOled = 0;

const int sendToServerInterval = 10000;
unsigned long previoussendToServer = 0;

const int co2Interval = 5000;
unsigned long previousCo2 = 0;
int Co2 = 0;

const int pm25Interval = 5000;
unsigned long previousPm25 = 0;
int pm25 = 0;

const int tempHumInterval = 2500;
unsigned long previousTempHum = 0;
float temp = 0;
int hum = 0;
long val;

int32_t voc_index = 0;
int32_t nox_index = 0;

void setup()
{
    Serial.begin(115200);
    while (!Serial) {
        delay(100);
    }
   
    u8g2.setBusClock(100000);
    u8g2.begin();
    updateOLED();

    if (connectWIFI) {
        connectToWifi();
    }
    
    updateOLED2("Warm Up", "Serial#", String(ESP.getChipId(), HEX));
    ag.CO2_Init();
    ag.PMS_Init();
    sht.init();
    sht.setAccuracy(SHTSensor::SHT_ACCURACY_MEDIUM);

// ===========================================================
  
    Wire.begin();
    sgp41.begin(Wire);

    delay(1000);  // needed on some Arduino boards in order to have Serial ready

    int32_t index_offset;
    int32_t learning_time_offset_hours;
    int32_t learning_time_gain_hours;
    int32_t gating_max_duration_minutes;
    int32_t std_initial;
    int32_t gain_factor;
    voc_algorithm.get_tuning_parameters(
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_max_duration_minutes, std_initial, gain_factor);

    Serial.println("\nVOC Gas Index Algorithm parameters");
    Serial.print("Index offset:\t");
    Serial.println(index_offset);
    Serial.print("Learing time offset hours:\t");
    Serial.println(learning_time_offset_hours);
    Serial.print("Learing time gain hours:\t");
    Serial.println(learning_time_gain_hours);
    Serial.print("Gating max duration minutes:\t");
    Serial.println(gating_max_duration_minutes);
    Serial.print("Std inital:\t");
    Serial.println(std_initial);
    Serial.print("Gain factor:\t");
    Serial.println(gain_factor);

    nox_algorithm.get_tuning_parameters(
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_max_duration_minutes, std_initial, gain_factor);

    Serial.println("\nNOx Gas Index Algorithm parameters");
    Serial.print("Index offset:\t");
    Serial.println(index_offset);
    Serial.print("Learing time offset hours:\t");
    Serial.println(learning_time_offset_hours);
    Serial.print("Gating max duration minutes:\t");
    Serial.println(gating_max_duration_minutes);
    Serial.print("Gain factor:\t");
    Serial.println(gain_factor);
    Serial.println("");

// ===========================================================

 
  // Server setup
  restServerRouting();
  server.begin();
  Serial.println("HTTP server started");
  
}

void loop()
{
  currentMillis = millis();
  updateOLED();
  updateCo2();
  updatePm25();
  updateTempHum();

// =================================================
    uint16_t error;
    uint16_t srawVoc = 0;
    uint16_t srawNox = 0;
    uint16_t defaultCompenstaionRh = 0x8000;  // in ticks as defined by SGP41
    uint16_t defaultCompenstaionT = 0x6666;   // in ticks as defined by SGP41
    uint16_t compensationRh = 0;              // in ticks as defined by SGP41
    uint16_t compensationT = 0;               // in ticks as defined by SGP41

    // 1. Sleep: Measure every second (1Hz), as defined by the Gas Index
    // Algorithm prerequisite
    delay(1000);

    compensationT = static_cast<uint16_t>((temp + 45) * 65535 / 175);
    compensationRh = static_cast<uint16_t>(hum * 65535 / 100);
    
    // Measure SGP4x signals
    if (conditioning_s > 0) {
        // During NOx conditioning (10s) SRAW NOx will remain 0
        error = sgp41.executeConditioning(compensationRh, compensationT, srawVoc);
        conditioning_s--;
    } else {
        error = sgp41.measureRawSignals(compensationRh, compensationT, srawVoc, srawNox);
    }

    // Process raw signals by Gas Index Algorithm to get the VOC and NOx
    // index values
        voc_index = voc_algorithm.process(srawVoc);
        nox_index = nox_algorithm.process(srawNox);
        Serial.print("VOC Index: ");
        Serial.print(voc_index);
        Serial.print("\t");
        Serial.print("NOx Index: ");
        Serial.println(nox_index);
// =========================================================================

  
  server.handleClient();

}

void getJson() {
      String data_json = "{\"device\": \"AIRGRADIENT_1\""
      + (Co2 < 0 ? "" : ", \"co2\":" + String(Co2))
      + (pm25 < 0 ? "" : ", \"pm\":" + String(pm25))
      + ", \"temp\":" + String(temp)
      + (hum < 0 ? "" : ", \"humid\":" + String(hum))
      + ", \"voc\":" + String(voc_index)
      + ", \"nox\":" + String(nox_index)
      + "}";
    server.send(200, "Content-Type: application/json", data_json);
}
 
void restServerRouting() {
    server.on("/", HTTP_GET, []() {
        server.send(200, F("text/html"),
            F("TBD"));
    });
    server.on(F("/json"), HTTP_GET, getJson);
}

void updateCo2()
{
    if (currentMillis - previousCo2 >= co2Interval) {
      previousCo2 += co2Interval;
      Co2 = ag.getCO2_Raw();
      Serial.println(String(Co2));
    }
}

void updatePm25()
{
    if (currentMillis - previousPm25 >= pm25Interval) {
      previousPm25 += pm25Interval;
      pm25 = ag.getPM2_Raw();
      Serial.println(String(pm25));
    }
}

void updateTempHum()
{
    if (currentMillis - previousTempHum >= tempHumInterval) {
      previousTempHum += tempHumInterval;
    if (sht.readSample()) {
      Serial.print("SHT:\n");
      Serial.print("  RH: ");
      Serial.print(sht.getHumidity(), 2);
      Serial.print("\n");
      Serial.print("  T:  ");
      Serial.print(sht.getTemperature(), 2);
      Serial.print("\n");
      temp = sht.getTemperature();
      hum = sht.getHumidity();
        } else {
      Serial.print("Error in readSample()\n");
      }
      Serial.println(String(temp));
    }
}

void updateOLED() {
   if (currentMillis - previousOled >= oledInterval) {
     previousOled += oledInterval;

    String ln1;
    String ln2;
    String ln3;

    if (inUSAQI){
       ln1 = "AQI:" + String(PM_TO_AQI_US(pm25));
    } else {
       ln1 = "P" + String(pm25) + "V" + String(voc_index);
    }

    ln2 = "C" + String(Co2) + "N" + String(nox_index);

      if (inF) {ln3 = String((temp* 9 / 5) + 32).substring(0,4) + " " + String(hum)+"%";
        } else {
        ln3 = String(temp).substring(0,4) + " " + String(hum)+"%";
       }
     updateOLED2(ln1, ln2, ln3);
   }
}

void updateOLED2(String ln1, String ln2, String ln3) {
      char buf[9];
          u8g2.firstPage();
          u8g2.firstPage();
          do {
          u8g2.setFont(u8g2_font_t0_16_tf);
          u8g2.drawStr(1, 10, String(ln1).c_str());
          u8g2.drawStr(1, 28, String(ln2).c_str());
          u8g2.drawStr(1, 46, String(ln3).c_str());
            } while ( u8g2.nextPage() );
}

// Wifi Manager
 void connectToWifi() {
   WiFiManager wifiManager;
   //WiFi.disconnect(); //to delete previous saved hotspot
   String HOTSPOT = "AG-" + String(ESP.getChipId(), HEX);
   updateOLED2("Connect", "Wifi AG-", String(ESP.getChipId(), HEX));
   delay(2000);
   wifiManager.setTimeout(90);
   if (!wifiManager.autoConnect((const char * ) HOTSPOT.c_str())) {
     updateOLED2("Booting", "offline", "mode");
     Serial.println("failed to connect and hit timeout");
     delay(6000);
   }
}

// Calculate PM2.5 US AQI
int PM_TO_AQI_US(int pm02) {
  if (pm02 <= 12.0) return ((50 - 0) / (12.0 - .0) * (pm02 - .0) + 0);
  else if (pm02 <= 35.4) return ((100 - 50) / (35.4 - 12.0) * (pm02 - 12.0) + 50);
  else if (pm02 <= 55.4) return ((150 - 100) / (55.4 - 35.4) * (pm02 - 35.4) + 100);
  else if (pm02 <= 150.4) return ((200 - 150) / (150.4 - 55.4) * (pm02 - 55.4) + 150);
  else if (pm02 <= 250.4) return ((300 - 200) / (250.4 - 150.4) * (pm02 - 150.4) + 200);
  else if (pm02 <= 350.4) return ((400 - 300) / (350.4 - 250.4) * (pm02 - 250.4) + 300);
  else if (pm02 <= 500.4) return ((500 - 400) / (500.4 - 350.4) * (pm02 - 350.4) + 400);
  else return 500;
};
