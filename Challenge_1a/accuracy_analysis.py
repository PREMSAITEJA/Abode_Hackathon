import json
import os
from pathlib import Path

def load_expected_results():
    """Expected results based on schema and requirements"""
    return {
        "file01.json": {
            "title": "Application form for grant of LTC advance",
            "headings": ["Age", "Date", "Designation", "Name", "PAY + SI + NPA", "Place", "Serial No.", "Signature of the applicant", "Station"]
        },
        "file02.json": {
            "title": "Revision History", 
            "headings": ["Revision History", "Document Information", "Version", "Date", "Author", "Description", "Approval", "Distribution", "References", "Glossary", "Appendices", "Contact Information", "Legal Notice"]
        },
        "file03.json": {
            "title": "RFP: R",
            "headings": ["RFP: R", "Access:", "Local points of entry:", "Provincial Purchasing & Licensing:", "Registration Requirements:", "Submission Requirements:", "Evaluation Criteria:", "Timeline:", "Contact Information:", "Terms and Conditions:", "Appendix A:", "Appendix B:", "Appendix C:", "Appendix D:", "Appendix E:", "Appendix F:", "Appendix G:", "Appendix H:", "Appendix I:", "Appendix J:", "Appendix K:", "Appendix L:"]
        },
        "file04.json": {
            "title": "Parsippany -Troy Hills STEM Pathways",
            "headings": ["STEM Career Exploration"]
        },
        "file05.json": {
            "title": "PARKWAY",
            "headings": ["PARKWAY"]
        }
    }

def calculate_heading_accuracy(actual_headings, expected_headings):
    """Calculate heading accuracy with partial matching"""
    if not expected_headings:
        return 1.0 if not actual_headings else 0.0
    
    matches = 0
    for expected in expected_headings:
        # Look for exact or partial matches
        for actual in actual_headings:
            actual_text = actual.get("text", "").strip()
            if expected == actual_text or expected in actual_text or actual_text in expected:
                matches += 1
                break
    
    return matches / len(expected_headings)

def analyze_accuracy():
    """Comprehensive accuracy analysis"""
    output_dir = "./sample_dataset/outputs"
    expected_results = load_expected_results()
    
    if not os.path.exists(output_dir):
        print(f"❌ Output directory not found: {output_dir}")
        return
    
    print("🎯 OPTIMIZED ACCURACY ANALYSIS")
    print("=" * 50)
    
    total_files = len(expected_results)
    title_correct = 0
    total_heading_accuracy = 0
    
    detailed_results = {}
    
    for filename, expected in expected_results.items():
        filepath = os.path.join(output_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ Missing output file: {filename}")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                actual = json.load(f)
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            continue
        
        # Title accuracy
        actual_title = actual.get("title", "").strip()
        expected_title = expected["title"]
        title_match = (actual_title == expected_title)
        
        if title_match:
            title_correct += 1
        
        # Heading accuracy
        actual_headings = actual.get("outline", [])
        expected_headings = expected["headings"]
        heading_accuracy = calculate_heading_accuracy(actual_headings, expected_headings)
        total_heading_accuracy += heading_accuracy
        
        # Store detailed results
        detailed_results[filename] = {
            "title_match": title_match,
            "actual_title": actual_title,
            "expected_title": expected_title,
            "heading_accuracy": heading_accuracy,
            "actual_headings": [h.get("text", "") for h in actual_headings],
            "expected_headings": expected_headings,
            "headings_found": len(actual_headings),
            "headings_expected": len(expected_headings)
        }
        
        # Individual file report
        status = "✅" if title_match else "❌"
        print(f"\n{filename} {status}")
        print(f"  Title: '{actual_title}' {'✅' if title_match else '❌'}")
        print(f"  Expected: '{expected_title}'")
        print(f"  Headings: {len(actual_headings)}/{len(expected_headings)} ({heading_accuracy:.1%})")
        
        if len(actual_headings) > 0:
            print(f"  Found headings: {actual_headings[:3]}{'...' if len(actual_headings) > 3 else ''}")
    
    # Overall accuracy
    title_accuracy = title_correct / total_files
    avg_heading_accuracy = total_heading_accuracy / total_files
    combined_accuracy = (title_accuracy + avg_heading_accuracy) / 2
    
    print("\n" + "=" * 50)
    print("📊 OVERALL ACCURACY RESULTS")
    print("=" * 50)
    print(f"Title Accuracy:    {title_accuracy:.1%} ({title_correct}/{total_files})")
    print(f"Heading Accuracy:  {avg_heading_accuracy:.1%}")
    print(f"Combined Accuracy: {combined_accuracy:.1%}")
    
    # Target assessment
    target_met = combined_accuracy >= 0.97
    print(f"\n🎯 TARGET STATUS: {'✅ ACHIEVED' if target_met else '⚠️ NEEDS IMPROVEMENT'}")
    print(f"Target: 97-100% | Current: {combined_accuracy:.1%}")
    
    if not target_met:
        print("\n🔧 OPTIMIZATION RECOMMENDATIONS:")
        for filename, result in detailed_results.items():
            if not result["title_match"] or result["heading_accuracy"] < 0.9:
                print(f"  • {filename}: Focus on {'title extraction' if not result['title_match'] else 'heading detection'}")
    
    return detailed_results

if __name__ == "__main__":
    analyze_accuracy()
