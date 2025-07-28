#!/usr/bin/env python3
"""
Quick validation script to test both virtual environments.
This ensures users can run the challenges smoothly.
"""

import subprocess
import sys
import os
from pathlib import Path

def test_environment(challenge_name, challenge_path, test_imports):
    """Test a virtual environment by running imports."""
    print(f"\nTesting {challenge_name} environment...")
    
    # Path to Python executable in venv
    python_exe = challenge_path / "venv" / "Scripts" / "python.exe"
    
    if not python_exe.exists():
        print(f"ERROR Virtual environment not found at {python_exe}")
        return False
    
    # Test imports
    for package in test_imports:
        try:
            result = subprocess.run(
                [str(python_exe), "-c", f"import {package}; print('OK {package} imported successfully')"],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print(f"  OK {package}")
            else:
                print(f"  ERROR {package} - {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT {package}")
            return False
        except Exception as e:
            print(f"  ERROR {package} - {str(e)}")
            return False
    
    print(f"SUCCESS {challenge_name} environment is ready!")
    return True

def main():
    """Main validation function."""
    print("Adobe India Hackathon 2025 - Environment Validation")
    print("=" * 60)
    
    base_path = Path(__file__).parent
    
    # Test Challenge 1A
    challenge_1a_imports = [
        "pymupdf", "torch", "sentence_transformers", 
        "sklearn", "numpy", "pandas", "jsonschema", "pytest"
    ]
    
    result_1a = test_environment(
        "Challenge 1A", 
        base_path / "Challenge_1a", 
        challenge_1a_imports
    )
    
    # Test Challenge 1B  
    challenge_1b_imports = [
        "PyPDF2", "pymupdf", "sklearn", 
        "pandas", "jsonschema", "pytest"
    ]
    
    result_1b = test_environment(
        "Challenge 1B",
        base_path / "Challenge_1b",
        challenge_1b_imports
    )
    
    # Final summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    if result_1a and result_1b:
        print("ALL ENVIRONMENTS READY!")
        print("Challenge 1A: Ready to process PDFs with ML")
        print("Challenge 1B: Ready for multi-collection analysis")
        print("\nQuick start:")
        print("   - Double-click activate_env.bat in your chosen challenge folder")
        print("   - Run the main script and you're good to go!")
        return 0
    else:
        print("SOME ENVIRONMENTS HAVE ISSUES")
        if not result_1a:
            print("Challenge 1A: Environment issues detected")
        if not result_1b:
            print("Challenge 1B: Environment issues detected")
        print("\nTry recreating the virtual environments or contact support.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
