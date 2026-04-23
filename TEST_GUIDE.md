# STAR API 功能测试指南

本指南将帮助您全面测试 STAR 自学进度管理器 API 的所有功能。

## 📋 测试方式概览

测试分为三个层次：
1. **简单快速** - 使用 Swagger UI 浏览器测试
2. **自动化** - 使用 curl 命令行测试
3. **编程测试** - 使用 Python 脚本进行完整测试

---

## 方式一：使用 Swagger UI 浏览器测试（推荐新手）

### 第一步：启动应用

```bash
cd d:\STAR
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

输出应该是这样：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 第二步：打开浏览器

访问：**http://localhost:8000/docs**

您应该看到 Swagger UI 界面，列出所有的 API 端点。

### 第三步：测试每个接口

#### 1. 首页重定向
- 找到 `GET /` 接口
- 点击 "Try it out"
- 点击 "Execute"
- 看到重定向到 `/docs` 的响应

#### 2. 获取用户信息
```
GET /users/me
```
- 点击 "Try it out"
- 点击 "Execute"
- 应该返回：
```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": 7,
    "name": "用户名",
    "avatar": "头像URL",
    "headline": "个人签名",
    "streakDays": 5,
    "enrolledCourseIds": []
  }
}
```

#### 3. 获取课程列表
```
GET /courses
```
- 点击 "Try it out"
- 可选：在 `keyword` 输入框输入搜索词，如 "Python"
- 可选：在 `category` 输入框输入分类，如 "CS自学"
- 点击 "Execute"
- 查看返回的课程列表

#### 4. 获取课程详情
```
GET /courses/{courseId}
```
- 在路径参数 `courseId` 输入 "1"（假设数据库中有ID为1的课程）
- 点击 "Execute"
- 应该返回课程的完整信息（包括章节、知识点、资源等）

#### 5. 报名课程
```
POST /courses/{courseId}/enroll
```
- 在路径参数 `courseId` 输入 "1"
- 点击 "Try it out"
- 点击 "Execute"
- 应该返回报名成功和报名时间
- 再次执行应该返回 "已加入学习" 错误（表示已报名）

#### 6. 获取学习进度
```
GET /courses/{courseId}/progress
```
- 在路径参数 `courseId` 输入 "1"（已报名的课程）
- 点击 "Execute"
- 应该返回当前学习进度、已完成知识点等信息

#### 7. 更新学习进度
```
PATCH /courses/{courseId}/progress
```
- 在路径参数 `courseId` 输入 "1"
- 在请求体输入（JSON格式）：
```json
{
  "lastLearningKnowledgePointId": 2,
  "completedKnowledgePointIds": [1, 2]
}
```
- 点击 "Execute"
- 应该返回更新后的进度信息

#### 8. 获取已报名课程列表
```
GET /users/me/enrollments
```
- 点击 "Try it out"
- 点击 "Execute"
- 应该返回用户已报名的所有课程及其进度

---

## 方式二：使用 curl 命令行测试

这种方法适合自动化测试和脚本集成。

### 准备工作

确保应用正在运行：
```bash
python -m uvicorn main:app --reload
```

### 测试脚本

#### 1. 测试首页
```bash
curl http://localhost:8000/
```

#### 2. 测试获取用户信息
```bash
curl http://localhost:8000/users/me
```

#### 3. 测试获取课程列表
```bash
# 获取所有课程
curl http://localhost:8000/courses

# 按关键词搜索
curl "http://localhost:8000/courses?keyword=Python"

# 按分类过滤
curl "http://localhost:8000/courses?category=CS自学"

# 组合搜索
curl "http://localhost:8000/courses?keyword=Python&category=CS自学"
```

#### 4. 测试获取课程详情
```bash
curl http://localhost:8000/courses/1
```

#### 5. 测试报名课程
```bash
curl -X POST http://localhost:8000/courses/1/enroll
```

#### 6. 测试获取学习进度
```bash
curl http://localhost:8000/courses/1/progress
```

#### 7. 测试更新学习进度
```bash
curl -X PATCH http://localhost:8000/courses/1/progress \
  -H "Content-Type: application/json" \
  -d '{
    "lastLearningKnowledgePointId": 2,
    "completedKnowledgePointIds": [1, 2]
  }'
