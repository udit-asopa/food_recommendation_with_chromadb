"""
Type definitions for the Food Recommendation System.

This module contains all custom type definitions, type aliases, and data structures
used throughout the food recommendation system for better type safety and code clarity.

Author: Food Recommendation Team
Version: 1.0.0
"""

from typing import Dict, List, Any, Union, Optional, Protocol, TypedDict, Literal, Callable
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# Core Data Types
# =============================================================================

class FoodItemDict(TypedDict, total=False):
    """Type definition for a food item dictionary."""
    food_name: str
    cuisine_type: str
    food_description: str
    food_calories_per_serving: int
    food_ingredients: Union[List[str], str]
    food_health_benefits: str
    cooking_method: str
    taste_profile: str

class SearchResultDict(TypedDict):
    """Type definition for search result dictionary."""
    food_name: str
    cuisine_type: str
    food_description: str
    food_calories_per_serving: int
    similarity_score: float
    food_ingredients: str
    food_health_benefits: str
    cooking_method: str
    taste_profile: str

# =============================================================================
# Enums
# =============================================================================

class CuisineType(Enum):
    """Enumeration of supported cuisine types."""
    ITALIAN = "Italian"
    CHINESE = "Chinese"
    INDIAN = "Indian"
    MEXICAN = "Mexican"
    THAI = "Thai"
    JAPANESE = "Japanese"
    FRENCH = "French"
    AMERICAN = "American"
    MEDITERRANEAN = "Mediterranean"
    MIDDLE_EASTERN = "Middle Eastern"
    KOREAN = "Korean"
    VIETNAMESE = "Vietnamese"
    GREEK = "Greek"
    SPANISH = "Spanish"
    BRITISH = "British"
    GERMAN = "German"
    TURKISH = "Turkish"
    LEBANESE = "Lebanese"
    BRAZILIAN = "Brazilian"
    AFRICAN = "African"
    FUSION = "Fusion"
    HEALTH = "Health"
    MODERN = "Modern"

class LogLevel(Enum):
    """Logging levels for the application."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class FoodItem:
    """
    Structured representation of a food item.
    
    Attributes:
        name: Name of the food item
        cuisine: Type of cuisine
        description: Detailed description
        calories: Calories per serving
        ingredients: List of ingredients
        health_benefits: Health-related information
        cooking_method: Method of preparation
        taste_profile: Flavor characteristics
    """
    name: str
    cuisine: CuisineType
    description: str
    calories: int
    ingredients: List[str]
    health_benefits: str = ""
    cooking_method: str = ""
    taste_profile: str = ""
    
    def to_dict(self) -> FoodItemDict:
        """Convert to dictionary format."""
        return FoodItemDict(
            food_name=self.name,
            cuisine_type=self.cuisine.value,
            food_description=self.description,
            food_calories_per_serving=self.calories,
            food_ingredients=self.ingredients,
            food_health_benefits=self.health_benefits,
            cooking_method=self.cooking_method,
            taste_profile=self.taste_profile
        )

@dataclass
class SearchResult:
    """
    Structured representation of a search result.
    
    Attributes:
        food_item: The matched food item
        similarity_score: Relevance score (0.0 to 1.0)
        metadata: Additional search metadata
    """
    food_item: FoodItem
    similarity_score: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> SearchResultDict:
        """Convert to dictionary format."""
        return SearchResultDict(
            food_name=self.food_item.name,
            cuisine_type=self.food_item.cuisine.value,
            food_description=self.food_item.description,
            food_calories_per_serving=self.food_item.calories,
            similarity_score=self.similarity_score,
            food_ingredients=", ".join(self.food_item.ingredients),
            food_health_benefits=self.food_item.health_benefits,
            cooking_method=self.food_item.cooking_method,
            taste_profile=self.food_item.taste_profile
        )

@dataclass
class UserQuery:
    """
    Structured representation of a user query.
    
    Attributes:
        text: The original query text
        intent: Detected intent (search, compare, help, etc.)
        filters: Applied filters (cuisine, calories, etc.)
        context: Additional context information
    """
    text: str
    intent: Literal["search", "compare", "help", "history", "quit"] = "search"
    filters: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.filters is None:
            self.filters = {}
        if self.context is None:
            self.context = {}

@dataclass
class ConversationContext:
    """
    Context for conversational interactions.
    
    Attributes:
        history: List of previous queries
        preferences: User preferences
        session_id: Unique session identifier
        timestamp: Session start time
    """
    history: List[str]
    preferences: Dict[str, Any]
    session_id: str
    timestamp: float
    
    def add_query(self, query: str) -> None:
        """Add a query to the conversation history."""
        self.history.append(query)
        # Keep only last 10 queries for memory efficiency
        if len(self.history) > 10:
            self.history = self.history[-10:]

@dataclass
class SystemConfig:
    """
    System configuration parameters.
    
    Attributes:
        embedding_model: Name of the embedding model
        llm_model: Name of the language model
        max_results: Maximum search results to return
        similarity_threshold: Minimum similarity score
        generation_params: LLM generation parameters
    """
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "google/flan-t5-base"
    max_results: int = 5
    similarity_threshold: float = 0.3
    generation_params: Optional[Dict[str, Union[int, float, bool]]] = None
    
    def __post_init__(self):
        """Initialize default generation parameters."""
        if self.generation_params is None:
            self.generation_params = {
                "max_length": 400,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
            }

# =============================================================================
# Protocol Definitions (Interfaces)
# =============================================================================

class EmbeddingModel(Protocol):
    """Protocol for embedding models."""
    
    def encode(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Encode text(s) into embeddings."""
        ...

