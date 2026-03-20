# 现有脚本盘点（阶段性）

## 当前最有价值的主模板候选
1. `workspace/smoke_manage_153.py`
2. `workspace/smoke_learning_153.py`

## 可参考但不宜直接作为主模板
- `workspace/smoke_upload.py`
- `workspace/smoke_upload_test.py`
- `workspace/smoke_final.py`
- `workspace/smoke_v3.py`
- `workspace/smoke_v4.py`
- `workspace/smoke_v5.py`
- `workspace/smoke_test_env.py`
- `workspace/smoke_test_env2.py`
- `workspace/smoke_test_env3.py`

## 已确认的共性问题
- 依赖外部 18800/18801 CDP 端口
- 登录成功判断不可靠
- 缺少关键 DOM 断言
- 路径、账号、截图目录硬编码
- 上传脚本依赖不统一（如 websockets）
