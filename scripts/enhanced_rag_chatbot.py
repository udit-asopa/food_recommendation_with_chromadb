from shared_functions import *
from typing import List, Dict, Any, Optional, Union
from transformers import pipeline, Pipeline
import json
import chromadb

# For simplicity and reliability, use direct Transformers pipeline
# This avoids LangChain version compatibility issues
print("🔧 Using direct Transformers pipeline for maximum compatibility")

# Global variables
food_items: List[Dict[str, Any]] = []

# Hugging Face LLM Configuration
model_id: str = 'google/flan-t5-base'  # CPU-friendly alternative to IBM Granite
generation_params: Dict[str, Union[int, float, bool]] = {
    "max_length": 400,
    "temperature": 0.7,
    "do_sample": True,
    "top_p": 0.9
}

# Initialize the Hugging Face LLM model
print("🔧 Initializing Hugging Face LLM...")
llm_pipeline = pipeline(
    "text2text-generation",
    model=model_id,
    device="cpu",  # Use CPU for local compatibility
    model_kwargs={"low_cpu_mem_usage": True}
)

# Simple function to call the model
def generate_text(prompt: str) -> str:
    """
    Generate text using the FLAN-T5 model.
    
    Args:
        prompt: Input text prompt for generation
        
    Returns:
        Generated text response
    """
    try:
        result = llm_pipeline(prompt, **generation_params)
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '').strip()
        return str(result).strip()
    except Exception as e:
        print(f"Model error: {e}")
        return ""

print("✅ Model ready for text generation")

def main() -> None:
    """Main function for enhanced RAG chatbot system."""
    try:
        print("🤖 Enhanced RAG-Powered Food Recommendation Chatbot")
        print("   Powered by Hugging Face FLAN-T5 & ChromaDB")
        print("=" * 55)
        
        # Load food data
        global food_items
        food_items = load_food_data('./data/FoodDataSet.json')
        print(f"✅ Loaded {len(food_items)} food items")
        
        # Create collection for RAG system
        collection = create_similarity_search_collection(
            "enhanced_rag_food_chatbot",
            {'description': 'Enhanced RAG chatbot with Hugging Face FLAN-T5 integration'}
        )
        populate_similarity_collection(collection, food_items)
        print("✅ Vector database ready")
        
        # Test LLM connection
        print("🔗 Testing LLM connection...")
        test_response = generate_text("Hello, this is a test.")
        if test_response:
            print("✅ LLM connection established")
        else:
            print("❌ LLM connection failed")
            return
        
        # Start enhanced RAG chatbot
        enhanced_rag_food_chatbot(collection)
        
    except Exception as error:
        print(f"❌ Error: {error}")



def generate_llm_rag_response(query: str, search_results: List[Dict[str, Any]]) -> str:
    """Generate response using FLAN-T5 with retrieved context"""
    if not search_results:
        return "I couldn't find any food items matching your request. Try describing what you're in the mood for with different words!"
    
    # Build simplified context
    foods = []
    for result in search_results[:3]:
        food_info = f"{result['food_name']} ({result['cuisine_type']}, {result['food_calories_per_serving']} cal)"
        foods.append(food_info)
    
    context = ", ".join(foods)
    
    # Simple, effective prompt
    prompt = f"User wants: {query}\nAvailable foods: {context}\nRecommend 2-3 foods and explain why:"
    
    try:
        response = generate_text(prompt)
        if response and len(response.strip()) > 20:
            return response
        else:
            # Fallback response
            top = search_results[0]
            return f"I recommend {top['food_name']}, a {top['cuisine_type']} dish with {top['food_calories_per_serving']} calories. It matches your request for '{query}'."
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        top = search_results[0]
        return f"I recommend {top['food_name']}, a {top['cuisine_type']} dish with {top['food_calories_per_serving']} calories."