```

#### 8. 测试获取已报名课程列表
```bash
curl http://localhost:8000/users/me/enrollments
```

---

## 方式三：使用 Python 脚本自动化测试

创建一个完整的测试脚本。

### 创建测试文件：test_api.py

```python
#!/usr/bin/env python
"""
STAR API 完整功能测试脚本
"""

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000"
USER_ID = 7

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
    
    def log_test(self, test_name, passed, message=""):
        """记录测试结果"""
        status = "PASS" if passed else "FAIL"
        self.results.append({
            "name": test_name,
            "status": status,
            "message": message
        })
        print(f"[{status}] {test_name}")
        if message:
            print(f"       {message}")
    
    def test_get_user_info(self):
        """测试获取用户信息"""
        try:
            resp = self.session.get(f"{self.base_url}/users/me")
            passed = resp.status_code == 200
            data = resp.json()
            self.log_test(
                "获取用户信息",
                passed,
                f"用户ID: {data.get('data', {}).get('id')}"
            )
            return passed, data.get('data')
        except Exception as e:
            self.log_test("获取用户信息", False, str(e))
            return False, None
    
    def test_get_courses(self):
        """测试获取课程列表"""
        try:
            resp = self.session.get(f"{self.base_url}/courses")
            passed = resp.status_code == 200
            data = resp.json()
            courses = data.get('data', [])
            self.log_test(
                "获取课程列表",
                passed,
                f"找到 {len(courses)} 个课程"
            )
            return passed, courses
        except Exception as e:
            self.log_test("获取课程列表", False, str(e))
            return False, []
    
    def test_search_courses(self, keyword):
        """测试课程搜索"""
        try:
            resp = self.session.get(
                f"{self.base_url}/courses",
                params={"keyword": keyword}
            )
            passed = resp.status_code == 200
            data = resp.json()
            courses = data.get('data', [])
            self.log_test(
                f"搜索课程 (keyword={keyword})",
                passed,
                f"找到 {len(courses)} 个课程"
            )
            return passed, courses
        except Exception as e:
            self.log_test(f"搜索课程 (keyword={keyword})", False, str(e))
            return False, []
    
    def test_get_course_detail(self, course_id):
        """测试获取课程详情"""
        try:
            resp = self.session.get(f"{self.base_url}/courses/{course_id}")
            passed = resp.status_code == 200
            data = resp.json()
            course = data.get('data', {})
            self.log_test(
                f"获取课程详情 (id={course_id})",
                passed,
                f"课程: {course.get('title')}"
            )
            return passed, course
        except Exception as e:
            self.log_test(f"获取课程详情 (id={course_id})", False, str(e))
            return False, {}
    
    def test_enroll_course(self, course_id):
        """测试报名课程"""
        try:
            resp = self.session.post(f"{self.base_url}/courses/{course_id}/enroll")
            passed = resp.status_code in [200, 409]  # 200成功，409已报名
            data = resp.json()
            msg = data.get('message', '')
            self.log_test(
                f"报名课程 (id={course_id})",
                passed,
                f"消息: {msg}"
            )
            return passed and resp.status_code == 200, data.get('data')
        except Exception as e:
            self.log_test(f"报名课程 (id={course_id})", False, str(e))
            return False, None
    
    def test_get_progress(self, course_id):
        """测试获取学习进度"""
        try:
            resp = self.session.get(
                f"{self.base_url}/courses/{course_id}/progress"
            )
            passed = resp.status_code == 200
            data = resp.json()
            progress = data.get('data', {})
            self.log_test(
                f"获取学习进度 (id={course_id})",
                passed,
                f"已完成: {len(progress.get('completedKnowledgePointIds', []))} 个知识点"
            )
            return passed, progress
        except Exception as e:
            self.log_test(f"获取学习进度 (id={course_id})", False, str(e))
            return False, {}
    
    def test_update_progress(self, course_id, kp_id):
        """测试更新学习进度"""
        try:
            payload = {
                "lastLearningKnowledgePointId": kp_id,
                "completedKnowledgePointIds": [kp_id]
            }
            resp = self.session.patch(
                f"{self.base_url}/courses/{course_id}/progress",
                json=payload
            )
            passed = resp.status_code == 200
            data = resp.json()
            progress = data.get('data', {})
            self.log_test(
                f"更新学习进度 (id={course_id}, kp={kp_id})",
                passed,
                f"已完成: {len(progress.get('completedKnowledgePointIds', []))} 个知识点"
            )
            return passed, progress
        except Exception as e:
            self.log_test(f"更新学习进度 (id={course_id})", False, str(e))
            return False, {}
    
    def test_get_enrollments(self):
        """测试获取已报名课程列表"""
        try:
            resp = self.session.get(f"{self.base_url}/users/me/enrollments")
            passed = resp.status_code == 200
            data = resp.json()
            courses = data.get('data', [])
            self.log_test(
                "获取已报名课程",
                passed,
                f"已报名 {len(courses)} 个课程"
            )
            return passed, courses
        except Exception as e:
            self.log_test("获取已报名课程", False, str(e))
            return False, []
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("STAR API 完整功能测试")
        print("="*60 + "\n")
        
        # 测试1: 获取用户信息
        user_ok, user = self.test_get_user_info()
        
        # 测试2: 获取课程列表
        courses_ok, courses = self.test_get_courses()
        
        if courses:
            course_id = courses[0]['id']
            
            # 测试3: 搜索课程
            self.test_search_courses("Python")
            
            # 测试4: 获取课程详情
            detail_ok, course = self.test_get_course_detail(course_id)
            
            # 测试5: 报名课程
            enroll_ok, enroll_data = self.test_enroll_course(course_id)
            
            if enroll_ok:
                # 测试6: 获取学习进度
                progress_ok, progress = self.test_get_progress(course_id)
                
                # 测试7: 更新学习进度（如果有知识点）
                if course.get('chapters'):
                    first_chapter = course['chapters'][0]
                    if first_chapter.get('knowledgePoints'):
                        kp_id = first_chapter['knowledgePoints'][0]['id']
                        self.test_update_progress(course_id, kp_id)
        
        # 测试8: 获取已报名课程
        self.test_get_enrollments()
        
        # 显示测试总结
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "="*60)
        print("测试总结")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        total = len(self.results)
        
        print(f"总计: {total} 项测试")
        print(f"通过: {passed} 项")
        print(f"失败: {failed} 项")
        
        if failed == 0:
            print("\n✓ 所有测试通过！")
            return True
        else:
            print(f"\n✗ 有 {failed} 项测试失败")
            return False


