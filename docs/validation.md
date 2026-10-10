# Validation evidence / 验证证据

This document distinguishes file/tooling verification from model behavior and outreach outcomes.
本记录区分文件与工具验证、模型行为及真实套磁结果。

## Protected baseline / 原始基线

The original seven-file v1.0 skill passed the pre-publication validator. Its SHA256 fingerprints are in [the manifest](../checksums/skill-sha256.json); release checks require these bytes to stay unchanged. Full local snapshots, working notes and the previous archive are preserved outside the public file set.

原始 7 文件 v1.0 在整理前通过验证。公开指纹用于检查其字节未改变；完整本地快照、工作记录和旧包均不上传。

## Manual scenarios / 人工情境

Twenty scenarios were walked through against the instructions before repository preparation: updated versus old availability; zero research; direct drafting without paper reading; student abstract/assistant partial-method reading; coauthor attribution; weak Python-only fit; unavailable homepage and stale recruitment; namesakes; absent GPA; absent attachment; existing user edits; uncertain sending result; two-day silence; explicit refusal; CV/interview invitation; expanding trial tasks; several contacts in one group; competing opportunities; single-letter revision; and ending a source-learning batch.

此前对指令人工走查 20 种情况：资料冲突、零科研、直接起草、阅读范围、共同作者、弱匹配、旧招聘与无法访问、同名导师、成绩或附件缺失、用户修改、发送不明、短期沉默、拒绝、材料与面谈、试做追加、组内多联系人、多机会、单次润色及结束资料学习。

These are instruction reviews, not independent live model executions, and do not measure reply or acceptance rates.

## Reproducible checks / 可复现检查

The repository provides 12 isolated regression tests for original validity, changed or missing core bytes, extra private skill records, manifest traversal, malformed frontmatter, missing or escaping links, stable skill-only packages, extra archive content, corrupt ZIPs and protected output paths. The builder checks its output against the same original manifest.

仓库提供 12 个隔离回归测试，覆盖有效基线及上述异常；构建包核对原始指纹。Commands and expected output: [README](../README.md).

On 2026-10-10, a newly created virtual environment on Windows with Python 3.12.14 and PyYAML 6.0.3 passed source validation, all 12 tests, ZIP construction and packaged-byte validation. The environment was created without system-site packages; the dependency was installed without a pip cache. The skill's seven original SHA256 values remained unchanged.

2026-10-10，在 Windows、Python 3.12.14、PyYAML 6.0.3 的新建虚拟环境中，源文件检查、12 项测试、ZIP 构建和包内字节校验全部通过。环境未启用系统包，依赖安装未使用 pip 缓存；7 个原始文件指纹保持不变。

The [GitHub Actions workflow](../.github/workflows/validate.yml) repeats these checks on Windows and Linux. Published run results are available in [Actions](https://github.com/Sean-xzx/Undergrad-Research-Outreach/actions). Live model/API execution, email transmission and professor responses are outside these checks.

Windows/Linux 自动检查结果可在 Actions 查看。这些检查不调用实际模型/API，不发送邮件，也不验证教授反馈。

## Not established / 尚未证明

- Stable execution of every stage by an independent model or another agent host.
- Current accessibility or correctness of every historical third-party post.
- Improved outreach success rate or guaranteed supervisor availability.
- Live mail integration, a standalone crawler, or strict cross-runtime ZIP compression byte identity.
- macOS execution, unless a later dated verification is added.

以上均不能由结构检查推断；当前没有独立行为评测数据集、模型训练结果或真实套磁效果实验。The project contains no model weights, dataset, random training process or performance benchmark.
