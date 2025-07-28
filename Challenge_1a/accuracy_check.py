import json
import os
from pathlib import Path

def load_expected_results():
    """Load expected results for accuracy testing"""
    expected_results = {
        "file01.pdf": {
            "title": "Application form for grant of LTC advance",
            "headings": [
                "Age", "Date", "Designation", "Name", "PAY + SI + NPA",
                "Place", "Serial No.", "Signature of the applicant", "Station"
            ]
        },
        "file02.pdf": {
            "title": "Revision History",
            "headings": [
                "Revision History", "Document Information", "Version", "Date", 
                "Author", "Description", "Approval", "Distribution", "References",
                "Glossary", "Appendices", "Contact Information", "Legal Notice"
            ]
        },
        "file03.pdf": {
            "title": "RFP: R",
            "headings": [
                "RFP: R", "Access:", "Local points of entry:", 
                "Provincial Purchasing & Licensing:", "Registration Requirements:",
                "Submission Requirements:", "Evaluation Criteria:", "Timeline:",
                "Contact Information:", "Terms and Conditions:", "Appendix A:",
                "Appendix B:", "Appendix C:", "Appendix D:", "Appendix E:",
                "Appendix F:", "Appendix G:", "Appendix H:", "Appendix I:",
                "Appendix J:", "Appendix K:", "Appendix L:"
            ]
        },
        "file04.pdf": {
            "title": "Parsippany -Troy Hills STEM Pathways",
            "headings": [
                "STEM Career Exploration"
            ]
        },
        "file05.pdf": {
            "title": "PARKWAY",
            "headings": [
                "PARKWAY"
            ]
        }
    }
    return expected_results

def calculate_accuracy(expected, actual):
    """Calculate accuracy metrics"""
    if not expected and not actual:
        return 1.0
    if not expected or not actual:
        return 0.0
    
    # Convert to sets for easier comparison
    expected_set = set(expected) if isinstance(expected, list) else {expected}
    actual_set = set(actual) if isinstance(actual, list) else {actual}
    
    # Calculate intersection
    matches = len(expected_set.intersection(actual_set))
    total_expected = len(expected_set)
    total_actual = len(actual_set)
    
    if total_expected == 0:
        return 1.0 if total_actual == 0 else 0.0
    
    # Calculate precision and recall
    precision = matches / total_actual if total_actual > 0 else 0
    recall = matches / total_expected if total_expected > 0 else 0
    
    # Return F1 score as accuracy metric
    if precision + recall == 0:
        return 0.0
    
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score

def check_accuracy():
    """Main accuracy checking function"""
    expected_results = load_expected_results()
    outputs_dir = Path("./sample_dataset/outputs")
    
    if not outputs_dir.exists():
        print("❌ Outputs directory not found!")
        return
    
    total_title_matches = 0
    total_heading_matches = 0
    total_expected_headings = 0
    total_actual_headings = 0
    total_files = 0
    
    print("=== ACCURACY CHECK RESULTS ===\n")
    
    for pdf_name, expected in expected_results.items():
        json_file = outputs_dir / f"{pdf_name.replace('.pdf', '.json')}"
        
        if not json_file.exists():
            print(f"❌ Output file not found for {pdf_name}")
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                actual_data = json.load(f)
            
            # Check title accuracy
            expected_title = expected["title"]
            actual_title = actual_data.get("title", "")
            title_match = expected_title.strip().lower() == actual_title.strip().lower()
            
            # Check heading accuracy
            expected_headings = expected["headings"]
            actual_headings = [item["text"] for item in actual_data.get("outline", [])]
            
            heading_matches = 0
            for exp_heading in expected_headings:
                if any(exp_heading.lower() in act_heading.lower() or 
                      act_heading.lower() in exp_heading.lower() 
                      for act_heading in actual_headings):
                    heading_matches += 1
            
            # Display results for this file
            print(f"=== {pdf_name.upper()} ===")
            print(f"Title Match: {'True' if title_match else 'False'}")
            print(f"Expected: \"{expected_title}\"")
            print(f"Actual: \"{actual_title}\"")
            print(f"Expected headings: {len(expected_headings)}")
            print(f"Actual headings: {len(actual_headings)}")
            print(f"Exact matches: {heading_matches}/{len(expected_headings)} ({100*heading_matches/len(expected_headings):.1f}%)")
            print()
            
            # Update totals
            if title_match:
                total_title_matches += 1
            total_heading_matches += heading_matches
            total_expected_headings += len(expected_headings)
            total_actual_headings += len(actual_headings)
            total_files += 1
            
        except Exception as e:
            print(f"❌ Error processing {pdf_name}: {e}")
    
    # Calculate overall accuracy
    print("=== OVERALL ACCURACY ===")
    title_accuracy = (total_title_matches / total_files) * 100 if total_files > 0 else 0
    heading_accuracy = (total_heading_matches / total_expected_headings) * 100 if total_expected_headings > 0 else 0
    combined_accuracy = (title_accuracy + heading_accuracy) / 2
    
    print(f"Title accuracy: {total_title_matches}/{total_files} ({title_accuracy:.1f}%)")
    print(f"Total headings expected: {total_expected_headings}")
    print(f"Total headings matched: {total_heading_matches}")
    print(f"Heading accuracy: {heading_accuracy:.1f}%")
    print(f"Combined accuracy: {combined_accuracy:.1f}%")

if __name__ == "__main__":
    check_accuracy()
