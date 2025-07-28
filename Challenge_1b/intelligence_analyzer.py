import json
import sys
from pathlib import Path
from collections import defaultdict
# Note: matplotlib and pandas imports removed to avoid dependencies
# Can be added back if visualization features are needed

def analyze_document_intelligence():
    """Analyze the intelligence and extraction quality across all collections"""
    base_dir = Path(".")
    collections = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("Collection")]
    
    analysis_results = {
        "collections": [],
        "overall_stats": {},
        "quality_metrics": {}
    }
    
    print("🧠 Document Intelligence Analysis")
    print("=" * 50)
    
    total_documents = 0
    total_pages = 0
    total_sections = 0
    all_scores = []
    
    for collection in sorted(collections):
        output_file = collection / "challenge1b_output.json"
        
        if not output_file.exists():
            print(f"⚠️  No output file for {collection.name}")
            continue
        
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            collection_analysis = analyze_collection_quality(data, collection.name)
            analysis_results["collections"].append(collection_analysis)
            
            # Update totals
            total_documents += collection_analysis["document_count"]
            total_pages += collection_analysis["total_pages"]
            total_sections += collection_analysis["total_sections"]
            all_scores.extend(collection_analysis["quality_scores"])
            
            print(f"\n📁 {collection.name}")
            print(f"  Documents: {collection_analysis['document_count']}")
            print(f"  Pages: {collection_analysis['total_pages']}")
            print(f"  Sections: {collection_analysis['total_sections']}")
            print(f"  Avg Quality Score: {collection_analysis['avg_quality_score']:.2f}")
            print(f"  Content Diversity: {collection_analysis['content_diversity']:.2f}")
            
        except Exception as e:
            print(f"❌ Error analyzing {collection.name}: {e}")
    
    # Calculate overall metrics
    analysis_results["overall_stats"] = {
        "total_documents": total_documents,
        "total_pages": total_pages,
        "total_sections": total_sections,
        "avg_pages_per_doc": total_pages / total_documents if total_documents > 0 else 0,
        "avg_sections_per_doc": total_sections / total_documents if total_documents > 0 else 0,
        "overall_quality_score": sum(all_scores) / len(all_scores) if all_scores else 0
    }
    
    print(f"\n📊 OVERALL STATISTICS")
    print("=" * 30)
    print(f"Total Documents: {total_documents}")
    print(f"Total Pages: {total_pages}")
    print(f"Total Sections: {total_sections}")
    print(f"Avg Pages/Doc: {analysis_results['overall_stats']['avg_pages_per_doc']:.1f}")
    print(f"Avg Sections/Doc: {analysis_results['overall_stats']['avg_sections_per_doc']:.1f}")
    print(f"Overall Quality: {analysis_results['overall_stats']['overall_quality_score']:.2f}/10")
    
    return analysis_results

def analyze_collection_quality(data, collection_name):
    """Analyze quality metrics for a single collection"""
    documents = data.get("documents", [])
    
    # Basic stats
    document_count = len(documents)
    total_pages = sum(doc.get("total_pages", 0) for doc in documents)
    total_sections = sum(len(doc.get("sections", [])) for doc in documents)
    
    # Quality scoring
    quality_scores = []
    word_counts = []
    section_counts = []
    
    for doc in documents:
        sections = doc.get("sections", [])
        section_count = len(sections)
        section_counts.append(section_count)
        
        # Calculate document quality score (0-10)
        doc_score = calculate_document_score(doc)
        quality_scores.append(doc_score)
        
        # Calculate word counts
        total_words = sum(section.get("word_count", 0) for section in sections)
        word_counts.append(total_words)
    
    # Calculate diversity metrics
    content_diversity = calculate_content_diversity(documents)
    
    return {
        "collection_name": collection_name,
        "document_count": document_count,
        "total_pages": total_pages,
        "total_sections": total_sections,
        "quality_scores": quality_scores,
        "avg_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
        "content_diversity": content_diversity,
        "word_distribution": {
            "min": min(word_counts) if word_counts else 0,
            "max": max(word_counts) if word_counts else 0,
            "avg": sum(word_counts) / len(word_counts) if word_counts else 0
        }
    }

