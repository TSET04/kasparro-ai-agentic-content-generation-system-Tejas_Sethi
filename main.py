import os
import json
import logging
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

# LanGraph Nodes
from agents.parser import ParserAgent
from agents.content_block import ContentBlockAgent
from agents.question_gen import QuestionGenerationAgent
from agents.page_assembler import PageAssemblerAgent
from agents.comparison import ComparisonAgent

load_dotenv()

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# STATE DEFINITION - TypedDict for LangGraph state management with Annotated
def keep_first(existing, new):
    """Reducer: Keep existing value (first write wins), ignore concurrent updates"""
    return existing if existing else new
class PipelineState(TypedDict):
    """Shared state across all LangGraph nodes with Annotated fields for concurrent writes"""
    template: Annotated[list, keep_first]
    product_a: Annotated[dict, keep_first]      
    product_b: Annotated[dict, keep_first]      
    faq_a: Annotated[dict, keep_first]          
    content_a: Annotated[dict, keep_first]      
    product_page: Annotated[dict, keep_first]   
    comparison: Annotated[dict, keep_first]     
    error: Annotated[str | None, keep_first]    

# UTILITY FUNCTIONS

def save_json(data: dict, path: str) -> None:
    """Safe JSON save utility"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved JSON: {path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {path}: {e}")

# Function for Node load_template
def load_template_node(state: PipelineState) -> PipelineState:
    """Load and validate template.json"""
    logger.info("Template Load Node Loaded successfully")
    
    try:
        with open('template.json', 'r', encoding='utf-8') as f:
            template = json.load(f)
        
        if len(template) < 2:
            error_msg = "Template JSON must contain at least 2 products."
            logger.error(error_msg)
            state['error'] = error_msg
            return state
        
        state['template'] = template
        logger.info("Template loaded successfully with 2 products")
        return state
    
    except Exception as e:
        error_msg = f"Failed to load template.json: {e}"
        logger.error(error_msg)
        state['error'] = error_msg
        return state

# Function for parse product_a node
def parse_product_a_node(state: PipelineState) -> PipelineState:
    """Parse Product A using ParserAgent"""
    parser = ParserAgent()
    return parser.run_product_a(state)

# Function for parse product_b node
def parse_product_b_node(state: PipelineState) -> PipelineState:
    """Parse Product B using ParserAgent"""
    parser = ParserAgent()
    return parser.run_product_b(state)

# Function for content block node
def generate_content_blocks_node(state: PipelineState) -> PipelineState:
    """Generate content blocks using ContentBlockAgent"""
    content_agent = ContentBlockAgent()
    return content_agent.run(state)

# Function for generating faq node
def generate_faq_node(state: PipelineState) -> PipelineState:
    """Generate FAQ using QuestionGenerationAgent"""
    faq_agent = QuestionGenerationAgent()
    state = faq_agent.run(state)
    
    # Save FAQ to output
    if state.get('faq_a'):
        save_json(state['faq_a'], os.path.join('output', 'faq.json'))
    
    return state

# Function for product page assemble node
def assemble_product_page_node(state: PipelineState) -> PipelineState:
    """Assemble product page using PageAssemblerAgent"""
    page_agent = PageAssemblerAgent()
    state = page_agent.run(state)
    
    # Save product page to output
    if state.get('product_page'):
        save_json(state['product_page'], os.path.join('output', 'product_page.json'))
    
    return state

# Function for comparing products node
def compare_products_node(state: PipelineState) -> PipelineState:
    """Compare products using ComparisonAgent"""
    compare_agent = ComparisonAgent()
    state = compare_agent.run(state)
    
    # Save comparison to output
    if state.get('comparison'):
        save_json(state['comparison'], os.path.join('output', 'comparison_page.json'))
    
    return state


#LangGraph Workflow with parallel execution
def build_pipeline_graph() -> StateGraph:
    logger.info("Building LangGraph pipeline with parallel execution...")
    
    # Create the state graph
    graph = StateGraph(PipelineState)
    
    # All nodes
    graph.add_node("load_template", load_template_node)
    graph.add_node("parse_product_a", parse_product_a_node)
    graph.add_node("parse_product_b", parse_product_b_node)
    graph.add_node("generate_content_blocks", generate_content_blocks_node)
    graph.add_node("generate_faq", generate_faq_node)
    graph.add_node("assemble_product_page", assemble_product_page_node)
    graph.add_node("compare_products", compare_products_node)
    

    # All Edges
    graph.add_edge(START, "load_template")
    graph.add_edge("load_template", "parse_product_a")
    graph.add_edge("parse_product_a", "generate_content_blocks")
    graph.add_edge("generate_content_blocks", "generate_faq")
    graph.add_edge("generate_faq", "assemble_product_page")
    graph.add_edge("load_template", "parse_product_b")
    graph.add_edge("assemble_product_page", "compare_products")
    graph.add_edge("parse_product_b", "compare_products")
    graph.add_edge("compare_products", END)
    
    logger.info("LangGraph pipeline built with parallel execution:")
    return graph


def main():
    """Main entry point for the pipeline"""
    try:
        # Build the graph
        graph = build_pipeline_graph()
        
        # Compile the graph
        compiled_graph = graph.compile()
        
        # Initialize state
        initial_state: PipelineState = {
            'template': [],
            'product_a': {},
            'product_b': {},
            'faq_a': {},
            'content_a': {},
            'product_page': {},
            'comparison': {},
            'error': None
        }
        
        # Execute the pipeline
        logger.info("Executing pipeline with parallel node execution...")
        final_state = compiled_graph.invoke(initial_state)
        
        if final_state.get('error'):
            logger.critical(f"Pipeline failed: {final_state['error']}")
            return
        
        logger.info("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
        logger.info(f"Output files saved successfully")
    
    except Exception as e:
        logger.critical(f"Pipeline failed unexpectedly: {e}")
        import traceback
        logger.critical(traceback.format_exc())

# Entry Point
if __name__ == "__main__":
    main()
