#!/usr/bin/env python
"""
STAR API 完整功能测试脚本
运行此脚本来测试所有API接口
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

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
                "GET /users/me - 获取用户信息",
                passed,
                f"用户ID: {data.get('data', {}).get('id')}"
            )
            return passed, data.get('data')
        except Exception as e:
            self.log_test("GET /users/me - 获取用户信息", False, str(e))
            return False, None
    
    def test_get_courses(self):
        """测试获取课程列表"""
        try:
            resp = self.session.get(f"{self.base_url}/courses")
            passed = resp.status_code == 200
            data = resp.json()
            courses = data.get('data', [])
            self.log_test(
                "GET /courses - 获取课程列表",
                passed,
                f"找到 {len(courses)} 个课程"
            )
            return passed, courses
        except Exception as e:
            self.log_test("GET /courses - 获取课程列表", False, str(e))
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
                f"GET /courses?keyword={keyword} - 课程搜索",
                passed,
                f"找到 {len(courses)} 个课程"
            )
            return passed, courses
        except Exception as e:
            self.log_test(f"课程搜索 (keyword={keyword})", False, str(e))
            return False, []
    
    def test_get_course_detail(self, course_id):
        """测试获取课程详情"""
        try:
            resp = self.session.get(f"{self.base_url}/courses/{course_id}")
            passed = resp.status_code == 200
            data = resp.json()
            course = data.get('data', {})
            self.log_test(
                f"GET /courses/{course_id} - 获取课程详情",
                passed,
                f"课程: {course.get('title', 'N/A')}"
            )
            return passed, course
        except Exception as e:
            self.log_test(f"获取课程详情 (id={course_id})", False, str(e))
            return False, {}
    
    def test_enroll_course(self, course_id):
        """测试报名课程"""
        try:
            resp = self.session.post(f"{self.base_url}/courses/{course_id}/enroll")
            passed = resp.status_code in [200, 409]
            data = resp.json()
            msg = data.get('message', '')
            is_new_enrollment = resp.status_code == 200
            self.log_test(
                f"POST /courses/{course_id}/enroll - 报名课程",
                passed,
                f"消息: {msg}"
            )
            return is_new_enrollment, data.get('data')
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
                f"GET /courses/{course_id}/progress - 获取学习进度",
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
                f"PATCH /courses/{course_id}/progress - 更新学习进度",
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
                "GET /users/me/enrollments - 获取已报名课程",
                passed,
                f"已报名 {len(courses)} 个课程"
            )
            return passed, courses
        except Exception as e:
            self.log_test("获取已报名课程", False, str(e))
            return False, []
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*70)
        print(" " * 15 + "STAR API 完整功能测试")
        print("="*70 + "\n")
        
        # 测试1: 获取用户信息
        user_ok, user = self.test_get_user_info()
        
        # 测试2: 获取课程列表
        courses_ok, courses = self.test_get_courses()
        
        if courses and len(courses) > 0:
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
                if course.get('chapters') and len(course['chapters']) > 0:
                    first_chapter = course['chapters'][0]
                    if first_chapter.get('knowledgePoints') and len(first_chapter['knowledgePoints']) > 0:
                        kp_id = first_chapter['knowledgePoints'][0]['id']
                        self.test_update_progress(course_id, kp_id)
        else:
            print("\n[INFO] 数据库中没有课程数据，跳过部分测试")
        
        # 测试8: 获取已报名课程
        self.test_get_enrollments()
        
        # 显示测试总结
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "="*70)
        print(" " * 25 + "测试总结")
        print("="*70 + "\n")
        
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        total = len(self.results)
        
        print(f"总计: {total} 项测试")
        print(f"通过: {passed} 项")
        print(f"失败: {failed} 项")
        
        if failed == 0:
            print("\n✓ 所有测试通过！API功能完全正常！")
            return True
        else:
            print(f"\n✗ 有 {failed} 项测试失败，请检查错误信息")
            return False


if __name__ == "__main__":
    import sys
    
    # 创建测试器
    tester = APITester(BASE_URL)
    
    # 运行所有测试
    success = tester.run_all_tests()
    
    # 返回结果
    sys.exit(0 if success else 1)
