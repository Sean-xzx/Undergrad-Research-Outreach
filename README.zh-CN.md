[English](README.md) | [简体中文](README.zh-CN.md)

# 本科生科研套磁 v1.1.5

帮助本科生主动发现导师、核验研究与参与条件，再推进论文入门、材料、写信、跟进和确认机会。原有用户记录保留在私人项目，不随发布包上传。

## v1.1.5 局部修订与完整稿恢复

保留已认可措辞，按修改范围合并片段并保存当前完整版本；单个导师的选题调整不覆盖总体兴趣。文字接受、附件定位/上传和实际发送分别判断。[12个恢复验收场景](evals/revision-recovery-cases.json)尚未执行独立模型测试。用户私人记录与历史版本保留，不随公共包发布。

## 这次更新

- 三种模式：快速起步、广泛发现、定向核查。要求拓广时，沿学校院系、论文作者与合作项目补漏，不依赖用户报齐学校。
- 字段证据：研究候选、可询问机会、公开条件符合分别呈现，未知和冲突不能当满足。
- 本地SQLite账本：稳定身份ID、唯一论文、年度下限计算、检索队列、真实联系事件、事务提交与中断恢复。
- 兼容导入旧候选，原payload和原联系状态保留，旧文字结论不自动变成已核实事实。
- 配套规则测试、发布测试与独立模型评测协议；不声称已验证召回率、回复率或接收率提升。

## 使用

安装单元是`undergrad-research-outreach/`。放入宿主的skills目录；已有同名安装先备份，只同步公共skill文件，不替换用户项目。新会话可能需要重新发现skill。

> 用 $undergrad-research-outreach。我是大二，想做具身世界动作模型，偏向长三角、深圳和香港，可远程。请主动拓广并整理候选，直接研究和相邻方向分开，保留未知条件与来源。

这是示例请求，不是已执行的模型测试。也可从已有导师、草稿或回复开始，不必重新找人。使用详见[指南](docs/usage.zh-CN.md)，运行工具详见[账本契约](undergrad-research-outreach/references/runtime.md)。

## 环境与检查

指令使用需要支持skill和联网工具的宿主。账本工具使用Python 3.12+标准库，无独立服务器、模型密钥或邮件发送功能。仓库验证另需PyYAML。联网发现和证据阅读由宿主完成，程序只检查结构、引用与确定性规则。

```bash
git clone https://github.com/Sean-xzx/Undergrad-Research-Outreach.git
cd Undergrad-Research-Outreach
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/validate_project.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/build_package.py
.\.venv\Scripts\python.exe scripts/validate_project.py --archive dist/undergrad-research-outreach-v1.1.5.zip
```

Linux/macOS使用`.venv/bin/python`替换解释器路径。CI运行Windows/Linux Python 3.12；本机结果见[验证记录](docs/validation.md)。

## 结构

`SKILL.md`负责模式与阶段路由；references按需加载发现、证据、记录、写作与跟进；包内scripts提供本地账本；仓库scripts负责版本校验与打包；tests验证业务及发布；evals提供尚需真实模型运行的行为评测用例。

当前发布清单有12个文件，旧v1.0七文件指纹另行保留。ZIP仅包含公共skill，不含私人数据库、名单、简历、输出、备份或凭据。包内代码没有爬虫和自动外部联系。导出视图为JSON，Excel由可用表格工具生成。

## 文档与限制

[设计](docs/design.md) · [开发](docs/development.md) · [验证](docs/validation.md) · [来源](docs/sources.md) · [行为评测](evals/README.md) · [Issues](https://github.com/Sean-xzx/Undergrad-Research-Outreach/issues)

程序无法证明网页真假或模型研究分类正确，需原文阅读和抽查。正式论文下限不足不直接判低产。独立模型发现性能与真实套磁结果尚未验证。

**保留所有权利，不授予开源许可**。使用、修改和分发需取得许可；用户明确授权本次项目升级。见[版权说明](COPYRIGHT.md)，第三方来源和依赖保留各自权利。

## v1.1.4 多导师连续写作

持续保留方向优先级；发送建议前核查时长、地点、实际承接组织及投递渠道；保留模型别名和时间承诺适用范围。微调不改结构，受限检索不宣称“全网没有表格”。[新增20个验收场景](evals/multi-target-cases.json)尚未运行独立模型测试。

## v1.1.3 邮件与申请表

按用户兴趣与教师实际角色共同选文；核对手工编辑中的录用/发表冲突；按需加入简短参与计划；按字段准备英文申请表并恢复最新局部修改。提交表单与发送邮件分别记录。[新增16个验收案例](evals/form-cases.json)尚未作为独立模型测试执行。

## v1.1.2 写作更新

从真实经历提炼有依据的能力和研究联系；支持具体、适度的认可，避免虚构技能与上手计划；局部修订保留用户编辑，核查近期论文及合作归属。个人偏好仍保存在私人项目。[写作验收案例](evals/writing-cases.json)与[验证范围](docs/validation.md)分别记录；未宣称模型行为或回复率已改善。
