# 独立单轴准备工具

本目录是历史单轴教学对照，正常完整版使用ProductionRelease的三轴并行回零。引脚与当前方向来源见[硬件映射](../../docs/hardware.md)，业务流程见[架构](../../docs/architecture.md)。

`execute_axis_home_after_approval.ps1`等脚本要求显式轴、已验证机械方向、方向证据及单次执行授权；不传入这些参数时在打开串口前拒绝运行。仅阅读或运行SelfTest不需要接机械臂。

独立镜像和正式固件的协议不同，不能把旧HOME/JOG命令发送给正常入口。实际操作前须确认空间、支撑和断电条件，先备份；不要复用已执行的claim，不自动重试动作。
