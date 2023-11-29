import time
import Adafruit_ADS1x15
import csv
n=0;
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')

while True:
    btemp1 = adc.read_adc(0, gain=GAIN) #bit ntc amp 1
    vtemp1 = btemp1*4096/(32767*1000) #volt ntc amp 1
    
    btemp2 = adc.read_adc(1, gain=GAIN) #bit ntc amp 2
    vtemp2 = btemp2*4096/(32767*1000) #volt ntc amp 2

    btemp3 = adc.read_adc(1, gain=GAIN) #bit ntc amp 3
    vtemp3 = btemp3*4096/(32767*1000) #volt ntc amp 3

    curr = 0 #current
    print('Temp1={0:5.5f} , Temp2={1:5.5f} , Temp3={2:5.5f} , curr={3:5.5f}'.format(vtemp1,vtemp2,vtemp3,curr))
    
    header = ['temp1', 'temp2', 'temp3', 'curr']
    data = [vtemp1, vtemp2, vtemp3, curr]

    with open('data_temp.csv', 'a+', encoding='UTF8', newline='') as f:
       writer = csv.writer(f)        
       if n==0:        
            writer.writerow(header)
       writer.writerow(data)
    n=1
    time.sleep(0.5)


