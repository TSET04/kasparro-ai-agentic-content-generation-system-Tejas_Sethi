                              START
                                ↓
                    ┌───────────────────────┐
                    │  load_template_node   │
                    │ (Load template.json)  │
                    └───────────┬───────────┘
                                ↓
                    ┌───────────────────────┐
                    │  PARALLEL BRANCHES    │
                    └─────┬─────────────┬───┘
                          ↓             ↓
            ┌─────────────────────┐  ┌────────────────────┐
            │ parse_product_a_node│  │parse_product_b_node| 
            │ (Parse Product A)   │  │ (Parse Product B)  |
            └──────────┬──────────┘  └────────┬───────────┘
                       ↓                      ↓
         ┌─────────────────────────┐         │
         │generate_content_blocks_ │         │
         │       node              │         │
         │(Content for Product A)  │         │
         └────────────┬────────────┘         │
                      ↓                      │
         ┌─────────────────────────┐         │
         │  generate_faq_node      │         │
         │ (FAQ for Product A)     │         │
         └────────────┬────────────┘         │
                      ↓                      │
         ┌─────────────────────────┐         │
         │assemble_product_page_   │         │
         │      node               │         │
         │(Merge A data)           │         │
         └────────────┬────────────┘         │
                      │                      │
                      └──────────┬───────────┘
                                 ↓
                    ┌─────────────────────────┐
                    │ compare_products_node   │
                    │(Compare A & B with LLM) │
                    └────────────┬────────────┘
                                 ↓
                                END
