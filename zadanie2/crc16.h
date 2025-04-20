#ifndef CRC16_H
#define CRC16_H

#include "crc16.cpp"

#include <stdint.h>

//uint16_t crc16(const uint8_t *data, uint16_t length);

unsigned short crc16_ccitt(const unsigned char *buf, int len);


#endif
