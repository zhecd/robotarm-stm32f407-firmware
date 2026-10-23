/** 真实协议/命令/规划链，替换串口字节端口与设备时间；不连接板卡。 */
#include "app/app_serial_protocol.h"
#include "command_service.h"
#include "motion_service.h"
#include "safety_service.h"
#include "state_service.h"
#include "app/app_teleop.h"
#include "fake_robot.h"
#include "fake_hardware.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static void Send(const char *line)
{FakeHardware_ClearTx();FakeHardware_SendLine(line);AppSerial_Service();}
int main(int argc,char **argv)
{
    assert(argc==2);FakeRobot_Reset();FakeHardware_Reset();StateService_Init();SafetyService_Init();
    MotionService_Init();MotionService_InitClosedLoop();
    assert(CommandService_Init(0,185,240)==ERR_OK);
    SafetyService_MarkHomed();SafetyService_ClearAfterSuccessfulHoming();
    App_Teleop_SetMode(SYS_MODE_GCODE);AppSerial_Init(APP_SERIAL_READY);
    if(!strcmp(argv[1],"queries")) {
        Send("M115");assert(strstr(fake_tx,"M115 FIRMWARE:RobotArm") && strstr(fake_tx,"UART:115200"));
        Send("M408");assert(strstr(fake_tx,"STATE:READY HOMED:1 ALLOWED:1 MODE:GCODE FAULT:0"));
        Send("M114");assert(strstr(fake_tx,"M114 PLAN X:0.00 Y:185.00 Z:240.00"));
        Send("M119");assert(strstr(fake_tx,"M1:OPEN M2:OPEN M3:OPEN"));
    } else {
        Send("G1 X5 Y190 Z235 F120");assert(CommandService_IsMotionPending());
        if(!strcmp(argv[1],"burst")) {
            Send("M400");assert(strstr(fake_tx,"error: previous command pending"));
            Send("M114");assert(strstr(fake_tx,"M114 PLAN"));
        }else assert(!strcmp(argv[1],"ordered"));
        FakeHardware_ClearTx();
        for(unsigned i=0;i<1000 && !strstr(fake_tx,"ok\r\n");i++) {
            CommandService_Service();AppSerial_Service();
        }
        assert(strstr(fake_tx,"ok\r\n")); /* G1受理回复，不是运动完成。 */
        Send("M400");assert(!strstr(fake_tx,"error:"));
        for(unsigned i=0;i<20000 && !strstr(fake_tx,"ok\r\n");i++) {
            CommandService_Service();
            for(unsigned j=0;j<100;j++)MotionService_OnStepTickFromISR();
            FakeRobot_AdvanceUs(2000);AppSerial_Service();
        }
        assert(strstr(fake_tx,"ok\r\n") && MotionService_IsIdle());
        Send("M114");assert(strstr(fake_tx,"M114 PLAN X:5.00 Y:190.00 Z:235.00"));
    }
    printf("serial_reply_flow %s passed\n",argv[1]);return 0;
}
