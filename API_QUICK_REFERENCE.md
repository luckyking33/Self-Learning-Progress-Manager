# STAR API 快速参考指南

## API 端点速览

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | `/users/me` | 获取当前用户信息 | ✅ 需要 |
| GET | `/users/me/enrollments` | 获取已报名课程列表 | ✅ 需要 |
| GET | `/courses` | 获取课程广场列表 | ❌ 不需要 |
| GET | `/courses/{courseId}` | 获取课程详情 | ❌ 不需要 |
| POST | `/courses/{courseId}/enroll` | 报名课程 | ✅ 需要 |
| GET | `/courses/{courseId}/progress` | 获取学习进度 | ✅ 需要 |
| PATCH | `/courses/{courseId}/progress` | 更新学习进度 | ✅ 需要 |

## 数据模型速览

### CurrentUserOut (用户信息)
```python
{
    "id": int,                      # 用户ID
    "name": str,                    # 用户名
    "avatar": str,                  # 头像URL
    "headline": str,                # 个人签名
    "streakDays": int,              # 连续学习天数
    "enrolledCourseIds": List[int]  # 已报名课程ID列表
}
```

### CourseCardOut (课程卡片)
```python
{
    "id": int,
    "title": str,
    "subtitle": str,
    "authorName": str,
    "authorAvatar": str,
    "tags": List[str],
    "forkCount": int,
    "enrollmentCount": int,
    "category": str,                # "CS自学" | "考研" | "职场提升"
    "coverTone": str
}
```

### CourseDetailOut (课程详情)
```python
{
    # 包含 CourseCardOut 的所有字段，加上：
    "description": str,
    "authorRole": str,
    "forkedFromTitle": str,
    "isPublic": bool,
    "chapterCount": int,
    "knowledgePointCount": int,
    "estimatedHours": int,
    "chapters": List[ChapterOut]     # 完整章节结构
}
```

### CourseProgressStateOut (学习进度)
```python
{
    "courseId": int,
    "selectedKnowledgePointId": int,
    "lastLearningKnowledgePointId": int,
    "completedKnowledgePointIds": List[int],
    "joinedAt": datetime
}
```

### EnrolledCourseCardOut (已报名课程)
```python
{
    "id": int,
    "title": str,
    "subtitle": str,
    "authorName": str,
    "authorAvatar": str,
    "coverTone": str,
    "completedKnowledgePointCount": int,
    "totalKnowledgePointCount": int,
    "progressPercent": int,
    "lastLearningKnowledgePointId": int,
    "lastLearningKnowledgePointTitle": str,
    "lastLearningChapterTitle": str
}
```

## 通用响应格式

所有API响应都采用 `ApiEnvelope` 包装格式：

```json
{
    "code": 0,                  // 0表示成功，非0表示错误
    "message": "ok",            // 状态消息
    "data": {}                  // 实际数据，类型根据接口决定
}
```

## 常见用法示例

### 1. 获取用户信息和已报名课程
```bash
# 获取用户基本信息
curl http://localhost:8000/users/me

# 获取用户已报名的课程及进度
curl http://localhost:8000/users/me/enrollments
```

### 2. 浏览课程
```bash
# 获取所有课程
curl http://localhost:8000/courses

# 按关键词搜索
curl "http://localhost:8000/courses?keyword=Python"

# 按分类过滤
curl "http://localhost:8000/courses?category=CS自学"

# 获取课程详情
curl http://localhost:8000/courses/1
```

### 3. 学习流程
```bash
# 1. 报名课程
curl -X POST http://localhost:8000/courses/1/enroll

# 2. 查看学习进度
curl http://localhost:8000/courses/1/progress

# 3. 完成一个知识点后更新进度
curl -X PATCH http://localhost:8000/courses/1/progress \
  -H "Content-Type: application/json" \
  -d '{
    "lastLearningKnowledgePointId": 2,
    "completedKnowledgePointIds": [1]
  }'

# 4. 继续学习并完成多个知识点
curl -X PATCH http://localhost:8000/courses/1/progress \
  -H "Content-Type: application/json" \
  -d '{
    "lastLearningKnowledgePointId": 5,
    "completedKnowledgePointIds": [1, 2, 3, 4, 5]
  }'
```

## 错误响应示例

### 400 Bad Request
```json
{
    "code": 400,
    "message": "无效的请求参数",
    "data": null
}
```

### 401 Unauthorized
```json
{
    "code": 401,
    "message": "未登录",
    "data": null
}
```

### 404 Not Found
```json
{
    "code": 404,
    "message": "课程不存在",
    "data": null
}
```

### 409 Conflict
```json
{
    "code": 409,
    "message": "已加入学习",
    "data": null
}
```

## 启动应用

### 方式1: 直接运行（推荐用于开发）
```bash
cd d:\STAR
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 方式2: 使用FastAPI运行命令
```bash
cd d:\STAR
fastapi run main.py --port 8000
```

### 方式3: 使用Gunicorn（推荐用于生产）
```bash
cd d:\STAR
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
```

## 访问文档

启动应用后，可访问以下地址：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 数据库初始化

首次运行应用时，访问任何端点（如 `/`）会自动创建所有数据库表。

确保 PostgreSQL 数据库已启动且配置正确：
```bash
# 使用 docker-compose 启动数据库
docker-compose up -d
```

## 配置文件

- `SQLconnet.py` - 数据库连接配置
- `.env` - 环境变量配置（如需要）

## 常见问题

### 1. "Connection refused" 错误
**原因**: PostgreSQL 数据库未启动或连接参数错误
**解决**: 
```bash
docker-compose up -d
# 或检查 SQLconnet.py 中的 DATABASE_URL
```

### 2. "No module named 'sqlalchemy'" 错误
**原因**: 依赖未安装
**解决**: 
```bash
pip install -r requirements.txt
```

### 3. 获取用户信息时总是用户ID 7
**原因**: 当前使用模拟认证
**说明**: 可在 `main.py` 中的 `get_current_user_id()` 修改为真实认证

## 扩展接口

Backend Development 文件夹中提供了标准的项目结构：
- `Backend Development/app/api/routes/` - 路由文件
- `Backend Development/app/db/` - 数据库配置
- `Backend Development/app/core/` - 核心功能模块

可以基于这个结构继续扩展更多功能。
