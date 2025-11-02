"""
Shared utility functions for the Food Recommendation System.

This module provides core functionality for loading data, managing ChromaDB collections,
performing similarity searches, and handling embeddings. These functions are used
across multiple components of the food recommendation system.

Dependencies:
    - chromadb: Vector database for similarity search
    - sentence_transformers: For generating text embeddings
    - json: For data loading and parsing
    - typing: For type hints and better code documentation

Author: Food Recommendation Team
Version: 1.0.0
Last Updated: $(date)
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import os

# Global embedding model instance for consistency across the application
_embedding_model = None

def get_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Get or create a singleton embedding model instance.
    
    This function ensures that only one embedding model is loaded in memory
    across the entire application, improving performance and memory usage.
    
    Args:
        model_name (str): Name of the SentenceTransformer model to use.
                         Default is 'all-MiniLM-L6-v2' which provides good
                         balance between speed and quality.
    
    Returns:
        SentenceTransformer: Configured embedding model instance
    
    Example:
        >>> embedder = get_embedding_model()
        >>> embeddings = embedder.encode(["pasta", "pizza"])
        >>> print(f"Generated {len(embeddings)} embeddings")
        Generated 2 embeddings
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(model_name)
    return _embedding_model

def load_food_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load and validate food dataset from JSON file.
    
    This function reads a JSON file containing food item data, validates the structure,
    and returns a list of food dictionaries ready for use in the recommendation system.
    
    Args:
        file_path (str): Path to the JSON dataset file. Can be relative or absolute.
                        Common paths: './data/FoodDataSet.json', '../../data/FoodDataSet.json'
    
    Returns:
        List[Dict[str, Any]]: List of food item dictionaries, each containing:
            - food_name (str): Name of the dish
            - cuisine_type (str): Type of cuisine (e.g., 'Italian', 'Chinese')
            - food_description (str): Detailed description of the food
            - food_calories_per_serving (int): Calories per serving
            - food_ingredients (List[str] | str): List of ingredients or string
            - food_health_benefits (str): Health benefits description
            - cooking_method (str): Method of preparation
            - taste_profile (str): Flavor characteristics
    
    Raises:
        FileNotFoundError: If the specified file path does not exist
        json.JSONDecodeError: If the file contains invalid JSON syntax  
        ValueError: If the JSON structure is invalid or missing required fields
        PermissionError: If the file cannot be read due to permissions
    
    Example:
        >>> food_items = load_food_data('./data/FoodDataSet.json')
        >>> print(f"Loaded {len(food_items)} food items")
        Loaded 185 food items
        >>> print(food_items[0]['food_name'])
        Chicken Tikka Masala
    
    Note:
        - The function performs basic validation on required fields
        - Missing optional fields are filled with default values
        - Large datasets (>1000 items) may take several seconds to load
        - File encoding is assumed to be UTF-8
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Food dataset file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in dataset file: {e}")
    except PermissionError:
        raise PermissionError(f"Cannot read file due to permissions: {file_path}")
    
    if not isinstance(data, list):
        raise ValueError("Dataset must be a JSON array of food items")
    
    # Validate and clean data
    validated_items = []
    required_fields = ['food_name', 'cuisine_type', 'food_description']
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            continue  # Skip invalid items
        
        # Check required fields
        if not all(field in item and item[field] for field in required_fields):
            continue  # Skip items missing required fields
        
        # Clean and standardize data
        cleaned_item = {
            'food_name': str(item['food_name']).strip(),
            'cuisine_type': str(item['cuisine_type']).strip(),
            'food_description': str(item['food_description']).strip(),
            'food_calories_per_serving': int(item.get('food_calories_per_serving', 0)),
            'food_ingredients': item.get('food_ingredients', []),
            'food_health_benefits': str(item.get('food_health_benefits', '')),
            'cooking_method': str(item.get('cooking_method', '')),
            'taste_profile': str(item.get('taste_profile', ''))
        }
        validated_items.append(cleaned_item)
    
    if len(validated_items) == 0:
        raise ValueError("No valid food items found in dataset")
    
    print(f"Successfully loaded {len(validated_items)} food items from {file_path}")
    return validated_items

def create_similarity_search_collection(name: str, metadata: Optional[Dict] = None) -> chromadb.Collection:
    """
    Create a ChromaDB collection for similarity search.
    
    This function initializes a new ChromaDB collection that will be used
    to store food item embeddings and perform vector-based similarity searches.
    If a collection with the same name already exists, it will be deleted first.
    
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
        ValueError: If collection name is invalid (empty or None)
        chromadb.errors.ChromaError: If ChromaDB client initialization fails
        ConnectionError: If ChromaDB service is not accessible
    
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
        - The collection uses cosine similarity by default for vector comparisons
    """
    if not name or not isinstance(name, str):
        raise ValueError("Collection name must be a non-empty string")
    
    try:
        client = chromadb.Client()
        
        # Delete existing collection if it exists
        try:
            client.delete_collection(name=name)
            print(f"Deleted existing collection: {name}")
        except ValueError:
            pass  # Collection doesn't exist, which is fine
        
        # Create new collection
        collection = client.create_collection(
            name=name,
            metadata=metadata or {}
        )
        
        print(f"Created new collection: {name}")
        return collection
        
    except Exception as e:
        raise ConnectionError(f"Failed to create ChromaDB collection: {e}")

def populate_similarity_collection(collection: chromadb.Collection, food_items: List[Dict[str, Any]]) -> None:
    """
    Populate a ChromaDB collection with food data and embeddings.
    
    This function takes a list of food items, generates embeddings for their
    searchable text content, and adds them to the specified ChromaDB collection
    for similarity search capabilities.
    
    Args:
        collection (chromadb.Collection): ChromaDB collection to populate
        food_items (List[Dict[str, Any]]): List of food item dictionaries
                                          from load_food_data()
    
    Raises:
        ValueError: If collection is None or food_items is empty
        RuntimeError: If embedding generation fails
        chromadb.errors.ChromaError: If adding to collection fails
    
    Example:
        >>> food_items = load_food_data('./data/FoodDataSet.json')
        >>> collection = create_similarity_search_collection("foods")
        >>> populate_similarity_collection(collection, food_items)
        Added 185 food items to collection
    
    Note:
        - This function generates embeddings for all food items at once
        - Large datasets may take several minutes to process
        - Existing data in the collection will be preserved
        - Each food item gets a unique ID in format 'food_{index}'
        - Embeddings are generated from food name, description, and other text fields
    """
    if collection is None:
        raise ValueError("Collection cannot be None")
    
    if not food_items or len(food_items) == 0:
        raise ValueError("food_items cannot be empty")
    
    print(f"Generating embeddings for {len(food_items)} food items...")
    
    try:
        # Get embedding model
        embedder = get_embedding_model()
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for i, item in enumerate(food_items):
            # Create searchable text by combining relevant fields
            searchable_parts = [
                item['food_name'],
                item['cuisine_type'], 
                item['food_description']
            ]
            
            # Add optional fields if available
            if item.get('food_ingredients'):
                if isinstance(item['food_ingredients'], list):
                    searchable_parts.append(' '.join(item['food_ingredients']))
                else:
                    searchable_parts.append(str(item['food_ingredients']))
            
            if item.get('taste_profile'):
                searchable_parts.append(item['taste_profile'])
            
            if item.get('cooking_method'):
                searchable_parts.append(item['cooking_method'])
            
            # Create final searchable document
            searchable_text = ' '.join(searchable_parts)
            documents.append(searchable_text)
            
            # Prepare metadata (ChromaDB requires string values)
            metadata = {
                'food_name': item['food_name'],
                'cuisine_type': item['cuisine_type'],
                'calories': str(item['food_calories_per_serving']),
                'ingredients': str(item.get('food_ingredients', [])),
                'health_benefits': item.get('food_health_benefits', ''),
                'cooking_method': item.get('cooking_method', ''),
                'taste_profile': item.get('taste_profile', ''),
                'description': item['food_description']
            }
            metadatas.append(metadata)
            ids.append(f"food_{i}")
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = embedder.encode(documents, show_progress_bar=True)
        
        # Add to collection
        print("Adding items to ChromaDB collection...")
        collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings.tolist(),
            ids=ids
        )
        
        print(f"Added {len(food_items)} food items to collection")
        
    except Exception as e:
        raise RuntimeError(f"Failed to populate collection: {e}")

def perform_similarity_search(collection: chromadb.Collection, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform similarity search on a ChromaDB collection.
    
    This function takes a natural language query, converts it to an embedding,
    and searches the ChromaDB collection for the most similar food items.
    Results are ranked by similarity score and returned as a formatted list.
    
    Args:
        collection (chromadb.Collection): ChromaDB collection to search
        query (str): Natural language search query (e.g., "spicy Italian pasta")
        n_results (int): Maximum number of results to return (default: 5)
    
    Returns:
        List[Dict[str, Any]]: List of similar food items, each containing:
            - food_name (str): Name of the food item
            - cuisine_type (str): Type of cuisine
            - food_description (str): Description of the food
            - food_calories_per_serving (int): Calories per serving
            - similarity_score (float): Similarity score (0.0 to 1.0, higher is better)
            - Additional metadata fields (ingredients, health_benefits, etc.)
    
    Raises:
        ValueError: If collection is None or query is empty
        RuntimeError: If search operation fails
        chromadb.errors.ChromaError: If ChromaDB query fails
    
    Example:
        >>> results = perform_similarity_search(collection, "healthy Italian pasta", 3)
        >>> for result in results:
        ...     print(f"{result['food_name']}: {result['similarity_score']:.2f}")
        Pasta Primavera: 0.89
        Spaghetti with Marinara: 0.84
        Whole Wheat Penne: 0.81
    
    Note:
        - Results are automatically sorted by similarity score (highest first)
        - Similarity scores range from 0.0 (no similarity) to 1.0 (identical)
        - Empty queries will return an empty list
        - The function uses the same embedding model used during population
    """
    if collection is None:
        raise ValueError("Collection cannot be None")
    
    if not query or not isinstance(query, str) or query.strip() == "":
        return []
    
    query = query.strip()
    
    try:
        # Get embedding model and generate query embedding
        embedder = get_embedding_model()
        query_embedding = embedder.encode([query])
        
        # Perform search
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=min(n_results, 100)  # Cap at reasonable limit
        )
        
        # Format results
        formatted_results = []
        
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                # Convert distance to similarity score (ChromaDB uses cosine distance)
                similarity_score = max(0.0, 1.0 - distance)
                
                result = {
                    'food_name': metadata['food_name'],
                    'cuisine_type': metadata['cuisine_type'],
                    'food_description': metadata['description'],
                    'food_calories_per_serving': int(metadata['calories']) if metadata['calories'].isdigit() else 0,
                    'similarity_score': similarity_score,
                    'food_ingredients': metadata.get('ingredients', ''),
                    'food_health_benefits': metadata.get('health_benefits', ''),
                    'cooking_method': metadata.get('cooking_method', ''),
                    'taste_profile': metadata.get('taste_profile', '')
                }
                formatted_results.append(result)
        
        # Sort by similarity score (highest first)
        formatted_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return formatted_results
        
    except Exception as e:
        raise RuntimeError(f"Similarity search failed: {e}")

