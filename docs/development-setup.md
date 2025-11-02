# Development Setup Guide

## 🛠️ Prerequisites

### **System Requirements**
- **OS**: Linux, macOS, or Windows 10/11
- **Python**: 3.10 or higher (3.11+ recommended)
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 5GB free space for models and data
- **Network**: Internet connection for initial model downloads

### **Required Tools**
```bash
# 1. Python 3.10+
python --version  # Should be 3.10 or higher

# 2. Git
git --version

# 3. Pixi Package Manager (recommended)
curl -fsSL https://pixi.sh/install.sh | bash
# or
curl -fsSL https://pixi.sh/install.sh | bash

# Alternative: Use conda/pip if pixi unavailable
```

## 🚀 Quick Setup

### **Option 1: Pixi (Recommended)**

```bash
# 1. Clone repository
git clone https://github.com/your-username/food_recommendation_with_chromadb.git
cd food_recommendation_with_chromadb

# 2. Install dependencies with pixi
pixi install

# 3. Activate environment
pixi shell

# 4. Verify installation
python scripts/enhanced_rag_chatbot.py
```

### **Option 2: Traditional Python + Pip**

```bash
# 1. Clone repository
git clone https://github.com/your-username/food_recommendation_with_chromadb.git
cd food_recommendation_with_chromadb

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install transformers torch sentence-transformers chromadb
pip install numpy pandas click rich typer

# 4. Install development tools
pip install pytest ruff black mypy

# 5. Verify installation
python scripts/enhanced_rag_chatbot.py
```

## 📦 Dependency Management

### **Core Dependencies**

| Package | Version | Purpose |
|---------|---------|---------|
| `transformers` | >=4.35.0 | Hugging Face model integration |
| `torch` | >=2.0.0 | PyTorch backend for models |
| `sentence-transformers` | >=2.2.0 | Text embedding generation |
| `chromadb` | >=0.4.0 | Vector database for similarity search |
| `numpy` | >=1.24.0 | Numerical computations |
| `pandas` | >=2.0.0 | Data manipulation |

### **Development Dependencies**

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `ruff` | Fast Python linter |
| `black` | Code formatter |
| `mypy` | Type checking |
| `pre-commit` | Git hooks for quality |

### **Optional Dependencies**

```bash
# Performance optimization
pixi add accelerate  # Faster model loading
pixi add optimum     # Model optimization

# Additional CLI features  
pixi add rich        # Beautiful terminal output
pixi add typer       # Modern CLI framework

# Jupyter notebook support
pixi add jupyter     # Interactive development
pixi add matplotlib  # Data visualization
```

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file in the project root:

```bash
# .env file
# Model configuration
DEFAULT_EMBEDDING_MODEL=all-MiniLM-L6-v2
DEFAULT_LLM_MODEL=google/flan-t5-base

# Performance settings
MAX_SEARCH_RESULTS=10
LLM_MAX_LENGTH=400
EMBEDDING_BATCH_SIZE=32

# Development settings
DEBUG_MODE=true
LOG_LEVEL=INFO
```

### **Pixi Configuration**

The `pixi.toml` file contains project configuration:

```toml
[project]
name = "food-recommendation-system"
version = "1.0.0"
description = "AI-powered food recommendation system"
authors = ["Your Name <email@example.com>"]
channels = ["conda-forge", "pytorch"]
platforms = ["linux-64", "osx-64", "win-64"]

[dependencies]
python = ">=3.10,<3.13"
pytorch = ">=2.0.0"
transformers = ">=4.35.0"
sentence-transformers = ">=2.2.0"
chromadb = ">=0.4.0"
numpy = ">=1.24.0"
pandas = ">=2.0.0"
click = ">=8.0.0"

[tasks]
# Development tasks
test = "pytest tests/ -v"
lint = "ruff check ."
format = "black ."
type-check = "mypy scripts/"

# Application tasks
interactive-search = "python scripts/exercise_scripts/ex_interactive_search.py"
rag-chatbot = "python scripts/enhanced_rag_chatbot.py"

# Setup tasks
download-models = "python scripts/download_models.py"
setup-data = "python scripts/setup_data.py"
```

## 🎯 Development Workflow

### **Daily Development Cycle**

```bash
# 1. Start development session
pixi shell
cd food_recommendation_with_chromadb

# 2. Pull latest changes
git pull origin main

# 3. Create feature branch
git checkout -b feature/your-feature

# 4. Make changes and test frequently
pixi run test              # Run tests
pixi run lint              # Check code quality
pixi run format            # Format code

# 5. Commit when ready
git add .
git commit -m "feat: describe your changes"

# 6. Push and create PR
git push origin feature/your-feature
```

### **Quality Assurance Workflow**

```bash
# Pre-commit checks (run before every commit)
pixi run format            # Auto-format code
pixi run lint              # Check linting errors
pixi run type-check        # Verify type annotations
pixi run test              # Run all tests

# Optional: Set up pre-commit hooks
pre-commit install
# Now these run automatically on git commit
```

## 🧪 Testing Setup

### **Test Environment Configuration**

```bash
# Create test data directory
mkdir -p tests/data

# Download test dataset (smaller version)
curl -o tests/data/test_food_data.json \
  https://example.com/test_dataset.json

# Set up test ChromaDB
export CHROMADB_TEST_PATH="./tests/chromadb_test"
```

### **Running Different Test Types**

