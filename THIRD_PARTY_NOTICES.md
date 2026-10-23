# 第三方组件

根目录 Apache-2.0 适用于项目自编部分，不替代第三方文件中的许可证和版权声明。

| 组件 | 路径 | 随原工程保留的许可文件 |
|---|---|---|
| STM32F4 HAL / LL | `Drivers/STM32F4xx_HAL_Driver/` | [原 LICENSE.txt](Drivers/STM32F4xx_HAL_Driver/LICENSE.txt)，原文说明包许可缺省时适用 BSD-3-Clause |
| Arm CMSIS Core headers | `Drivers/CMSIS/Include/` | [Apache-2.0 原文](Drivers/CMSIS/LICENSE.txt) |
| STM32F4 CMSIS Device headers | `Drivers/CMSIS/Device/ST/STM32F4xx/Include/` | [原 LICENSE.txt](Drivers/CMSIS/Device/ST/STM32F4xx/LICENSE.txt)，原文说明包许可缺省时适用 Apache-2.0 |
| CubeMX 生成的启动、系统及外设文件 | `Core/`、根目录启动文件 | 保留各文件的 STMicroelectronics 版权与许可说明 |

这里只分发本工程构建需要的驱动和头文件，未打包无关的 CMSIS DSP/NN 示例、文档或预编译库。没有改写第三方源文件和许可内容。根 LICENSE 是完整 Apache-2.0 文本。
