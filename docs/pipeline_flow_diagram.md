PIPELINE FLOW
════════════════════════════════════════════════════════════════

    [START]
       ↓
    [Load template.json]
       ↓
    [Validate: ≥2 products?] ──NO──→ [EXIT with ERROR]
       ↓ YES
    [Extract Product A & B]
       ↓
    [Initialize Agents]
       ↓
    ╔═══════════════════════════════════╗
    ║  STEP 1: Parse Products (Parallel)║
    ║  ParserAgent A  │  ParserAgent B  ║
    ╚═══════════════════════════════════╝
       ↓
    [Validation Check] ──FAIL──→ [EXIT with ERROR]
       ↓ PASS
    ╔═══════════════════════════════════════════════════╗
    ║ STEP 2: Generate FAQ & Content (Parallel)         ║
    ║ QuestionGenerationAgent │ ContentBlockAgent       ║
    ║ → Output: faq.json      │ → Output: content.json  ║
    ╚═══════════════════════════════════════════════════╝
       ↓
    ╔══════════════════════════════════════╗
    ║ STEP 3: Assemble Product Page        ║
    ║ PageAssemblerAgent                   ║
    ║ Input: Product A + FAQ + Content     ║
    ║ → Output: product_page.json          ║
    ╚══════════════════════════════════════╝
       ↓
    ╔═══════════════════════════════════════╗
    ║ STEP 4: Compare Products              ║
    ║ ComparisonAgent                       ║
    ║ Input: Product A + Product B          ║
    ║ → Output: comparison_page.json        ║
    ╚═══════════════════════════════════════╝
       ↓
    [Pipeline Complete]
       ↓
    [EXIT]
