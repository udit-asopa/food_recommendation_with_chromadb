# Food Recommendation System with ChromaDB

🍽️ **Advanced food recommendation system** demonstrating three distinct approaches to similarity search and conversational AI using ChromaDB vector database and natural language processing.

## 🚀 Quick Start

```bash
# Setup environment
pixi install

# Run interactive search
pixi run python scripts/ex_interactive_search.py

# Run RAG chatbot
pixi run python scripts/enhanced_rag_chatbot.py
```

## 📋 Features

- **🔍 Interactive CLI Search** - Real-time food similarity search
- **🤖 RAG Chatbot** - AI-powered conversational recommendations  
- **📊 Advanced Filtering** - Cuisine, calories, ingredients matching
- **⚡ Vector Search** - ChromaDB-powered semantic similarity
- **🎯 Multiple Interfaces** - CLI, chatbot, and comparison modes

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Vector DB** | ChromaDB |
| **LLM** | Hugging Face FLAN-T5 |
| **Embeddings** | Sentence Transformers |
| **Framework** | Python + Transformers |
| **Package Manager** | Pixi |

## 📚 Documentation

| Topic | Location |
|-------|----------|
| **📖 Complete Guide** | [docs/README.md](docs/README.md) |
| **🏗️ Architecture** | [docs/architecture.md](docs/architecture.md) |
| **🎯 Use Cases** | [docs/use-cases.md](docs/use-cases.md) |
| **🔧 Implementation** | [docs/implementation.md](docs/implementation.md) |
| **📝 Exercise Scripts** | [scripts/exercise_scripts/README.md](scripts/exercise_scripts/README.md) |

## 🎯 Quick Examples

```bash
# Search for Italian food
"Italian pasta under 400 calories"

# Find healthy breakfast
"protein-rich breakfast options"

# Compare recommendations
"spicy dinner" vs "light meal"
```

## 📁 Project Structure

```
food_recommendation_with_chromadb/
├── scripts/           # Main application scripts
├── docs/             # Comprehensive documentation
├── data/             # Food dataset
└── pixi.toml         # Environment configuration
```

## 🤝 Contributing

See [docs/contributing.md](docs/contributing.md) for development guidelines.

## Data Source

```bash 

wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/sN1PIR8qp1SJ6K7syv72qQ/FoodDataSet.json

```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.