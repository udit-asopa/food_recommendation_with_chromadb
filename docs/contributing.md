# Contributing Guidelines

## 🤝 Welcome Contributors!

Thank you for your interest in contributing to the Food Recommendation System! This project welcomes contributions from developers, researchers, students, and food enthusiasts.

## 🎯 Types of Contributions

### **🐛 Bug Reports**
- Report issues with search accuracy
- Document performance problems
- Identify UI/UX improvements
- Flag documentation errors

### **✨ Feature Requests**
- New search capabilities
- Additional cuisine types
- Enhanced AI responses
- Mobile app integration ideas

### **💻 Code Contributions**
- Bug fixes and optimizations
- New features and enhancements
- Documentation improvements
- Test coverage expansion

### **📚 Documentation**
- Tutorial improvements
- API documentation
- Use case examples
- Translation to other languages

## 🚀 Getting Started

### **Development Environment Setup**

```bash
# 1. Fork and clone the repository
git clone https://github.com/udit-asopa/food_recommendation_with_chromadb.git
cd food_recommendation_with_chromadb

# 2. Set up development environment
pixi install
pixi shell

# 3. Install development dependencies
pixi add --dev pytest ruff black mypy pre-commit

# 4. Set up pre-commit hooks
pre-commit install

# 5. Run tests to ensure everything works
pixi run pytest
```

### **Development Workflow**

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# ... code, test, document ...

# 3. Run quality checks
pixi run ruff check .        # Linting
pixi run black .             # Code formatting  
pixi run mypy .              # Type checking
pixi run pytest             # All tests

# 4. Commit and push
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name

# 5. Create pull request
```

## 📋 Code Style Guidelines

### **Python Code Standards**

```python
# ✅ Good: Clear function with type hints and docstring
def search_food_items(query: str, max_results: int = 5) -> List[FoodItem]:
    """
    Search for food items using semantic similarity.
    
    Args:
        query: Natural language search query
        max_results: Maximum number of results to return
        
    Returns:
        List of matching food items sorted by relevance
    """
    # Implementation here
    pass

# ❌ Bad: No types, unclear naming, no documentation
def search(q, n=5):
    # What does this do?
    pass
```

### **Documentation Standards**

```python
# ✅ Good: Comprehensive docstring
def generate_food_recommendation(
    query: str, 
    search_results: List[Dict], 
    user_context: Optional[UserContext] = None
) -> str:
    """
    Generate natural language food recommendations using LLM.
    
    This function takes search results from vector similarity search and
    uses a language model to generate human-friendly recommendations
    that explain why certain foods match the user's query.
    
    Args:
        query: Original user query (e.g., "healthy breakfast options")
        search_results: List of food items from similarity search
        user_context: Optional user preferences and dietary restrictions
        
    Returns:
        Natural language recommendation text
        
    Raises:
        ValueError: If search_results is empty
        RuntimeError: If LLM generation fails
        
    Example:
        >>> results = search_similar_foods("spicy pasta")
        >>> recommendation = generate_food_recommendation(
        ...     "spicy pasta", results
        ... )
        >>> print(recommendation)
        "For spicy pasta, I recommend Penne Arrabbiata with its 
         fiery tomato sauce and red pepper flakes..."
    """
```

### **Testing Standards**

```python
# ✅ Good: Comprehensive test with clear intent
def test_similarity_search_returns_relevant_results():
    """Test that similarity search returns contextually relevant food items."""
    # Arrange
    food_items = create_test_food_data()
    collection = setup_test_collection(food_items)
    
    # Act
    results = perform_similarity_search(collection, "spicy Italian pasta")
    
    # Assert
    assert len(results) > 0
    assert all(result['similarity_score'] > 0.5 for result in results)
    assert any('Italian' in result['cuisine_type'] for result in results)
    assert any('pasta' in result['food_name'].lower() for result in results)

def test_similarity_search_handles_empty_query():
    """Test that empty queries return empty results gracefully."""
    collection = setup_test_collection()
    
    results = perform_similarity_search(collection, "")
    
    assert results == []
