import json
import os
from pathlib import Path
import sys

def validate_collection_outputs():
    """Validate all collection outputs against expected structure"""
    base_dir = Path(".")
    collections = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("Collection")]
    
    results = {
        "total_collections": len(collections),
        "validation_results": [],
        "overall_status": "UNKNOWN"
    }
    
    print("🔍 Validating Challenge 1B Collection Outputs...")
    print("=" * 50)
    
    all_valid = True
    
    for collection in sorted(collections):
        collection_result = {
            "collection_name": collection.name,
            "status": "PASS",
            "issues": [],
            "stats": {}
        }
        
        print(f"\n📁 Validating {collection.name}...")
        
        # Check required files
        input_file = collection / "challenge1b_input.json"
        output_file = collection / "challenge1b_output.json"
        pdfs_dir = collection / "PDFs"
        
        if not input_file.exists():
            collection_result["issues"].append("Missing challenge1b_input.json")
            collection_result["status"] = "FAIL"
            all_valid = False
        
        if not output_file.exists():
            collection_result["issues"].append("Missing challenge1b_output.json")
            collection_result["status"] = "FAIL"
            all_valid = False
        else:
            # Validate output structure
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    output_data = json.load(f)
                
                # Check required fields
                required_fields = ["collection_name", "processing_date", "total_documents", "documents"]
                for field in required_fields:
                    if field not in output_data:
                        collection_result["issues"].append(f"Missing required field: {field}")
                        collection_result["status"] = "FAIL"
                        all_valid = False
                
                # Collect statistics
                if "documents" in output_data:
                    collection_result["stats"]["total_documents"] = len(output_data["documents"])
                    collection_result["stats"]["total_pages"] = sum(
                        doc.get("total_pages", 0) for doc in output_data["documents"]
                    )
                    collection_result["stats"]["total_sections"] = sum(
                        len(doc.get("sections", [])) for doc in output_data["documents"]
                    )
                
                print(f"  ✅ Output structure valid")
                print(f"  📄 Documents: {collection_result['stats'].get('total_documents', 0)}")
                print(f"  📖 Pages: {collection_result['stats'].get('total_pages', 0)}")
                print(f"  📝 Sections: {collection_result['stats'].get('total_sections', 0)}")
                
            except json.JSONDecodeError as e:
                collection_result["issues"].append(f"Invalid JSON in output file: {e}")
                collection_result["status"] = "FAIL"
                all_valid = False
            except Exception as e:
                collection_result["issues"].append(f"Error reading output file: {e}")
                collection_result["status"] = "FAIL"
                all_valid = False
        
        if not pdfs_dir.exists():
            collection_result["issues"].append("Missing PDFs directory")
            collection_result["status"] = "FAIL"
            all_valid = False
        else:
            pdf_count = len(list(pdfs_dir.glob("*.pdf")))
            collection_result["stats"]["pdf_files"] = pdf_count
            print(f"  📚 PDF files: {pdf_count}")
        
        # Display issues if any
        if collection_result["issues"]:
            print(f"  ❌ Issues found:")
            for issue in collection_result["issues"]:
                print(f"    - {issue}")
        
        results["validation_results"].append(collection_result)
    
    # Overall summary
    results["overall_status"] = "PASS" if all_valid else "FAIL"
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results["validation_results"] if r["status"] == "PASS")
    failed = sum(1 for r in results["validation_results"] if r["status"] == "FAIL")
    
    print(f"Collections validated: {results['total_collections']}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Overall status: {'✅ PASS' if all_valid else '❌ FAIL'}")
    
    # Save validation report
    report_file = "validation_report.json"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"\n📋 Validation report saved to: {report_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save validation report: {e}")
    
    return results

def compare_collections():
    """Compare statistics across all collections"""
    base_dir = Path(".")
    collections = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("Collection")]
    
    print("📊 Collection Comparison")
    print("=" * 60)
    print(f"{'Collection':<15} {'PDFs':<8} {'Pages':<8} {'Sections':<10} {'Avg Sections/Doc':<15}")
    print("-" * 60)
    
    for collection in sorted(collections):
        output_file = collection / "challenge1b_output.json"
        pdfs_dir = collection / "PDFs"
        
        pdf_count = len(list(pdfs_dir.glob("*.pdf"))) if pdfs_dir.exists() else 0
        pages = 0
        sections = 0
        documents = 0
        
        if output_file.exists():
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                documents = len(data.get("documents", []))
                pages = sum(doc.get("total_pages", 0) for doc in data.get("documents", []))
                sections = sum(len(doc.get("sections", [])) for doc in data.get("documents", []))
                
            except Exception:
                pass
        
        avg_sections = sections / documents if documents > 0 else 0
        
        print(f"{collection.name:<15} {pdf_count:<8} {pages:<8} {sections:<10} {avg_sections:<15.1f}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        compare_collections()
    else:
        validate_collection_outputs()
