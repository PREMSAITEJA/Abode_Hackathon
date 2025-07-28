# Adobe India Hackathon 2025 - Virtual Environment Setup

## ✅ Successfully Created Virtual Environments

Two separate virtual environments have been created with all required packages installed and ready to use.

### Challenge_1a Environment

**Location:** `Challenge_1a/venv/`
**Purpose:** PDF processing with advanced ML and NLP capabilities

**Key Packages Installed:**

- PyMuPDF (1.26.3) - PDF manipulation and text extraction
- sentence-transformers (5.0.0) - Advanced NLP for text processing
- torch (2.7.1) - Deep learning framework
- transformers (4.54.0) - Hugging Face transformers
- scikit-learn (1.7.1) - Machine learning algorithms
- numpy (2.3.2) - Numerical computing
- pandas (2.3.1) - Data manipulation
- jsonschema (4.25.0) - JSON schema validation
- pytest (8.4.1) - Testing framework

**Quick Start:**

1. Double-click `Challenge_1a/activate_env.bat` to activate the environment
2. Run the main script: `python process_pdfs.py`

### Challenge_1b Environment

**Location:** `Challenge_1b/venv/`
**Purpose:** Multi-collection PDF intelligence with dual library support

**Key Packages Installed:**

- PyPDF2 (3.0.1) - Primary PDF processing library
- PyMuPDF (1.26.3) - Fallback PDF processing
- scikit-learn (1.7.1) - Machine learning support
- pandas (2.3.1) - Data manipulation
- jsonschema (4.25.0) - Schema validation
- pytest (8.4.1) - Testing framework

**Quick Start:**

1. Double-click `Challenge_1b/activate_env.bat` to activate the environment
2. Work with the three collections:
   - Collection 1: Travel guides (South of France)
   - Collection 2: Acrobat tutorials (15 documents)
   - Collection 3: Recipe collection (9 documents)

## 🛠️ Manual Activation (Alternative)

If you prefer manual activation:

### For Challenge_1a:

```bash
cd "C:\Users\PREMSAITEJA\Downloads\Adobe-India-Hackathon25-main\Challenge_1a"
venv\Scripts\activate
```

### For Challenge_1b:

```bash
cd "C:\Users\PREMSAITEJA\Downloads\Adobe-India-Hackathon25-main\Challenge_1b"
venv\Scripts\activate
```

## 📦 Environment Isolation

Both environments are completely isolated:

- No package conflicts between challenges
- Each has its own Python interpreter and packages
- Independent dependency management
- Clean separation of concerns

## 🎯 Benefits

1. **Ready to Run:** No setup required - all dependencies pre-installed
2. **Isolated:** Each challenge has its own environment
3. **Complete:** All ML, NLP, and PDF processing libraries included
4. **User-Friendly:** Simple activation scripts provided
5. **Robust:** Flexible version ranges to avoid conflicts

## 🚀 Next Steps

1. Choose your challenge (1a or 1b)
2. Activate the corresponding environment
3. Start coding and experimenting!
4. Run tests with `pytest` when ready

Both environments are production-ready and include all necessary packages for smooth local development.
