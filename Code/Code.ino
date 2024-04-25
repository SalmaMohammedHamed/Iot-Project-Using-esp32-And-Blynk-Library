//Firmware configuration
#define BLYNK_TEMPLATE_ID "TMPL2DmWhTEJo"
#define BLYNK_TEMPLATE_NAME "Time"
#define BLYNK_AUTH_TOKEN "pgRs8S_sHWUokleM0Wufb2rqVa_GiTc_"

//Debudding console
#define BLYNK_PRINT Serial

//liberaries
#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

char auth[] = BLYNK_AUTH_TOKEN;
// Your WiFi credentials.
char ssid[] = "YourNetworkName";
char pass[] = "YourNetworkPassword";
BlynkTimer timer;
//relay pin
#define RelayPin 13
//motor pins
#define ClkWiseBin 18
#define AntiClkWiseBin 19

int MotorState = LOW;
int MotorDirInput =LOW;//the input of the motor Dir buttons
int on =LOW;
int Time =0;  //the value sent from the slider
unsigned long startTime = 0; //timer start time
bool timerRunning = false; 
unsigned long elapsedTime=0; //elpsed time i ms
unsigned long remainingTime = 0; //remaining time in ms


//vitual bins
#define ON    V1
#define SliderVpin V3
#define MotorOFF    V2
#define MotorDir V4
#define RemianingTimeV  V5


//------------------------------------------------------------------------------
// This function is called every time the device is connected to the Blynk.Cloud
// Request the latest state from the server
BLYNK_CONNECTED() {
  Blynk.syncVirtual(ON);
  Blynk.syncVirtual(MotorOFF);
  Blynk.syncVirtual(SliderVpin);
  Blynk.syncVirtual(MotorDir);
  Blynk.syncVirtual(RemianingTimeV);
}

/*******LED*********/
// This function is called every time the Virtual Pin state change
//i.e when web push switch from Blynk App or Web Dashboard
BLYNK_WRITE(ON) {
  static int ONButton = LOW; //the state of the relay control button
  ONButton = param.asInt();


  if (ONButton==LOW)
  {
    if (on ==HIGH || timerRunning == true)
    {
      digitalWrite(RelayPin, LOW);
      on=LOW;
      if (timerRunning==true)
      {
        timerRunning = false;
        remainingTime=0;
        Blynk.virtualWrite(SliderVpin,  remainingTime); 
        Blynk.virtualWrite(RemianingTimeV, remainingTime);
      }
     Serial.print("ON state = ");
      Serial.println(on);
    }

  }
  else if (ONButton==HIGH)
  {
    if (on==LOW)
    {
      digitalWrite(RelayPin, HIGH);
      on=HIGH;
        Serial.print("ON state = ");
        Serial.println(on);
    }
  }

}

 
BLYNK_WRITE(SliderVpin) {
  Time = param.asInt();

    Serial.print("Time = ");
    Serial.println(Time);
    startTime = millis();
    Blynk.virtualWrite(RemianingTimeV, Time); 
    timerRunning = true;
    if (Time!=0)
    {
      digitalWrite(RelayPin, HIGH);
      on=HIGH;
      Blynk.virtualWrite(ON,HIGH);
    }
  

}


void checkTimer() {
  if (timerRunning) {
    unsigned long elapsedTime = millis() - startTime;
    if (elapsedTime >= (Time * 1000)) {
      digitalWrite(RelayPin, LOW);
      on=LOW;
      Blynk.virtualWrite(ON,LOW);
      timerRunning = false;
    }

    if (elapsedTime%1000==0) //send the remaining time to the RemianingTimeV every second
    {
      remainingTime = Time * 1000 - elapsedTime;
      Blynk.virtualWrite(RemianingTimeV, remainingTime / 1000); // Send remaining time in seconds
      if (remainingTime<=0) //if the remainingTime <=0 reset the slider 
      {
        Blynk.virtualWrite(SliderVpin,  0); // Send remaining time in seconds
      }
    }
  }
}
/**************************/

/********motor*********/
BLYNK_WRITE(MotorOFF) 
{
  static int MotorStateInput =LOW;//the input of the motor OFF button
  MotorStateInput=param.asInt();
  if (MotorStateInput==LOW)
  {
    digitalWrite(ClkWiseBin,LOW);
    digitalWrite(AntiClkWiseBin,LOW);
    MotorState=LOW;

  }
  else if (MotorStateInput=HIGH)
  {
    MotorState=HIGH;
    if (MotorDirInput==LOW )
    {
      digitalWrite(ClkWiseBin,HIGH);
      digitalWrite(AntiClkWiseBin,LOW);

    }
    else if (MotorDirInput==HIGH)
    {
      digitalWrite(ClkWiseBin,LOW);
      digitalWrite(AntiClkWiseBin,HIGH);

    }
  }

}

BLYNK_WRITE(MotorDir) 
{
  
  MotorDirInput=param.asInt();
  if (MotorDirInput==LOW && MotorState==HIGH)
  {
    digitalWrite(ClkWiseBin,HIGH);
    digitalWrite(AntiClkWiseBin,LOW);

  }
  else if (MotorDirInput==HIGH && MotorState==HIGH)
  {
    digitalWrite(ClkWiseBin,LOW);
    digitalWrite(AntiClkWiseBin,HIGH);

  }

}

//************************/

void setup()
{
  //start Debug console
  Serial.begin(115200);

  //bin directions

  pinMode(RelayPin, OUTPUT);
  pinMode(ClkWiseBin, OUTPUT);
  pinMode(AntiClkWiseBin, OUTPUT);

  //During Starting the relay should TURN OFF
  digitalWrite(RelayPin, LOW);
  digitalWrite(ClkWiseBin, LOW);
  digitalWrite(AntiClkWiseBin, LOW);
  //connect with the wifi network
  Blynk.begin(auth, ssid, pass);
  timer.setInterval(1, checkTimer); // Run checkTimer every msecond
}

/****reconnction mechanism*******/
void Reconnect(){
  if (!Blynk.connected() ) {
    delay(10); // Wait 10 msecond before retrying
    Serial.println("Reconnecting...");
    Blynk.connect(); // Try to reconnect to Blynk server
  }
}
void loop()
{
  Blynk.run();
  timer.run();
  Reconnect();
}