## Problem Statement

E-commerce and product comparison platforms struggle to generate rich, structured product information and meaningful comparisons at scale. Manually creating product pages with FAQs, content blocks, and comparison analyses is time-consuming and error-prone. Businesses need an automated solution that can:

- Parse structured product data and convert it into richly formatted product pages.
- Generate contextual FAQs from product information without manual effort.
- Compare multiple products automatically and provide clear, actionable insights.
- Maintain data consistency and formatting across all generated outputs.
- Provide a scalable, maintainable, and orchestrated workflow using modern agentic frameworks.

This project addresses these challenges by providing a **LangGraph-based agentic pipeline** that automates content generation, comparison, and structuring using LLM integration.

---

## Solution Overview

This Project is an intelligent **LangGraph-powered agentic pipeline** that generates structured product pages, FAQs, and product comparison results from a simple JSON template. It reads two product entries, parses them into internal product objects, generates enriched content blocks and FAQ items (via LLM integration with Mistral AI), assembles comprehensive product pages, and produces a detailed comparison summary between the two products. All outputs are JSON files placed in the `output/` folder.

**Architecture**: Built on LangGraph's StateGraph framework, where each agent is implemented as a node in a directed acyclic graph (DAG). State is shared across all nodes via a TypedDict-based state management system. The pipeline leverages Annotated state fields with reducer functions to handle concurrent writes during parallel node execution.

Key capabilities:
- **Product Parsing**: Convert raw JSON product data into structured Product objects.
- **Parallel Processing**: Execute independent product parsing tasks simultaneously using LangGraph's DAG structure.
- **Content Generation**: Automatically create content blocks (summaries, benefits, usage instructions, ingredients, side effects, and pricing information).
- **FAQ Generation**: Use Mistral AI via LangChain to generate contextual Q&A pairs based solely on product data.
- **Page Assembly**: Merge product information with generated content into complete product pages.
- **Product Comparison**: Compare two products using AI-driven analysis to provide meaningful insights and recommendations.
- **Orchestrated Execution**: Leverage LangGraph's node-based execution with state management for robust, scalable pipelines.

---

## Scopes and Assumptions

**Scope:**
- The pipeline processes exactly two products per run (input from `template.json`).
- Generates FAQs and content blocks for the first product (Product A) only.
- Produces a comparison analysis between the two products.
- Outputs are JSON files saved to the `output/` directory.
- Integrates with Mistral AI's LLM via LangChain ChatMistralAI for intelligent content and comparison generation.
- Supports skin care and beauty products (as per the example template).
- Uses LangGraph for workflow orchestration with node-based execution and state management.

**Out of Scope:**
- Real-time or streaming pipeline execution.
- Database integration or persistence layers.
- Web UI or REST API (currently CLI-only).
- Multi-language support (English only).
- Product image processing or metadata beyond JSON fields.

**Assumptions:**
- Input template (`template.json`) contains at least two well-formed product entries with required fields.
- All product data is present; missing or malformed fields may produce incomplete or odd outputs.
- Mistral API key is available and valid (required for FAQ and comparison generation).
- Network connectivity is available for LLM API calls.
- Python 3.10+ is available in the runtime environment.
- The `/output` directory is writable by the application.
- LLM responses follow the expected JSON structure (see Contracts & Data Shapes section).

---

## System Design

### Architecture Overview

The system is built on **LangGraph's StateGraph framework**, where each step in the pipeline is implemented as a node in a directed acyclic graph (DAG). All computation is orchestrated through shared state (a TypedDict called `PipelineState`), promoting modularity, maintainability, and scalability.

**Core Architecture:**
- **Framework**: LangGraph (StateGraph-based)
- **LLM Integration**: LangChain + ChatMistralAI for intelligent content generation
- **State Management**: TypedDict-based `PipelineState` shared across all nodes
- **Execution Model**: Node-based with conditional routing and error handling

**Core Components (All in main.py):**

1. **State Definition** (`PipelineState`):
   - `template`: list of product dictionaries
   - `product_a`, `product_b`: parsed product dictionaries
   - `faq_a`: generated FAQ data
   - `content_a`: generated content blocks
   - `product_page`: assembled product page
   - `comparison`: comparison analysis result
   - `error`: error message tracking

