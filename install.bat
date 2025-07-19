@echo off
echo Installing Hegelian-AI-Framework...

echo.
echo 1. Installing minimal dependencies...
pip install -r requirements-minimal.txt

echo.
echo 2. Creating required directories...
mkdir logs 2>nul
mkdir models 2>nul
mkdir data\ethical_cases 2>nul
mkdir data\knowledge_graphs 2>nul  
mkdir data\training_data 2>nul

echo.
echo 3. Testing basic configuration...
python -c "from backend.config import Settings; s = Settings(); print('✓ Configuration loaded successfully')"

echo.
echo 4. Testing FastAPI app...
python -c "import sys; sys.path.append('.'); from backend.main import app; print('✓ FastAPI app created successfully')"

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python backend/main.py
echo.
echo To install optional dependencies:
echo   pip install -r requirements-optional.txt
echo.
echo Access the API at: http://localhost:8000
echo API documentation: http://localhost:8000/docs