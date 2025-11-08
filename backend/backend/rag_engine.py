"""
LangGraph-based RAG engine for ingredient analysis.
"""

from typing import List, TypedDict
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph

from backend.config import CHAT_MODEL


class IngredientAnalysisState(TypedDict):
    """State for the ingredient analysis workflow."""
    cereal_name: str
    ingredients: str
    question: str
    context: List[Document]
    analysis: str


class IngredientAnalyzer:
    """LangGraph-based ingredient analyzer using RAG."""
    
    def __init__(self, retriever, openai_api_key: str, retrieval_strategy: str = "naive"):
        """
        Initialize the ingredient analyzer.
        
        Args:
            retriever: Vector store retriever
            openai_api_key: OpenAI API key
            retrieval_strategy: Name of the retrieval strategy being used
        """
        self.retriever = retriever
        self.retrieval_strategy = retrieval_strategy
        self.llm = ChatOpenAI(
            model=CHAT_MODEL,
            api_key=openai_api_key,
            temperature=0.3  # Slightly lower for more consistent analysis
        )
        
        # Create the analysis prompt
        self.analysis_prompt = ChatPromptTemplate.from_template("""
You are a pediatric nutrition expert helping parents understand food ingredients for their children.

You have access to FDA food labeling guidelines and nutritional information. Use this context to provide accurate, evidence-based analysis.

Cereal Product: {cereal_name}
Ingredients List: {ingredients}

Question: {question}

Relevant Guidelines and Information:
{context}

IMPORTANT: Structure your response in the following format:

## VERDICT: [GOOD ✅ or MODERATE ⚠️ or BAD ❌]

**Quick Summary:** [1-2 sentences explaining the verdict]

VERDICT CLASSIFICATION RULES (Apply in order):

**Use BAD ❌ if the product has ANY of these red flags:**
- Artificial colors (Red 40, Yellow 5, Blue 1, etc.)
- Artificial flavors or artificial sweeteners (aspartame, sucralose, etc.)
- Harmful preservatives (BHT, BHA, TBHQ, sodium benzoate with vitamin C)
- High fructose corn syrup (HFCS)
- Partially hydrogenated oils (trans fats)
- Multiple sources of added sugar in first 5 ingredients
- Sugar/sweetener listed as the 1st or 2nd ingredient

**Use MODERATE ⚠️ if:**
- Contains some added sugars (sugar, cane sugar, honey, corn syrup, molasses, etc.) but NOT in first 2 ingredients
- Has some processed ingredients but nothing artificial or harmful
- Contains natural flavors or common preservatives that are generally safe
- Not ideal for daily consumption but okay occasionally

**Use GOOD ✅ if:**
- Primarily whole, natural ingredients with minimal processing
- No added sugars OR natural sweeteners like fruit in reasonable amounts
- No artificial anything
- Safe for regular/daily consumption
- Would be recommended by pediatricians

CRITICAL DECISION LOGIC:
1. First check for BAD red flags → If found, classify as BAD ❌
2. If no red flags, check for added sugars/processing → If found, classify as MODERATE ⚠️
3. If clean and natural → classify as GOOD ✅

---

## Detailed Analysis

### 1. Overall Assessment
Is this product generally safe and healthy for children? Provide a balanced view considering:
- Base ingredients quality
- Presence of added sugars (CRITICAL for classification)
- Artificial vs natural ingredients
- Processing level

### 2. Red Flag Ingredients (Check First!)
**Check for BAD category triggers:**
- Artificial colors (Red 40, Yellow 5, Blue 1, etc.) → Linked to hyperactivity in children
- Artificial flavors/sweeteners → Unnecessary chemicals
- Harmful preservatives (BHT, BHA, TBHQ) → Potential health concerns
- High fructose corn syrup → Worse than regular sugar, linked to obesity
- Trans fats (partially hydrogenated oils) → Harmful to heart health
- If ANY of these are present → Classify as BAD ❌

### 3. Added Sugar Analysis
If no red flags above, then check sugars:
- Does this product contain added sugars? (sugar, cane sugar, brown sugar, honey, corn syrup, molasses, etc.)
- Where in the ingredient list? (1st-2nd ingredient = worse than 5th-6th)
- If sugar is 1st or 2nd ingredient → Often still BAD ❌
- If sugar is present but not dominant → MODERATE ⚠️
- American Heart Association: Children ages 2-18 should have <25g added sugar/day

### 4. Ingredient-by-Ingredient Breakdown
For each ingredient or category of ingredients:
- **Ingredient Name**: Good/Concerning/Harmful
  - Explanation based on nutritional science and FDA guidelines
  - Flag if it's a red flag ingredient (artificial colors, HFCS, etc.)
  - Any specific concerns for children
  - Nutritional benefits (if applicable)

### 5. Key Concerns (Prioritized)
**List in order of severity:**
1. **Red Flag Ingredients**: Artificial colors, HFCS, harmful preservatives (if present)
2. **Added Sugars**: Amount and position in ingredient list
3. **Processing Level**: How processed vs whole food
4. **Other Concerns**: Allergens, sodium, etc.

### 6. Positive Aspects
- Beneficial ingredients and their nutritional value
- Whole grains, fiber, protein, vitamins
- What makes this product have any redeeming qualities (if applicable)

Be honest, clear, and evidence-based. Use BAD ❌ for truly harmful products with red flag ingredients. Use MODERATE ⚠️ for processed foods with added sugars but no dangerous ingredients. Reserve GOOD ✅ for genuinely healthy products.

Remember: Start with the clear VERDICT (GOOD ✅, MODERATE ⚠️, or BAD ❌) and quick summary at the top!
""")
        
        # Build the LangGraph workflow
        self.graph = self._build_graph()
    
    def _retrieve(self, state: IngredientAnalysisState) -> dict:
        """
        Retrieve relevant documents from the knowledge base.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with retrieved context
        """
        retrieved_docs = self.retriever.invoke(state["question"])
        return {"context": retrieved_docs}
    
    def _generate_analysis(self, state: IngredientAnalysisState) -> dict:
        """
        Generate ingredient analysis using LLM.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with analysis
        """
        # Format context from retrieved documents
        context_text = "\n\n".join([
            f"Source {i+1}:\n{doc.page_content}"
            for i, doc in enumerate(state["context"])
        ])
        
        # Generate analysis
        messages = self.analysis_prompt.format_messages(
            cereal_name=state["cereal_name"],
            ingredients=state["ingredients"],
            question=state["question"],
            context=context_text
        )
        
        response = self.llm.invoke(messages)
        return {"analysis": response.content}
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.
        
        Returns:
            Compiled graph
        """
        # Create graph
        graph_builder = StateGraph(IngredientAnalysisState)
        
        # Add nodes
        graph_builder.add_node("retrieve", self._retrieve)
        graph_builder.add_node("analyze", self._generate_analysis)
        
        # Add edges
        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "analyze")
        
        # Compile and return
        return graph_builder.compile()
    
    def analyze_ingredients(self, cereal_name: str, ingredients: str) -> str:
        """
        Analyze ingredients for a cereal product.
        
        Args:
            cereal_name: Name of the cereal product
            ingredients: Comma-separated list of ingredients
            
        Returns:
            Detailed ingredient analysis
        """
        print(f"Using retrieval strategy: {self.retrieval_strategy}")
        
        # Create the question for retrieval
        question = f"""
        Analyze these food ingredients for a children's cereal product: {ingredients}
        
        Consider:
        - Are these ingredients safe for children?
        - Are there any concerning additives, preservatives, or artificial ingredients?
        - What do terms like "Natural Flavors" really mean?
        - Are there any allergens or ingredients that commonly cause issues?
        - What are the nutritional benefits or concerns?
        """
        
        # Initial state
        initial_state = {
            "cereal_name": cereal_name,
            "ingredients": ingredients,
            "question": question,
            "context": [],
            "analysis": ""
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return result["analysis"]

