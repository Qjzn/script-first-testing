# 测试脚本分类标准

## L1 冒烟测试
- 页面是否打开
- 核心元素是否存在
- 是否明显报错

命名：`smoke.spec.ts` 或 `*-smoke.py`

## L2 页面功能测试
- 上传
- 搜索
- 保存
- 删除
- 筛选

命名：`image-upload.spec.ts`、`search-course.spec.ts`

## L3 业务流程测试
- 登录 -> 创建 -> 提交
- 查询 -> 审核 -> 发布

命名：`create-course-flow.spec.ts`

## L4 回归测试集
- 按模块聚合执行
- 面向发版前回归

## 路径规则
`项目 / 模块 / 页面 / 功能点`

示例：
- `tests/projects/fzyc/learning/upload/image-upload.spec.ts`
- `tests/projects/fzyc/manage/course/create-course.spec.ts`
