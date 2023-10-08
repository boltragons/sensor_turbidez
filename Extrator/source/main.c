#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#include "bsp.h"

typedef enum {
	kSENSOR_01_ID = 1,
	kSENSOR_02_ID,
	kSENSOR_03_ID,
	kSENSOR_04_ID
} SensorID;

#define SENSORS_NUMBER    4
#define SENSOR_01_CHANNEL 9
#define SENSOR_02_CHANNEL 11
#define SENSOR_03_CHANNEL 14
#define SENSOR_04_CHANNEL 20

static uint16_t PRV_ReadSensor(SensorID sensor_id);

static const char *PRV_PrepareMessage(SensorID sensor_id, uint16_t sensor_reading);

static void PRV_ReadSensorAndSend(SensorID sensor_id);

int main(void) {
    BSP_InitBoard();

    while(true) {
    	PRV_ReadSensorAndSend(kSENSOR_01_ID);
    	PRV_ReadSensorAndSend(kSENSOR_02_ID);
    	PRV_ReadSensorAndSend(kSENSOR_03_ID);
    	PRV_ReadSensorAndSend(kSENSOR_04_ID);
    }
}

static uint16_t PRV_ReadSensor(SensorID sensor_id) {
	static uint8_t sensors_channels[] = {
			SENSOR_01_CHANNEL,
			SENSOR_02_CHANNEL,
			SENSOR_03_CHANNEL,
			SENSOR_04_CHANNEL
	};
	return BSP_ReadAdc(sensors_channels[sensor_id]);
}

static const char *PRV_PrepareMessage(SensorID sensor_id, uint16_t sensor_reading) {
    static char message_string[20];
	sprintf(message_string, "%d,%d\n", ((uint8_t) sensor_id + 1), sensor_reading);
	return (const char *) message_string;
}

static void PRV_ReadSensorAndSend(SensorID sensor_id) {
	if(sensor_id < 0 || sensor_id > SENSORS_NUMBER ) {
		return;
	}
	uint16_t sensor_reading = PRV_ReadSensor(sensor_id);
	const char *message = PRV_PrepareMessage(sensor_id, sensor_reading);
	BSP_SendUart((const uint8_t *) message);
}
