/*
  Polo Arduino Light Controller
  Receives newline-terminated commands from Python over USB serial.
  Connect an LED (with suitable resistor) to pin 13, or adapt the pin
  and output logic for a properly rated relay module.
*/
const int LIGHT_PIN = 13;
String command = "";

void setup() {
  pinMode(LIGHT_PIN, OUTPUT);
  digitalWrite(LIGHT_PIN, LOW);
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() > 0) {
    char incoming = (char)Serial.read();

    if (incoming == '\n' || incoming == '\r') {
      command.trim();
      command.toUpperCase();

      if (command == "ON") {
        digitalWrite(LIGHT_PIN, HIGH);
        Serial.println("LIGHT_ON");
      } else if (command == "OFF") {
        digitalWrite(LIGHT_PIN, LOW);
        Serial.println("LIGHT_OFF");
      } else if (command.length() > 0) {
        Serial.println("UNKNOWN_COMMAND");
      }

      command = "";
    } else {
      command += incoming;
    }
  }
}
