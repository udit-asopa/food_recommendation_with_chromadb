# API Documentation

## 📚 **Function Reference**

This document provides comprehensive API documentation for all public functions in the Food Recommendation System.

## 🗂️ **Module Overview**

### **Core Modules**
- [`shared_functions.py`](#shared_functions) - Core utilities for data loading, ChromaDB operations
- [`enhanced_rag_chatbot.py`](#enhanced_rag_chatbot) - RAG chatbot implementation
- [`ex_interactive_search.py`](#ex_interactive_search) - Interactive CLI search interface
- [`types.py`](#types) - Type definitions and data structures

---

## 📁 **shared_functions.py** {#shared_functions}

Core utility functions for data management and vector operations.

### **Data Loading**

#### `load_food_data(file_path: str) -> List[Dict[str, Any]]`

Load and validate food dataset from JSON file.

**Parameters:**
- `file_path` (str): Path to the JSON dataset file

**Returns:**
- `List[Dict[str, Any]]`: List of validated food item dictionaries

**Raises:**
- `FileNotFoundError`: If the specified file path does not exist
- `ValueError`: If JSON structure is invalid or missing required fields
- `PermissionError`: If file cannot be read due to permissions

**Example:**
```python
from shared_functions import load_food_data

food_items = load_food_data('./data/FoodDataSet.json')
print(f"Loaded {len(food_items)} food items")
# Output: Loaded 185 food items

# Access first item
first_item = food_items[0]
print(first_item['food_name'])  # "Chicken Tikka Masala"
```

**Required Fields in JSON:**
```json
{
  "food_name": "Chicken Tikka Masala",
  "cuisine_type": "Indian",
  "food_description": "Creamy tomato-based curry with tender chicken",
  "food_calories_per_serving": 450
}
```

### **ChromaDB Operations**

#### `create_similarity_search_collection(name: str, metadata: Optional[Dict] = None) -> chromadb.Collection`

Create a ChromaDB collection for similarity search.

**Parameters:**
- `name` (str): Unique name for the collection
- `metadata` (Optional[Dict]): Additional metadata for the collection

**Returns:**
- `chromadb.Collection`: ChromaDB collection object

**Raises:**
- `ValueError`: If collection name is invalid
- `ConnectionError`: If ChromaDB client initialization fails

**Example:**
```python
from shared_functions import create_similarity_search_collection

collection = create_similarity_search_collection(
    "food_search",
    {"description": "Food recommendation system", "version": "1.0"}
)
print(f"Created collection: {collection.name}")
```

#### `populate_similarity_collection(collection: chromadb.Collection, food_items: List[Dict[str, Any]]) -> None`

Populate ChromaDB collection with food data and embeddings.

**Parameters:**
- `collection` (chromadb.Collection): ChromaDB collection to populate
- `food_items` (List[Dict[str, Any]]): List of food item dictionaries

**Raises:**
- `ValueError`: If collection is None or food_items is empty
- `RuntimeError`: If embedding generation fails

**Example:**
```python
from shared_functions import populate_similarity_collection

food_items = load_food_data('./data/FoodDataSet.json')
populate_similarity_collection(collection, food_items)
# Output: Added 185 food items to collection
```

#### `perform_similarity_search(collection: chromadb.Collection, query: str, n_results: int = 5) -> List[Dict[str, Any]]`

Perform similarity search on ChromaDB collection.

**Parameters:**
- `collection` (chromadb.Collection): ChromaDB collection to search
- `query` (str): Natural language search query
- `n_results` (int): Maximum number of results to return (default: 5)

**Returns:**
- `List[Dict[str, Any]]`: List of similar food items with scores

**Example:**
```python
results = perform_similarity_search(collection, "spicy Italian pasta", 3)

for result in results:
    print(f"{result['food_name']}: {result['similarity_score']:.2f}")
# Output:
# Penne Arrabbiata: 0.89
# Spaghetti Puttanesca: 0.84
# Spicy Marinara Pasta: 0.81
```

**Result Structure:**
```python
{
    'food_name': str,              # Name of the food item
    'cuisine_type': str,           # Type of cuisine
    'food_description': str,       # Description of the food
    'food_calories_per_serving': int,  # Calories per serving
    'similarity_score': float,     # Similarity score (0.0 to 1.0)
    'food_ingredients': str,       # Ingredients list
    'food_health_benefits': str,   # Health benefits
    'cooking_method': str,         # Cooking method
    'taste_profile': str          # Flavor characteristics
}
```

### **Utility Functions**

#### `get_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer`

Get or create singleton embedding model instance.

**Parameters:**
- `model_name` (str): Name of the SentenceTransformer model

**Returns:**
- `SentenceTransformer`: Configured embedding model instance

**Example:**
```python
embedder = get_embedding_model()
embeddings = embedder.encode(["pasta", "pizza"])
print(f"Generated {len(embeddings)} embeddings")
```

#### `validate_collection_health(collection: chromadb.Collection) -> Dict[str, Any]`

Validate the health and status of a ChromaDB collection.

**Parameters:**
- `collection` (chromadb.Collection): ChromaDB collection to validate

**Returns:**
- `Dict[str, Any]`: Health report with status and metrics

**Example:**
```python
health = validate_collection_health(collection)
if health['is_healthy']:
    print(f"Collection is healthy with {health['item_count']} items")
else:
    print(f"Issues found: {health['issues']}")
```

---

## 🤖 **enhanced_rag_chatbot.py** {#enhanced_rag_chatbot}

RAG-powered conversational interface for food recommendations.

### **Text Generation**

#### `generate_text(prompt: str) -> str`

Generate text using the FLAN-T5 model.

**Parameters:**
- `prompt` (str): Input text prompt for generation

**Returns:**
- `str`: Generated text response

**Example:**
```python
prompt = "Recommend a healthy breakfast with high protein"
response = generate_text(prompt)
print(response)
# Output: "Try Greek yogurt with berries and granola for a protein-rich start to your day."
```

### **RAG Functions**

#### `generate_llm_rag_response(query: str, search_results: List[Dict[str, Any]]) -> str`

Generate natural language food recommendations using RAG.

**Parameters:**
- `query` (str): User's original query
- `search_results` (List[Dict[str, Any]]): List of similar food items from vector search

**Returns:**
- `str`: Natural language recommendation response

**Example:**
```python
query = "healthy Italian pasta"
results = perform_similarity_search(collection, query, 3)
response = generate_llm_rag_response(query, results)
print(response)
# Output: "For healthy Italian pasta, I recommend Pasta Primavera with its fresh vegetables and light olive oil dressing..."
```

#### `generate_llm_comparison(query1: str, query2: str, results1: List[Dict[str, Any]], results2: List[Dict[str, Any]]) -> str`

Generate AI-powered comparison between two food queries.

**Parameters:**
- `query1` (str): First query
- `query2` (str): Second query
- `results1` (List[Dict[str, Any]]): Results for first query
- `results2` (List[Dict[str, Any]]): Results for second query

**Returns:**
- `str`: Comparison analysis

### **Interface Functions**

#### `enhanced_rag_food_chatbot(collection: chromadb.Collection) -> None`

Start the enhanced RAG chatbot interface.

**Parameters:**
- `collection` (chromadb.Collection): Populated ChromaDB collection

**Usage:**
```python
collection = create_similarity_search_collection("foods")
populate_similarity_collection(collection, food_items)
enhanced_rag_food_chatbot(collection)
```

#### `handle_enhanced_rag_query(collection: chromadb.Collection, query: str, conversation_history: List[str]) -> None`

Process user query with RAG approach.

**Parameters:**
- `collection` (chromadb.Collection): ChromaDB collection to search
- `query` (str): User query string
- `conversation_history` (List[str]): Previous conversation context

---

## 🔍 **ex_interactive_search.py** {#ex_interactive_search}

Interactive CLI interface for food similarity search.

### **Main Interface**

#### `interactive_food_chatbot(collection: chromadb.Collection) -> None`

Start interactive CLI chatbot for food recommendations.

**Parameters:**
- `collection` (chromadb.Collection): ChromaDB collection for search

**Commands:**
- `help` - Show help menu
- `history` - Show search history
- `quit` - Exit the system

#### `search_food(collection: chromadb.Collection, query: str) -> None`

Handle food similarity search with enhanced display.

**Parameters:**
- `collection` (chromadb.Collection): ChromaDB collection to search
- `query` (str): Search query string

### **Utility Functions**

#### `show_help_menu() -> None`

Display help information for users.

#### `suggest_related_searches(results: List[Dict[str, Any]]) -> None`

Suggest related searches based on current results.

**Parameters:**
- `results` (List[Dict[str, Any]]): Current search results

---

## 🏷️ **types.py** {#types}

Type definitions and data structures.

### **Type Aliases**
```python
FoodDataset = List[FoodItemDict]
SearchResults = List[SearchResultDict]
EmbeddingVector = List[float]
QueryText = str
ResponseText = str
```

### **TypedDict Definitions**

#### `FoodItemDict`
```python
class FoodItemDict(TypedDict, total=False):
    food_name: str
    cuisine_type: str
    food_description: str
    food_calories_per_serving: int
    food_ingredients: Union[List[str], str]
    food_health_benefits: str
    cooking_method: str
    taste_profile: str
```

#### `SearchResultDict`
```python
class SearchResultDict(TypedDict):
    food_name: str
    cuisine_type: str
    food_description: str
    food_calories_per_serving: int
    similarity_score: float
    food_ingredients: str
    food_health_benefits: str
    cooking_method: str
    taste_profile: str
```

### **Data Classes**

#### `FoodItem`
```python
@dataclass
class FoodItem:
    name: str
    cuisine: CuisineType
    description: str
    calories: int
    ingredients: List[str]
    health_benefits: str = ""
    cooking_method: str = ""
    taste_profile: str = ""
```

### **Enums**

#### `CuisineType`
```python
class CuisineType(Enum):
    ITALIAN = "Italian"
    CHINESE = "Chinese"
    INDIAN = "Indian"
    # ... more cuisine types
```

### **Validation Functions**

#### `validate_food_item(item: Dict[str, Any]) -> bool`

Validate if dictionary represents a valid food item.

#### `validate_search_result(result: Dict[str, Any]) -> bool`

Validate if dictionary represents a valid search result.

#### `validate_system_config(config: Dict[str, Any]) -> bool`

Validate system configuration parameters.

---

## 📊 **Constants & Configuration**

### **Default Values**
```python
DEFAULT_MAX_RESULTS: int = 5
DEFAULT_SIMILARITY_THRESHOLD: float = 0.3
DEFAULT_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
DEFAULT_LLM_MODEL: str = "google/flan-t5-base"
```

### **Limits**
```python
MAX_QUERY_LENGTH: int = 500
MAX_RESULTS_LIMIT: int = 50
MAX_CONVERSATION_HISTORY: int = 10
MAX_EMBEDDING_BATCH_SIZE: int = 100
```

### **File Paths**
```python
DEFAULT_DATA_PATH: str = "./data/FoodDataSet.json"
DEFAULT_MODELS_PATH: str = "./models/"
DEFAULT_CACHE_PATH: str = "./cache/"
```

---

## 🔧 **Usage Examples**

### **Complete Workflow Example**
```python
from shared_functions import *

# 1. Load data
food_items = load_food_data('./data/FoodDataSet.json')
print(f"Loaded {len(food_items)} food items")

# 2. Create collection
collection = create_similarity_search_collection("food_search")

# 3. Populate collection
populate_similarity_collection(collection, food_items)

# 4. Perform search
results = perform_similarity_search(collection, "healthy breakfast", 5)

# 5. Display results
for i, result in enumerate(results, 1):
    print(f"{i}. {result['food_name']} ({result['similarity_score']:.2f})")
```

### **RAG Chatbot Example**
```python
from enhanced_rag_chatbot import *

# Setup
food_items = load_food_data('./data/FoodDataSet.json')
collection = create_similarity_search_collection("rag_foods")
populate_similarity_collection(collection, food_items)

# Start chatbot
enhanced_rag_food_chatbot(collection)
```

### **Interactive Search Example**
```python
from ex_interactive_search import *

# Setup and start
main()  # This handles everything: loading, setup, and interaction
```

---

## 🏆 **Best Practices**

### **Error Handling**
```python
try:
    results = perform_similarity_search(collection, query)
except Exception as e:
    print(f"Search failed: {e}")
    results = []
```

### **Performance Optimization**
```python
# Cache embedding model
embedder = get_embedding_model()  # Reuse across calls

# Limit results for performance
results = perform_similarity_search(collection, query, n_results=3)
```

### **Type Safety**
```python
from typing import List, Dict, Any
from types import FoodItemDict, SearchResultDict

def process_results(results: List[SearchResultDict]) -> None:
    for result in results:
        # Type-safe access
        name: str = result['food_name']
        score: float = result['similarity_score']
```

This API documentation provides complete reference for all public functions and their usage patterns in the Food Recommendation System.