2. **LangGraph Nodes** (7 nodes total):
   - `load_template_node` — Load and validate template.json
   - `parse_product_a_node` — Parse Product A into structured Product object
   - `parse_product_b_node` — Parse Product B into structured Product object
   - `generate_content_blocks_node` — Create content blocks (summary, benefits, usage, ingredients, side effects, price)
   - `generate_faq_node` — Generate FAQs using LangChain + ChatMistralAI
   - `assemble_product_page_node` — Merge product, content, and FAQ data
   - `compare_products_node` — Compare two products using LangChain + ChatMistralAI

3. **Workflow Control & State Reducers**:
   - `PipelineState` — TypedDict with Annotated fields using `keep_first()` reducer for concurrent write safety
   - `build_pipeline_graph()` — Constructs the StateGraph with 7 nodes and declarative edge definitions
   - Reducer function `keep_first()` — Handles concurrent writes to state fields during parallel node execution

4. **Node Functions** (in main.py):
   - `load_template_node(state)` — Entry point; loads and validates template.json
   - `parse_product_a_node(state)` — Calls ParserAgent.run_product_a() (Branch A)
   - `parse_product_b_node(state)` — Calls ParserAgent.run_product_b() (Branch B)
   - `generate_content_blocks_node(state)` — Calls ContentBlockAgent.run()
   - `generate_faq_node(state)` — Calls QuestionGenerationAgent.run(); saves output
   - `assemble_product_page_node(state)` — Calls PageAssemblerAgent.run(); saves output
   - `compare_products_node(state)` — Calls ComparisonAgent.run(); saves output

5. **Static Files**:
   - `template.json` — Example input with two product records
   - `requirements.txt` — Python dependencies (LangGraph, LangChain, mistralai, etc.)
   - `output/` — Directory for generated JSON artifacts


**Execution Sequence:**

1. **load_template_node** — Loads template.json, validates 2+ products, populates `state['template']`
2. **parse_product_a_node & parse_product_b_node** (Parallel) — Both execute simultaneously:
   - parse_product_a: Extracts first product → `state['product_a']`
   - parse_product_b: Extracts second product → `state['product_b']`
3. **generate_content_blocks_node** — Creates content structures for Product A → `state['content_a']`
4. **generate_faq_node** — Calls Mistral AI to generate FAQs → `state['faq_a']` + saves to `output/faq.json`
5. **assemble_product_page_node** — Merges product_a + content_a + faq_a → `state['product_page']` + saves to `output/product_page.json`
6. **compare_products_node** (Convergence) — Waits for both branches, calls Mistral AI to compare → `state['comparison']` + saves to `output/comparison_page.json`
7. **END** — Pipeline completes

**State Mutations Along Pipeline:**
1. `load_template_node`: Populates `state['template']`
2. `parse_product_a_node`: Populates `state['product_a']` (Parallel)
3. `parse_product_b_node`: Populates `state['product_b']` (Parallel)
4. `generate_content_blocks_node`: Populates `state['content_a']`
5. `generate_faq_node`: Populates `state['faq_a']` and saves to `output/faq.json`
6. `assemble_product_page_node`: Populates `state['product_page']` and saves to `output/product_page.json`
7. `compare_products_node`: Populates `state['comparison']` and saves to `output/comparison_page.json`


### LangGraph-LangChain Integration

**LangChain Components Used:**
- `ChatMistralAI`: LLM client for FAQ and comparison generation
- `HumanMessage`: Message type for LLM prompts
- Structured prompting for JSON-based outputs from the LLM

**Benefits of This Architecture:**
- **Declarative Workflow**: Define graph edges declaratively (clearer intent than ThreadPoolExecutor)
- **Built-in Logging**: LangGraph provides execution tracing and debugging
- **Easy Extension**: Add new nodes or modify edges without changing node implementations
- **Error Isolation**: Each node's error is caught and propagated through state; pipeline can continue gracefully
- **State Persistence**: Full state snapshot at each step allows resumption and debugging

### Dependencies & Environment

