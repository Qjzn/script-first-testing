# 真实测试记录 JSON 规范

用于把真实手测结果结构化沉淀，再交给 `manual_to_script.py` 生成测试脚本骨架。

## 最小字段

```json
{
  "preconditions": ["已登录", "已进入目标页面"],
  "steps": ["点击按钮", "上传文件"],
  "assertions": ["URL 正确", "接口返回 200"]
}
```

## 推荐字段

```json
{
  "meta": {
    "project": "fzyc",
    "module": "learning",
    "page": "home",
    "feature": "default-cover",
    "env": "prod",
    "source": "真实手测"
  },
  "preconditions": [
    "已登录 learning",
    "已进入 /course/add"
  ],
  "steps": [
    "点击 选择默认封面",
    "确认弹窗打开",
    "确认默认封面图片数量大于 0"
  ],
  "assertions": [
    "URL 包含 /course/add",
    "默认封面图片数量 > 0"
  ],
  "artifacts": [
    "/tmp/vibetesting/e2e/31_course_add页面.png"
  ],
  "notes": [
    "如上传后 fileInputs 变为 0，不直接判失败，优先看真实请求链路"
  ]
}
```

## 约束

- `preconditions`：前置条件数组
- `steps`：操作步骤数组
- `assertions`：断言数组
- 可选 `meta` / `artifacts` / `notes`
- 一次记录只描述一个功能点，避免把多个流程混在一个 JSON 里

## 推荐实践

1. 一次手测一个功能点
2. 先写最小可复现步骤
3. 再写最关键断言
4. 有截图/日志就写入 `artifacts`
5. 生成骨架后再补自动化实现
