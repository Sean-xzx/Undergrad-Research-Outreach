[English](README.md) | [简体中文](README.zh-CN.md)

# 本科生科研套磁

一个以真实证据建立匹配的 AI skill，帮助本科生把科研兴趣转成联系高校或研究所课题组的具体下一步。

## 价值、贡献、方法与证据

- **价值**：解决“想做科研，却不知道找谁、怎么说明自己的基础、收到回复后如何推进”的断点。
- **贡献**：明确本科生场景，综合 11 篇经验资料和两个 skill 项目，设计完整流程、依据记录与简洁交互，并补齐可复现的验证和打包。开发由作者主导，AI 辅助完成。
- **方法**：允许从任意阶段进入，按需读取指导，把教授工作与学生实际贡献连接起来，以真实联系状态推进回复、面谈、试做和接收确认。
- **证据**：v1.0 保留 **7 个核心文件**，记录 **20 个人工情境**，提供 **12 个仓库回归测试**。测试检查完整性、配置、链接、异常与打包；不能据此认定教授回复率或接收率提高。

## 已实现的范围

目标澄清 → 筛选教授 → 论文入门 → 简历与首信 → 跟进 → 回复解读 → 面谈与试做准备 → 确认机会。

支持已有简历、链接、草稿或回复；零科研可从课程和自学证据开始。区分助手读过与学生本人读过的论文，不强凑匹配；每轮默认一份主要成果和一个下一步。详见[设计与来源](docs/design.md)及[操作指南](docs/usage.zh-CN.md)。

## 快速开始

以下供作者及获准评估者使用，详见[版权说明](COPYRIGHT.md)。

**环境：**Git；科研套磁流程需要支持 skill 的 Codex 环境；仓库验证可选 Python 3.12。核心是 Markdown/YAML，无需 Python、模型权重、数据集、数据库或仓库 API 密钥。查询教授当前信息需要宿主浏览工具；代发邮件需要可用邮件工具与明确授权。

```bash
git clone https://github.com/Sean-xzx/Undergrad-Research-Outreach.git
cd Undergrad-Research-Outreach
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m pip install --no-cache-dir -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/validate_project.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/build_package.py
.\.venv\Scripts\python.exe scripts/validate_project.py --archive dist/undergrad-research-outreach-v1.0.0.zip
```

Linux/macOS 终端：将上述五条命令中的 `.\.venv\Scripts\python.exe` 替换为 `.venv/bin/python`。本机验证使用 Windows、Python 3.12.14；[验证记录](docs/validation.md)区分本机证据、CI 与未验证的宿主行为。

成功时应看到：

```text
PASS: 7 core files unchanged; YAML and local documentation links valid.
Ran 12 tests
OK
Built undergrad-research-outreach-v1.0.0.zip: 7 verified skill files.
PASS: archive contains exactly the 7 original core files.
```

ZIP 只包含 skill。安装依赖需要联网；之后验证、测试和打包可离线完成，不联系教授、不调用模型 API，也不需要 GPU 或付费服务。宿主订阅和工具费用另计；不承诺固定运行或回复时间。

## 在 Codex 中使用

`undergrad-research-outreach/` 是安装单元。本项目使用的本地 Codex 配置将其放在用户的 `.codex/skills/` 目录中。已有同名安装时先备份再替换；宿主发现新 skill 可能需要新会话。

Windows PowerShell 首次安装：

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -LiteralPath .\undergrad-research-outreach -Destination "$env:USERPROFILE\.codex\skills" -Recurse
```

Linux/macOS 终端首次安装：

```bash
mkdir -p ~/.codex/skills
cp -R undergrad-research-outreach ~/.codex/skills/
```

然后发送：

> 用 $undergrad-research-outreach。我是大二本科生，做过 Python 课程项目，没有论文，想探索暑期科研，目前不知道找哪位教授。请从我的情况开始，每次给我一个具体下一步。

这是**示例输入**，不是实际模型测试结果。预期行为是整理已有事实，只问影响当前决策的缺项，不虚构论文或自动发送邮件。见[完整示例](examples/first-contact.md)。若宿主未自动发现，可让它读取 `undergrad-research-outreach/SKILL.md` 及当前阶段需要的参考文件。

## 结构与协作

```text
undergrad-research-outreach/  原样保留的 v1.0 skill 与五份阶段参考
docs/                       设计、来源、使用、验证和开发说明
examples/                   虚构的首次联系情境
scripts/                    验证器与 skill 专用 ZIP 构建工具
tests/                      隔离的有效和无效输入回归测试
checksums/skill-sha256.json  核心文件指纹
.github/workflows/          Windows/Linux Python 3.12 自动检查
```

`SKILL.md` 按当前困境选择机会筛选、写作或后续推进指导；`records.md` 在需要时提供最小个人情况与联系记录；`learning.md` 管理基于来源的修订。宿主负责工具调用与判断。验证器核对原始文件及文档，打包工具封装同一组已验证字节。见[模块关系](docs/design.md)。

## 开发、限制与权利

- [开发与更新命令](docs/development.md)、[验证范围](docs/validation.md)、[来源索引](docs/sources.md)。
- 当前是 v1.0 指令项目，未内置独立爬虫、邮件发送程序或训练模型。自动检查不能证明联网查证质量、模型稳定遵循或真实套磁效果。未提供成功率提升、性能基准或跨 agent 兼容性的实测结论。
- 个人情况、联系记录、缓存、备份及本机工作记录均排除；仓库检查无需秘密配置。
- 工具问题可通过 [Issues](https://github.com/Sean-xzx/Undergrad-Research-Outreach/issues) 提供复现步骤。使用、修改和分发需取得许可；公开展示不授权修改核心功能。
- **保留所有权利，不授予开源许可。**详见[版权与平台权利](COPYRIGHT.md)。外部来源和依赖保留各自权利。
