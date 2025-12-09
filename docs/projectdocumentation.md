## Applied AI Project Documentation

This document describes the AI Applied Agent Project: what it does, how it is organized, how to set it up and run it, and notes for contributors and maintainers. It's written so new developers and users can understand, run, and extend the project.

---

## Problem Statement

E-commerce and product comparison platforms struggle to generate rich, structured product information and meaningful comparisons at scale. Manually creating product pages with FAQs, content blocks, and comparison analyses is time-consuming and error-prone. Businesses need an automated solution that can:

- Parse structured product data and convert it into richly formatted product pages.
- Generate contextual FAQs from product information without manual effort.
- Compare multiple products automatically and provide clear, actionable insights.
- Maintain data consistency and formatting across all generated outputs.

This project addresses these challenges by providing an agent-based pipeline that automates content generation, comparison, and structuring using LLM integration.

---

## Solution Overview

This is an intelligent pipeline that generates structured product pages, FAQs, and product comparison results from a simple JSON template. It reads two product entries, parses them into internal product objects, generates enriched content blocks and FAQ items (via LLM integration with Mistral AI), assembles comprehensive product pages, and produces a detailed comparison summary between the two products. All outputs are JSON files placed in the `output/` folder.

Key capabilities:
- **Product Parsing**: Convert raw JSON product data into structured Product objects.
- **Content Generation**: Automatically create content blocks (summaries, benefits, usage instructions, ingredients, side effects, and pricing information).
- **FAQ Generation**: Use Mistral AI to generate contextual Q&A pairs based solely on product data.
- **Page Assembly**: Merge product information with generated content into complete product pages.
- **Product Comparison**: Compare two products using AI-driven analysis to provide meaningful insights and recommendations.
- **Parallel Processing**: Leverage concurrent execution for improved performance.

---

## Scopes and Assumptions

**Scope:**
- The pipeline processes exactly two products per run (input from `template.json`).
- Generates FAQs and content blocks for the first product (Product A) only.
- Produces a comparison analysis between the two products.
- Outputs are JSON files saved to the `output/` directory.
- Integrates with Mistral AI's LLM for intelligent content and comparison generation.
- Supports skin care and beauty products (as per the example template).

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

The system is built on a modular, agent-based architecture where each agent is responsible for a single, well-defined task in the pipeline. This design promotes reusability, testability, and extensibility.

**Core Components:**
- `main.py` — pipeline orchestration and entry point.
- `agents/` — modular agents implementing each pipeline step:
  - `parser.py` — converts input product JSON into a Product object.
  - `content_block.py` — creates content blocks (summary, benefits, usage, ingredients, side effects, price).
  - `question_gen.py` — generates FAQs using Mistral AI (LLM) and the product data.
  - `page_assembler.py` — assembles the final product JSON combining product fields, content blocks and FAQs.
  - `comparison.py` — compares two products using the Mistral AI client and returns a JSON comparison.
- `template.json` — example input file containing two product records used by the pipeline.
- `requirements.txt` — Python dependencies.
- `output/` — pipeline artifacts (e.g., `faq.json`, `product_page.json`, `comparison_page.json`).

### Data Flow

The pipeline follows a sequential and parallel processing model:

1. `main.py` loads `template.json` (expects at least 2 products).
2. Parser agents convert each product entry to a `Product` object (executed in parallel using ThreadPoolExecutor).
3. For product A, the pipeline runs:
	- FAQ generation (`QuestionGenerationAgent`) — uses the Mistral client and returns JSON FAQs.
	- Content generation (`ContentBlockAgent`) — creates structured content blocks.
	- Page assembly (`PageAssemblerAgent`) — merges product fields and generated content into a product page JSON.
4. Comparison (`ComparisonAgent`) uses both parsed products to produce a comparison JSON (via Mistral).
5. Results (if successful) are saved under `output/`.

### Concurrency Model

- `main.py` uses `ThreadPoolExecutor` to parallelize the two ParserAgent runs and the FAQ/content generation steps.
- This allows parsing of both products and content generation to occur simultaneously, improving overall pipeline performance.

