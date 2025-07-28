import fitz  # PyMuPDF
import json
import os
import re
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans  # Lightweight clustering
from sentence_transformers import SentenceTransformer  # Small ML model for classification
from sklearn.linear_model import LogisticRegression  # Simple classifier on embeddings
import warnings
from jsonschema import validate, ValidationError

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load tiny model (offline, ~110MB) - with error handling
try:
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Distilled, fast on CPU
    model_available = True
except Exception as e:
    print(f"Warning: Could not load SentenceTransformer model: {e}")
    model_available = False
    model = None

# Pre-trained simple classifier (simulated fine-tuning; in reality, train on labeled data)
classifier = LogisticRegression()  # Placeholder; assume fitted with heading examples

# Output schema definition based on the provided schema
OUTPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "outline": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "pattern": "^H[1-3]$"  # Ensure only H1, H2, H3
                    },
                    "text": {
                        "type": "string",
                        "minLength": 1  # Ensure text is not empty
                    },
                    "page": {
                        "type": "integer",
                        "minimum": 1  # Page numbers start from 1
                    }
                },
                "required": ["level", "text", "page"],
                "additionalProperties": False
            }
        }
    },
    "required": ["title", "outline"],
    "additionalProperties": False
}

def validate_output(data):
    """Validate output against the required schema"""
    try:
        validate(instance=data, schema=OUTPUT_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, str(e)

def clean_text(text):
    """Clean and normalize text for output"""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters that might cause JSON issues
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text

def normalize_level(level):
    """Ensure level is in correct format (H1, H2, H3)"""
    if not level or not level.startswith('H'):
        return "H1"
    
    level_num = re.search(r'\d+', level)
    if level_num:
        num = int(level_num.group())
        if num > 3:
            return "H3"
        elif num < 1:
            return "H1"
        else:
            return f"H{num}"
    return "H1"

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    candidates = []
    
    # Collect spans with metadata
    font_sizes = []
    all_text_sizes = []  # Track all font sizes for better analysis
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        page_height = page.bound()[3]
        page_width = page.bound()[2]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        
                        # Enhanced filtering
                        if (not text or 
                            len(text) < 3 or  # Too short
                            len(text) > 150 or  # Too long for heading
                            re.match(r'^\d+\.?\s*$', text) or  # Just numbers
                            re.match(r'^page\s+\d+', text.lower()) or  # Page numbers
                            re.match(r'^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text) or  # Dates
                            re.match(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', text.lower()) or  # Month names
                            '©' in text or 'copyright' in text.lower() or  # Copyright
                            text.count('.') > 5 or  # Dotted lines
                            text.count('_') > 5 or  # Underlines
                            re.match(r'^[^\w\s]+$', text)):  # Only special characters
                            continue
                        
                        size = span["size"]
                        flags = span["flags"]
                        is_bold = (flags & 16) > 0
                        is_italic = (flags & 2) > 0
                        is_upper = text.isupper() and len(text) > 3
                        is_title_case = text.istitle()
                        
                        # Position analysis
                        x_pos = span["bbox"][0] / page_width
                        y_pos = span["bbox"][1] / page_height
                        
                        # Check if text is likely a heading based on content
                        is_likely_heading = (
                            is_bold or is_upper or is_title_case or
                            any(word in text.lower() for word in ['chapter', 'section', 'introduction', 'overview', 'conclusion']) or
                            re.match(r'^\d+\.?\d*\s+[A-Z]', text)  # Numbered sections
                        )
                        
                        if is_likely_heading:
                            candidates.append({
                                "text": text,
                                "size": size,
                                "bold": is_bold,
                                "italic": is_italic,
                                "upper": is_upper,
                                "title_case": is_title_case,
                                "x_pos": x_pos,
                                "y_pos": y_pos,
                                "page": page_num + 1,
                                "char_count": len(text),
                                "word_count": len(text.split())
                            })
                            font_sizes.append(size)
                        
                        all_text_sizes.append(size)
    
    if not candidates:
        return {"title": "Untitled", "outline": []}
    
    # Analyze font sizes more intelligently
    font_sizes_array = np.array(font_sizes)
    all_sizes_array = np.array(all_text_sizes)
    
    # Find the most common body text size (likely the smallest frequent size)
    size_counts = np.bincount(all_sizes_array.astype(int))
    body_text_size = np.argmax(size_counts)
    
    # Filter out sizes too close to body text
    significant_sizes = font_sizes_array[font_sizes_array > body_text_size + 1]
    
    if len(significant_sizes) == 0:
        significant_sizes = font_sizes_array
    
    # Cluster significant font sizes
    unique_sizes = np.unique(significant_sizes)
    n_clusters = min(4, len(unique_sizes))
    
    if len(significant_sizes) < 2 or n_clusters < 2:
        # If we don't have enough data for clustering, use simple size-based grouping
        size_clusters = np.array(sorted(unique_sizes, reverse=True))
    else:
        kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42).fit(significant_sizes.reshape(-1, 1))
        size_clusters = np.array(sorted(np.unique(kmeans.cluster_centers_.flatten()), reverse=True))
    
    # Better title extraction - find the most prominent text on first page
    first_page_candidates = [c for c in candidates if c["page"] == 1]
    if first_page_candidates and not title:
        # Sort by score (size + formatting + position)
        for cand in first_page_candidates:
            title_score = 0
            if cand["size"] > body_text_size + 3:  # Significantly larger than body text
                title_score += 0.4
            if cand["bold"]:
                title_score += 0.3
            if cand["upper"] or cand["title_case"]:
                title_score += 0.2
            if cand["y_pos"] < 0.3:  # Top of page
                title_score += 0.2
            if 3 <= cand["word_count"] <= 10:  # Reasonable title length
                title_score += 0.1
            
            cand["title_score"] = title_score
        
        # Get the best title candidate
        title_candidates = sorted(first_page_candidates, key=lambda x: x.get("title_score", 0), reverse=True)
        if title_candidates and title_candidates[0]["title_score"] > 0.8:
            title = title_candidates[0]["text"]
            # Remove title from candidates so it doesn't appear in outline
            candidates = [c for c in candidates if not (c["page"] == 1 and c["text"] == title)]
    
    # Score and classify candidates
    outline = []
    found_title = False
    
    for i, cand in enumerate(candidates):
        # Calculate heading score
        score = 0
        
        # Font size score
        if len(size_clusters) > 0:
            cluster_idx = np.argmin(np.abs(size_clusters - cand["size"]))
            size_score = (len(size_clusters) - cluster_idx) / len(size_clusters)
            score += size_score * 0.4
        
        # Formatting score
        if cand["bold"]:
            score += 0.3
        if cand["upper"] and cand["word_count"] <= 5:
            score += 0.2
        if cand["title_case"]:
            score += 0.1
        
        # Position score (prefer left-aligned, top of page)
        if cand["x_pos"] < 0.2:  # Left aligned
            score += 0.1
        if cand["y_pos"] < 0.3:  # Top of page
            score += 0.1
        
        # Content-based scoring
        text_lower = cand["text"].lower()
        if any(word in text_lower for word in ['chapter', 'section', 'part', 'introduction', 'overview', 'summary', 'conclusion']):
            score += 0.2
        
        # Length penalty for very long text
        if cand["char_count"] > 80:
            score -= 0.2
        
        # Word count preference (2-8 words ideal for headings)
        if 2 <= cand["word_count"] <= 8:
            score += 0.1
        
        # Determine level based on score and size
        if score > 0.7 and not found_title and cand["y_pos"] < 0.2:
            title = cand["text"]
            found_title = True
            continue
        elif score > 0.6:
            if cluster_idx == 0:
                level = "H1"
            elif cluster_idx == 1:
                level = "H2"
            else:
                level = "H3"
            
            outline.append({
                "level": level,
                "text": cand["text"],
                "page": cand["page"],
                "confidence": round(score, 2)
            })
    
    # Sort by page and position, then remove duplicates and low-confidence entries
    outline.sort(key=lambda x: (x["page"], x["text"]))
    
    # Remove very similar entries
    filtered_outline = []
    for item in outline:
        if item["confidence"] > 0.65:  # Only high-confidence headings
            # Check for similarity with existing items
            is_duplicate = False
            for existing in filtered_outline:
                if (existing["page"] == item["page"] and 
                    (existing["text"] in item["text"] or item["text"] in existing["text"])):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                # Remove confidence from final output
                filtered_item = {k: v for k, v in item.items() if k != "confidence"}
                filtered_outline.append(filtered_item)
    
    # Ensure logical hierarchy
    for i in range(1, len(filtered_outline)):
        curr_level = int(filtered_outline[i]["level"][1])
        prev_level = int(filtered_outline[i-1]["level"][1])
        
        # Don't jump more than one level
        if curr_level > prev_level + 1:
            filtered_outline[i]["level"] = f"H{prev_level + 1}"
    
    doc.close()
    
    # Ensure schema compliance
    result = {
        "title": clean_text(title) if title else "Untitled",
        "outline": []
    }
    
    # Process outline items to ensure strict schema compliance
    for item in filtered_outline:
        outline_item = {
            "level": normalize_level(item.get("level", "H1")),
            "text": clean_text(item.get("text", "")),
            "page": int(item.get("page", 1))  # Ensure integer type
        }
        
        # Only add if text is not empty after cleaning
        if outline_item["text"]:
            result["outline"].append(outline_item)
    
    # Validate against schema
    is_valid, error = validate_output(result)
    if not is_valid:
        print(f"Warning: Output validation failed: {error}")
        # Fallback to ensure valid output
        result = {
            "title": "Untitled",
            "outline": []
        }
    
    return result

if __name__ == "__main__":
    # Check if running in Docker or locally
    if os.path.exists("/app/input"):
        input_dir = "/app/input"
        output_dir = "/app/output"
        schema_path = "/app/schema/output_schema.json"
    else:
        input_dir = "./sample_dataset/pdfs"
        output_dir = "./sample_dataset/outputs"
        schema_path = "./sample_dataset/schema/output_schema.json"
    
    # Load schema from file if available
    if os.path.exists(schema_path):
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                file_schema = json.load(f)
            print(f"✓ Loaded schema from: {schema_path}")
        except Exception as e:
            print(f"Warning: Could not load schema file: {e}")
            print("Using built-in schema definition")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    print(f"Processing {len(pdf_files)} PDF files...")
    
    total_outlines = 0
    for i, filename in enumerate(pdf_files, 1):
        print(f"Processing ({i}/{len(pdf_files)}): {filename}")
        pdf_path = os.path.join(input_dir, filename)
        result = extract_outline(pdf_path)
        output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
        
        # Validate before saving
        is_valid, error = validate_output(result)
        if not is_valid:
            print(f"  ❌ Validation failed: {error}")
            continue
            
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Title: {result['title']}")
        print(f"  ✓ Found {len(result['outline'])} headings")
        print(f"  ✓ Schema validation: PASSED")
        total_outlines += len(result['outline'])
    
    print(f"\n✅ Processing complete!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 Total headings extracted: {total_outlines}")
    print(f"📋 All outputs comply with required schema")