#include <Printers.h>
#include <XBee.h>
#include <Metro.h>

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
// create reusable response objects for responses we expect to handle
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

byte dataIn[13];// = {0, 0, 0, 0, 0, 0, 0, 0};

Metro USBtransmitMetro = Metro(200); // 10ms delay

long lastMessage = 0;

void setup() {
  delay(2000);

  Serial5.begin(115200);
  xbee.setSerial(Serial5);

}

void loop() {
  // put your main code here, to run repeatedly:

  xbee.readPacket();

    if (xbee.getResponse().isAvailable()) {

      // got something

      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        // got a zb rx packet

        // now fill our zb rx class
        xbee.getResponse().getZBRxResponse(rx);

        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
            // the sender got an ACK

        } else {
            // we got it (obviously) but sender didn't get an ACK

        }
        // get our data

        dataIn[0] = rx.getData(0);
        dataIn[1] = rx.getData(1);
        dataIn[2] = rx.getData(2);
        dataIn[3] = rx.getData(3);
        dataIn[4] = rx.getData(4);
        dataIn[5] = rx.getData(5);
        dataIn[6] = rx.getData(6);
        dataIn[7] = rx.getData(7);
        dataIn[8] = rx.getData(8);
        dataIn[9] = rx.getData(9);
        dataIn[10] = rx.getData(10);
        dataIn[11] = rx.getData(11);

        lastMessage = millis();

      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        // the local XBee sends this response on certain events, like association/dissociation

        if (msr.getStatus() == ASSOCIATED) {
          // yay this is great.  flash led

        } else if (msr.getStatus() == DISASSOCIATED) {
          // this is awful.. flash led to show our discontent

        } else {
          // another status

        }
      } else {
        // not something we were expecting

      }
    } else if (xbee.getResponse().isError()) {
      //nss.print("Error reading packet.  Error code: ");
      //nss.println(xbee.getResponse().getErrorCode());
    }

    if (USBtransmitMetro.check()) {


      dataIn[12] = 1000 / (millis() - lastMessage);


      Serial.write(dataIn, sizeof(dataIn));
    }
}
