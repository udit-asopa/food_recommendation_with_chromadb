# Implementation Guide

## 🚀 Step-by-Step Implementation

### Phase 1: Environment Setup

#### **1.1 Project Initialization**
```bash
# Clone or create project directory
mkdir food_recommendation_with_chromadb
cd food_recommendation_with_chromadb

# Initialize pixi environment
pixi init
```

#### **1.2 Dependencies Installation**
```bash
# Core ML dependencies
pixi add transformers pytorch sentence-transformers chromadb

# Utility packages  
pixi add numpy pandas click rich typer

# Development tools
pixi add pytest ruff black
```

#### **1.3 Project Structure Setup**
```bash
# Create directory structure
mkdir -p {scripts,docs,data,tests}
mkdir -p scripts/exercise_scripts
mkdir -p tests/{unit,integration,e2e}
```

### Phase 2: Data Layer Implementation

#### **2.1 Food Dataset Preparation**
```python
# data_loader.py
import json
from typing import List, Dict, Any

def load_food_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load food dataset from JSON file.
    
    Args:
        file_path: Path to the JSON dataset file
        
    Returns:
        List of food item dictionaries
        
    Raises:
        FileNotFoundError: If dataset file doesn't exist
        JSONDecodeError: If file contains invalid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in dataset file: {e}")

def validate_food_data(food_items: List[Dict]) -> List[Dict]:
    """
    Validate and clean food dataset.
    
    Args:
        food_items: Raw food data from JSON
        
    Returns:
        Validated and cleaned food data
    """
    required_fields = ['food_name', 'cuisine_type', 'food_description']
    validated_items = []
    
    for item in food_items:
        # Check required fields
        if all(field in item for field in required_fields):
            # Clean and standardize data
            cleaned_item = {
                'food_name': str(item['food_name']).strip(),
                'cuisine_type': str(item['cuisine_type']).strip(),
                'food_description': str(item['food_description']).strip(),
                'food_calories_per_serving': int(item.get('food_calories_per_serving', 0)),
                'food_ingredients': item.get('food_ingredients', []),
                'food_health_benefits': item.get('food_health_benefits', ''),
                'cooking_method': item.get('cooking_method', ''),
                'taste_profile': item.get('taste_profile', '')
            }
            validated_items.append(cleaned_item)
    
    return validated_items
```

### Phase 3: Vector Search Implementation

#### **3.1 ChromaDB Integration**
```python
# vector_search.py
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional

class VectorSearchEngine:
    """
    Handles vector-based similarity search using ChromaDB.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector search engine.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.client = chromadb.Client()
        self.embedder = SentenceTransformer(model_name)
        self.collections = {}
    
    def create_collection(self, name: str, metadata: Optional[Dict] = None) -> chromadb.Collection:
        """
        Create a new ChromaDB collection.
        
        Args:
            name: Collection name
            metadata: Optional metadata for the collection
            
        Returns:
            ChromaDB collection object
        """
        try:
            # Delete existing collection if it exists
            self.client.delete_collection(name=name)
        except ValueError:
            pass  # Collection doesn't exist
        
        collection = self.client.create_collection(
            name=name,
            metadata=metadata or {}
        )
        self.collections[name] = collection
        return collection
    
    def populate_collection(self, collection: chromadb.Collection, food_items: List[Dict]):
        """
        Populate collection with food data and embeddings.
        
        Args:
            collection: ChromaDB collection to populate
            food_items: List of food item dictionaries
        """
        documents = []
        metadatas = []
        ids = []
        
        for i, item in enumerate(food_items):
            # Create searchable text
            searchable_text = self._create_searchable_text(item)
            documents.append(searchable_text)
            
            # Prepare metadata
            metadata = {
                'food_name': item['food_name'],
                'cuisine_type': item['cuisine_type'],
                'calories': item['food_calories_per_serving'],
                'ingredients': str(item.get('food_ingredients', [])),
                'health_benefits': item.get('food_health_benefits', ''),
                'cooking_method': item.get('cooking_method', ''),
                'taste_profile': item.get('taste_profile', '')
            }
            metadatas.append(metadata)
            ids.append(f"food_{i}")
        
        # Generate embeddings
        embeddings = self.embedder.encode(documents).tolist()
        
        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )
    
    def search_similar(self, collection: chromadb.Collection, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for similar food items.
        
        Args:
            collection: ChromaDB collection to search
            query: Search query string
            n_results: Number of results to return
            
        Returns:
            List of similar food items with scores
        """
        # Generate query embedding
        query_embedding = self.embedder.encode([query]).tolist()
        
        # Search in collection
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            result = {
                'food_name': results['metadatas'][0][i]['food_name'],
                'cuisine_type': results['metadatas'][0][i]['cuisine_type'],
                'food_description': results['documents'][0][i],
                'food_calories_per_serving': results['metadatas'][0][i]['calories'],
                'similarity_score': 1 - results['distances'][0][i],  # Convert distance to similarity
                'ingredients': results['metadatas'][0][i]['ingredients'],
                'health_benefits': results['metadatas'][0][i]['health_benefits'],
                'cooking_method': results['metadatas'][0][i]['cooking_method'],
                'taste_profile': results['metadatas'][0][i]['taste_profile']
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def _create_searchable_text(self, item: Dict) -> str:
        """
        Create searchable text representation of food item.
        
        Args:
            item: Food item dictionary
            
        Returns:
            Concatenated searchable text
        """
        parts = [
            item['food_name'],
            item['cuisine_type'],
            item['food_description']
        ]
        
        # Add optional fields if available
        if item.get('food_ingredients'):
            if isinstance(item['food_ingredients'], list):
                parts.append(' '.join(item['food_ingredients']))
            else:
                parts.append(str(item['food_ingredients']))
        
        if item.get('taste_profile'):
            parts.append(item['taste_profile'])
        
        if item.get('cooking_method'):
            parts.append(item['cooking_method'])
        
        return ' '.join(parts)
```

