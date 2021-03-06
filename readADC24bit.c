// 24 bit ADC
//gcc -o 2readADC readADClog.c minIni.c -l wiringPi
#include <wiringPi.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include "minIni.h"

#define CLK 14
#define DATA 13

const char inifile[] = "/home/pi/config.ini";

int main() {
    int i;
    int value;
    int twoCompVal;
    int x =0;
    float zeroweight;
    float weight;
    int y = 0;
    int z = 0;
    float calibVal;    

    wiringPiSetup ();
    pinMode (CLK, OUTPUT);
    pinMode (DATA, INPUT);

    digitalWrite (CLK, 0);

    //Calibrate based on current load
/*    delay(500);

    for(x=0;x<20;x++)
    {
     if (digitalRead (DATA) == 0)
       {
        zeroweight = (zeroweight + rawADC(twoCompVal));
        delay(50);
       }
     else{x=x-1;}
     }
     zeroweight = zeroweight/(x);
*/
    zeroweight = ini_getl("dataVars", "tare", -1283217, inifile);
    //zeroweight = -1283217;

    calibVal =ini_getl("dataVars", "calibrationVal", 38500, inifile);

    //Read the raw ADC value and average out over 10 reads
    while(weight ==0)
    { weight=0;
      if (digitalRead (DATA) == 0)
     {printf("b");
     for(y = 0; y<10; y++)
     {if (digitalRead (DATA) == 0)
       {
       printf("c");
       weight = weight + ((rawADC(twoCompVal) - zeroweight)/calibVal);
       }
      else {y = y-1;
      printf("d");
      }
     }
     weight = weight/(y);

    printf("%.2f \n", weight); 
     }
    }
}


int rawADC(value, twoCompVal, i)
{
   if (digitalRead (DATA) == 0)
   {
   value = 0;
   for (i = 0 ; i < 25 ; ++i)
   {
    digitalWrite (CLK, 1) ;
    delayMicroseconds (1) ;
    value = (value << 1) | digitalRead (DATA) ;
    digitalWrite (CLK, 0) ;
    delayMicroseconds (1) ;
   }
         if (value >= (1<<23)) {twoCompVal=(value<<8)>>8;}
         else {twoCompVal=value;}
   }
}
