# First-contact scenario / 首次联系示例

**Synthetic input and expected behavior, not a recorded model run or real professor contact.**
**以下是虚构输入与预期行为，不是实际模型运行记录，也没有联系真实教授。**

## Input / 输入

> Use $undergrad-research-outreach. I am a second-year undergraduate with a Python course project and no publications. I am exploring summer research and do not know which professors to contact.

> 用 $undergrad-research-outreach。我是大二本科生，做过 Python 课程项目，没有论文，想探索暑期科研，不知道联系哪位教授。

## Expected next action / 预期下一步

The host should reuse known facts, explain that coursework can provide starting evidence, and ask only questions needed for screening: for example the student's subject/interests and available summer dates/location. It should then provide a small, source-backed candidate list when browsing and necessary facts are available, or clearly mark unknowns.

整理已知背景，以实际课程工作作为起点，只补足筛选所需的问题，例如专业/兴趣、暑期时间与地点。条件和浏览工具具备后给少量有来源的候选；未核实内容保留未知。

A good result contains one main deliverable and one next step. It must not invent publications, assume independent mastery from a course project, guess a professor's email, claim the student read a paper, or silently send a message.

主要成果配一个下一步；不虚构论文、不把课程基础夸成独立科研能力、不拼猜邮箱、不冒称读过论文、不自动发信。

## Repository output you can actually reproduce / 可实际复现的仓库输出

Run the validation, tests and packaging commands in [README](../README.md). Success is a passing check plus a ZIP with exactly the seven original skill files. For the difference between this result and live agent evaluation, see [validation scope](../docs/validation.md).
