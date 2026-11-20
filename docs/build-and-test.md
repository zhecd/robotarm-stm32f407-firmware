# 构建与测试

所有命令从仓库根目录执行。Python ≥3.10；CMake ≥3.22；Ninja；原生 GNU GCC；固件另需 `arm-none-eabi-gcc`、`arm-none-eabi-objcopy`、`arm-none-eabi-nm`、`arm-none-eabi-objdump`。Windows 可用 MinGW-w64，不使用 MSVC 构建这些 GNU 链接测试。PowerShell 7 或 Windows PowerShell 用于部分脚本 SelfTest；未安装时对应可选测试不会注册，测试数可能少于 Windows 本机的 559 项。

## 电脑验证（不接硬件）

```sh
cmake --preset HostTests
cmake --build --preset HostTests --parallel
ctest --test-dir build/HostTests --output-on-failure
cmake --preset HostTestsRelease
cmake --build --preset HostTestsRelease --parallel
ctest --test-dir build/HostTestsRelease --output-on-failure
python -B scripts/check_architecture_dependencies.py
```

Python只用标准库完成默认测试，不要求 pyserial。可通过 `-DPython3_EXECUTABLE=...` 指定解释器。若切换编译器，请使用新的构建目录，不复用不同工具链的缓存。运行测试只使用替身、自检分支及临时目录，不创建真实串口连接。

教学可独立执行 `cmake --build build/HostTests --target check_stage0`，阶段范围0至7；完整测试列表用 `ctest --test-dir build/HostTests -N`。Release保留assert并把警告视为错误。

## 固件构建

```sh
cmake --preset ProductionRelease
cmake --build --preset ProductionRelease --parallel
cmake --preset ProductionDebug
cmake --build --preset ProductionDebug --parallel
arm-none-eabi-objcopy -O ihex build/ProductionRelease/robotarm_stm32f407.elf build/ProductionRelease/robotarm_stm32f407.hex
arm-none-eabi-objcopy -O binary --gap-fill 0xff build/ProductionRelease/robotarm_stm32f407.elf build/ProductionRelease/robotarm_stm32f407.bin
```

`ProductionRelease`、`ProductionDebug` 和 `VisionStationRelease` 上电执行自动夹爪关闭及并行回零。构建只生成产物。

```sh
cmake --preset VisionStationRelease
cmake --build --preset VisionStationRelease --parallel
arm-none-eabi-objcopy -O ihex build/VisionStationRelease/robotarm_stm32f407.elf build/VisionStationRelease/VisionStationRelease.hex
arm-none-eabi-objcopy -O binary --gap-fill 0xff build/VisionStationRelease/robotarm_stm32f407.elf build/VisionStationRelease/VisionStationRelease.bin
```

发布版使用 Arm GNU Toolchain 15.2.Rel1（GCC 15.2.1）构建。视觉工位版启用此前用于查验关节往返的诊断入口，正常分拣仍使用通用协议。使用 [SHA-256 清单](../firmware/SHA256SUMS) 核对发布文件。

```sh
# 编译层禁止动作的诊断入口；仍不会自动烧录
cmake --preset ProductionLocked
cmake --build --preset ProductionLocked --parallel
```

`ProductionTrial`、`ProductionHold*`及`Teaching*`保留教学/诊断用途，有各自专用协议与动作条件；不是正式固件的替代名。不要把它们的START/KEEP/HOME指令发送给正常正式入口。

## 一次执行全部离线验证

`python -B scripts/validate.py --firmware` 会重复 Debug/Release、架构、7种固件审计和发布树检查；不加 `--firmware` 只运行电脑测试与检查。日志输出到被忽略的 `build/validation/`，不会连接设备。

## ELF与发布树检查

```sh
python -B scripts/audit_firmware.py --name ProductionRelease --build-dir build/ProductionRelease --output build/audit --home-period-ms 1
python -B scripts/check_release.py
```

审计检查实际生成的GPIO限位/并行回零分支、采样路由、协议字符串及配置。它不是实物波形测试。审计应使用与ELF同套的Arm工具，工具通过PATH发现。

CI只在电脑上执行配置、编译、测试及ELF审计，没有烧录、机械动作、推送或Release发布步骤。工作流随推送触发，实际结果见仓库Actions；本机测试与在线测试分别记录。离线PowerShell传输自检的CTest外层预算为60秒，以容纳托管执行器冷启动，协议内部等待和机械臂保护期限不变。

## CubeMX

保留 `.ioc` 供查看硬件配置。重新生成可能覆盖手工调整（尤其GPIO限位分支、UART和中断适配）；生成后必须检查差异并重跑测试，不要把CubeMX生成成功当作业务逻辑正确。
