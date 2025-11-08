import os
import csv
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# In production (Render/Vercel), environment variables are set via platform
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print("✅ Loaded environment variables from .env file")

app = Flask(__name__)

# CORS configuration for local development and production
# Update with your Vercel frontend URL after deployment
CORS(app, origins=[
    "http://localhost:3000",  # Local development
    "http://127.0.0.1:3000",  # Alternative local
    "https://*.vercel.app",   # All Vercel deployments (preview & production)
    "*"  # Allow all origins during development (remove in production if needed)
])

# Global variables for backend components
vector_store_manager = None
ingredient_analyzer = None
advanced_retrieval_manager = None
api_keys = {}
current_retrieval_strategy = "ensemble"  # Default to ensemble
system_initialized = False

# Auto-load API keys from environment variables
def load_api_keys_from_env():
    """Load API keys from environment variables."""
    keys = {
        'openai_api_key': os.environ.get('OPENAI_API_KEY', ''),
        'langsmith_api_key': os.environ.get('LANGCHAIN_API_KEY', ''),
        'cohere_api_key': os.environ.get('COHERE_API_KEY', '')
    }
    
    # Validate required keys
    if not keys['openai_api_key'] or keys['openai_api_key'] == 'your_openai_api_key_here':
        print("⚠️  WARNING: OPENAI_API_KEY not set or using default placeholder")
        print("   Set it in backend/.env file (local) or Render dashboard (production)")
    
    if not keys['langsmith_api_key'] or keys['langsmith_api_key'] == 'your_langsmith_api_key_here':
        print("⚠️  WARNING: LANGCHAIN_API_KEY not set or using default placeholder")
        print("   Set it in backend/.env file (local) or Render dashboard (production)")
    
    return keys

def initialize_system():
    """Initialize the RAG system with environment variables."""
    global vector_store_manager, ingredient_analyzer, advanced_retrieval_manager, api_keys, current_retrieval_strategy, system_initialized
    
    if system_initialized:
        return True
    
    try:
        # Load API keys from environment
        env_keys = load_api_keys_from_env()
        
        # Check if required keys are present
        if not env_keys['openai_api_key'] or not env_keys['langsmith_api_key']:
            print("⚠️  Warning: Required API keys not set in environment variables")
            print("   Set OPENAI_API_KEY and LANGCHAIN_API_KEY in Render environment variables")
            return False
        
        api_keys = env_keys
        
        # Set environment variables for LangSmith tracing
        os.environ['OPENAI_API_KEY'] = api_keys['openai_api_key']
        os.environ['LANGCHAIN_API_KEY'] = api_keys['langsmith_api_key']
        os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        os.environ['LANGCHAIN_PROJECT'] = 'KidSafe-Food-Analyzer'
        
        if api_keys['cohere_api_key']:
            os.environ['COHERE_API_KEY'] = api_keys['cohere_api_key']
        
        # Initialize vector store and RAG system
        from backend.vector_store import VectorStoreManager
        from backend.rag_engine import IngredientAnalyzer
        from backend.advanced_retrieval import AdvancedRetrievalManager
        
        print("🚀 Initializing KidSafe Analyzer...")
        print("📚 Loading vector store...")
        vector_store_manager = VectorStoreManager(api_keys['openai_api_key'])
        vectorstore = vector_store_manager.load_and_index_documents()
        chunks = vector_store_manager.get_chunks()
        
        print("🔍 Initializing advanced retrieval manager...")
        advanced_retrieval_manager = AdvancedRetrievalManager(
            vectorstore=vectorstore,
            documents=chunks,
            openai_api_key=api_keys['openai_api_key'],
            cohere_api_key=api_keys['cohere_api_key'] if api_keys['cohere_api_key'] else None
        )
        
        # Use ensemble retrieval strategy
        print(f"⚙️  Setting up {current_retrieval_strategy} retrieval...")
        use_compression = bool(api_keys['cohere_api_key'])
        retriever = advanced_retrieval_manager.get_ensemble_retriever(k=5, use_compression=use_compression)
        
        print("🤖 Initializing ingredient analyzer...")
        ingredient_analyzer = IngredientAnalyzer(
            retriever, 
            api_keys['openai_api_key'],
            retrieval_strategy=current_retrieval_strategy
        )
        
        system_initialized = True
        print("✅ KidSafe Analyzer initialized successfully!")
        return True
        
    except Exception as e:
        import traceback
        print("=" * 70)
        print("❌ ERROR during system initialization:")
        print(traceback.format_exc())
        print("=" * 70)
        return False