def calculate_document_score(document):
    """Calculate a quality score for a document (0-10)"""
    score = 0
    
    # Title quality (0-2 points)
    title = document.get("document_name", "")
    if title and len(title) > 5:
        score += 2
    elif title:
        score += 1
    
    # Section count (0-3 points)
    sections = document.get("sections", [])
    section_count = len(sections)
    if section_count >= 10:
        score += 3
    elif section_count >= 5:
        score += 2
    elif section_count >= 1:
        score += 1
    
    # Content quality (0-3 points)
    if sections:
        avg_words_per_section = sum(s.get("word_count", 0) for s in sections) / len(sections)
        if avg_words_per_section >= 50:
            score += 3
        elif avg_words_per_section >= 20:
            score += 2
        elif avg_words_per_section >= 5:
            score += 1
    
    # Structure quality (0-2 points)
    has_varied_sections = len(set(s.get("title", "").lower() for s in sections)) > 1
    if has_varied_sections:
        score += 2
    elif sections:
        score += 1
    
    return min(score, 10)

def calculate_content_diversity(documents):
    """Calculate content diversity score (0-10)"""
    if not documents:
        return 0
    
    # Collect all section titles
    all_titles = []
    for doc in documents:
        for section in doc.get("sections", []):
            title = section.get("title", "").lower().strip()
            if title:
                all_titles.append(title)
    
    if not all_titles:
        return 0
    
    # Calculate uniqueness ratio
    unique_titles = len(set(all_titles))
    total_titles = len(all_titles)
    
    diversity_ratio = unique_titles / total_titles
    return min(diversity_ratio * 10, 10)

def generate_insights_report():
    """Generate detailed insights about document processing"""
    print("📋 Generating Document Intelligence Report...")
    
    analysis = analyze_document_intelligence()
    
    # Create detailed report
    report = {
        "report_metadata": {
            "generated_at": "2024-12-19",
            "report_type": "Document Intelligence Analysis",
            "collections_analyzed": len(analysis["collections"])
        },
        "executive_summary": generate_executive_summary(analysis),
        "detailed_analysis": analysis,
        "recommendations": generate_recommendations(analysis)
    }
    
    # Save report
    report_file = "intelligence_report.json"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Report saved to: {report_file}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
    
    return report

def generate_executive_summary(analysis):
    """Generate executive summary from analysis"""
    stats = analysis["overall_stats"]
    
    # Determine quality level
    quality_score = stats["overall_quality_score"]
    if quality_score >= 8:
        quality_level = "Excellent"
    elif quality_score >= 6:
        quality_level = "Good"
    elif quality_score >= 4:
        quality_level = "Fair"
    else:
        quality_level = "Needs Improvement"
    
    return {
        "total_documents_processed": stats["total_documents"],
        "total_content_extracted": f"{stats['total_pages']} pages, {stats['total_sections']} sections",
        "processing_efficiency": f"{stats['avg_sections_per_doc']:.1f} sections per document",
        "overall_quality_assessment": f"{quality_level} ({quality_score:.1f}/10)",
        "key_findings": [
            f"Successfully processed {stats['total_documents']} documents across multiple collections",
            f"Extracted {stats['total_sections']} structured sections from {stats['total_pages']} pages",
            f"Average document contains {stats['avg_pages_per_doc']:.1f} pages and {stats['avg_sections_per_doc']:.1f} sections"
        ]
    }

def generate_recommendations(analysis):
    """Generate actionable recommendations"""
    recommendations = []
    
    stats = analysis["overall_stats"]
    
    if stats["overall_quality_score"] < 6:
        recommendations.append({
            "category": "Quality Improvement",
            "issue": "Low overall quality score",
            "recommendation": "Implement enhanced text cleaning and section detection algorithms",
            "priority": "High"
        })
    
    if stats["avg_sections_per_doc"] < 3:
        recommendations.append({
            "category": "Section Detection",
            "issue": "Low section count per document",
            "recommendation": "Improve heading detection algorithms or adjust section boundary detection",
            "priority": "Medium"
        })
    
    # Collection-specific recommendations
    for collection in analysis["collections"]:
        if collection["avg_quality_score"] < stats["overall_quality_score"] - 1:
            recommendations.append({
                "category": "Collection-Specific",
                "issue": f"Low quality score for {collection['collection_name']}",
                "recommendation": f"Review and optimize processing for {collection['collection_name']} document types",
                "priority": "Medium"
            })
    
    return recommendations

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        generate_insights_report()
    else:
        analyze_document_intelligence()