```bash
# Unit tests (fast, no external dependencies)
pixi run pytest tests/unit/ -v

# Integration tests (slower, real ChromaDB)
pixi run pytest tests/integration/ -v

# End-to-end tests (full system)
pixi run pytest tests/e2e/ -v

# Performance tests
pixi run pytest tests/performance/ -v --benchmark

# Coverage report
pixi run pytest --cov=scripts --cov-report=html
open htmlcov/index.html  # View coverage report
```

## 🐛 Debugging Setup

### **IDE Configuration**

#### **VS Code Settings**

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": ".pixi/envs/default/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.associations": {
        "pixi.toml": "toml"
    }
}
```

#### **PyCharm Configuration**

1. Open project in PyCharm
2. Go to File → Settings → Project → Python Interpreter  
3. Add interpreter → Existing environment
4. Point to `.pixi/envs/default/bin/python`
5. Configure test runner to use pytest

### **Debugging Tools**

```python
# Enhanced debugging with rich
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

def debug_search_results(results):
    """Pretty print search results for debugging."""
    table = Table(title="Search Results")
    table.add_column("Food Name", style="cyan")
    table.add_column("Cuisine", style="magenta")  
    table.add_column("Score", style="green")
    
    for result in results:
        table.add_row(
            result['food_name'],
            result['cuisine_type'],
            f"{result['similarity_score']:.3f}"
        )
    
    console.print(table)

# Usage in code
results = perform_similarity_search(collection, query)
debug_search_results(results)  # Beautiful table output
```

## 📊 Performance Monitoring

### **Profiling Tools**

```bash
# Install profiling tools
pixi add line_profiler memory_profiler

# Profile memory usage
python -m memory_profiler scripts/enhanced_rag_chatbot.py

# Profile function execution time
kernprof -l -v scripts/shared_functions.py
```

### **Performance Benchmarks**

```python
# benchmark_search.py
import time
from scripts.shared_functions import perform_similarity_search

def benchmark_search_performance():
    """Benchmark search performance across different query types."""
    queries = [
        "Italian pasta",
        "healthy breakfast options", 
        "spicy comfort food",
        "low calorie vegetarian"
    ]
    
    results = {}
    for query in queries:
        start_time = time.time()
        search_results = perform_similarity_search(collection, query)
        end_time = time.time()
        
        results[query] = {
            'duration': end_time - start_time,
            'result_count': len(search_results),
            'avg_score': sum(r['similarity_score'] for r in search_results) / len(search_results)
        }
    
    return results

# Run benchmarks
pixi run python benchmark_search.py
```

## 🚀 Deployment Preparation

### **Production Environment**

```bash
# Create production-ready build
pixi run build-prod

# Install production dependencies only
pixi install --production

# Create Docker image (optional)
docker build -t food-recommendation-system .

# Test production configuration
pixi run test-prod
```

### **Model Optimization**

```python
# scripts/optimize_models.py
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

def optimize_models_for_production():
    """Optimize models for faster inference."""
    # Convert FLAN-T5 to ONNX for faster CPU inference
    model = ORTModelForSequenceClassification.from_pretrained(
        "google/flan-t5-base",
        from_transformers=True
    )
    model.save_pretrained("./models/optimized/flan-t5-base-onnx")
    
    # Quantize embedding model
    # Implementation depends on specific requirements
    
# Run optimization
pixi run python scripts/optimize_models.py
```

## ✅ Verification Checklist

### **Installation Verification**

- [ ] **Python Version**: 3.10+ installed and accessible
- [ ] **Pixi/Dependencies**: All packages installed without errors
- [ ] **Models Download**: Embedding and LLM models downloaded successfully
- [ ] **Data Access**: Food dataset loaded correctly
- [ ] **ChromaDB**: Vector database operational
- [ ] **Tests**: All tests pass
- [ ] **CLI Interface**: Interactive search works
- [ ] **RAG Chatbot**: Conversational interface functional

### **Development Readiness**

- [ ] **Code Editor**: Properly configured with Python interpreter
- [ ] **Git Setup**: Repository cloned and accessible
- [ ] **Testing**: Can run and create new tests
- [ ] **Linting**: Code quality tools working
- [ ] **Debugging**: Can set breakpoints and debug code
- [ ] **Documentation**: Can build and view docs locally

## 🆘 Troubleshooting

### **Common Issues**

#### **Model Download Failures**

```bash
# Manual model download
python -c "
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Download embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')
print('✅ Embedding model downloaded')

# Download LLM
llm = pipeline('text2text-generation', 'google/flan-t5-base')
print('✅ LLM downloaded')
"
```

#### **ChromaDB Issues**

```bash
# Reset ChromaDB
rm -rf ./chroma_db/  # Remove existing database
python -c "
import chromadb
client = chromadb.Client()
print('✅ ChromaDB working')
"
```

#### **Memory Issues**

```python
# Reduce memory usage
import torch
torch.set_num_threads(1)  # Reduce CPU usage

# Use smaller models
model_name = "all-MiniLM-L6-v2"  # Instead of larger models
```

### **Getting Help**

- **Documentation**: Check [docs/](../docs/) for detailed guides
- **Issues**: Create GitHub issue with error details
- **Discussions**: Use GitHub Discussions for questions
- **Community**: Join our Discord/Slack for real-time help

Your development environment is now ready! 🎉 Start with the [Contributing Guidelines](contributing.md) to understand the development workflow.