if __name__ == "__main__":
    # 创建测试器
    tester = APITester(BASE_URL)
    
    # 运行所有测试
    success = tester.run_all_tests()
    
    # 返回结果
    import sys
    sys.exit(0 if success else 1)
```

### 运行测试脚本

```bash
cd d:\STAR
python test_api.py
```

输出应该是这样：
```
============================================================
STAR API 完整功能测试
============================================================

[PASS] 获取用户信息
       用户ID: 7
[PASS] 获取课程列表
       找到 5 个课程
[PASS] 搜索课程 (keyword=Python)
       找到 2 个课程
[PASS] 获取课程详情 (id=1)
       课程: Python基础
[PASS] 报名课程 (id=1)
       消息: joined
[PASS] 获取学习进度 (id=1)
       已完成: 0 个知识点
[PASS] 更新学习进度 (id=1, kp=1)
       已完成: 1 个知识点
[PASS] 获取已报名课程
       已报名 1 个课程

============================================================
测试总结
============================================================
总计: 8 项测试
通过: 8 项
失败: 0 项

✓ 所有测试通过！
```

---

## 📊 数据库测试

### 查看数据库中的数据

使用 PostgreSQL 客户端连接到数据库：

```bash
# 使用 psql 连接
psql -U star_user -h localhost -d star_db
```

然后执行SQL查询：

```sql
-- 查看用户表
SELECT * FROM users;

-- 查看课程表
SELECT id, title, author_name, is_public FROM courses;

-- 查看报名记录
SELECT * FROM enrollments;

-- 查看学习进度
SELECT * FROM knowledge_point_progress;
```

---

## 🐛 常见问题和排查

### 问题 1：无法连接到数据库
**症状**: `psycopg2.OperationalError: connection to server at "localhost" failed`

**解决方案**:
```bash
# 检查Docker是否启动
docker ps

# 启动PostgreSQL容器
docker-compose up -d

# 检查是否启动成功
docker logs star-postgres
```

### 问题 2：端口 8000 被占用
**症状**: `OSError: [Errno 48] Address already in use`

**解决方案**:
```bash
# 使用其他端口
python -m uvicorn main:app --reload --port 8001

# 或者杀死占用8000的进程
lsof -i :8000
kill -9 <PID>
```

### 问题 3：数据库表不存在
**症状**: `ProgrammingError: relation "users" does not exist`

**解决方案**:
```bash
# 访问首页来初始化数据库
curl http://localhost:8000/

# 或在Python中手动初始化
python -c "from SQLconnet import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

### 问题 4：没有测试数据
**症状**: 查询课程返回空列表

**解决方案**:
```bash
# 运行初始化脚本
python init_data.py

# 或使用Swagger UI手动创建测试数据
# 通过admin接口或直接插入数据库
```

---

## ✅ 完整测试检查清单

- [ ] 启动 PostgreSQL 数据库
- [ ] 启动 FastAPI 应用
- [ ] 访问 Swagger UI 文档
- [ ] 测试获取用户信息
- [ ] 测试获取课程列表
- [ ] 测试搜索课程
- [ ] 测试获取课程详情
- [ ] 测试报名课程
- [ ] 测试获取学习进度
- [ ] 测试更新学习进度
- [ ] 测试获取已报名课程列表
- [ ] 查看数据库表数据
- [ ] 运行完整的 Python 测试脚本
- [ ] 验证所有接口响应格式正确
- [ ] 测试错误场景（已报名、不存在的课程等）

---

## 📝 记录测试结果

在运行测试后，建议记录以下信息：

```
测试日期: 2024-XX-XX
测试者: 
环境: Windows 10 / Python 3.10

API接口测试结果:
- 获取用户信息: PASS / FAIL
- 获取课程列表: PASS / FAIL
- 课程搜索: PASS / FAIL
- 获取课程详情: PASS / FAIL
- 报名课程: PASS / FAIL
- 获取学习进度: PASS / FAIL
- 更新学习进度: PASS / FAIL
- 获取已报名课程: PASS / FAIL

总体结果: PASS / FAIL
备注: 
```

---

## 🚀 性能测试（可选）

使用 Apache Bench 进行负载测试：

```bash
# 测试获取课程列表的吞吐量
ab -n 100 -c 10 http://localhost:8000/courses

# 测试获取用户信息的响应时间
ab -n 100 -c 1 http://localhost:8000/users/me
```

---

祝您测试顺利！如有任何问题，请参考本指南或查看 API 文档。
