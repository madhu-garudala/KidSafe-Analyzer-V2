#!/usr/bin/env python3
"""
Generate Pre-computed Analysis Results for All Cereals

This script analyzes all cereals in the database once and stores the results
in a JSON file that can be used by the frontend for instant display.

Run this script whenever:
- You add new cereals to the database
- You change the analysis prompts/logic
- You want to refresh the analysis results
"""

import os
import json
import csv
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

def initialize_system():
    """Initialize the RAG system."""
    print("🚀 Initializing KidSafe Analyzer...")
    
    # Set environment variables
    os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')
    os.environ['LANGCHAIN_API_KEY'] = os.environ.get('LANGCHAIN_API_KEY', '')
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_PROJECT'] = 'KidSafe-Food-Analyzer'
    
    if os.environ.get('COHERE_API_KEY'):
        os.environ['COHERE_API_KEY'] = os.environ.get('COHERE_API_KEY')
    
    # Initialize components
    from backend.vector_store import VectorStoreManager
    from backend.rag_engine import IngredientAnalyzer
    from backend.advanced_retrieval import AdvancedRetrievalManager
    
    print("📚 Loading vector store...")
    vector_store_manager = VectorStoreManager(os.environ['OPENAI_API_KEY'])
    vectorstore = vector_store_manager.load_and_index_documents()
    chunks = vector_store_manager.get_chunks()
    
    print("🔍 Initializing advanced retrieval manager...")
    advanced_retrieval_manager = AdvancedRetrievalManager(
        vectorstore=vectorstore,
        documents=chunks,
        openai_api_key=os.environ['OPENAI_API_KEY'],
        cohere_api_key=os.environ.get('COHERE_API_KEY')
    )
    
    print("⚙️  Setting up ensemble retrieval...")
    use_compression = bool(os.environ.get('COHERE_API_KEY'))
    retriever = advanced_retrieval_manager.get_ensemble_retriever(k=5, use_compression=use_compression)
    
    print("🤖 Initializing ingredient analyzer...")
    ingredient_analyzer = IngredientAnalyzer(
        retriever, 
        os.environ['OPENAI_API_KEY'],
        retrieval_strategy='ensemble'
    )
    
    print("✅ System initialized!\n")
    return ingredient_analyzer

def load_cereals():
    """Load cereals from CSV file."""
    cereals = []
    data_file = Path(__file__).parent / 'Data' / 'cereal.csv'
    
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Brand_Name'):
                cereals.append({
                    'brand': row['Brand_Name'],
                    'ingredients': row.get('Ingredients', '')
                })
    
    return cereals

def analyze_all_cereals(ingredient_analyzer):
    """Analyze all cereals and store results."""
    cereals = load_cereals()
    results = {}
    
    print(f"📊 Analyzing {len(cereals)} cereals...\n")
    
    for i, cereal in enumerate(cereals, 1):
        cereal_name = cereal['brand']
        ingredients = cereal['ingredients']
        
        print(f"[{i}/{len(cereals)}] Analyzing: {cereal_name}")
        
        try:
            # Perform analysis
            analysis = ingredient_analyzer.analyze_ingredients(cereal_name, ingredients)
            
            # Store result
            results[cereal_name] = {
                'cereal_name': cereal_name,
                'ingredients': ingredients,
                'analysis': analysis,
                'success': True
            }
            
            print(f"    ✅ Complete\n")
            
        except Exception as e:
            print(f"    ❌ Error: {str(e)}\n")
            results[cereal_name] = {
                'cereal_name': cereal_name,
                'ingredients': ingredients,
                'analysis': f"Error analyzing this cereal: {str(e)}",
                'success': False
            }
    
    return results

def save_results(results):
    """Save results to JSON file in frontend directory."""
    # Save to frontend public directory
    output_path = Path(__file__).parent.parent / 'frontend' / 'public' / 'precomputed-analyses.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_path}")
    print(f"📦 Total cereals analyzed: {len(results)}")
    print(f"✅ Successful: {sum(1 for r in results.values() if r['success'])}")
    print(f"❌ Failed: {sum(1 for r in results.values() if not r['success'])}")

def main():
    print("=" * 70)
    print("🍎 KidSafe Analyzer - Pre-compute Analysis Results")
    print("=" * 70)
    print()
    
    # Check for API keys
    if not os.environ.get('OPENAI_API_KEY') or not os.environ.get('LANGCHAIN_API_KEY'):
        print("❌ Error: API keys not set!")
        print("   Make sure OPENAI_API_KEY and LANGCHAIN_API_KEY are set in .env file")
        return
    
    # Initialize system
    ingredient_analyzer = initialize_system()
    
    # Analyze all cereals
    results = analyze_all_cereals(ingredient_analyzer)
    
    # Save results
    save_results(results)
    
    print("\n" + "=" * 70)
    print("✅ Pre-computation complete!")
    print("=" * 70)
    print("\n💡 The frontend will now load results instantly from the JSON file.")
    print("   Run this script again whenever you update cereal data or prompts.\n")

if __name__ == '__main__':
    main()

