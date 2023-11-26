import machine
import utime
 
analog_valueV = machine.ADC(26)
analog_valueH = machine.ADC(27)
 
while True:
    readingV = analog_valueV.read_u16()/16
    readingH = analog_valueH.read_u16()/16
    print("ADCV: ",readingV, "ADCH: ", readingH)
    utime.sleep(0.2)
