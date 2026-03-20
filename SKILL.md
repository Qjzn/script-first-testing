---
name: script-first-testing
description: 为前端页面、功能点、业务流程建立“脚本优先”的自动化测试体系。用于：用户要求测试某个页面/功能/模块时，先查现有测试脚本并执行；若无脚本，则先自主测试并梳理结构化步骤，再询问是否沉淀为脚本。也用于：生成测试脚本模板、统一执行测试脚本、维护测试索引、迁移历史 smoke/upload 脚本。适用于冒烟测试、页面功能测试、上传/搜索/表单/流程测试、测试脚本盘点、脚本归档、脚本模板化、自动生成测试脚本。
---

# Script First Testing

## 核心原则

1. 先查脚本，再测试。
2. 有脚本先执行，没有脚本再手测。
3. 手测后必须形成结构化步骤。
4. 用户确认后再沉淀成正式脚本。
5. 脚本按“项目/模块/页面/功能点”归档。

## 先看什么

- 查索引：`/home/mifu/openclaw-data/tests/TEST_INDEX.md`
- 看技能目录：`/home/mifu/openclaw-data/skills/script-first-testing/`
- 通用 CLI：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py`
- 查找脚本：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/locate_test.py`
- 生成测试能力目录：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/build_test_catalog.py`
- catalog 字段规范：`/home/mifu/openclaw-data/skills/script-first-testing/references/test-catalog-schema.md`
- 项目配置模板：`/home/mifu/openclaw-data/skills/script-first-testing/references/project-config-template.json`
- 生成真实测试记录模板：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/create_manual_record.py`
- 生成脚本模板：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/scaffold_test.py`
- 从真实测试记录生成脚本骨架：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/manual_to_script.py`
- 登记测试索引：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/register_test.py`
- 统一执行入口：`/home/mifu/openclaw-data/tests/run_test.py`
- 持续推进队列：`/home/mifu/openclaw-data/skills/script-first-testing/tasks/QUEUE.md`
- 下一步建议生成器：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/next_actions.py`
- 看门狗：`/home/mifu/openclaw-data/skills/script-first-testing/scripts/watchdog.sh`

## 标准流程

### 1. 识别测试目标
提取：
- 项目
- 环境
- 模块
- 页面
- 功能点
- 是否已有明确脚本

### 2. 查索引和脚本
优先检查：
- `tests/TEST_INDEX.md`
- `tests/projects/...`
- `locate_test.py` 查具体路径
- 旧脚本目录（如 `workspace/smoke*.py`）

### 3. 决策
- 找到脚本：执行脚本
- 未找到脚本：先用 `locate_test.py` 再确认一次，再自主测试并梳理步骤
- 需要沉淀：用 `scaffold_test.py` 生成模板，用 `register_test.py` 登记索引

### 4. 统一执行
推荐优先走统一 CLI：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py find --project fzyc --module learning --page home --keyword upload
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py run --project fzyc --module learning --page home --keyword upload
```

底层仍可直接使用 `run_test.py`：

```bash
python3 /home/mifu/openclaw-data/tests/run_test.py --project fzyc --module learning --page home
```

如已知要测某个能力点，可直接带 `--feature` 或 `--keyword`，让系统优先选中最匹配的 L2 脚本，而不是默认回退 `smoke.py`：

```bash
python3 /home/mifu/openclaw-data/tests/run_test.py --project fzyc --module learning --page home --keyword upload
python3 /home/mifu/openclaw-data/tests/run_test.py --project fzyc --module manage --page home --keyword default
```

### 5. 模板生成
需要先落一个标准模板时使用：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/scaffold_test.py \
  --project fzyc --module learning --page upload --feature image-upload --level L2 --register-index
```

### 6. 真实测试记录模板
先生成统一记录模板：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py record-template \
  --project fzyc --module learning --page home --feature default-cover --env prod
```

记录规范见：
- `/home/mifu/openclaw-data/skills/script-first-testing/references/manual-record-schema.md`

### 7. 真实测试记录转脚本骨架
真实测试完成后，可把结构化记录转成脚本骨架：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py generate-from-record \
  --input /home/mifu/openclaw-data/tests/drafts/manual-records/fzyc-learning-home-default-cover.json \
  --project fzyc --module learning --page home --feature manual-default-cover --level L2
```

再执行：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py register \
  --project fzyc --module learning --page home --feature manual-default-cover --level L2 \
  --script-path /home/mifu/openclaw-data/tests/projects/fzyc/learning/home/manual-default-cover.py
```

最后重建 catalog：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/test_cli.py build-catalog
```

### 8. 持续推进与看门狗

查看当前推荐下一步：

```bash
python3 /home/mifu/openclaw-data/skills/script-first-testing/scripts/next_actions.py
```

执行看门狗：

```bash
bash /home/mifu/openclaw-data/skills/script-first-testing/scripts/watchdog.sh
```

看门狗会输出：
- skill 仓库 git 状态
- Queue 摘要
- Catalog 数量 / todo 数量
- 当前建议下一步

## 目录规范

```text
tests/
  projects/{project}/{module}/{page}/{feature}.py
  shared/
  reports/
  screenshots/
  TEST_INDEX.md
```

## 何时读取参考文件

- 看整体方案：读取 `references/implementation-plan.md`
- 看脚本分类与目录：读取 `references/test-taxonomy.md`
- 看现有脚本盘点：读取 `references/script-inventory.md`
- 需要统一执行入口时：读取 `references/runner-design.md`

## 当前落地要求

第一阶段先覆盖：
- fzyc
- agent-cockpit
- saas

优先复用并重构现有脚本，不从零重写。

## 已落地样板（真实流程优先）

### fzyc 学习端
- 正式脚本：`/home/mifu/openclaw-data/tests/projects/fzyc/learning/home/smoke.py`
- 文档：`/home/mifu/openclaw-data/output/福州烟草学习端-course-add-真实测试流程.md`
- 真实入口：登录后通过 Vue Router 进入 `/course/add`
- 已验证：默认封面 + 上传链路

### fzyc 管理端
- 正式脚本：`/home/mifu/openclaw-data/tests/projects/fzyc/manage/home/smoke.py`
- 文档：`/home/mifu/openclaw-data/output/福州烟草管理端-course-manage-真实测试流程.md`
- 真实入口：学习端登录后点 `.manage-box` 进入管理中心，再进入 `/dashboard/course-manage`
- 已验证：创建课程表单 + 默认封面 + 上传链路

## 当前执行边界

- `run_test.py` 目前是最小可用版：定位脚本并执行，输出 JSON 结果。
- `scaffold_test.py` 目前是最小可用版：生成标准 Python 模板并可登记到 `TEST_INDEX.md`。
- 复杂浏览器自动化细节优先以“真实手测/真实 E2E 路线跑通后再固化”为准，不再直接迷信旧 smoke 脚本。
