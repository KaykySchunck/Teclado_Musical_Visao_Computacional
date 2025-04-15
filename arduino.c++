#define BUZZER_PIN 8

int notas[] = {262, 294, 330, 349, 392}; // C, D, E, F, G

void setup()
{
    Serial.begin(9600);
    pinMode(BUZZER_PIN, OUTPUT);
}

void loop()
{
    if (Serial.available())
    {
        char notaChar = Serial.read();
        int notaIndex = notaChar - '0';
        if (notaIndex >= 0 && notaIndex < 5)
        {
            tone(BUZZER_PIN, notas[notaIndex], 300);
        }
    }
}
