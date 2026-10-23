# 教学及诊断工具

当前正常入口是根目录ProductionRelease，不需要运行本目录脚本即可构建或用串口控制。

- `host/`：已有协议解析、单次发送客户端、离线任务预检和C模型预演，作为后续视觉接入的参考；不包含OpenCV识别或相机标定产品。
- `startup_trial/`：独立锁定/单次启动试验、离线ELF比较、只读解析和SelfTest。与正常固件协议不同。
- `m1_homing/`、`gripper_test/`、`tmc_bench/`：独立单轴/夹爪/外接电机教学对照。
- `limit_probe/`、`startup_audit/`、`limit_seek_trial/`：旧EXTI与输入隔离诊断对照；正常限位为GPIO周期采样。
- `tmc_config_probe/`、`uart_boot_probe/`：独立配置确认及串口心跳诊断入口。

保留这些源文件是因为测试与CMake诊断目标需要它们，不表示需要重新执行历史现场流程。历史电脑专用OpenOCD运行助手已排除。其余带execute/run/query字样的脚本也不是普通构建入口；运行前阅读参数和授权门禁，永远不要复用已用claim。

部分主机脚本需要PowerShell，真实串口参考工具可能需要另装pyserial；默认电脑C/Python测试只用标准库与替身，不接设备。