def validate_collection_health(collection: chromadb.Collection) -> Dict[str, Any]:
    """
    Validate the health and status of a ChromaDB collection.
    
    This function performs various checks on a ChromaDB collection to ensure
    it's properly configured and contains valid data for similarity search.
    
    Args:
        collection (chromadb.Collection): ChromaDB collection to validate
    
    Returns:
        Dict[str, Any]: Health report containing:
            - is_healthy (bool): Overall health status
            - item_count (int): Number of items in collection
            - has_embeddings (bool): Whether embeddings are present
            - metadata_fields (List[str]): Available metadata fields
            - sample_item (Dict): Sample item for inspection
            - issues (List[str]): List of any issues found
    
    Example:
        >>> health = validate_collection_health(collection)
        >>> if health['is_healthy']:
        ...     print(f"Collection is healthy with {health['item_count']} items")
        ... else:
        ...     print(f"Issues found: {health['issues']}")
    """
    health_report = {
        'is_healthy': True,
        'item_count': 0,
        'has_embeddings': False,
        'metadata_fields': [],
        'sample_item': None,
        'issues': []
    }
    
    try:
        # Get collection info
        result = collection.get(limit=1)
        
        if result['ids']:
            health_report['item_count'] = collection.count()
            health_report['has_embeddings'] = len(result.get('embeddings', [])) > 0
            
            if result['metadatas'] and len(result['metadatas']) > 0:
                health_report['metadata_fields'] = list(result['metadatas'][0].keys())
                health_report['sample_item'] = result['metadatas'][0]
            
            # Check for common issues
            if health_report['item_count'] == 0:
                health_report['issues'].append("Collection is empty")
                health_report['is_healthy'] = False
            
            if not health_report['has_embeddings']:
                health_report['issues'].append("No embeddings found")
                health_report['is_healthy'] = False
            
            if not health_report['metadata_fields']:
                health_report['issues'].append("No metadata found")
                health_report['is_healthy'] = False
                
        else:
            health_report['issues'].append("Collection is empty")
            health_report['is_healthy'] = False
            
    except Exception as e:
        health_report['issues'].append(f"Health check failed: {e}")
        health_report['is_healthy'] = False
    
    return health_report

