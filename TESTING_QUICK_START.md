# STAR API 快速测试指南

快速开始测试您的 STAR 项目！

---

## 🚀 最快的方式 - 一键测试（推荐）

### Windows 用户

1. **打开命令提示符** 或 **PowerShell**
2. 导航到项目目录：
   ```bash
   cd d:\STAR
   ```
3. 运行一键测试脚本：
   ```bash
   run_tests.bat
   ```

就这样！脚本会自动：
- ✅ 启动 PostgreSQL 数据库
- ✅ 启动 FastAPI 应用
- ✅ 运行完整的功能测试
- ✅ 显示测试结果

### Mac/Linux 用户

```bash
cd ~/STAR
chmod +x run_tests.sh
./run_tests.sh
```

---

## 📝 方式二：手动逐步测试

### 步骤 1：启动数据库

```bash
cd d:\STAR
docker-compose up -d
```

等待 PostgreSQL 启动（大约 10-15 秒）。

### 步骤 2：启动应用

打开新的终端窗口，运行：

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

输出应该显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 步骤 3：在浏览器中测试

打开浏览器访问：

**http://localhost:8000/docs**

您会看到 Swagger UI，可以在这里直接测试所有接口：

1. 点击任何接口
2. 点击 **"Try it out"** 按钮
3. 点击 **"Execute"** 按钮
4. 查看响应结果

---

## 🧪 方式三：运行自动化测试脚本

在新的终端窗口运行：

```bash
cd d:\STAR
python test_api.py
```

输出示例：
```
======================================================================
               STAR API 完整功能测试
======================================================================

[PASS] GET /users/me - 获取用户信息
       用户ID: 7
[PASS] GET /courses - 获取课程列表
       找到 5 个课程
[PASS] GET /courses?keyword=Python - 课程搜索
       找到 2 个课程
[PASS] GET /courses/1 - 获取课程详情
       课程: Python基础
[PASS] POST /courses/1/enroll - 报名课程
       消息: joined
[PASS] GET /courses/1/progress - 获取学习进度
       已完成: 0 个知识点
[PASS] PATCH /courses/1/progress - 更新学习进度
       已完成: 1 个知识点
[PASS] GET /users/me/enrollments - 获取已报名课程
       已报名 1 个课程

======================================================================
                         测试总结
======================================================================

总计: 8 项测试
通过: 8 项
失败: 0 项

✓ 所有测试通过！API功能完全正常！
```

---

## 🌐 方式四：使用 curl 命令测试

### 测试单个接口

```bash
# 获取用户信息
curl http://localhost:8000/users/me

# 获取课程列表
curl http://localhost:8000/courses

# 搜索课程
curl "http://localhost:8000/courses?keyword=Python"

# 获取课程详情
curl http://localhost:8000/courses/1

# 报名课程
curl -X POST http://localhost:8000/courses/1/enroll

# 获取学习进度
curl http://localhost:8000/courses/1/progress

# 更新学习进度
curl -X PATCH http://localhost:8000/courses/1/progress \
  -H "Content-Type: application/json" \
  -d '{
    "lastLearningKnowledgePointId": 2,
    "completedKnowledgePointIds": [1, 2]
  }'

# 获取已报名课程
curl http://localhost:8000/users/me/enrollments
```

---

## 📊 测试检查清单

在充分测试后，确保以下所有项目都通过：

### 用户管理
- [ ] ✓ `GET /users/me` 返回用户信息
- [ ] ✓ `GET /users/me/enrollments` 返回已报名课程列表

### 课程管理
- [ ] ✓ `GET /courses` 返回课程列表
- [ ] ✓ `GET /courses?keyword=X` 搜索功能正常
- [ ] ✓ `GET /courses?category=X` 分类过滤正常
- [ ] ✓ `GET /courses/{id}` 返回课程完整信息

### 报名功能
- [ ] ✓ `POST /courses/{id}/enroll` 报名成功
- [ ] ✓ 第二次报名返回 "已加入学习" 错误

### 学习进度
- [ ] ✓ `GET /courses/{id}/progress` 返回进度信息
- [ ] ✓ `PATCH /courses/{id}/progress` 更新进度成功
- [ ] ✓ 更新后数据被正确保存

### 数据验证
- [ ] ✓ 所有响应都包含 `code`、`message`、`data` 字段
- [ ] ✓ 成功返回 `code: 0`
- [ ] ✓ 错误返回相应的错误代码和消息

---

## 🐛 遇到问题？

### 问题 1：无法连接到数据库

```bash
# 检查数据库是否运行
docker ps | grep postgres

# 如果没有，启动数据库
docker-compose up -d

# 查看日志
docker logs star-postgres
```

### 问题 2：端口 8000 被占用

```bash
# 使用其他端口启动
python -m uvicorn main:app --reload --port 8001

# 然后访问 http://localhost:8001/docs
```

### 问题 3：应用启动失败

```bash
# 检查 Python 依赖是否安装
pip install -r requirements.txt

# 重新启动应用
python -m uvicorn main:app --reload
```

### 问题 4：没有测试数据

默认情况下，数据库可能是空的。您可以：

1. **通过 Swagger UI 创建数据**：使用 admin 接口（如果有）
2. **运行初始化脚本**：`python init_data.py`
3. **手动插入数据**：使用 `psql` 命令或管理工具

---

## 📚 详细测试指南

想要更详细的信息？查看：

**完整测试指南**: `d:\STAR\TEST_GUIDE.md`

这个文件包含：
- 所有接口的详细说明
- 更多的测试场景
- 常见问题排查
- 性能测试方法

---

## ✨ 测试成功标志

如果看到以下信息，说明您的 API 功能完全正常：

```
✓ 所有测试通过！API功能完全正常！
```

此时您可以：
- 📱 开始前端开发并与后端集成
- 🔍 运行更多深入的功能测试
- 🚀 部署到生产环境
- 📊 进行性能优化

---

## 🎯 测试建议

1. **首次测试**：使用一键测试脚本 (`run_tests.bat` 或 `run_tests.sh`)
2. **交互式测试**：使用 Swagger UI 手动测试各个接口
3. **自动化测试**：运行 `test_api.py` 进行完整的自动化测试
4. **集成测试**：在前端中调用 API 并测试实际应用场景

---

## 📞 支持资源

- **API 完整文档**: `API_INTERFACE_SUMMARY.md`
- **快速参考**: `API_QUICK_REFERENCE.md`
- **项目结构**: `PROJECT_STRUCTURE.md`
- **配置报告**: `CONFIGURATION_REPORT.md`

---

**祝您测试顺利！** 🚀

如有任何问题，请参考详细的测试指南或查看自动生成的 Swagger 文档。
