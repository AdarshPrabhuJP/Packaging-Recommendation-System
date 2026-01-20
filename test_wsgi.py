#!/usr/bin/env python3
"""
Test script to verify WSGI setup works correctly
"""

def test_wsgi_import():
    """Test if the WSGI app can be imported successfully"""
    try:
        from wsgi import app
        print("✓ WSGI app imported successfully")
        print(f"✓ App type: {type(app)}")
        print(f"✓ App name: {app.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to import WSGI app: {e}")
        return False

def test_app_factory():
    """Test if the app factory works"""
    try:
        from app import create_app
        test_app = create_app()
        print("✓ App factory works")
        print(f"✓ Created app: {test_app.name}")
        return True
    except Exception as e:
        print(f"✗ App factory failed: {e}")
        return False

def test_routes():
    """Test if routes are registered"""
    try:
        from wsgi import app
        with app.app_context():
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append(f"{rule.methods} {rule.rule}")
            
            print("✓ Routes registered:")
            for route in sorted(routes):
                print(f"  {route}")
            return True
    except Exception as e:
        print(f"✗ Failed to check routes: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("WSGI DEPLOYMENT TEST")
    print("=" * 50)
    
    tests = [
        ("WSGI Import", test_wsgi_import),
        ("App Factory", test_app_factory),
        ("Routes", test_routes)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✓ Ready for deployment!")
    else:
        print("✗ Fix issues before deploying")
    print("=" * 50)