def load_cereals():
    """Load cereal names from the cereal.csv file."""
    cereals = []
    data_file = os.path.join(os.path.dirname(__file__), 'Data', 'cereal.csv')
    
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Brand_Name'):
                cereals.append({
                    'brand': row['Brand_Name'],
                    'ingredients': row.get('Ingredients', '')
                })
    
    return cereals

@app.route('/')
def index():
    """API root - health check endpoint."""
    return jsonify({
        'status': 'running',
        'message': 'KidSafe Analyzer API is running!',
        'version': '1.0.0',
        'endpoints': {
            'status': '/api/status',
            'cereals': '/api/cereals',
            'configure': '/api/configure (POST)',
            'analyze': '/api/analyze (POST)',
            'chat': '/api/chat (POST)'
        }
    })

@app.route('/api/cereals')
def get_cereals():
    """API endpoint to get cereal list."""
    cereals = load_cereals()
    return jsonify(cereals)

@app.route('/api/search-product', methods=['POST'])
def search_product():
    """Search for product ingredients online using AI."""
    try:
        data = request.get_json()
        product_name = data.get('product_name', '').strip()
        
        if not product_name:
            return jsonify({
                'success': False,
                'error': 'Product name is required'
            }), 400
        
        print(f"🔍 Searching for ingredients: {product_name}")
        
        # Use OpenAI to search for ingredients
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.environ.get('OPENAI_API_KEY')
        )
        
        search_prompt = f"""You are a food product information assistant. 
        
Find the complete ingredient list for: "{product_name}"

IMPORTANT INSTRUCTIONS:
1. If you know the actual ingredient list for this specific product, provide it
2. The ingredients should be the exact list from the product packaging
3. If you're not certain or the product doesn't exist, respond with: "PRODUCT_NOT_FOUND"
4. Only provide real, verified ingredients - do not make up ingredients

Respond in this format:
If found: Just list the ingredients separated by commas (e.g., "Sugar, Cocoa, Milk, etc.")
If not found: Respond exactly with: PRODUCT_NOT_FOUND

Product to search: {product_name}
Ingredients:"""
        
        response = llm.invoke(search_prompt)
        ingredients_text = response.content.strip()
        
        print(f"   AI Response: {ingredients_text[:100]}...")
        
        # Check if product was found
        if "PRODUCT_NOT_FOUND" in ingredients_text.upper() or len(ingredients_text) < 10:
            return jsonify({
                'success': False,
                'found': False,
                'message': f'Could not find ingredient information for "{product_name}" online. Please enter ingredients manually.'
            })
        
        # Product found with ingredients
        print(f"   ✅ Found ingredients!")
        
        return jsonify({
            'success': True,
            'found': True,
            'product_name': product_name,
            'ingredients': ingredients_text,
            'message': f'Found ingredients for {product_name}!'
        })
        
    except Exception as e:
        print(f"   ❌ Error searching: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'found': False,
            'error': str(e),
            'message': 'Error searching for product. Please enter ingredients manually.'
        }), 500