**Primary Dependencies** (see `requirements.txt`):
- `python-dotenv>=1.0.0` — Load environment variables from `.env` file
- `requests>=2.31.0` — HTTP library (used by mistralai)
- `mistralai>=0.0.11` — Mistral AI Python SDK (used internally by LangChain)
- `langgraph>=0.0.1` — Graph execution framework for agentic workflows
- `langchain>=0.1.0` — Core LLM/RAG framework
- `langchain-mistralai>=0.0.1` — LangChain integration for Mistral AI
- `langchain-core>=0.1.0` — Core LangChain types and interfaces

**Python Version:**
- Python 3.10+ (developed and tested on 3.10–3.11)
- Requires Python's `typing.TypedDict` from the standard library

**Environment Variables:**
- `MISTRAL_API_KEY` — Required for `generate_faq_node` and `compare_products_node` to invoke the Mistral LLM
- Create a `.env` file in the project root with: `MISTRAL_API_KEY=your_api_key_here`
- Alternatively, set the environment variable in your shell

## Run / Quickstart

1. Create and activate a virtual environment (recommended):

	- Windows (PowerShell):
	  - `python -m venv .venv`
	  - `.\.venv\Scripts\Activate.ps1`

2. Install dependencies:

	- `pip install -r requirements.txt`

3. Provide the Mistral API key (if you plan to use the LLM agents):

	- Create a `.env` file in the project root with:
	  ```
	  MISTRAL_API_KEY=your_api_key_here
	  ```
	- Or set the environment variable in your shell

4. Confirm `template.json` contains at least two product entries. The repository includes an example `template.json`.

5. Run the pipeline:

	- `python main.py`

6. Inspect outputs in `output/`:
	- `faq.json` — FAQ data generated for Product A
	- `product_page.json` — Complete product page (product + content + FAQ)
	- `comparison_page.json` — Comparison analysis of Product A vs B

**Notes:**
- When LLM calls are invoked and the key is missing, those nodes log a warning and return empty results; the pipeline continues execution.
- Check the console logs for detailed execution trace and any errors.
- LangGraph provides detailed logging of node execution order and state changes.

---

## Example (What to Expect)

### Output Structure

**faq.json** (from `generate_faq_node`):
```json
{
  "FAQs": [
    {
      "Id": 1,
      "Question": "What is the concentration of Vitamin C in this product?",
      "Answer": "This product contains 10% Vitamin C as specified in the formulation."
    },
    ...
  ]
}
```

**product_page.json** (from `assemble_product_page_node`):
```json
{
  "id": 1234567,
  "product_name": "GlowBoost Vitamin C Serum",
  "summary_block": "GlowBoost Vitamin C Serum with 10% Vitamin C is suitable for oily, combination skin and helps with brightening.",
  "benefits_block": [
    {
      "benefit": "Brightening",
      "explanation": "This product supports brightening based on the provided product details."
    }
  ],
  "usage_block": [
    {
      "step_number": 1,
      "instruction": "Apply 2–3 drops in the morning before sunscreen"
    }
  ],
  ...
}
```

**comparison_page.json** (from `compare_products_node`):
```json
{
  "Product A": "GlowBoost Vitamin C Serum is a 10% Vitamin C serum...",
  "Product B": "Aqualogica Vitamin C Serum is a 15% Vitamin C serum...",
  "Comparison": [
    {
      "point": "Vitamin C Concentration",
      "detail": "...",
      "conclusion": "..."
    }
  ],
  "Recommendation": "Choose Product A if... Choose Product B if..."
}
```

---

## File Map

- `main.py` — Complete pipeline with LangGraph nodes and state management (all-in-one)
- `template.json` — Sample input with two product entries
- `requirements.txt` — Python dependencies with langgraph, langchain, langchain-mistralai
- `.env.example` (optional) — Template for environment variables
- `output/` — Directory for generated JSON outputs
- `docs/projectdocumentation.md` — This comprehensive documentation
- `docs/pipeline_flow_diagram.md` — The DAG of the workflow

---

### Note: Mistral API Key is free to generate and use. The model for the LLM is also by-default added so you must only plug-in the right api key in the .env file.