# Troubleshooting Guide

## 🛠️ **Common Issues & Solutions**

This guide covers the most frequently encountered problems when setting up and running the Food Recommendation System.

## 🚀 **Installation & Setup Issues**

### **❌ Problem: Pixi Installation Fails**

**Symptoms:**
```bash
bash: pixi: command not found
```

**Solution:**
```bash
# Install pixi using alternative methods:

# Method 1: Direct download
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc

# Method 2: Using conda/mamba
conda install -c conda-forge pixi

# Method 3: Using pip (fallback)
pip install pixi
```

### **❌ Problem: Python Version Incompatibility**

**Symptoms:**
```bash
ERROR: Python 3.9 is not supported. Requires Python 3.10+
```

**Solution:**
```bash
# Check Python version
python --version

# If < 3.10, install newer Python:
# Using pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Using conda
conda install python=3.11

# Verify installation
python --version  # Should show 3.10+
```

### **❌ Problem: Dependencies Installation Fails**

**Symptoms:**
```bash
ERROR: Could not find a version that satisfies the requirement transformers>=4.35.0
```

**Solution:**
```bash
# Clear package cache
pip cache purge
pixi clean

# Install with verbose output to identify issues
pixi install -v

# Alternative: Use conda-forge channel
pixi install -c conda-forge transformers sentence-transformers chromadb

# Fallback: Manual pip installation
pip install transformers>=4.35.0 sentence-transformers>=2.2.0 chromadb>=0.4.0
```

## 💾 **Data Loading Issues**

### **❌ Problem: FoodDataSet.json Not Found**

**Symptoms:**
```bash
FileNotFoundError: Food dataset file not found: ./data/FoodDataSet.json
```

**Solution:**
```bash
# Check if data directory exists
ls -la data/

# If missing, create data directory and download dataset
mkdir -p data

# If you have the dataset elsewhere, copy it:
cp /path/to/your/FoodDataSet.json data/

# Verify file exists and is readable
ls -la data/FoodDataSet.json
head data/FoodDataSet.json  # Check first few lines
```

### **❌ Problem: Invalid JSON in Dataset**

**Symptoms:**
```bash
json.JSONDecodeError: Expecting ',' delimiter: line 42 column 5
```

**Solution:**
```bash
# Validate JSON syntax
python -m json.tool data/FoodDataSet.json > /dev/null

# If invalid, fix common issues:
# 1. Missing commas between objects
# 2. Trailing commas at end of arrays/objects
# 3. Unescaped quotes in strings

# Use online JSON validator for complex issues
# Example fix for common trailing comma issue:
sed -i 's/,\s*}/}/g' data/FoodDataSet.json
sed -i 's/,\s*]/]/g' data/FoodDataSet.json
```

## 🤖 **Model Loading Issues**

### **❌ Problem: Sentence Transformer Model Download Fails**

**Symptoms:**
```bash
OSError: Can't load the tokenizer for 'all-MiniLM-L6-v2'
```

**Solution:**
```bash
# Check internet connection
ping huggingface.co

# Clear model cache and retry
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/sentence_transformers/

# Manual model download
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print('Model downloaded successfully')
"

# Alternative: Use different model
# In scripts, change model name to:
# 'sentence-transformers/all-MiniLM-L6-v2'
```

### **❌ Problem: FLAN-T5 Model Loading Fails**

**Symptoms:**
```bash
OSError: google/flan-t5-base does not appear to be a valid model identifier
```

**Solution:**
```bash
# Check available disk space (models are ~1GB)
df -h

# Clear transformers cache
rm -rf ~/.cache/huggingface/transformers/

# Manual download with error handling
python -c "
from transformers import pipeline
try:
    llm = pipeline('text2text-generation', 'google/flan-t5-base')
    print('FLAN-T5 loaded successfully')
except Exception as e:
    print(f'Error: {e}')
    print('Trying alternative model...')
    llm = pipeline('text2text-generation', 't5-small')
    print('T5-small loaded as fallback')
"
```

## 🔍 **ChromaDB Issues**

### **❌ Problem: ChromaDB Connection Failed**

**Symptoms:**
```bash
ConnectionError: Failed to create ChromaDB collection
```

**Solution:**
```bash
# Check if ChromaDB directory is writable
mkdir -p ./chroma_db
ls -la ./chroma_db

# Clear existing ChromaDB data if corrupted
rm -rf ./chroma_db/*

# Test ChromaDB installation
python -c "
import chromadb
client = chromadb.Client()
print('ChromaDB working correctly')
"

# If still failing, reinstall ChromaDB
pip uninstall chromadb
pip install chromadb>=0.4.0
```

### **❌ Problem: Collection Already Exists Error**

**Symptoms:**
```bash
ValueError: Collection 'food_recommendations' already exists
```

**Solution:**
```bash
# The code should handle this automatically, but if not:
python -c "
import chromadb
client = chromadb.Client()
try:
    client.delete_collection('food_recommendations')
    print('Existing collection deleted')
except:
    print('No existing collection found')
"
```