@app.route('/api/configure', methods=['POST'])
def configure_api_keys():
    """Configure API keys and initialize the RAG system.
    
    NOTE: This endpoint is now deprecated in favor of environment variables.
    The system auto-initializes using env vars on startup.
    This is kept for backward compatibility.
    """
    global system_initialized
    
    # If system is already initialized via env vars, just return success
    if system_initialized:
        return jsonify({
            'success': True,
            'message': 'System already initialized using environment variables',
            'retrieval_strategy': current_retrieval_strategy
        })
    
    # Try to initialize from environment variables
    if initialize_system():
        return jsonify({
            'success': True,
            'message': 'System initialized successfully using environment variables',
            'retrieval_strategy': current_retrieval_strategy
        })
    else:
        return jsonify({
            'success': False,
            'error': 'System initialization failed. Please check environment variables (OPENAI_API_KEY, LANGCHAIN_API_KEY) are set in Render dashboard.',
            'error_type': 'ConfigurationError'
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_ingredients():
    """Analyze ingredients for a cereal product."""
    global ingredient_analyzer
    
    try:
        # Check if system is initialized
        if ingredient_analyzer is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized. Please configure API keys first.'
            }), 400
        
        data = request.get_json()
        cereal_name = data.get('cereal_name')
        ingredients = data.get('ingredients')
        generate_video = data.get('generate_video', True)  # New parameter
        
        if not cereal_name or not ingredients:
            return jsonify({
                'success': False,
                'error': 'Missing cereal_name or ingredients'
            }), 400
        
        print(f"Analyzing ingredients for: {cereal_name}")
        
        # Perform analysis
        analysis = ingredient_analyzer.analyze_ingredients(cereal_name, ingredients)
        
        result = {
            'success': True,
            'cereal_name': cereal_name,
            'ingredients': ingredients,
            'analysis': analysis
        }
        
        # Generate video explanation with D-ID
        if generate_video:
            try:
                from backend.video_generator import VideoGenerator
                video_gen = VideoGenerator()
                video_result = video_gen.create_explanation_video(analysis, cereal_name)
                result['video'] = video_result
            except Exception as e:
                print(f"⚠️  Video generation failed: {str(e)}")
                result['video'] = {
                    'success': False,
                    'error': str(e),
                    'script': '',
                    'type': 'video'
                }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status')
def get_status():
    """Check if the RAG system is initialized."""
    global system_initialized
    
    # Try to auto-initialize if not already initialized
    if not system_initialized:
        initialize_system()
    
    return jsonify({
        'initialized': system_initialized,
        'has_api_keys': bool(api_keys),
        'auto_configured': True  # Indicates using env vars
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chatbot questions about ingredients."""
    global ingredient_analyzer
    
    try:
        # Check if system is initialized
        if ingredient_analyzer is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized. Please configure API keys first.'
            }), 400
        
        data = request.get_json()
        cereal_name = data.get('cereal_name')
        ingredients = data.get('ingredients')
        question = data.get('question')
        previous_analysis = data.get('previous_analysis', '')
        chat_history = data.get('chat_history', [])
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Missing question'
            }), 400
        
        print(f"Chat question for {cereal_name}: {question}")
        
        # Import ChatOpenAI
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        
        # Create chat LLM
        chat_llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_keys['openai_api_key'],
            temperature=0.7
        )
        
        # Build conversation context
        history_text = ""
        if len(chat_history) > 1:  # More than just the initial greeting
            history_text = "\n\nPrevious conversation:\n"
            for msg in chat_history[-4:]:  # Last 4 messages for context
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if role == 'user':
                    history_text += f"User: {content}\n"
                else:
                    history_text += f"Assistant: {content}\n"
        
        # Create chat prompt
        chat_prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant specializing in food ingredients and nutrition for children. 

You have already analyzed this product:
Product: {cereal_name}
Ingredients: {ingredients}

Previous Analysis:
{previous_analysis}
{history}

User Question: {question}

Provide a helpful, clear, and concise answer based on the analysis and your knowledge of food ingredients. 
Be friendly and conversational. If the question is about something not covered in the analysis, 
use your knowledge about food ingredients to provide accurate information.

Keep your response focused and under 200 words unless more detail is specifically requested.
""")
        
        # Format and invoke
        messages = chat_prompt.format_messages(
            cereal_name=cereal_name,
            ingredients=ingredients,
            previous_analysis=previous_analysis,
            history=history_text,
            question=question
        )
        
        response = chat_llm.invoke(messages)
        
        return jsonify({
            'success': True,
            'answer': response.content
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    # Use PORT environment variable for deployment (Render, Railway, etc.)
    # Default to 5001 for local development
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"Starting Flask server on port {port}...")
    app.run(debug=debug, host='0.0.0.0', port=port)

