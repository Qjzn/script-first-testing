# TEST_CATALOG 结构化字段

每条测试脚本记录建议包含：

- `project`
- `module`
- `page`
- `feature`
- `summary`
- `tags`
- `capability`
- `entry`
- `requires_login`
- `assertion_type`

## 字段说明

### capability
脚本主要能力，如：
- `upload-cover`
- `default-cover`
- `create-course`
- `smoke`

### entry
脚本真实入口，如：
- `learning#/course/add`
- `manage#/dashboard/course-manage`

### requires_login
是否依赖登录态：
- `true`
- `false`

### assertion_type
主要断言类型数组，如：
- `dom`
- `request`
- `upload`
- `route`
- `dialog`
