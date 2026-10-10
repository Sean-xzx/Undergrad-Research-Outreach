# Development and verification / 开发与验证

These instructions apply to the author or authorized evaluators. [All rights reserved](../COPYRIGHT.md); public visibility does not authorize changes to core behavior.

以下供作者及获准评估者使用；公开查看不授权修改核心功能。

## Environment / 环境

Python 3.12 and Git; PyYAML 6.0.3 is the sole validation dependency. Tests use Python's standard-library unittest; packaging uses zipfile. No secrets, CVs, professor contacts or model API are needed. No third-party runtime code is vendored.

Python 3.12、Git；验证仅依赖固定版本 PyYAML 6.0.3。测试与打包使用标准库，无需密钥、个人履历或模型 API。

Use the clean-venv commands in the [English README](../README.md) or [Chinese README](../README.zh-CN.md). Linux/macOS equivalents:

```bash
python -m venv .venv
.venv/bin/python -m pip install --no-cache-dir -r requirements-dev.txt
.venv/bin/python scripts/validate_project.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_package.py
.venv/bin/python scripts/validate_project.py --archive dist/undergrad-research-outreach-v1.0.0.zip
```

## What the checks establish / 检查的意义

- Validate the seven exact core bytes, YAML metadata and local documentation links.
- Reject missing/modified core files, unexpected private skill files, unsafe manifest paths, malformed metadata, and broken or escaping documentation links.
- Build two archives with identical metadata in one runtime; verify only original skill bytes are included. ZIP compression bytes across different zlib/runtime versions are not a strict portability promise.
- Reject corrupted archives, added private files and output paths inside the protected skill directory.

核对核心字节、配置与内部链接；拒绝缺失、修改、私人附加文件、越界路径、损坏配置和打包错误。同一运行环境中构建结果稳定；跨压缩库版本不承诺 ZIP 压缩字节完全相同，核心文件内容仍按指纹校验。

Validation is deterministic and offline after dependency installation. It does not run the skill through a live model, send mail, or validate an outreach success rate. [Evidence and limitations](validation.md).

## Troubleshooting / 排错

- Missing yaml module: install requirements using the same venv interpreter used to run the commands.
- Integrity failure: compare the named core file against the committed v1.0 source. Do not update the checksum merely to suppress an unexpected change.
- Broken link: repair the document path; do not remove an important resource to pass the check.
- Discovery failure: ask the host to read the skill entry file and relevant references; discovery locations are host-specific.

缺少 yaml 时用同一虚拟环境安装依赖；指纹失败先比较原始文件，不改指纹掩盖变更；链接失效时修正文档引用；未发现 skill 时可明确要求宿主读取主文件。

## Updating the repository / 更新仓库

Run validation, tests and packaging, review the staged files, then use ordinary commits and pushes. No force push is necessary. Publishing tooling never uses the account password or stores an API token in the repository.

先验证、测试和打包，检查暂存内容，再普通提交和推送。不要提交用户记录、备份、缓存或凭据。核心功能变更需作者另行授权。

```bash
git status --short
git add README.md README.zh-CN.md docs scripts tests requirements-dev.txt .github
git diff --cached --stat
git commit -m "Update documentation and verification"
git push origin main
```

CI runs the same validation, 12 tests and build on Windows/Linux standard hosted runners, with read-only repository permissions. Issues should contain the failing command, runtime version and redacted error output. The workflow does not run an external model or use paid runners.
