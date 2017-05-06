# Hardware Setup

The hardware consists of Arduino Flora V3 board, 10K Epoxy precision thermistor, a set of FSRs created using DIY Sensor Film kit and four 10KOHM resistors. 


## Force-Sensitive Resistor (FSR)
Use the DIY Sensor Film kit to create the FSRs below. Follow [this link](http://www.sensorfilmkit.com/) if you need a tutorial to follow when making your own FSRs. The trick is to ensure that the FSRs created match the intended placement on the glove based prototype. Create one FSR for the thumb (FSR1), one for the forefinger (HR1) and one long FSR (FSR2) for the area  extending from the little finger to the base of the wrist as shown in the figure below.
 


FSRs use a pull down resistor connected to the ground on the Flora board. One terminal of the FSR is connected to VCC and the other terminal to the ADC pin on the board. The 10KOHM resistor is connected in series to the FSR with one lead connected to ground and the other connected to the ADC pins.

The ADC pins connected are:
* FSR1 --- #12
* FSR2 --- #6
* HR1  --- #9

## Thermistor
The thermistor is connected to the pin #10 on the board. The 10K OHM resistor is connected as a pull-up resistor to the thermistor with one lead to the VCC and the other to the ADC pin. The thermistor is connected to the GND pin and the ADC pin in series with the resistor.


## Adafruit Flora V3 Board
The code is flashed to the board using the Arduino IDE. Use [this link](https://learn.adafruit.com/getting-started-with-flora/download-software) to help set up and operate the Arduino IDE. To see the code, follow the GitHub link above and see file 

The board is powered by Micro USB connection to a computer. This connection also pushes data through serial connection for the service software to process and record.

# Expected User Commands
The following images illustrate the expected user commands for the glove based prototype.

Pressing on the FSR located on the thumb and flexing the FSR on the back of the hand will trigger a context-switch to measure heart rate. This means that that the data sent to the service will be the pressure data recorded from the FSR on the index finger.

Only flexing the FSR on the back of the hand will trigger a context-switch to begin measuring from the thermistor. This will also send the thermistor temperatures to the service.

Apply pressure to the thumb sensor will begin recording pure pressure data from the FSR on the index finger. This is different than the heart rate measurement in that it sends the resistance values to the service without doing any extra calculations.