#!/usr/bin/env python
"""
API Configuration Verification Script
Verify all interfaces are correctly configured and imported
"""

import sys
sys.path.insert(0, 'd:\\STAR')

def verify_imports():
    """Verify all necessary imports"""
    print("=" * 60)
    print("Step 1: Verify Imports")
    print("=" * 60)
    
    try:
        from models import (
            Base, User, Course, Enrollment, Chapter, 
            KnowledgePoint, KnowledgePointProgress, Resource
        )
        print("[OK] models.py imported successfully")
    except Exception as e:
        print(f"[ERROR] models.py import failed: {e}")
        return False
    
    try:
        from schemas import (
            ApiEnvelope, CourseCardOut, CourseDetailOut,
            CourseProgressStateOut, CurrentUserOut, 
            EnrolledCourseCardOut, CourseProgressPatchIn
        )
        print("[OK] schemas.py imported successfully")
    except Exception as e:
        print(f"[ERROR] schemas.py import failed: {e}")
        return False
    
    try:
        from SQLconnet import SessionLocal, engine
        print("[OK] SQLconnet.py imported successfully")
    except Exception as e:
        print(f"[ERROR] SQLconnet.py import failed: {e}")
        return False
    
    return True


def verify_app_creation():
    """Verify FastAPI application creation"""
    print("\n" + "=" * 60)
    print("Step 2: Verify Application Creation")
    print("=" * 60)
    
    try:
        import main
        print("[OK] main.py imported successfully")
        print(f"  Application Name: {main.app.title}")
        print(f"  Application Version: {main.app.version}")
        return main.app
    except Exception as e:
        print(f"[ERROR] main.py import failed: {e}")
        return None


def verify_routes(app):
    """Verify all API routes"""
    print("\n" + "=" * 60)
    print("Step 3: Verify API Routes")
    print("=" * 60)
    
    routes_dict = {}
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            # Filter out Swagger documentation routes
            if not any(x in route.path for x in ['openapi', 'docs', 'redoc']):
                if route.path not in routes_dict:
                    routes_dict[route.path] = set()
                routes_dict[route.path].update(route.methods)
    
    expected_routes = {
        '/': {'GET'},
        '/users/me': {'GET'},
        '/users/me/enrollments': {'GET'},
        '/courses': {'GET'},
        '/courses/{courseId}': {'GET'},
        '/courses/{courseId}/enroll': {'POST'},
        '/courses/{courseId}/progress': {'GET', 'PATCH'},
    }
    
    print("\nConfigured API Endpoints:")
    for path in sorted(routes_dict.keys()):
        methods = routes_dict[path]
        methods_str = ', '.join(sorted(methods))
        print(f"  [{methods_str:20s}] {path}")
    
    # Verify required routes exist
    print("\nVerify Required Routes:")
    all_exist = True
    for expected_path, expected_methods in expected_routes.items():
        if expected_path in routes_dict:
            actual_methods = routes_dict[expected_path]
            if expected_methods.issubset(actual_methods):
                print(f"  [OK] {expected_path}")
            else:
                print(f"  [ERROR] {expected_path} - missing methods {expected_methods - actual_methods}")
                all_exist = False
        else:
            print(f"  [ERROR] {expected_path} - route not found")
            all_exist = False
    
    return all_exist


def verify_models():
    """Verify database models"""
    print("\n" + "=" * 60)
    print("Step 4: Verify Database Models")
    print("=" * 60)
    
    try:
        from models import Base
        
        tables = [table.name for table in Base.metadata.tables.values()]
        print(f"Defined Database Tables ({len(tables)}):")
        for table_name in sorted(tables):
            print(f"  - {table_name}")
        
        expected_tables = {
            'users', 'courses', 'chapters', 'knowledge_points',
            'resources', 'enrollments', 'knowledge_point_progress'
        }
        
        print("\nVerify Required Tables:")
        all_exist = True
        for expected_table in expected_tables:
            if expected_table in tables:
                print(f"  [OK] {expected_table}")
            else:
                print(f"  [ERROR] {expected_table} - missing")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        return False


def verify_schemas():
    """Verify Pydantic models"""
    print("\n" + "=" * 60)
    print("Step 5: Verify Pydantic Models")
    print("=" * 60)
    
    try:
        from schemas import (
            ApiEnvelope, CourseCardOut, CourseDetailOut,
            CourseProgressStateOut, CurrentUserOut, 
            EnrolledCourseCardOut, CourseProgressPatchIn
        )
        
        models = {
            'ApiEnvelope': ApiEnvelope,
            'CourseCardOut': CourseCardOut,
            'CourseDetailOut': CourseDetailOut,
            'CourseProgressStateOut': CourseProgressStateOut,
            'CurrentUserOut': CurrentUserOut,
            'EnrolledCourseCardOut': EnrolledCourseCardOut,
            'CourseProgressPatchIn': CourseProgressPatchIn,
        }
        
        print(f"Defined Pydantic Models ({len(models)}):")
        for name, model_class in models.items():
            try:
                fields = len(model_class.model_fields)
                print(f"  [OK] {name} ({fields} fields)")
            except:
                print(f"  [OK] {name}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        return False


def main():
    """Main verification function"""
    print("\n")
    print("+" + "=" * 58 + "+")
    print("|  STAR API Configuration Verification                      |")
    print("+" + "=" * 58 + "+")
    
    # Execute verification steps
    results = []
    
    results.append(("Import Verification", verify_imports()))
    
    if results[-1][1]:
        app = verify_app_creation()
        results.append(("Application Creation", app is not None))
        
        if app:
            results.append(("Route Verification", verify_routes(app)))
    
    results.append(("Model Verification", verify_models()))
    results.append(("Schema Verification", verify_schemas()))
    
    # Display final results
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    for step_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}  {step_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    if failed == 0:
        print(f"[SUCCESS] All verifications passed! ({passed}/{passed+failed})")
        print("\nNext steps:")
        print("  1. Start PostgreSQL: docker-compose up -d")
        print("  2. Run app: python -m uvicorn main:app --reload")
        print("  3. Visit API docs: http://localhost:8000/docs")
        return 0
    else:
        print(f"[FAILED] Verification failed ({passed} passed, {failed} failed)")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