### Contracts & Data Shapes

**Product Input Shape** (from `template.json`) — expected keys:
- `product_name`, `concentration`, `skin_type` (list), `key_ingredients` (list), `benefits` (list), `how_to_use`, `side_effects`, `price`.

**Internal Product Object** (Product class in `parser.py`):
- Attributes: `name`, `concentration`, `skin_type`, `ingredients`, `use`, `benefits`, `price`, `side_effects`.

**ContentBlockAgent Output:**
- `summary_block`: string
- `benefits_block`: list of {"benefit","explanation"}
- `usage_block`: list of steps {"step_number","instruction"}
- `ingredients_block`: list of {"ingredient"}
- `side_effects_block`: {"description","severity"}
- `price_block`: {"value","currency"}

**LLM Output Contracts:**
- QuestionGenerationAgent and ComparisonAgent produce JSON by asking the Mistral LLM to return a properly formatted JSON string; the code then parses that returned string into Python objects.

**Environment Contract:**
- The LLM-based agents require a Mistral API client and a valid API key in the environment variable `MISTRAL_API_KEY`. If this is not present or the API call fails, those agents will raise or return errors; the pipeline attempts to handle some failures gracefully (e.g., proceed with empty FAQ content).

### Dependencies & Environment

**Primary Dependencies** (see `requirements.txt`):
- python-dotenv — load environment variables from `.env` (optional but convenient)
- requests — used by some libraries
- mistralai — Mistral AI client used by LLM agents

**Python Version:**
- The repo was developed for Python 3.10+ (tested with 3.10–3.11). Use the system or virtualenv Python.

**Environment Variables:**
- `MISTRAL_API_KEY` — required for `question_gen.py` and `comparison.py` agents when you want to call the remote Mistral API. You can create a `.env` file with this key for convenience.

---

## Run / Quickstart

1. Create and activate a virtual environment (recommended):

	- Windows (PowerShell):
	  - python -m venv .venv 
      - .venv\\Scripts\\Activate

2. Install dependencies:

	- pip install -r requirements.txt

3. Provide the Mistral API key (if you plan to use the LLM agents):

	- create a `.env` file with:

	  MISTRAL_API_KEY=your_api_key_here

	- or set the environment variable in your shell.


4. Confirm `template.json` contains at least two product entries. The repository includes an example `template.json`.

5. Run the pipeline:

	- python main.py

6. Inspect outputs in `output/`: `faq.json`, `product_page.json`, `comparison_page.json` (if each step succeeded).

Notes:
- When LLM calls are used and the key is missing, those agents will fail; `main.py` contains some handling to continue with empty results where possible but comparison and FAQ will not be generated.

## Example (what to expect)

- `output/product_page.json` — merges the product information with the generated content blocks and FAQs.
- `output/faq.json` — the FAQ object generated by `QuestionGenerationAgent` (expected to be JSON following the prompt's format).
- `output/comparison_page.json` — JSON returned by `ComparisonAgent` with summaries and differences.

## Troubleshooting

- If pipeline exits with "Failed to load template.json": ensure `template.json` is present and valid JSON.
- If LLM agents fail: verify `MISTRAL_API_KEY` is set and the `mistralai` library is installed and configured correctly.
- If outputs are missing keys: check agent implementations for defensive checks and validate `template.json` fields.

## File Map (short)

- `main.py` — pipeline orchestration and entry point
- `template.json` — sample input
- `requirements.txt` — dependency list
- `agents/parser.py` — Product class + parser
- `agents/content_block.py` — builds the content blocks
- `agents/question_gen.py` — calls LLM to create FAQs
- `agents/page_assembler.py` — merges product fields and generated content
- `agents/comparison.py` — calls LLM for product comparison

### Note: Mistral API Key is free to generate and use. Simply generate the key and plug the value in the .env folder. There is NO need to change the Model used for LLM call as it is handled in the code. The used model is free to use.