### Phase 4: LLM Integration

#### **4.1 Text Generation Setup**
```python
# llm_integration.py
from transformers import pipeline
from typing import List, Dict, Any

class LLMResponseGenerator:
    """
    Handles natural language response generation using Hugging Face models.
    """
    
    def __init__(self, model_name: str = "google/flan-t5-base"):
        """
        Initialize the LLM response generator.
        
        Args:
            model_name: Hugging Face model name
        """
        self.model_name = model_name
        self.generator = pipeline(
            "text2text-generation",
            model=model_name,
            device="cpu",
            model_kwargs={"low_cpu_mem_usage": True}
        )
        self.generation_params = {
            "max_length": 400,
            "temperature": 0.7,
            "do_sample": True,
            "top_p": 0.9
        }
    
    def generate_food_recommendation(self, query: str, search_results: List[Dict]) -> str:
        """
        Generate natural language food recommendations.
        
        Args:
            query: User's original query
            search_results: List of similar food items from vector search
            
        Returns:
            Natural language recommendation response
        """
        if not search_results:
            return self._generate_no_results_response(query)
        
        # Build context from search results
        context = self._build_context(search_results)
        
        # Create prompt
        prompt = f"""Based on the user's food query and available options, provide a helpful recommendation.

User asked: {query}

Available foods: {context}

Provide a friendly recommendation that mentions 2-3 specific foods and explains why they match:"""

        try:
            # Generate response
            response = self.generator(prompt, **self.generation_params)
            
            if isinstance(response, list) and len(response) > 0:
                generated_text = response[0].get('generated_text', '').strip()
                
                if len(generated_text) > 30:
                    return generated_text
            
            # Fallback to template response
            return self._generate_template_response(query, search_results)
            
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._generate_template_response(query, search_results)
    
    def generate_comparison(self, query1: str, query2: str, results1: List[Dict], results2: List[Dict]) -> str:
        """
        Generate comparison between two food queries.
        
        Args:
            query1: First query
            query2: Second query  
            results1: Results for first query
            results2: Results for second query
            
        Returns:
            Comparison analysis
        """
        if not results1 and not results2:
            return "No results found for either query."
        
        if not results1:
            return f"Found results for '{query2}' but none for '{query1}'."
        
        if not results2:
            return f"Found results for '{query1}' but none for '{query2}'."
        
        # Build comparison prompt
        food1 = results1[0]['food_name']
        food2 = results2[0]['food_name']
        
        prompt = f"Compare: '{query1}' (best match: {food1}) vs '{query2}' (best match: {food2}). Which is better and why?"
        
        try:
            response = self.generator(prompt, **self.generation_params)
            
            if isinstance(response, list) and len(response) > 0:
                generated_text = response[0].get('generated_text', '').strip()
                
                if len(generated_text) > 30:
                    return generated_text
            
            return f"For '{query1}', I recommend {food1}. For '{query2}', {food2} would be perfect."
            
        except Exception as e:
            return f"For '{query1}', I recommend {food1}. For '{query2}', {food2} would be perfect."
    
    def _build_context(self, search_results: List[Dict]) -> str:
        """Build context string from search results."""
        foods = []
        for result in search_results[:3]:
            food_info = f"{result['food_name']} ({result['cuisine_type']}, {result['food_calories_per_serving']} cal)"
            foods.append(food_info)
        return ", ".join(foods)
    
    def _generate_template_response(self, query: str, search_results: List[Dict]) -> str:
        """Generate template-based fallback response."""
        top_result = search_results[0]
        return f"Based on your request for '{query}', I recommend {top_result['food_name']}, a {top_result['cuisine_type']} dish with {top_result['food_calories_per_serving']} calories per serving."
    
    def _generate_no_results_response(self, query: str) -> str:
        """Generate response when no results found."""
        return f"I couldn't find any food items matching '{query}'. Try describing what you're in the mood for with different words!"
```