def generate_fallback_response(query: str, search_results: List[Dict]) -> str:
    """Generate fallback response when LLM fails"""
    if not search_results:
        return "I couldn't find any food items matching your request. Try describing what you're in the mood for with different words!"
    
    top_result = search_results[0]
    response_parts = []
    
    response_parts.append(f"Based on your request for '{query}', I'd recommend {top_result['food_name']}.")
    response_parts.append(f"It's a {top_result['cuisine_type']} dish with {top_result['food_calories_per_serving']} calories per serving.")
    
    if len(search_results) > 1:
        second_choice = search_results[1]
        response_parts.append(f"Another great option would be {second_choice['food_name']}.")
    
    return " ".join(response_parts)

def enhanced_rag_food_chatbot(collection: chromadb.Collection) -> None:
    """Enhanced RAG-powered conversational food chatbot with Hugging Face FLAN-T5."""
    print("\n" + "="*70)
    print("🤖 ENHANCED RAG FOOD RECOMMENDATION CHATBOT")
    print("   Powered by Hugging Face FLAN-T5 Model")
    print("="*70)
    print("💬 Ask me about food recommendations using natural language!")
    print("\nExample queries:")
    print("  • 'I want something spicy and healthy for dinner'")
    print("  • 'What Italian dishes do you recommend under 400 calories?'")
    print("  • 'I'm craving comfort food for a cold evening'")
    print("  • 'Suggest some protein-rich breakfast options'")
    print("\nCommands:")
    print("  • 'help' - Show detailed help menu")
    print("  • 'compare' - Compare recommendations for two different queries")
    print("  • 'quit' - Exit the chatbot")
    print("-" * 70)
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                print("🤖 Bot: Please tell me what kind of food you're looking for!")
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n🤖 Bot: Thank you for using the Enhanced RAG Food Chatbot!")
                print("      Hope you found some delicious recommendations! 👋")
                break
            
            elif user_input.lower() in ['help', 'h']:
                show_enhanced_rag_help()
            
            elif user_input.lower() in ['compare']:
                handle_enhanced_comparison_mode(collection)
            
            else:
                # Process the food query with enhanced RAG
                handle_enhanced_rag_query(collection, user_input, conversation_history)
                conversation_history.append(user_input)
                
                # Keep conversation history manageable
                if len(conversation_history) > 5:
                    conversation_history = conversation_history[-3:]
                
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! Hope you find something delicious! 👋")
            break
        except Exception as e:
            print(f"❌ Bot: Sorry, I encountered an error: {e}")

def handle_enhanced_rag_query(collection: chromadb.Collection, query: str, conversation_history: List[str]) -> None:
    """Handle user query with enhanced RAG approach using Hugging Face FLAN-T5."""
    print(f"\n🔍 Searching vector database for: '{query}'...")
    
    # Perform similarity search with more results for better context
    search_results = perform_similarity_search(collection, query, 3)
    
    if not search_results:
        print("🤖 Bot: I couldn't find any food items matching your request.")
        print("      Try describing what you're in the mood for with different words!")
        return
    
    print(f"✅ Found {len(search_results)} relevant matches")
    print("🧠 Generating AI-powered response...")
    
    # Generate enhanced RAG response using FLAN-T5
    ai_response = generate_llm_rag_response(query, search_results)
    
    print(f"\n🤖 Bot: {ai_response}")
    
    # Show detailed results for reference
    print(f"\n📊 Search Results Details:")
    print("-" * 45)
    for i, result in enumerate(search_results[:3], 1):
        print(f"{i}. 🍽️  {result['food_name']}")
        print(f"   📍 {result['cuisine_type']} | 🔥 {result['food_calories_per_serving']} cal | 📈 {result['similarity_score']*100:.1f}% match")
        if i < 3:
            print()