class VectorDatabase(Protocol):
    """Protocol for vector database operations."""
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadata: List[Dict[str, Any]]) -> None:
        """Add documents to the database."""
        ...
    
    def search(self, query_embedding: List[float], k: int) -> List[SearchResult]:
        """Search for similar documents."""
        ...

class LanguageModel(Protocol):
    """Protocol for language models."""
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt."""
        ...

# =============================================================================
# Type Aliases
# =============================================================================

# Common type aliases for better readability
FoodDataset = List[FoodItemDict]
SearchResults = List[SearchResultDict]
EmbeddingVector = List[float]
EmbeddingMatrix = List[List[float]]
QueryText = str
ResponseText = str
CollectionMetadata = Dict[str, Any]
UserPreferences = Dict[str, Any]

# Function type aliases
EmbeddingFunction = Callable[[Union[str, List[str]]], Union[EmbeddingVector, EmbeddingMatrix]]
GenerationFunction = Callable[[str], str]
SearchFunction = Callable[[QueryText, int], SearchResults]

# =============================================================================
# Validation Functions
# =============================================================================

def validate_food_item(item: Dict[str, Any]) -> bool:
    """
    Validate if a dictionary represents a valid food item.
    
    Args:
        item: Dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['food_name', 'cuisine_type', 'food_description']
    return all(field in item and item[field] for field in required_fields)

def validate_search_result(result: Dict[str, Any]) -> bool:
    """
    Validate if a dictionary represents a valid search result.
    
    Args:
        result: Dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['food_name', 'similarity_score']
    return (
        all(field in result for field in required_fields) and
        isinstance(result['similarity_score'], (int, float)) and
        0.0 <= result['similarity_score'] <= 1.0
    )

def validate_system_config(config: Dict[str, Any]) -> bool:
    """
    Validate system configuration parameters.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['embedding_model', 'llm_model', 'max_results']
    return (
        all(field in config for field in required_fields) and
        isinstance(config['max_results'], int) and
        config['max_results'] > 0
    )

# =============================================================================
# Constants
# =============================================================================

# Default values
DEFAULT_MAX_RESULTS: int = 5
DEFAULT_SIMILARITY_THRESHOLD: float = 0.3
DEFAULT_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
DEFAULT_LLM_MODEL: str = "google/flan-t5-base"

# Limits
MAX_QUERY_LENGTH: int = 500
MAX_RESULTS_LIMIT: int = 50
MAX_CONVERSATION_HISTORY: int = 10
MAX_EMBEDDING_BATCH_SIZE: int = 100

# File paths
DEFAULT_DATA_PATH: str = "./data/FoodDataSet.json"
DEFAULT_MODELS_PATH: str = "./models/"
DEFAULT_CACHE_PATH: str = "./cache/"