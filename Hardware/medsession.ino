#include <FilterDerivative.h>
#include <FilterOnePole.h>
#include <Filters.h>
#include <FilterTwoPole.h>
#include <FloatDefine.h>
#include <RunningStatistics.h>



// the value of the 'other' resistor
#define SERIESRESISTOR 10000
#define THERMISTORNOMINAL 10000
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5
// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 3950
// What pin to connect the sensor to
#define HR1 A11
//#define HR2 A9
#define FSR1 A9
#define FSR2 A7
//#define FSR3 A3
#define THERMISTORPIN A10


int samples[NUMSAMPLES];

void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  float hr1, hr2, fsr1, fsr2, fsr3, therm;

  hr1 =  reading(hr1, HR1);
  //hr2 =  reading(hr2, HR2);
  fsr1 =  reading(fsr1, FSR1);
  fsr2 =  reading(fsr2, FSR2);
  //fsr3 =  reading(fsr3, FSR3);
//  therm = reading(therm, THERMISTORPIN);

  if (fsr1 > 0 && fsr2 > 0 ) {

      HR();

  }
  if (fsr1 > 0 && fsr2 == 0) {

//    Serial.println("FSR 1 high ");
     temp();
  }
  if (fsr1 == 0 && fsr2 > 0) {

    //Serial.println("FSR 2 high ");
    stress();

  }
  //if (fsr1 == 0 && fsr2 == 0) {
    //Serial.println("FSRs sleep ");
    

  //}
}


//Function to convert voltage at ADC pin to Resistor
float reading(float val, int analogpin) {

  val = analogRead(analogpin);
/*
  Serial.print("Pin ");
  Serial.println(analogpin);

  Serial.print("Raw Val ");
  Serial.println(val);
*/
  // convert the value to resistance
  val = (1023 / val)  - 1;
  val = SERIESRESISTOR / val;
  //Serial.print("resistance~");
  //Serial.print(val);

  delay(100);
  return val;
}

//Function to measure Temperature
void temp(void) {
  uint8_t i;
  float average;

  // take N samples in a row, with a slight delay
  for (i = 0; i < NUMSAMPLES; i++) {
    samples[i] = analogRead(THERMISTORPIN);
    delay(10);
  }

  // average all the samples out
  average = 0;
  for (i = 0; i < NUMSAMPLES; i++) {
    average += samples[i];
  }
  average /= NUMSAMPLES;

  //Serial.print("Average analog reading ");
  //Serial.println(average);

  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
//  Serial.print("Thermistor resistance ");
  //Serial.println(average);

  float steinhart;
  steinhart = average / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert to C

  Serial.print("temp~");
  Serial.print(steinhart);
  Serial.print("#");

  delay(1000);
}

//Function to estimate Heartrate
void heartrate() {

  uint8_t i;
  float average;

  // take N samples in a row, with a slight delay
  for (i = 0; i < NUMSAMPLES; i++) {
    samples[i] = analogRead(HR1);
    delay(1);
  }

  // average all the samples out
  average = 0;
  for (i = 0; i < NUMSAMPLES; i++) {
    average += samples[i];
  }
  average /= NUMSAMPLES;

  //Serial.print("HR~");
  //Serial.println(average);

  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
  Serial.print("rate~");
  Serial.print(average);
  Serial.print("#");
  delay(100);

}


//Function to estimate force
void stress() {
  // filters out changes faster that 5 Hz.
float filterFrequency = 50;  
float signal1;
// create a one pole (RC) lowpass filter
FilterOnePole lowpassFilter( LOWPASS, filterFrequency );   
 
signal1 = lowpassFilter.input( analogRead( HR1 ) );
  // do something else
Serial.print("press~");
Serial.print(signal1);
Serial.print("#");
delay(1000);
}

