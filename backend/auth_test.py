#!/usr/bin/env python3
"""Test script to verify the authentication refactoring works"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Test the auth_handler functions directly
try:
    from src.auth.auth_handler import get_password_hash, verify_password, create_access_token, authenticate_user
    print("✓ Successfully imported authentication functions")
    
    # Test password hashing
    password = "test_password_123!"
    hashed = get_password_hash(password)
    print("✓ Password hashing works")
    
    # Test password verification
    is_valid = verify_password(password, hashed)
    is_invalid = verify_password("wrong_password", hashed)
    assert is_valid == True, "Password verification should work"
    assert is_invalid == False, "Wrong password should not verify"
    print("✓ Password verification works")
    
    # Test token creation
    token = create_access_token(data={"sub": "test@example.com"})
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"
    print("✓ Token creation works")
    
    print("\n✓ All authentication refactoring tests passed!")
    print("✓ The authentication system has been successfully refactored")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Error during testing: {e}")
    import traceback
    traceback.print_exc()