## 🖥️ **Runtime Issues**

### **❌ Problem: Search Returns No Results**

**Symptoms:**
```bash
❌ No matching foods found.
```

**Troubleshooting:**
```bash
# Check if collection is populated
python -c "
import sys, os
sys.path.append('scripts')
from shared_functions import *

# Load data and create collection
food_items = load_food_data('./data/FoodDataSet.json')
print(f'Loaded {len(food_items)} items')

collection = create_similarity_search_collection('test')
populate_similarity_collection(collection, food_items)

# Test search
results = perform_similarity_search(collection, 'pasta', 3)
print(f'Found {len(results)} results for pasta')
"

# If no results, try simpler queries:
# 'food', 'chicken', 'rice'
```

### **❌ Problem: Memory Usage Too High**

**Symptoms:**
```bash
MemoryError: Unable to allocate array
```

**Solution:**
```bash
# Monitor memory usage
htop  # or top on macOS

# Reduce model size by using smaller alternatives:
# In scripts, change to:
# model_name = "all-MiniLM-L6-v2"  # Instead of larger models
# model_id = "t5-small"            # Instead of flan-t5-base

# Process data in smaller batches
# Modify batch_size in embedding generation:
embeddings = embedder.encode(documents, batch_size=16)  # Default: 32
```

### **❌ Problem: Slow Performance**

**Symptoms:**
- Search takes > 5 seconds
- Model loading takes > 2 minutes

**Solution:**
```bash
# Use CPU optimization
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

# Enable model caching
mkdir -p ~/.cache/sentence_transformers/
mkdir -p ~/.cache/huggingface/

# Use smaller dataset for testing
head -50 data/FoodDataSet.json > data/test_data.json

# Profile performance
python -c "
import time
# Your search code here
start = time.time()
# ... search operation ...
print(f'Search took {time.time() - start:.2f} seconds')
"
```

## 🎯 **Type Checking Issues**

### **❌ Problem: MyPy Type Errors**

**Symptoms:**
```bash
error: Cannot find implementation or library stub for module "chromadb"
```

**Solution:**
```bash
# Install type stubs
pip install types-requests types-setuptools

# Create mypy.ini configuration
cat > mypy.ini << EOF
[mypy]
python_version = 3.10
ignore_missing_imports = True
warn_return_any = True
warn_unused_configs = True

[mypy-chromadb.*]
ignore_missing_imports = True

[mypy-sentence_transformers.*]
ignore_missing_imports = True
EOF

# Run mypy with configuration
mypy --config-file mypy.ini scripts/
```

## 🐛 **Debugging Tips**

### **Enable Debug Mode**
```python
# Add to script beginning for detailed output
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use print statements strategically
print(f"Debug: Loaded {len(food_items)} food items")
print(f"Debug: Query '{query}' generated {len(results)} results")
```

### **Test Components Individually**
```bash
# Test data loading only
python -c "from scripts.shared_functions import *; data = load_food_data('./data/FoodDataSet.json'); print(f'Success: {len(data)} items')"

# Test embedding generation only
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); print('Embedding model loaded')"

# Test ChromaDB only
python -c "import chromadb; client = chromadb.Client(); print('ChromaDB working')"
```

### **Check System Resources**
```bash
# Check available memory
free -h

# Check disk space
df -h

# Check Python environment
python -c "import sys; print('Python:', sys.version); print('Path:', sys.executable)"

# Check installed packages
pip list | grep -E "(transformers|chromadb|sentence-transformers)"
```

## 🆘 **Getting Help**

### **Before Asking for Help**
1. ✅ Check this troubleshooting guide
2. ✅ Search existing GitHub issues
3. ✅ Try running minimal test cases
4. ✅ Collect error messages and system info

### **Creating Effective Bug Reports**
Include:
- **Operating System**: `uname -a`
- **Python Version**: `python --version`
- **Package Versions**: `pip list`
- **Error Messages**: Full stack traces
- **Steps to Reproduce**: Minimal example
- **Expected vs Actual Behavior**

### **Where to Get Help**
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community help
- **Documentation**: Comprehensive guides and examples
- **Stack Overflow**: Tag questions with `chromadb`, `huggingface`, `food-recommendation`

## ✅ **Prevention Best Practices**

### **Environment Management**
```bash
# Always use virtual environments
python -m venv venv
source venv/bin/activate

# Keep dependencies up to date
pixi update

# Regular cleanup
pixi clean
pip cache purge
```

### **Data Backup**
```bash
# Backup important data
cp data/FoodDataSet.json data/FoodDataSet.json.backup

# Version control your configurations
git add pixi.toml .gitignore
git commit -m "Save working configuration"
```

### **Testing Before Deployment**
```bash
# Test core functionality
python scripts/ex_interactive_search.py
# Try basic searches: "pasta", "healthy", "spicy"

# Test error handling
python -c "from scripts.shared_functions import *; perform_similarity_search(None, 'test')"
```

Remember: Most issues are environment-related and can be solved by ensuring clean installations and proper dependencies! 🎯