@echo off
echo Activating Challenge_1b virtual environment...
cd /d "C:\Users\PREMSAITEJA\Downloads\Adobe-India-Hackathon25-main\Challenge_1b"
call venv\Scripts\activate.bat
echo.
echo Challenge_1b environment activated!
echo Available packages for PDF processing:
echo - PyPDF2 (Primary PDF processing)
echo - PyMuPDF (Fallback PDF processing)
echo - scikit-learn (Machine Learning)
echo - pandas (Data manipulation)
echo - jsonschema (Schema validation)
echo - pytest (Testing)
echo.
echo Collections available:
echo - Collection 1 (Travel guides)
echo - Collection 2 (Acrobat tutorials)
echo - Collection 3 (Recipe collection)
echo.
echo To deactivate: deactivate
cmd /k
