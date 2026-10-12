# 本地账本运行契约

Python 3.12+标准库，SQLite单写入者；不访问网络、不发送邮件。路径下的数据库、来源与导出只在用户项目，保持原Markdown和Excel不变。

## 操作

把`<skill>`替换为实际安装目录，`<project>`为用户工作目录，JSON文件由助手根据原始来源整理。

```text
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 init
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 ingest --input batch.json
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 evaluate
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 next-tasks
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 resume
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 export-view --output view.json
python <skill>/scripts/outreach_state.py --db <project>/outreach/state.sqlite3 import-legacy --input candidates.json
```

所有命令输出JSON，错误返回非零退出码。export-view输出结构化视图，Excel由可用表格工具生成；不能声称脚本已生成xlsx。init对已有库不重置；未知schema版本报错保留。单次ingest整批校验、事务提交；重复ID内容相同不增加历史，不同内容保留revision。events不可改写，修正追加事件。

## 输入

顶层仅允许entities、sources、claims、papers、constraints、tasks、events数组，具体字段见[JSON Schema](../scripts/schemas/batch.schema.json)。不提供的数组表示不变；没有删除操作。

- entities：稳定id，type为researcher/institution/project/paper，name及可选aliases/institution_id/legacy。ID由助手确认身份后分配，不能只用姓名，也不能把学生当researcher导师实体。legacy只是原样保存，不是核实。
- sources：id、http(s) url、带时区observed_at、access（retrieved/restricted/failed）、read_scope，可附page_date/excerpt。原始短摘录及定位足够，不需复制整页。
- claims：id、subject_id、predicate、value、status、evidence数组。状态pending/supported/contradicted/conflict/superseded。evidence包含source_id、locator、relation（supports/contradicts）；引擎保存source_digest。supported不能没有支持或带未解决反证。语义审查由助手承担。
- papers：实体paper的id、author_ids、year（venue年度）、status、paper_type、ccf_category、ccf_catalog及evidence字典。六个计数字段各绑定同主体、同predicate、同value的claim_id。缺证据可保存，但不计数。相同论文不同版本必须先归为同一个id。
- constraints：id、predicate、operator（eq/in/ge）、value、kind（hard/preference）、scope（all或实体ID）、origin，可附exceptions实体ID数组。annual_ccf_ab_count使用ge，value为year/catalog/minimum；其余从教师同predicate的claims取结论。机构条件可整理成教师对应断言，例外按institution_id匹配；声明对应关系不得凭空推断。
- tasks：id、kind、target_id、state、reason、path；可附depends_on/attempts。state为pending/running/done/retryable/blocked/cancelled，依赖须存在且无环。coverage任务reason写已查范围、发现/无结果/受限的具体结论。next-tasks排序身份冲突、覆盖、核查、发现；任务生成和补漏语义判断由助手进行，不是自动爬虫。
- events：id、subject_id、type、带时区occurred_at、basis，可附payload。type见schema；确认发送/回复需工具回执或用户明确说明。真实事件独立于候选重建，旧状态import只存legacy_imported。

## 结果与边界

evaluate返回snapshot、逐条件状态、已核实年度下限、研究分类、三类候选状态和contact_state。current_identity、research_category、contact_channel为教师断言predicate；可信的支持值才进入研究/询问视图。不同有效支持值视作冲突；未明确superseded的相反记录会阻断结论。

年度数量不足输出UNKNOWN，而非从不完整列表判FAIL；需人工完整核查时另存依据。source内容/读取记录变化后依赖claim退回pending；同源重读产生新读取版本也需确认后重新提交证据。引擎不判断文章是否被模型误读，仍要抽查高价值结论。

resume把未提交完成的running任务改retryable，返回约束、队列与视图。scope_complete只度量登记coverage任务；不能替代广泛发现的范围检查。首版未内置网页抓取、模型调用、跨进程任务租约、历史snapshot重导出或自动实体合并。

import-legacy原样保留每条记录和旧联系状态，身份ID以学校/姓名/主页组合生成迁移锚点，仍需消歧；这是一次性兼容路径，不是今后身份合并算法。重导旧数据不改变现有真实事件，也不把旧文字变为达标。
