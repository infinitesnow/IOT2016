#ifndef SAMPLER_H
#define SAMPLER_H

#define INVALID_SAMPLE_VALUE 0x0000
#define UQ_SAMPLER "Sampler"

uint32_t SAMPLE_INTERVAL = 5*1024U; // How often to sample sensors

typedef nx_struct Entry {
  nx_uint16_t values[uniqueCount(UQ_SAMPLER)];
} Entry;

enum {
  SENSORS_NO = uniqueCount(UQ_SAMPLER),   // Total number of sensors
  RETRY_NO = 3,   // Total number of retries before declaring operation failure
};

#endif
