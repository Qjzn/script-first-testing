# 自动化测试技能实施计划

## Phase 1：盘点现有脚本
- 识别可运行脚本
- 标记主模板 / 归档 / 淘汰
- 提取共性问题：依赖、CDP、登录态、断言不足

## Phase 2：建立统一目录
建议目录：

```text
tests/
  projects/
    fzyc/
      learning/
      manage/
      env/
    agent-cockpit/
    saas/
  shared/
    helpers/
    config/
  reports/
  screenshots/
  _archive/
  TEST_INDEX.md
```

## Phase 3：提炼主模板
当前优先模板：
- `smoke_manage_153.py`
- `smoke_learning_153.py`

提炼公共能力：
- Chrome/CDP 启动
- 登录态检查
- URL 断言
- 页面关键 DOM 断言
- 截图
- console 错误收集

## Phase 4：统一执行入口
形态：
- `run_test.py`
- `locate_test.py`
- `register_test.py`
- `scaffold_test.py`

## Phase 5：脚本沉淀规则
无脚本时：
1. 自主测试
2. 梳理步骤
3. 用户确认
4. 生成脚本
5. 更新索引
