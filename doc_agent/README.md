## docs agent

借用多段翻译的思路处理STT文本， 并输出成最终稿；

### GPTs 实现

https://chatgpt.com/g/g-uBhKUJJTl-ke-ji-wen-zhang-fan-yi



### 代码实现

借用了[translation-agent](https://github.com/andrewyng/translation-agent/tree/main)

其逻辑：

```mermaid
graph TD
    A[translate] --> B{num_tokens_in_text < max_tokens}
    B -- Yes --> C[one_chunk_translate_text]
    B -- No --> D[caculate_chunk_size]
    D --> E[RecursiveCharacterTextSplitter.from_tiktoken_encoder]
    E --> F[multichunk_translation]
    F --> G[multichunk_initial_translation]
    G --> H[Translation Prompt]
    H --> I[get_completion]
    I --> J[translation_chunks]
    J --> K[multichunk_reflect_on_translation]
    K --> L[Reflection Prompt]
    L --> M[get_completion]
    M --> N[reflection_chunks]
    N --> O[multichunk_improve_translation]
    O --> P[Improvement Prompt]
    P --> Q[get_completion]
    Q --> R[translation_2_chunks]
    R --> S[join translation_2_chunks]
    S --> F
    F --> T[final_translation]

```