def handle_enhanced_comparison_mode(collection: chromadb.Collection) -> None:
    """Enhanced comparison between two food queries using LLM."""
    print("\n🔄 ENHANCED COMPARISON MODE")
    print("   Powered by AI Analysis")
    print("-" * 35)
    
    query1 = input("Enter first food query: ").strip()
    query2 = input("Enter second food query: ").strip()
    
    if not query1 or not query2:
        print("❌ Please enter both queries for comparison")
        return
    
    print(f"\n🔍 Analyzing '{query1}' vs '{query2}' with AI...")
    
    # Get results for both queries
    results1 = perform_similarity_search(collection, query1, 3)
    results2 = perform_similarity_search(collection, query2, 3)
    
    # Generate AI-powered comparison
    comparison_response = generate_llm_comparison(query1, query2, results1, results2)
    
    print(f"\n🤖 AI Analysis: {comparison_response}")
    
    # Show side-by-side results
    print(f"\n📊 DETAILED COMPARISON")
    print("=" * 60)
    print(f"{'Query 1: ' + query1[:20] + '...' if len(query1) > 20 else 'Query 1: ' + query1:<30} | {'Query 2: ' + query2[:20] + '...' if len(query2) > 20 else 'Query 2: ' + query2}")
    print("-" * 60)
    
    max_results = max(len(results1), len(results2))
    for i in range(min(max_results, 3)):
        left = f"{results1[i]['food_name']} ({results1[i]['similarity_score']*100:.0f}%)" if i < len(results1) else "---"
        right = f"{results2[i]['food_name']} ({results2[i]['similarity_score']*100:.0f}%)" if i < len(results2) else "---"
        print(f"{left[:30]:<30} | {right[:30]}")

def generate_llm_comparison(query1: str, query2: str, results1: List[Dict[str, Any]], results2: List[Dict[str, Any]]) -> str:
    """Generate AI-powered comparison between two queries"""
    # Simple fallback if no results
    if not results1 and not results2:
        return "No results found for either query."
    if not results1:
        return f"Found results for '{query2}' but none for '{query1}'."
    if not results2:
        return f"Found results for '{query1}' but none for '{query2}'."
    
    # Build simple comparison prompt
    food1 = results1[0]['food_name']
    food2 = results2[0]['food_name']
    
    prompt = f"Compare: '{query1}' (best match: {food1}) vs '{query2}' (best match: {food2}). Which is better and why?"
    
    try:
        response = generate_text(prompt)
        if response and len(response.strip()) > 30:
            return response.strip()
        else:
            return f"For '{query1}', I recommend {food1}. For '{query2}', {food2} would be perfect."
    except Exception as e:
        return f"For '{query1}', I recommend {food1}. For '{query2}', {food2} would be perfect."



def show_enhanced_rag_help() -> None:
    """Display help information for enhanced RAG chatbot."""
    print("\n📖 ENHANCED RAG CHATBOT HELP")
    print("=" * 45)
    print("🧠 This chatbot uses Hugging Face FLAN-T5 to understand your")
    print("   food preferences and provide intelligent recommendations.")
    print("\nHow to get the best recommendations:")
    print("  • Be specific: 'healthy Italian pasta under 350 calories'")
    print("  • Mention preferences: 'spicy comfort food for cold weather'")
    print("  • Include context: 'light breakfast for busy morning'")
    print("  • Ask about benefits: 'protein-rich foods for workout recovery'")
    print("\nSpecial features:")
    print("  • 🔍 Vector similarity search finds relevant foods")
    print("  • 🧠 AI analysis provides contextual explanations")
    print("  • 📊 Detailed nutritional and cuisine information")
    print("  • 🔄 Smart comparison between different preferences")
    print("\nCommands:")
    print("  • 'compare' - AI-powered comparison of two queries")
    print("  • 'help' - Show this help menu")
    print("  • 'quit' - Exit the chatbot")
    print("\nTips for better results:")
    print("  • Use natural language - talk like you would to a friend")
    print("  • Mention dietary restrictions or preferences")
    print("  • Include meal timing (breakfast, lunch, dinner)")
    print("  • Specify if you want healthy, comfort, or indulgent options")

if __name__ == "__main__":
    main()