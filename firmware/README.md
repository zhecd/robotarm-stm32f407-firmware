# 视觉分拣配套固件 190-vision-20261120

| 文件 | 用途 |
|---|---|
| [VisionStationRelease.hex](VisionStationRelease.hex) / [BIN](VisionStationRelease.bin) | 对应已完成三色分拣的视觉工位。HEX 与该工位此前烧录的镜像逐字节一致。此版编入此前用于排查关节往返的 `M413` 诊断。 |
| [ProductionRelease.hex](ProductionRelease.hex) / [BIN](ProductionRelease.bin) | 通用构建，包含本次回零与 `M400` 更新。此版通过本机编译和 ELF 审计，实机分拣记录对应视觉工位版。 |

两版面向 STM32F407VETx。HEX 自带地址，使用 BIN 时指定 Flash 起址 `0x08000000`。在 [SHA-256 清单](SHA256SUMS) 中核对下载文件。

上电或复位会自动关闭夹爪并三轴并行回零。寻位和退回均为 1000 微步/秒，M1／M2／M3 分别退回 101.7°／29°／4°，整轮截止为 220 秒。构建和测试均在电脑上执行。

按 [构建说明](../docs/build-and-test.md) 导出文件，按 [验证说明](../docs/validation.md) 核对实机记录和适用范围。
