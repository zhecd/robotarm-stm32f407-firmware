# 教学阅读与独立测试顺序

按模块依赖组织，无需和原课程课次一一对应。先看公开合同与单位，再看实现和替身测试，最后才做实机实验。

| 顺序 | 模块与阅读入口 | 电脑验证 |
|---|---|---|
| 0 | Algorithm运动学、微步换算；`robot_config.h` | `check_stage0`、`robotarm_logic_tests` |
| 1 | UART行组帧、超时、环缓冲 | `check_stage1`、`uart_line_reader_tests` |
| 2 | Motion帧队列和STEP执行 | `check_stage2`、`motion_engine_tests` |
| 3 | Device映射、AS5600/TMC/PS2/MG90S；GPIO消抖、回零纯算法 | `check_stage3`、`gpio_filter_*`、`parallel_homing_*` |
| 4 | Command/Planning/Safety/State服务职责 | `check_stage4`、`planning_service_tests` |
| 5 | App启动/M999/协议、模式和闭环集成 | `check_stage5`、`gpio_runtime_*`、`mode_switch_visibility_*` |
| 6 | 其他阶段与诊断对照 | `check_stage6`（以CTest实际标签为准，阶段可能无专属测试） |
| 7 | TMC CRC、地址、寄存器确认和静音 | `check_stage7`、`tmc2209_driver_tests` |

执行示例：`cmake --build build/HostTests --target check_stage5`；单项筛选：`ctest --test-dir build/HostTests -R mode_switch_visibility --output-on-failure`。分阶段命令不是硬件动作。

`tests/support`和`tests/hal_stubs`提供设备、时间或传输替身；被测Service/App/Algorithm及器件代码仍为生产实现。替身不模拟真实接触、重力、电流或声学。测试通过只表示对应软件合同成立。

先读 [架构](../architecture.md)、[串口协议](../serial-protocol.md)和[验证边界](../validation.md)。`tools/`保留旧EXTI、单轴和锁定试验供分析对照，默认阅读不运行，不据此推断当前Production使用EXTI限位或低速500/s参数。
