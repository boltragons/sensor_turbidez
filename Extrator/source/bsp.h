#ifndef BSP_
#define BSP_

#include <stdint.h>

void BSP_InitBoard(void);

uint16_t BSP_ReadAdc(uint8_t channel);

void BSP_SendUart(const uint8_t *data);

#endif