### Phase 5: CLI Interface Implementation

#### **5.1 Interactive Search Interface**
```python
# Example implementation pattern for interactive search
# Based on scripts/exercise_scripts/ex_interactive_search.py

def interactive_food_chatbot(collection: chromadb.Collection) -> None:
    """Interactive CLI chatbot for food recommendations."""
    search_history = []
    
    while True:
        try:
            user_input = input("\n🔍 Search: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'help':
                show_help_menu()
            else:
                search_food(collection, user_input)
                search_history.append(user_input)
    
def search_food(collection: chromadb.Collection, query: str) -> None:
    """Handle food similarity search with enhanced display."""
    results = perform_similarity_search(collection, query, 5)
    
    if not results:
        print("❌ No matching foods found.")
        return
    
    print(f"\n✅ Found {len(results)} recommendations:")
    for i, result in enumerate(results, 1):
        score = result['similarity_score'] * 100
        print(f"{i}. 🍽️ {result['food_name']}")
        print(f"   📊 Match: {score:.1f}% | 🏷️ {result['cuisine_type']}")
    
    def start_interactive_session(self):
        """Start the interactive CLI session."""
        self._show_welcome()
        
        while True:
            try:
                user_input = input("\n🔍 Search: ").strip()
                
                if not user_input:
                    print("Please enter a search term or 'help' for commands")
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using the Food Recommendation System!")
                    break
                elif user_input.lower() in ['help', 'h']:
                    self._show_help()
                elif user_input.lower() == 'history':
                    self._show_history()
                else:
                    self._handle_search(user_input)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _handle_search(self, query: str):
        """Handle food search query."""
        print(f"\n🔍 Searching for '{query}'...")
        
        # Perform vector search
        results = self.vector_engine.search_similar(self.collection, query, n_results=5)
        
        if not results:
            print("❌ No matching foods found.")
            print("💡 Try different keywords like: 'Italian', 'spicy', 'sweet', 'healthy'")
            return
        
        # Generate AI response
        ai_response = self.llm_generator.generate_food_recommendation(query, results)
        
        # Display results
        print(f"\n🤖 AI Recommendation:")
        print(f"{ai_response}")
        
        print(f"\n✅ Found {len(results)} recommendations:")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            score = result['similarity_score'] * 100
            print(f"\n{i}. 🍽️  {result['food_name']}")
            print(f"   📊 Match: {score:.1f}% | 🏷️  {result['cuisine_type']} | 🔥 {result['food_calories_per_serving']} cal")
            print(f"   📝 {result['food_description'][:100]}...")
        
        print("=" * 60)
        
        # Add to history
        self.search_history.append(query)
        
        # Show suggestions
        self._suggest_related_searches(results)
    
    def _show_welcome(self):
        """Display welcome message."""
        print("\n🤖 INTERACTIVE FOOD SEARCH CHATBOT")
        print("="*50)
        print("Type food descriptions to search, 'help' for commands, 'quit' to exit")
        print("-" * 50)
    
    def _show_help(self):
        """Display help menu."""
        print("\n📖 HELP MENU")
        print("-" * 30)
        print("Search Examples:")
        print("  • 'chocolate dessert' - Find chocolate desserts")
        print("  • 'Italian food' - Find Italian cuisine")
        print("  • 'low calorie' - Find lower-calorie options")
        print("\nCommands:")
        print("  • 'help' - Show this help menu")
        print("  • 'history' - Show search history")
        print("  • 'quit' - Exit the system")
    
    def _show_history(self):
        """Display search history."""
        if not self.search_history:
            print("📝 No search history available")
            return
        
        print("\n📝 Your Search History:")
        print("-" * 30)
        for i, search in enumerate(self.search_history[-10:], 1):
            print(f"{i}. {search}")
    
    def _suggest_related_searches(self, results: List[Dict]):
        """Suggest related searches."""
        if not results:
            return
        
        cuisines = list(set([r['cuisine_type'] for r in results]))
        
        print("\n💡 Related searches you might like:")
        for cuisine in cuisines[:3]:
            print(f"   • Try '{cuisine} dishes' for more {cuisine} options")
```

