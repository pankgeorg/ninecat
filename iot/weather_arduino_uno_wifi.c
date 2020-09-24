/*
   Web client

   This sketch connects to a website (http://www.arduino.cc)
   using an Arduino board with WiFi Link.

   This example is written for a network using WPA encryption. For
   WEP or WPA, change the Wifi.begin() call accordingly.

   This example is written for a network using WPA encryption. For
   WEP or WPA, change the Wifi.begin() call accordingly.

   created 13 July 2010
   by dlf (Metodo2 srl)
   modified 31 May 2012
   by Tom Igoe
   modified 10 March 2017
   by Sergio Tomasello and Andrea Cannistrá
   modified Nov 2017
   by Juraj Andr�ssy
 */

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; // I2C
//Adafruit_BME680 bme(BME_CS); // hardware SPI
//Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO,  BME_SCK);

#include <WiFiLink.h>
#include <UnoWiFiDevEdSerial1.h> // change Serial1.begin to 115200

#if !defined(ESP_CH_SPI) && !defined(HAVE_HWSERIAL1)
#include "SoftwareSerial.h"
SoftwareSerial Serial1(6, 7); // RX, TX
#endif

// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
// IPAddress server(,,,);  // numeric IP (no DNS)

char server[] = "api.pankgeorg.com";    // name address  (using DNS)

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;
int counter = 0;

void setup() {
    setup_serial();
    setup_sensor(true);

    Serial.println("\nStarting connection to server...");
    // if you get a connection, report back via serial:

    testConnect();
    printServerResponse(true);
}

void loop() {
    Serial.print(counter);
    Serial.println(" loop");
    counter += 1;

    if(counter % 7200 == 0)
        setup();
    if(counter % 100 == 0)
        setup_sensor(true);
    if(counter % 10 == 0){
        sendBME();
        printServerResponse(true);
    }
    writelnReading();
    delay(1000);
}

void sendBME () {
    if(!bme.performReading()){
        Serial.println("Failed to perform reading :( - Nothing to send");
        return;
    }
    if(client.connect(server, 80)) {
        client.print("GET /station-readings");
        client.print("?t=");
        client.print(bme.temperature);
        client.print("&p=");
        client.print(bme.pressure/100.0);
        client.print("&g=");
        client.print(bme.gas_resistance/1000.0);
        client.print("&h=");
        client.print(bme.humidity);
        client.print("&s=");
        client.print("Georgia%20Panagiotis%20Psychiko");
        client.println(" HTTP/1.1");
        client.println("Host: api.pankgeorg.com");
        client.println("Connection: close");
        client.println();
    }
}

void testConnect(){
    Serial.print("Trying to connect to ");
    Serial.println(server);
    if (client.connect(server, 80)) {
        Serial.println("connected to server");
        // Make a HTTP request:
        client.println("GET /asciilogo.txt HTTP/1.1");
        client.println("Host: arduino.cc");
        client.println("Connection: close");
        client.println();
    }
}
void printServerResponse(bool close){
    // if there are incoming bytes available
    // from the server, read them and print them:
    Serial.println("Server Response (success=null)");
    while (client.available()) {
        char c = client.read();
        Serial.write(c);
    }
    // if the server's disconnected, stop the client:
    if (!client.connected() or close) {
        Serial.println();
        Serial.println("disconnecting from server.");
        client.stop();
    }
}

void printWifiStatus() {
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print your WiFi shield's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");
}

void setup_serial() {
    //Initialize serial and wait for port to open:
    Serial.begin(115200);
    while (!Serial);// wait for serial port to connect. Needed for native USB port only

#if !defined(ESP_CH_SPI)
    Serial1.begin(115200); // speed must match with BAUDRATE_COMMUNICATION setting in firmware config.h
    WiFi.init(&Serial1);
#endif

    if (WiFi.checkFirmwareVersion("1.1.0")) {
        WiFi.resetESP(); // to clear 'sockets' after sketch upload
    }
    delay(3000); //wait while WiFiLink firmware connects to WiFi with Web Panel settings

    while (WiFi.status() != WL_CONNECTED) {
        delay(10);
    }

    Serial.println("Connected to wifi");
    printWifiStatus();
}

void setup_sensor(bool verbose) {
    if (!bme.begin(0x76)) {
        Serial.println("Could not find a valid BME680 sensor, check wiring!");
        delay(15000); // delaying 15sec
    }
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150); // 320*C for 150 ms
    if(verbose){
        Serial.println("Adafruit BME680 Setup complete");
    }
}


void writelnReading() {
    if (! bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
    }
    Serial.print("Temperature = ");
    Serial.print(bme.temperature);
    Serial.println(" *C");

    Serial.print("Pressure = ");
    Serial.print(bme.pressure / 100.0);
    Serial.println(" hPa");

    Serial.print("Humidity = ");
    Serial.print(bme.humidity);
    Serial.println(" %");

    Serial.print("Gas = ");
    Serial.print(bme.gas_resistance / 1000.0);
    Serial.println(" KOhms");

    Serial.print("Approx. Altitude = ");
    Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
    Serial.println(" m");

    Serial.println();
}
