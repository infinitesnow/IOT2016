#include "Sampler.h"

configuration SamplerC {}

implementation
{
  components MainC, LedsC, NoLedsC,
    new TimerMilliC() as Timer,
    SerialActiveMessageC as Serial,
    new SerialAMSenderC(0),
    SamplerP;

  components new SensirionSht11C() as TempAndHumid;
  components new HamamatsuS1087ParC() as Photo;

  SamplerP.Read[unique(UQ_SAMPLER)] -> TempAndHumid.Temperature;
  SamplerP.Read[unique(UQ_SAMPLER)] -> TempAndHumid.Humidity;
  SamplerP.Read[unique(UQ_SAMPLER)] -> Photo;
  SamplerP.Boot -> MainC;
  SamplerP.Timer -> Timer;
  SamplerP.Leds -> LedsC;
  SamplerP.SerialSplitControl -> Serial;
  SamplerP.AMSend -> SerialAMSenderC;
}
