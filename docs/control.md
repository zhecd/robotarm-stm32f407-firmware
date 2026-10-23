# 控制参数与调试入口

| 参数 | 当前默认 | 源码位置 |
|---|---|---|
| 寻位/退回 | 各1000微步/秒，220秒整轮故障截止 | `RobotArm/Service/homing/svc_homing_sequence.c` |
| M1/M2/M3退回 | 4000/1240/400微步，约100°/31°/10° | 同上及`home_sequence` |
| 夹爪 | 开100°、关72°、600ms保持后停PWM | `RobotArm/BSP/driver/include/bsp_driver_config.h` |
| TMC细分/电流码 | 16细分，IRUN28、IHOLD15；码值不是安培 | 同上 |
| 闭环到位死区 | 3°电机轴，约0.667°关节 | `RobotArm/Algorithm/include/common/robot_config.h` |
| 允许尝试恢复窗口 | ≤10°关节，含边界 | 同上 |
| 每轮恢复幅度 | ≤1°关节，约40微步 | 同上 |
| 恢复总期限 | 20000ms，含轨迹和稳定等待 | 同上 |
| 无进展/发散 | 连续3轮改善不足停止；连续2轮明显增长停止 | 同上和`motion/internal/ctrl_closed_loop.c` |

正常轨迹运动时不会仅因离最终目标较远而误触发恢复窗口；静置恢复会用未滤波反馈检查超窗。G-code允许自主恢复，PS2只保留反馈/保护。M411的TARGET_MOTOR/ERROR_MOTOR是电机轴角，ROUNDS表示受理的补偿轮数，不是实际发出STEP的证明。

TMC启动/M999先完成原配置确认，再在EN禁用时写PWMCONF、TPWMTHRS、GCONF，IFCNT独立增3且GCONF/PWMCONF读回及SPREAD输入符合才放行。补偿SPREAD_EN硬件极性，TPWMTHRS写0，启用PWM自动缩放/梯度；不在PS2每帧中反复重配，也不改写VREF、采样电阻、电流或细分。

故障查询优先M408/M409/M411/M412；先保留日志再恢复。配置确认、理论角度、软件队列结束各有边界，不能代替实际电流、波形、末端精度或机械到位测量。
