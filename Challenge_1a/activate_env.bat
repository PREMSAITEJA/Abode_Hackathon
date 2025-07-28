@echo off
echo Activating Challenge_1a virtual environment...
cd /d "C:\Users\PREMSAITEJA\Downloads\Adobe-India-Hackathon25-main\Challenge_1a"
call venv\Scripts\activate.bat
echo.
echo Challenge_1a environment activated!
echo Available packages for PDF processing and ML:
echo - PyMuPDF (PDF processing)
echo - sentence-transformers (NLP)
echo - torch (Deep Learning)
echo - scikit-learn (Machine Learning)
echo - pandas (Data manipulation)
echo - jsonschema (Schema validation)
echo - pytest (Testing)
echo.
echo To run the challenge: python process_pdfs.py
echo To deactivate: deactivate
cmd /k
