# 统一执行入口设计

建议统一入口：

```bash
python3 tests/run_test.py --project fzyc --module learning --page upload --feature image-upload
```

## 职责
1. 根据参数定位脚本
2. 执行脚本
3. 保存日志
4. 保存截图
5. 生成测试结果摘要

## 输出格式
- result: pass/fail/partial
- script_path
- screenshots[]
- logs_path
- summary
- suggestions

## 后续脚本生成器
`scaffold_test.py` 根据项目/模块/页面/功能点生成基础脚本模板。
