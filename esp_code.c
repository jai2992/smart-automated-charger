#define LED_PIN 2

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("ESP Ready. Type 'on' or 'off'.");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "on") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED turned ON");
    } else if (cmd == "off") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED turned OFF");
    } else {
      Serial.println("Unknown command");
    }
  }
}
