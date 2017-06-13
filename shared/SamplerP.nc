module SamplerP
{
  uses {
    interface Boot;
    interface Leds;
    interface SplitControl as SerialSplitControl;
    interface AMSend;
    interface Timer<TMilli>;
    interface Read<uint16_t>[uint8_t id];
  }
}

implementation
{
  uint8_t sensor_no = 0;  // The sensor currently being sampled
  uint8_t retry_no = 0;   // Number of retries so far
  
  message_t msg;
  Entry* entry;

  event void Boot.booted()
  {
    // entry points to the message payload
    entry = call AMSend.getPayload(&msg, sizeof(Entry));
    call Leds.led1Off();
    // Power on serial output controller. startDone event 
    // will start the timer once the controller is ready 
    call SerialSplitControl.start();
  }

  event void SerialSplitControl.startDone(error_t error)
  {
    call Timer.startOneShot(SAMPLE_INTERVAL);
  }
  
  task void write()
  {
    if ((retry_no <= RETRY_NO)) {
      // Try to print to serial console
      error_t outcome = call AMSend.send(AM_BROADCAST_ADDR, &msg, sizeof(Entry));
      if ( outcome != SUCCESS) {
        // If it didn't succeed, increment counter and try again
        retry_no++;
        post write();
      } 
    } else {
      // Maximum retries number exceeded. Sleeping until next sampling
      call Timer.startOneShot(SAMPLE_INTERVAL);   
    }
  }
  
  task void sample()
  {
    if (sensor_no < SENSORS_NO) {
      // Read the current sensor
      error_t outcome = call Read.read[sensor_no]();
      if ( outcome != SUCCESS) {
        entry->values[sensor_no] = INVALID_SAMPLE_VALUE;
        sensor_no++;
        post sample();   // Samples the next sensor
      }
    } else {
      // All sensors have been read; writes sensor samples 
      // collected in this session to serial console
      retry_no = 0;
      post write();
    }
  }
  
  event void Timer.fired()
  {
    sensor_no = 0;
    call Leds.led1On();
    post sample();   // Samples the first sensor
  }
  
  event void Read.readDone[uint8_t id](error_t error, uint16_t val)
  {
    // Caches the sampled value
    entry->values[sensor_no] = (error == SUCCESS) ? val : INVALID_SAMPLE_VALUE;
    sensor_no++;
    post sample();   // Samples the next sensor
  }
  
  event void AMSend.sendDone(message_t* amsg, error_t error)
  {
    if (error == SUCCESS) {
      call Leds.led1Off();
      call Timer.startOneShot(SAMPLE_INTERVAL);  // Sleep until next sampling
    } else {
      retry_no++;
      post write();
    }
  }

  event void SerialSplitControl.stopDone(error_t error) {}
  default command error_t Read.read[uint8_t id]() { return FAIL; }
}
