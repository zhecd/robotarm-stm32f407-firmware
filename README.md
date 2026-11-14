# RobotArm STM32F407 Firmware

教学机械臂下位机固件。

用于空载教学机械臂的 STM32F407 固件：三轴运动、回零、限位保护、编码器反馈、有界闭环恢复、PS2 遥操作和 MG90S 夹爪。上位机通过 **115200 / 8N1** 的 ASCII G-code 协议控制末端位置。

本项目基于 **190 功能基线**，正式回零配置为 **2026-11-14 校准版**，使用独立仓库与独立版本历史。包含生产源码、必要第三方驱动、模块测试、中文文档和正式固件，不包含历史工程的大量备份和构建缓存。

GitHub仓库：[`zhecd/robotarm-stm32f407-firmware`](https://github.com/zhecd/robotarm-stm32f407-firmware)，初始可见性为私有，许可证为Apache-2.0。

**正式固件上电/复位会自动关闭夹爪并执行三轴回零。** 测试前保证机构行程、支撑及线束允许，能现场切断电源。`M112` 是软件停止，会撤销零位并禁用电机输出；M3 关节断能后可能受重力移动。纯软件测试不连接机械臂。

| 功能 | 当前实现 |
|---|---|
| 启动与恢复 | 驱动配置读回确认；三轴并行寻限位，全部确认后并行退回；显式 M999 恢复 |
| 回零参数 | M1/M2 D0、M3 D1；寻退 1000 微步/秒；退回 100°/29°/4°；整轮 220 秒截止 |
| 限位 | 普通 GPIO、1ms 周期采样、10ms 稳定确认；限位 EXTI 关闭，SW7 仍用 EXTI |
| 控制与反馈 | 直线分段规划、逆解、STEP 队列、三路 AS5600；≤10°关节误差有界恢复 |
| 人机交互 | G-code / PS2 模式切换；LED1 串口常亮、PS2 慢闪，LED2/3/4 对应三路限位 |
| 夹爪 | MG90S：100°打开、72°关闭，600ms 保持后停 PWM |
| TMC2209 | 串口配置确认及 StealthChop 配置；保留限流、细分及故障保护 |
| 视觉扩展 | 保留坐标运动、反馈、夹爪与恢复协议；未新增 OpenCV 或相机标定实现 |

## 快速开始

依赖：CMake ≥3.22、Ninja、Python ≥3.10、原生 GCC（电脑测试），Arm GNU Toolchain（固件）。工具放入 PATH；不需要特定电脑的安装目录。

```sh
# 不接硬件即可运行的电脑测试
cmake --preset HostTests
cmake --build --preset HostTests --parallel
ctest --test-dir build/HostTests --output-on-failure

# 完整正常固件；构建不会自动烧录
cmake --preset ProductionRelease
cmake --build --preset ProductionRelease --parallel
```

输出：`build/ProductionRelease/robotarm_stm32f407.elf`。仓库 `firmware/` 提供已校验的正式 HEX/BIN；说明和哈希见 [固件入口](firmware/README.md)。[构建与测试](docs/build-and-test.md)包含 Release 测试、阶段测试、HEX 导出与编译锁定版本。

## 目录与阅读顺序

```text
Core/                CubeMX 外设、启动与中断入口
RobotArm/            App / Service / Device / BSP / Algorithm / Platform
Drivers/             构建所需 STM32 HAL 与 CMSIS
cmake/               工具链和 CubeMX 构建描述
tests/               真实生产模块的电脑测试及设备/时钟替身
tools/               离线协议参考、教学诊断和受控试验工具
scripts/             架构检查、ELF 审计和离线发布校验
docs/                当前架构、硬件、协议、教学与验证边界
firmware/            190 正常固件和校验清单
.github/workflows/   仅构建/测试的 CI，不烧录、不发布
```

推荐阅读：[架构](docs/architecture.md) → [硬件映射](docs/hardware.md) → [构建测试](docs/build-and-test.md) → [串口协议](docs/serial-protocol.md) → [教学模块顺序](docs/teaching/module-guide.md)。[贡献约定](CONTRIBUTING.md)、[变更摘要](CHANGELOG.md)、[已知限制与验证](docs/validation.md)。

## 交付边界

190 已通过 Debug/Release 各 558 项本机电脑测试、7 种固件构建审计及部署时独立 Flash 回读。本地发布整理会再次独立验证；准确结果见 `docs/validation-summary.json`。历史整机空载回归与最新补丁测试分开记录，不把历史通过等同于190所有工况已重新验收。

本项目面向空载教学。绝对末端精度、实际10°扰动纠偏效果、持续运行及实际降噪仍需相应实测。PS2 曾有偶发异常帧，现有保护和首坏帧诊断保留，根因未宣称消除。详情见 [验证说明](docs/validation.md)。

自编代码采用 [Apache-2.0](LICENSE)。第三方组件保留原许可及版权，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