```

## 🧪 Testing Guidelines

### **Test Categories**

1. **Unit Tests** (`tests/unit/`)
   - Individual function testing
   - Mock external dependencies
   - Fast execution (< 1 second each)

2. **Integration Tests** (`tests/integration/`)
   - Component interaction testing
   - Real ChromaDB instances
   - Moderate execution time

3. **End-to-End Tests** (`tests/e2e/`)
   - Full user workflow testing
   - Real data and models
   - Slower execution acceptable

### **Running Tests**

```bash
# Run all tests
pixi run pytest

# Run specific test categories
pixi run pytest tests/unit/           # Unit tests only
pixi run pytest tests/integration/    # Integration tests only
pixi run pytest tests/e2e/           # E2E tests only

# Run with coverage
pixi run pytest --cov=scripts --cov-report=html

# Run performance tests
pixi run pytest tests/performance/ -v
```

## 📊 Performance Guidelines

### **Optimization Priorities**
1. **Search Speed**: < 500ms for similarity search
2. **Memory Usage**: < 2GB for standard dataset
3. **Model Loading**: < 30 seconds for first load
4. **Response Generation**: < 3 seconds for LLM responses

### **Performance Testing**

```python
def test_search_performance():
    """Ensure search performance meets requirements."""
    collection = setup_large_test_collection(1000)  # 1000 items
    
    start_time = time.time()
    results = perform_similarity_search(collection, "healthy breakfast")
    end_time = time.time()
    
    assert end_time - start_time < 0.5  # Must be under 500ms
    assert len(results) > 0
```

## 🚦 Pull Request Process

### **Before Submitting**

- [ ] **Tests Pass**: All existing tests continue to pass
- [ ] **New Tests**: New functionality includes comprehensive tests
- [ ] **Documentation**: Functions have proper docstrings
- [ ] **Code Style**: Follows project formatting standards
- [ ] **Performance**: No significant performance regressions
- [ ] **Compatibility**: Works with supported Python versions

### **Pull Request Template**

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Performance Impact
- [ ] No performance impact
- [ ] Performance improvement
- [ ] Potential performance regression (explain)

## Screenshots (if applicable)
Include screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added and passing
```

## 🎯 Contribution Areas

### **High Priority**
- **Search Quality Improvements**: Better embedding models, advanced filtering
- **Performance Optimization**: Faster search, memory efficiency
- **User Experience**: Better CLI interface, error messages
- **Test Coverage**: Expanding test coverage to >90%

### **Medium Priority**
- **New Features**: Image search, meal planning, nutrition analysis
- **Documentation**: Video tutorials, interactive examples
- **Internationalization**: Support for multiple languages
- **Mobile Integration**: API endpoints for mobile apps

### **Research Projects**
- **Advanced RAG**: Multi-modal search, personalization
- **Model Comparison**: Benchmarking different embedding models
- **Domain Adaptation**: Applying system to other domains
- **Evaluation Metrics**: Systematic quality measurement

## 🏆 Recognition

### **Contributor Levels**

- **🌟 First-time Contributors**: Welcome package and mentorship
- **🚀 Regular Contributors**: Recognition in README and releases
- **🎯 Core Contributors**: Commit access and decision-making involvement
- **👑 Maintainers**: Full repository access and leadership responsibilities

### **Recognition Methods**
- Contributor mentions in release notes
- "Contributors" section in README
- LinkedIn recommendations for significant contributions
- Conference presentation opportunities
- Co-authorship on research papers

## 📞 Getting Help

### **Communication Channels**
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Code Reviews**: Detailed feedback on pull requests
- **Documentation**: Comprehensive guides and examples

### **Mentorship Program**
New contributors are paired with experienced developers for guidance on:
- Understanding the codebase
- Best practices and coding standards
- Testing and documentation
- Career development in AI/ML

## 🎉 Thank You!

Every contribution, no matter how small, makes this project better for everyone. Whether you're fixing a typo, adding a feature, or improving documentation, your effort is appreciated and valued.

**Let's build something delicious together!** 🍽️✨