### Phase 6: Testing Implementation

#### **6.1 Unit Tests**
```python
# tests/unit/test_vector_search.py
import pytest
from unittest.mock import Mock, patch
from scripts.vector_search import VectorSearchEngine

class TestVectorSearchEngine:
    """Unit tests for VectorSearchEngine."""
    
    @pytest.fixture
    def search_engine(self):
        """Create a VectorSearchEngine instance for testing."""
        with patch('chromadb.Client'):
            with patch('sentence_transformers.SentenceTransformer'):
                return VectorSearchEngine()
    
    @pytest.fixture
    def sample_food_data(self):
        """Sample food data for testing."""
        return [
            {
                'food_name': 'Chicken Tikka Masala',
                'cuisine_type': 'Indian',
                'food_description': 'Creamy tomato-based curry with tender chicken',
                'food_calories_per_serving': 450,
                'food_ingredients': ['chicken', 'tomatoes', 'cream'],
                'food_health_benefits': 'High protein',
                'cooking_method': 'Grilled and simmered',
                'taste_profile': 'Spicy and creamy'
            }
        ]
    
    def test_create_searchable_text(self, search_engine, sample_food_data):
        """Test searchable text creation."""
        item = sample_food_data[0]
        result = search_engine._create_searchable_text(item)
        
        assert 'Chicken Tikka Masala' in result
        assert 'Indian' in result
        assert 'Creamy tomato-based curry' in result
        assert 'chicken tomatoes cream' in result
    
    def test_create_collection(self, search_engine):
        """Test collection creation."""
        mock_collection = Mock()
        search_engine.client.create_collection.return_value = mock_collection
        
        collection = search_engine.create_collection('test_collection')
        
        assert collection == mock_collection
        assert 'test_collection' in search_engine.collections
```

### Phase 7: Documentation & Deployment

#### **7.1 API Documentation**
```python
def create_similarity_search_collection(name: str, metadata: Dict = None) -> chromadb.Collection:
    """
    Create a ChromaDB collection for similarity search.
    
    This function initializes a new ChromaDB collection that will be used
    to store food item embeddings and perform vector-based similarity searches.
    
    Args:
        name (str): Unique name for the collection. Should be descriptive
                   and follow naming conventions (e.g., 'food_recommendations').
        metadata (Dict, optional): Additional metadata to associate with
                                 the collection. Useful for versioning,
                                 descriptions, and configuration settings.
    
    Returns:
        chromadb.Collection: ChromaDB collection object that can be used
                           for adding documents and performing searches.
    
    Raises:
        ValueError: If collection name is invalid or already exists.
        ConnectionError: If ChromaDB client cannot be initialized.
    
    Example:
        >>> collection = create_similarity_search_collection(
        ...     "food_search",
        ...     {"description": "Food recommendation system", "version": "1.0"}
        ... )
        >>> print(f"Created collection: {collection.name}")
        Created collection: food_search
    
    Note:
        - Collection names must be unique within a ChromaDB instance
        - If a collection with the same name exists, it will be deleted first
        - Metadata is stored with the collection and can be retrieved later
    """
    pass
```

This implementation guide provides a **complete roadmap** from initial setup to production deployment, with detailed code examples and best practices for each phase.