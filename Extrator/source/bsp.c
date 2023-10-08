#include "bsp.h"

#include "board.h"
#include "peripherals.h"
#include "pin_mux.h"
#include "clock_config.h"

#include "fsl_adc16.h"
#include "fsl_uart.h"
#include "fsl_debug_console.h"

#include <string.h>

#define ADC_MODULE 				ADC0
#define ADC_CHANNEL_GROUP		0

static void BSP_InitAdc(void);

void BSP_InitBoard(void) {
    BOARD_InitBootPins();
    BOARD_InitBootClocks();
    BOARD_InitBootPeripherals();
    BOARD_InitDebugConsole();

	BSP_InitAdc();
}

uint16_t BSP_ReadAdc(uint8_t channel) {
	static adc16_channel_config_t adc_channel_config = {
			.channelNumber = 0,
			.enableInterruptOnConversionCompleted = false,
			.enableDifferentialConversion = false
	};

	adc_channel_config.channelNumber = channel;
	ADC16_DoAutoCalibration(ADC_MODULE);
	ADC16_SetChannelConfig(ADC_MODULE, ADC_CHANNEL_GROUP, &adc_channel_config);
	while(ADC16_GetChannelStatusFlags(ADC_MODULE, ADC_CHANNEL_GROUP) != kADC16_ChannelConversionDoneFlag);
	return (uint16_t) ADC16_GetChannelConversionValue(ADC0, ADC_CHANNEL_GROUP);
}

void BSP_SendUart(const uint8_t *data) {
	UART_WriteBlocking(BOARD_DEBUG_UART_BASEADDR, data, strlen((const char *) data));
}

static void BSP_InitAdc(void) {
	adc16_config_t adc_config;
	ADC16_GetDefaultConfig(&adc_config);
	adc_config.resolution = kADC16_ResolutionSE16Bit;
	adc_config.referenceVoltageSource = kADC16_ReferenceVoltageSourceValt;
	adc_config.longSampleMode = kADC16_LongSampleCycle24;
	ADC16_Init(ADC_MODULE, &adc_config);
	ADC16_EnableHardwareTrigger(ADC_MODULE, false);
	ADC16_SetHardwareAverage(ADC_MODULE, kADC16_HardwareAverageCount32);
}
