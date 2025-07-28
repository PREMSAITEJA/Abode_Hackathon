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

> 📖 **New here? Check out `GETTING_STARTED.md` for the simplest possible setup guide!**

### Prerequisites

- Python 3.9+
- Docker (optional)

### ⚡ Super Easy Setup - Virtual Environments Ready!

**No manual installation needed!** We've pre-configured separate virtual environments for each challenge with all required packages.

#### Option 1: One-Click Activation (Recommended)

**For Challenge 1A:**

1. Double-click `Challenge_1a/activate_env.bat`
2. You're ready to go! All ML, NLP, and PDF packages pre-installed.

**For Challenge 1B:**

1. Double-click `Challenge_1b/activate_env.bat`
2. You're ready to go! All PDF processing packages pre-installed.

#### Option 2: Manual Activation

**For Challenge 1A:**

```bash
cd Challenge_1a
venv\Scripts\activate
```

**For Challenge 1B:**

```bash
cd Challenge_1b
venv\Scripts\activate
```

💡 **See `VIRTUAL_ENVIRONMENTS_SETUP.md` for detailed package lists and technical info.**

### Running the Solutions

#### Challenge 1A: PDF Outline Extraction

```bash
# 1. Activate the environment (if not already active)
cd Challenge_1a
# Double-click activate_env.bat OR run: venv\Scripts\activate

# 2. Process PDFs with ML enhancement
python process_pdfs.py

# 3. Check accuracy against expected results
python accuracy_check.py

# 4. Run comprehensive tests
python test_suite.py
```

#### Challenge 1B: Multi-Collection Analysis

```bash
# 1. Activate the environment (if not already active)
cd Challenge_1b
# Double-click activate_env.bat OR run: venv\Scripts\activate

# 2. Process all document collections
python examine_pdf.py

# 3. Validate outputs
python collection_validator.py

# 4. Generate intelligence analysis
python intelligence_analyzer.py
```

### 🔥 What Makes This Setup Special

- **Zero Setup Time**: Virtual environments pre-configured with all dependencies
- **Isolated Environments**: No package conflicts between challenges
- **Production-Ready**: All packages tested and compatible
- **User-Friendly**: One-click activation scripts
- **Complete Stack**: ML, NLP, PDF processing, testing - everything included

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

## 🛠️ Troubleshooting

### Environment Issues

If you encounter any issues:

1. **Environment not activating?**

   - Try manual activation: `venv\Scripts\activate`
   - Ensure you're in the correct challenge folder

2. **Import errors?**

   - Check that the virtual environment is activated
   - Look for `(venv)` in your command prompt
   - All packages are pre-installed, no additional installs needed

3. **Script errors?**

   - Ensure you're running from the correct directory
   - Check that input files exist in expected locations

4. **Need fresh start?**
   - Deactivate environment: `deactivate`
   - Re-activate using the steps above

### Getting Help

- Check `VIRTUAL_ENVIRONMENTS_SETUP.md` for detailed package info
- Verify your Python version: `python --version` (requires 3.9+)
- All environments are tested and ready - no setup should be needed!

## 📞 Support

For any issues or questions:

- Check the individual challenge READMEs for specific guidance
- Environment setup is fully automated - just activate and run!

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
