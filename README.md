# Adobe India Hackathon 2025 - "Connecting the Dots" Challenge

## 🚀 Project Overview

This repository contains advanced PDF processing solutions for the Adobe India Hackathon 2025. Our goal is to transform PDFs from static documents into intelligent, interactive experiences that understand structure, extract insights, and connect ideas across document collections.

### 🎯 What This Project Does

- **Extracts structured outlines** from PDF documents with high accuracy
- **Analyzes content across multiple document collections** using AI/ML techniques
- **Provides comprehensive testing and validation frameworks**
- **Offers Docker-ready deployment** for scalable processing

## 📁 Project Structure

```
├── Challenge_1a/           # PDF Outline Extraction (Round 1A)
│   ├── process_pdfs.py     # Main PDF processing with ML enhancement
│   ├── accuracy_check.py   # Accuracy validation system
│   ├── test_suite.py       # Comprehensive testing framework
│   ├── Dockerfile          # Container deployment
│   └── sample_dataset/     # Test PDFs and schemas
├── Challenge_1b/           # Multi-Collection Analysis (Round 1B)
│   ├── examine_pdf.py      # Advanced PDF processor
│   ├── collection_validator.py  # Output validation
│   ├── intelligence_analyzer.py # Quality analysis
│   └── Collection*/        # Test document collections
└── TESTING_FRAMEWORK.md    # Complete testing documentation
```

## 🌟 Key Features

### Challenge 1A: PDF Outline Extraction

- ✅ **100% Title Accuracy** - Perfect document title extraction
- 🧠 **ML-Enhanced Processing** - Uses SentenceTransformer and K-means clustering
- 📊 **Schema Compliance** - JSON output validation against provided schemas
- 🐳 **Docker Ready** - Complete containerization for deployment
- 🎯 **64.1% Combined Accuracy** with continuous improvement

### Challenge 1B: Multi-Collection Intelligence

- 📚 **Batch Processing** - Handles multiple document collections simultaneously
- 🔍 **Smart Section Detection** - Advanced heading and content extraction
- 📈 **Quality Scoring** - 9.26/10 average quality score across collections
- 📊 **31 Documents Processed** across 3 collections (461 pages, 1,281 sections)
- ✅ **100% Processing Success Rate**

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional)

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Adobe-India-Hackathon25-main
   ```

2. **Set up Python environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install PyMuPDF scikit-learn sentence-transformers numpy jsonschema PyPDF2
   ```

### Running the Solutions

#### Challenge 1A: PDF Outline Extraction

```bash
cd Challenge_1a

# Process PDFs with ML enhancement
python process_pdfs.py

# Check accuracy against expected results
python accuracy_check.py

# Run comprehensive tests
python test_suite.py
```

#### Challenge 1B: Multi-Collection Analysis

```bash
cd Challenge_1b

# Process all document collections
python examine_pdf.py

# Validate outputs
python collection_validator.py

# Generate intelligence analysis
python intelligence_analyzer.py
```

## 📊 Performance Results

### Challenge 1A Achievements

| Metric            | Result        | Status       |
| ----------------- | ------------- | ------------ |
| Title Accuracy    | 100% (5/5)    | ✅ Perfect   |
| Schema Compliance | 100%          | ✅ Perfect   |
| Test Suite        | 14/14 passing | ✅ Perfect   |
| Combined Accuracy | 64.1%         | 🔄 Improving |

### Challenge 1B Achievements

| Collection   | Documents | Pages   | Sections  | Success Rate |
| ------------ | --------- | ------- | --------- | ------------ |
| Collection 1 | 7         | 75      | 107       | 100%         |
| Collection 2 | 15        | 256     | 589       | 100%         |
| Collection 3 | 9         | 130     | 585       | 100%         |
| **Total**    | **31**    | **461** | **1,281** | **100%**     |

## 🔧 Technology Stack

### Core Technologies

- **Python** - Main development language
- **PyMuPDF/PyPDF2** - PDF processing libraries
- **SentenceTransformers** - AI/ML text embeddings
- **scikit-learn** - Machine learning algorithms
- **Docker** - Containerization

### ML/AI Components

- **Sentence Embeddings** - `paraphrase-MiniLM-L3-v2` model
- **K-means Clustering** - Font size analysis for heading detection
- **Confidence Scoring** - Multi-factor quality assessment
- **Text Normalization** - Advanced content cleaning

## 🧪 Testing Framework

Our comprehensive testing system includes:

- **Unit Tests** - Individual function validation
- **Integration Tests** - End-to-end processing validation
- **Accuracy Validation** - Performance against expected results
- **Schema Compliance** - JSON structure validation
- **Docker Testing** - Container functionality verification

### Run All Tests

```bash
# Challenge 1A tests
cd Challenge_1a
python test_suite.py

# Challenge 1B validation
cd ../Challenge_1b
python collection_validator.py
```

## 🐳 Docker Deployment

### Build and Run (Challenge 1A)

```bash
cd Challenge_1a
docker build -t pdf-processor .
docker run -v $(pwd)/sample_dataset:/sample_dataset pdf-processor
```

## 📈 Key Innovations

### 1. **ML-Enhanced Section Detection**

- Uses semantic embeddings to identify meaningful headings
- K-means clustering for font size analysis
- Multi-criteria heading detection (caps, titles, keywords, numbering)

### 2. **Robust Error Handling**

- Graceful degradation when individual files fail
- Comprehensive error reporting and logging
- Fallback mechanisms for different PDF libraries

### 3. **Intelligent Quality Assessment**

- 0-10 quality scoring system
- Content diversity analysis
- Processing success rate tracking
- Performance benchmarking

### 4. **Scalable Architecture**

- Docker containerization for deployment
- Batch processing capabilities
- Modular design for easy extension

## 🎯 Future Roadmap

### Round 2 Plans

- 🌐 **Web Application** - Build interactive reading webapp using Adobe PDF Embed API
- 🔗 **Idea Linking** - Connect related concepts across documents
- 💡 **Smart Insights** - Surface contextual information automatically
- 📱 **Responsive Design** - Modern, intuitive user interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is created for the Adobe India Hackathon 2025. Please refer to the hackathon terms and conditions.

## 👥 Team

**Developer**: PREMSAITEJA  
**Challenge**: Adobe India Hackathon 2025 - "Connecting the Dots"

---

## 🎯 Challenge Motto

> _"Rethink Reading. Rediscover Knowledge."_

Transform every PDF from a static document into an intelligent, interactive experience that understands, connects, and responds like a trusted research companion.

**Ready to connect the dots? Let's build the future of document intelligence! 🚀**
