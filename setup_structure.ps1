# SETUP SCRIPT - Run this to create your project structure
# Copy and paste these commands in PowerShell one by one

# Step 1: Create main directories
mkdir app
mkdir templates  
mkdir static
mkdir static\css
mkdir static\js
mkdir static\images
mkdir tests

# Step 2: Create empty Python files with TODO comments
New-Item app\__init__.py -ItemType File
New-Item app\config.py -ItemType File  
New-Item app\models.py -ItemType File
New-Item app\forms.py -ItemType File
New-Item app\routes.py -ItemType File
New-Item app\scraper.py -ItemType File
New-Item app\utils.py -ItemType File

# Step 3: Create empty template files
New-Item templates\base.html -ItemType File
New-Item templates\index.html -ItemType File
New-Item templates\results.html -ItemType File
New-Item templates\history.html -ItemType File

# Step 4: Create empty static files
New-Item static\css\style.css -ItemType File
New-Item static\js\main.js -ItemType File

# Step 5: Create other files
New-Item run.py -ItemType File
New-Item requirements.txt -ItemType File
New-Item README.md -ItemType File
New-Item .gitignore -ItemType File

# Step 6: Create test files
New-Item tests\__init__.py -ItemType File
New-Item tests\test_models.py -ItemType File
New-Item tests\test_routes.py -ItemType File

Write-Host "Project structure created! Now you can start coding."
Write-Host "Next: Create your virtual environment and install requirements."
