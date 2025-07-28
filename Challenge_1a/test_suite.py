import unittest
import json
import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from process_pdfs import extract_outline, validate_output, clean_text, normalize_level
except ImportError:
    print("Warning: Could not import process_pdfs module. Some tests will be skipped.")

class TestPDFProcessing(unittest.TestCase):
    """Test suite for PDF processing functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests"""
        cls.test_data_dir = Path("./sample_dataset")
        cls.pdfs_dir = cls.test_data_dir / "pdfs"
        cls.outputs_dir = cls.test_data_dir / "outputs"
        cls.schema_file = cls.test_data_dir / "schema" / "output_schema.json"
        
        # Ensure test directories exist
        cls.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def setUp(self):
        """Set up before each test"""
        self.sample_outline_data = {
            "title": "Test Document",
            "outline": [
                {"level": "H1", "text": "Introduction", "page": 1},
                {"level": "H2", "text": "Background", "page": 2},
                {"level": "H3", "text": "Methodology", "page": 3}
            ]
        }
    
    def test_schema_file_exists(self):
        """Test that the schema file exists and is valid JSON"""
        self.assertTrue(self.schema_file.exists(), "Schema file should exist")
        
        with open(self.schema_file, 'r') as f:
            schema = json.load(f)
        
        self.assertIn("type", schema)
        self.assertIn("properties", schema)
        self.assertIn("title", schema["properties"])
        self.assertIn("outline", schema["properties"])
    
    def test_pdf_files_exist(self):
        """Test that all expected PDF files exist"""
        expected_files = ["file01.pdf", "file02.pdf", "file03.pdf", "file04.pdf", "file05.pdf"]
        
        for pdf_file in expected_files:
            pdf_path = self.pdfs_dir / pdf_file
            self.assertTrue(pdf_path.exists(), f"PDF file {pdf_file} should exist")
            self.assertGreater(pdf_path.stat().st_size, 0, f"PDF file {pdf_file} should not be empty")
    
    def test_output_json_structure(self):
        """Test that output JSON files have the correct structure"""
        if not self.outputs_dir.exists():
            self.skipTest("Outputs directory does not exist")
        
        json_files = list(self.outputs_dir.glob("*.json"))
        self.assertGreater(len(json_files), 0, "Should have at least one output JSON file")
        
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Test required fields
            self.assertIn("title", data, f"JSON file {json_file.name} should have 'title' field")
            self.assertIn("outline", data, f"JSON file {json_file.name} should have 'outline' field")
            
            # Test title is string
            self.assertIsInstance(data["title"], str, "Title should be a string")
            
            # Test outline is list
            self.assertIsInstance(data["outline"], list, "Outline should be a list")
            
            # Test outline items structure
            for item in data["outline"]:
                self.assertIn("level", item, "Outline item should have 'level' field")
                self.assertIn("text", item, "Outline item should have 'text' field")
                self.assertIn("page", item, "Outline item should have 'page' field")
                
                self.assertIsInstance(item["level"], str, "Level should be a string")
                self.assertIsInstance(item["text"], str, "Text should be a string")
                self.assertIsInstance(item["page"], int, "Page should be an integer")
    
    @unittest.skipIf('process_pdfs' not in sys.modules, "process_pdfs module not available")
    def test_clean_text_function(self):
        """Test the clean_text function"""
        test_cases = [
            ("  Hello World  ", "Hello World"),
            ("Text\twith\ttabs", "Text with tabs"),
            ("Multiple   spaces", "Multiple spaces"),
            ("Line\nbreaks\nhere", "Line breaks here"),
            ("", ""),
            ("   ", ""),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = clean_text(input_text)
                self.assertEqual(result, expected)
    
    @unittest.skipIf('process_pdfs' not in sys.modules, "process_pdfs module not available")
    def test_normalize_level_function(self):
        """Test the normalize_level function"""
        test_cases = [
            ("H0", "H1"),  # Should convert to H1
            ("H1", "H1"),
            ("H2", "H2"),
            ("H3", "H3"),
            ("H4", "H3"),  # Should cap at H3
            ("H10", "H3"),  # Should cap at H3
            ("", "H1"),    # Empty string should default to H1
            ("invalid", "H1"),  # Invalid format should default to H1
        ]
        
        for input_level, expected in test_cases:
            with self.subTest(input_level=input_level):
                result = normalize_level(input_level)
                self.assertEqual(result, expected)
    
    @unittest.skipIf('process_pdfs' not in sys.modules, "process_pdfs module not available")
    def test_validate_output_function(self):
        """Test the validate_output function"""
        # Test valid data
        valid_data = self.sample_outline_data
        is_valid, errors = validate_output(valid_data)
        self.assertTrue(is_valid, f"Valid data should pass validation. Errors: {errors}")
        
        # Test invalid data - missing title
        invalid_data = {"outline": []}
        is_valid, errors = validate_output(invalid_data)
        self.assertFalse(is_valid, "Data missing title should fail validation")
        
        # Test invalid data - wrong type for page
        invalid_data2 = {
            "title": "Test",
            "outline": [{"level": "H1", "text": "Test", "page": "1"}]  # page should be int
        }
        is_valid, errors = validate_output(invalid_data2)
        self.assertFalse(is_valid, "Data with wrong page type should fail validation")
    
    def test_output_files_count(self):
        """Test that the correct number of output files are generated"""
        if not self.outputs_dir.exists():
            self.skipTest("Outputs directory does not exist")
        
        pdf_count = len(list(self.pdfs_dir.glob("*.pdf"))) if self.pdfs_dir.exists() else 0
        json_count = len(list(self.outputs_dir.glob("*.json")))
        
        self.assertEqual(json_count, pdf_count, 
                        f"Should have {pdf_count} JSON files to match {pdf_count} PDF files")
    
    def test_heading_levels_are_valid(self):
        """Test that all heading levels are valid (H1, H2, or H3)"""
        if not self.outputs_dir.exists():
            self.skipTest("Outputs directory does not exist")
        
        valid_levels = {"H1", "H2", "H3"}
        
        for json_file in self.outputs_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data.get("outline", []):
                level = item.get("level")
                self.assertIn(level, valid_levels, 
                             f"Invalid heading level '{level}' in {json_file.name}")
    
    def test_page_numbers_are_positive(self):
        """Test that all page numbers are positive integers"""
        if not self.outputs_dir.exists():
            self.skipTest("Outputs directory does not exist")
        
        for json_file in self.outputs_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data.get("outline", []):
                page = item.get("page")
                self.assertIsInstance(page, int, f"Page should be integer in {json_file.name}")
                self.assertGreater(page, 0, f"Page should be positive in {json_file.name}")
    
    def test_text_content_not_empty(self):
        """Test that text content is not empty"""
        if not self.outputs_dir.exists():
            self.skipTest("Outputs directory does not exist")
        
        for json_file in self.outputs_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Test title is not empty
            title = data.get("title", "")
            self.assertNotEqual(title.strip(), "", f"Title should not be empty in {json_file.name}")
            
            # Test outline text is not empty
            for item in data.get("outline", []):
                text = item.get("text", "")
                self.assertNotEqual(text.strip(), "", 
                                   f"Outline text should not be empty in {json_file.name}")

class TestDockerConfiguration(unittest.TestCase):
    """Test suite for Docker configuration"""
    
    def setUp(self):
        self.dockerfile_path = Path("./Dockerfile")
    
    def test_dockerfile_exists(self):
        """Test that Dockerfile exists"""
        self.assertTrue(self.dockerfile_path.exists(), "Dockerfile should exist")
    
    def test_dockerfile_has_required_components(self):
        """Test that Dockerfile has all required components"""
        if not self.dockerfile_path.exists():
            self.skipTest("Dockerfile does not exist")
        
        with open(self.dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
        
        required_components = [
            "FROM",
            "WORKDIR",
            "COPY",
            "RUN pip install",
            "CMD"
        ]
        
        for component in required_components:
            self.assertIn(component, dockerfile_content, 
                         f"Dockerfile should contain '{component}'")

class TestAccuracyMetrics(unittest.TestCase):
    """Test suite for accuracy checking functionality"""
    
    def test_accuracy_check_script_exists(self):
        """Test that accuracy check script exists"""
        accuracy_script = Path("./accuracy_check.py")
        self.assertTrue(accuracy_script.exists(), "accuracy_check.py should exist")
    
    def test_accuracy_check_can_import(self):
        """Test that accuracy check script can be imported"""
        try:
            import accuracy_check
            self.assertTrue(hasattr(accuracy_check, 'check_accuracy'), 
                          "accuracy_check should have check_accuracy function")
        except ImportError as e:
            self.fail(f"Could not import accuracy_check: {e}")

def run_tests():
    """Run all tests and display results"""
    print("🧪 Running PDF Processing Test Suite...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPDFProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestDockerConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestAccuracyMetrics))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Display summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "N/A")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n⚠️  ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("\n✅ All tests passed!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
