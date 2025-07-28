import json
import sys
from datetime import datetime
import os
from pathlib import Path

# Try importing PDF libraries with fallback options
PDF_LIBRARY = None
try:
    import PyPDF2
    PDF_LIBRARY = "PyPDF2"
    print("✅ Using PyPDF2 for PDF processing")
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_LIBRARY = "PyMuPDF"
        print("✅ Using PyMuPDF as fallback for PDF processing")
    except ImportError:
        print("❌ No PDF processing library available. Please install PyPDF2 or PyMuPDF")
        sys.exit(1)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using available PDF library."""
    text_by_page = {}
    
    try:
        if PDF_LIBRARY == "PyPDF2":
            # Use PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Extract text from each page
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        text_by_page[i+1] = text  # Page numbers start from 1
        
        elif PDF_LIBRARY == "PyMuPDF":
            # Use PyMuPDF as fallback
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text:
                    text_by_page[page_num + 1] = text
            doc.close()
        
        return text_by_page
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return {}

def process_collection(collection_path):
    """Process a collection of PDFs and generate structured output."""
    collection_path = Path(collection_path)
    pdfs_dir = collection_path / "PDFs"
    input_file = collection_path / "challenge1b_input.json"
    output_file = collection_path / "challenge1b_output.json"
    
    if not pdfs_dir.exists():
        print(f"❌ PDFs directory not found in {collection_path}")
        return
    
    # Load input configuration if exists
    input_config = {}
    if input_file.exists():
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                input_config = json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load input config: {e}")
    
    # Process all PDFs in the collection
    pdf_files = list(pdfs_dir.glob("*.pdf"))
    results = []
    
    if not pdf_files:
        print(f"  ⚠️  No PDF files found in {pdfs_dir}")
        return
    
    print(f"📚 Processing {len(pdf_files)} PDF files in {collection_path.name}...")
    
    for idx, pdf_file in enumerate(sorted(pdf_files), 1):
        print(f"  📄 Processing ({idx}/{len(pdf_files)}): {pdf_file.name}")
        
        try:
            # Extract text from PDF
            text_by_page = extract_text_from_pdf(pdf_file)
            
            if not text_by_page:
                print(f"    ⚠️  Warning: No text extracted from {pdf_file.name}")
                continue
            
            # Create document structure
            doc_info = {
                "document_name": pdf_file.name,
                "total_pages": len(text_by_page),
                "sections": [],
                "extracted_text": text_by_page if input_config.get("output_format", {}).get("include_full_text", True) else {},
                "processing_timestamp": datetime.now().isoformat(),
                "file_size_bytes": pdf_file.stat().st_size,
                "processing_status": "success"
            }

            # Enhanced section extraction with better heuristics
            sections = []
            for page_num, text in text_by_page.items():
                if not text.strip():
                    continue
                    
                # Clean and split text into lines
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                current_section = None
                section_content = []
                
                for line in lines:
                    # Enhanced heading detection with multiple criteria
                    is_heading = False
                    
                    # Check various heading patterns
                    if len(line) < 100:  # Reasonable heading length
                        # Check for all caps (common in headings)
                        if line.isupper() and len(line.split()) <= 8:
                            is_heading = True
                        # Check for title case
                        elif line.istitle() and len(line.split()) <= 10:
                            is_heading = True
                        # Check for keywords that indicate sections
                        elif any(keyword in line.lower() for keyword in [
                            'chapter', 'section', 'part', 'introduction', 'conclusion',
                            'overview', 'summary', 'background', 'methodology', 'results',
                            'discussion', 'references', 'appendix', 'contents', 'index'
                        ]):
                            is_heading = True
                        # Check for numbered sections (1., 2., I., II., etc.)
                        elif any(line.startswith(prefix) for prefix in [
                            '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.',
                            'I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.', 'VIII.', 'IX.', 'X.',
                            'A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'H.'
                        ]):
                            is_heading = True
                    
                    if is_heading:
                        # Save previous section
                        if current_section and section_content:
                            content_text = '\n'.join(section_content)
                            if len(content_text.split()) >= 5:  # Minimum content threshold
                                sections.append({
                                    "title": current_section,
                                    "content": content_text,
                                    "page": page_num,
                                    "word_count": len(content_text.split())
                                })
                        
                        # Start new section
                        current_section = line
                        section_content = []
                    else:
                        section_content.append(line)
                
                # Don't forget the last section
                if current_section and section_content:
                    content_text = '\n'.join(section_content)
                    if len(content_text.split()) >= 5:  # Minimum content threshold
                        sections.append({
                            "title": current_section,
                            "content": content_text,
                            "page": page_num,
                            "word_count": len(content_text.split())
                        })

            doc_info["sections"] = sections
            
            # Add processing statistics
            doc_info["statistics"] = {
                "total_sections": len(sections),
                "total_words": sum(section["word_count"] for section in sections),
                "average_words_per_section": sum(section["word_count"] for section in sections) / len(sections) if sections else 0,
                "pages_with_sections": len(set(section["page"] for section in sections))
            }
            
            results.append(doc_info)
            print(f"    ✅ Extracted {len(sections)} sections from {len(text_by_page)} pages")
        
        except Exception as e:
            print(f"    ❌ Error processing {pdf_file.name}: {e}")
            # Add failed document info
            results.append({
                "document_name": pdf_file.name,
                "total_pages": 0,
                "sections": [],
                "extracted_text": {},
                "processing_timestamp": datetime.now().isoformat(),
                "file_size_bytes": pdf_file.stat().st_size if pdf_file.exists() else 0,
                "processing_status": "failed",
                "error_message": str(e)
            })    # Generate comprehensive output
    successful_docs = [doc for doc in results if doc.get("processing_status") == "success"]
    failed_docs = [doc for doc in results if doc.get("processing_status") == "failed"]
    
    output_data = {
        "collection_name": collection_path.name,
        "processing_date": datetime.now().isoformat(),
        "total_documents": len(results),
        "successful_documents": len(successful_docs),
        "failed_documents": len(failed_docs),
        "input_config": input_config,
        "documents": results,
        "statistics": {
            "total_pages": sum(doc["total_pages"] for doc in successful_docs),
            "total_sections": sum(len(doc["sections"]) for doc in successful_docs),
            "total_words": sum(doc.get("statistics", {}).get("total_words", 0) for doc in successful_docs),
            "average_sections_per_document": sum(len(doc["sections"]) for doc in successful_docs) / len(successful_docs) if successful_docs else 0,
            "average_pages_per_document": sum(doc["total_pages"] for doc in successful_docs) / len(successful_docs) if successful_docs else 0,
            "average_words_per_document": sum(doc.get("statistics", {}).get("total_words", 0) for doc in successful_docs) / len(successful_docs) if successful_docs else 0,
            "processing_success_rate": len(successful_docs) / len(results) * 100 if results else 0
        },
        "processing_summary": {
            "pdf_library_used": PDF_LIBRARY,
            "total_file_size_bytes": sum(doc.get("file_size_bytes", 0) for doc in results),
            "processing_errors": [{"document": doc["document_name"], "error": doc.get("error_message", "")} for doc in failed_docs]
        }
    }
    
    # Save output with enhanced error handling
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Output saved to: {output_file}")
        
        # Generate comprehensive summary
        stats = output_data["statistics"]
        print(f"  📊 Processing Summary:")
        print(f"    📄 Documents processed: {len(successful_docs)}/{len(results)}")
        print(f"    � Total pages: {stats['total_pages']}")
        print(f"    📝 Total sections: {stats['total_sections']}")
        print(f"    📊 Success rate: {stats['processing_success_rate']:.1f}%")
        print(f"    🔧 Library used: {PDF_LIBRARY}")
        
        if failed_docs:
            print(f"  ⚠️  Failed documents: {[doc['document_name'] for doc in failed_docs]}")
        
    except Exception as e:
        print(f"  ❌ Error saving output: {e}")
        return False
    
    return True

def generate_sample_input(collection_path):
    """Generate a sample input configuration file."""
    collection_path = Path(collection_path)
    input_file = collection_path / "challenge1b_input.json"
    
    sample_config = {
        "processing_options": {
            "extract_images": False,
            "extract_tables": False,
            "language": "auto",
            "min_section_length": 50
        },
        "output_format": {
            "include_full_text": True,
            "include_sections": True,
            "include_statistics": True
        },
        "filters": {
            "exclude_pages": [],
            "include_only_sections": [],
            "min_word_count": 10
        }
    }
    
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2)
        print(f"✅ Sample input config created: {input_file}")
    except Exception as e:
        print(f"❌ Error creating sample input: {e}")

def main():
    """Main processing function."""
    base_dir = Path("../Challenge_1b")
    
    if not base_dir.exists():
        print("Challenge_1b directory not found!")
        return
    
    # Find all collections
    collections = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("Collection")]
    
    if not collections:
        print("No collections found!")
        return
    
    print(f"Found {len(collections)} collections to process:")
    for collection in sorted(collections):
        print(f"  - {collection.name}")
    
    print("\n" + "="*50)
    
    # Process each collection
    for collection in sorted(collections):
        print(f"\n🔄 Processing {collection.name}...")
        
        # Generate sample input if it doesn't exist
        input_file = collection / "challenge1b_input.json"
        if not input_file.exists():
            print(f"  📝 Creating sample input config...")
            generate_sample_input(collection)
        
        # Process the collection
        process_collection(collection)
    
    print(f"\n✅ Processing complete!")
    print("Generated outputs:")
    for collection in sorted(collections):
        output_file = collection / "challenge1b_output.json"
        if output_file.exists():
            print(f"  - {output_file}")

if __name__ == "__main__":
    main()
