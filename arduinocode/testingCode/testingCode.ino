#include <SPI.h>
#include <Metro.h>
byte data [13];
Metro USBtransmitMetro = Metro(200);
// int lastMessage = 0;
void setup()
{
  delay(2000);
  Serial.begin(9600);
}


void loop() {
  data[0] = 100 + random(1, 6);
  data[1] = 200 + random(6, 20);
  data[2] = 97 + random(10, 20);
  data[3] = 98 + random(10, 20);
  data[4] = 99 + random(10, 20);
  data[5] = 50 + random(10, 20);
  data[6] = 55 + random(10, 20);
  data[7] = 56 + random(10, 20);
  data[8] = 66 + random(10, 20);
  data[9] = 70 + random(10, 20);
  data[10] = 80 + random(10, 20);
  data[11] = 32 + random(10, 20);
  if (USBtransmitMetro.check())
  {
    data[12] = millis();
    Serial.write(data, sizeof(data));
  }
  // put your main code here, to run repeatedly:

}
