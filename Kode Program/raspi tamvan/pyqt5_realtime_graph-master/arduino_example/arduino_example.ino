// ----------------------------------------------------------------------------
//
//
// ----------------------------------------------------------------------------
#include <TimerOne.h>
#include <stdbool.h>

// ----------------------------------------------------------------------------
#define MSG_MAX_LEN 100
volatile uint8_t m_packetBuffer[MSG_MAX_LEN];

// ----------------------------------------------------------------------------
volatile uint8_t m_msgLen;
volatile uint8_t last_val;
volatile uint8_t m_newMessage;
volatile uint32_t m_msgTimeoutCnt_ms;
volatile uint8_t m_packetBufferInd;

// ----------------------------------------------------------------------------
volatile uint32_t testVal0;
volatile uint32_t testVal0_inc;

// ----------------------------------------------------------------------------
volatile uint32_t testVal1;
volatile uint32_t testVal1_inc;

// ----------------------------------------------------------------------------
volatile uint32_t testVal2;
volatile uint32_t testVal2_inc;

// ----------------------------------------------------------------------------
void testVal_init()
{
  testVal0 = 0;
  testVal1 = 0;
  testVal2 = 0;

  testVal0_inc = 100;
  testVal1_inc = 200;
  testVal2_inc = 300;
}

// ----------------------------------------------------------------------------
void timer_tick()
{
  // Packet timeout handler
  if(m_msgTimeoutCnt_ms > 0)
  {
    m_msgTimeoutCnt_ms -= 1;
    if(m_msgTimeoutCnt_ms == 0)
    {
      comHandler_reset();
    }
  }

  // Increment the test values
  testVal0 += (testVal0_inc * 1001);
  testVal1 += (testVal1_inc * 1002);
  testVal2 += (testVal2_inc * 1003);
}

// ----------------------------------------------------------------------------
void timer_init()
{
  Timer1.initialize(1 * 1000);
  Timer1.attachInterrupt(timer_tick);
}

// ----------------------------------------------------------------------------
void uart_init()
{
  Serial.begin(115200);
}

// ----------------------------------------------------------------------------
void uart_sendch(uint8_t ch)
{
  Serial.write(ch);
}

// ----------------------------------------------------------------------------
void comHandler_init()
{
  uint8_t i = 0;
  for(i=0;i<MSG_MAX_LEN;i++)
  {
    m_packetBuffer[i] = 0;
  }
  comHandler_reset();
}

// ----------------------------------------------------------------------------
void comHandler_reset()
{
  m_packetBufferInd = 0;
  m_newMessage = false;
}

// ----------------------------------------------------------------------------
void serialEvent()
{
  while(Serial.available())
  {
    // Read the msg
    volatile uint8_t ch = Serial.read();

    if(m_newMessage == true)
    {
      // ...
    }
    else
    {
      m_packetBuffer[m_packetBufferInd] = ch;
      m_packetBufferInd = m_packetBufferInd + 1;

      if(m_packetBufferInd > MSG_MAX_LEN)
      {
        // Protect from buffer overflow
        m_packetBufferInd = 0;
        m_newMessage = false;
      }
      else if(m_packetBufferInd == m_packetBuffer[0])
      {
        // Signal the main method for new message
        m_packetBufferInd = 0;
        m_newMessage = true;
      }
      else
      {
        m_msgTimeoutCnt_ms = 200;
      }
    }
  }
}

// ----------------------------------------------------------------------------
uint32_t make32b(uint8_t* buff, int32_t offset)
{
  uint32_t rv = 0;
  rv += buff[offset+0] <<  0;
  rv += buff[offset+1] <<  8;
  rv += buff[offset+2] << 16;
  rv += buff[offset+3] << 24;
  return rv;
}

// ----------------------------------------------------------------------------
void put32b(uint32_t val)
{
  uint8_t tmpBuf[4];
  tmpBuf[0] = (val & 0x000000FF) >>  0;
  tmpBuf[1] = (val & 0x0000FF00) >>  8;
  tmpBuf[2] = (val & 0x00FF0000) >> 16;
  tmpBuf[3] = (val & 0xFF000000) >> 24;

  uart_sendch(tmpBuf[0]);
  uart_sendch(tmpBuf[1]);
  uart_sendch(tmpBuf[2]);
  uart_sendch(tmpBuf[3]);
}

// ----------------------------------------------------------------------------
void comHandler_handlePacket()
{
  switch(m_packetBuffer[1])
  {
    // ------------------------------------------------------------------------
    // Test response
    case 0:
    {
      uint8_t i = 0;
      for(i=0;i<10;i++)
      {
        uart_sendch(i);
      }
      break;
    }
    // ------------------------------------------------------------------------
    // Send values of test signals
    case 1:
    {
      put32b(testVal0);
      put32b(testVal1);
      put32b(testVal2);
      break;
    }
    // ------------------------------------------------------------------------
    // Get increment values for test signals
    case 2:
    {
      testVal0_inc = make32b(m_packetBuffer, 2);
      testVal1_inc = make32b(m_packetBuffer, 6);
      testVal2_inc = make32b(m_packetBuffer, 10);
      break;
    }
  }
}

// ----------------------------------------------------------------------------
void setup()
{
  uart_init();
  timer_init();
  testVal_init();
  comHandler_init();
}

// ----------------------------------------------------------------------------
void loop()
{
  // Check for command message
  if(m_newMessage)
  {
    comHandler_handlePacket();
    m_newMessage = false;
  }
}