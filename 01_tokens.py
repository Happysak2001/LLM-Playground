"""
PROJECT 1 — TOKENS
==================
What is a token?
  A token is the smallest unit of text the model reads and produces.
  It is NOT a word. It is NOT a character. It is a chunk of text
  decided by a "tokenizer" trained to balance vocabulary size vs coverage.

  Rule of thumb: 1 token ≈ 4 characters ≈ 0.75 words (for English text)

Why does it matter?
  1. COST    — APIs charge per token (input + output)
  2. LIMITS  — Every model has a max token limit (context window)
  3. SPEED   — More tokens = slower response
"""

import tiktoken

# tiktoken is OpenAI's tokenizer library.
# Claude uses a different tokenizer, but the CONCEPT is identical.
# "cl100k_base" is the encoding used by GPT-4 / GPT-3.5.
enc = tiktoken.get_encoding("cl100k_base")


def tokenize(text: str) -> dict:
    token_ids = enc.encode(text)
    token_strings = [enc.decode([t]) for t in token_ids]
    return {
        "text": text,
        "token_ids": token_ids,
        "token_strings": token_strings,
        "count": len(token_ids),
    }


def show(result: dict):
    print(f"\nText   : {result['text']!r}")
    print(f"Tokens : {result['token_strings']}")
    print(f"IDs    : {result['token_ids']}")
    print(f"Count  : {result['count']}")
    print("-" * 60)


# ── EXPERIMENT 1: Simple words ──────────────────────────────────────────────
print("=" * 60)
print("EXPERIMENT 1: How common words are tokenized")
print("=" * 60)

words = ["hello", "world", "Python", "ChatGPT", "AI", "tokenization"]
for w in words:
    show(tokenize(w))

# ── EXPERIMENT 2: Long vs rare words ────────────────────────────────────────
print("\n" + "=" * 60)
print("EXPERIMENT 2: Common word vs rare/long word")
print("=" * 60)

show(tokenize("cat"))
show(tokenize("supercalifragilisticexpialidocious"))
show(tokenize("antidisestablishmentarianism"))

# ── EXPERIMENT 3: Spaces and punctuation matter ──────────────────────────────
print("\n" + "=" * 60)
print("EXPERIMENT 3: Spaces change token boundaries")
print("=" * 60)

show(tokenize("token"))
show(tokenize(" token"))   # leading space = different token
show(tokenize("token!"))

# ── EXPERIMENT 4: Code vs prose ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("EXPERIMENT 4: Code vs natural language")
print("=" * 60)

prose = "The quick brown fox jumps over the lazy dog."
code  = "for i in range(10): print(i)"

r1 = tokenize(prose)
r2 = tokenize(code)

print(f"\nProse ({len(prose)} chars): {r1['count']} tokens -> {len(prose)/r1['count']:.1f} chars/token")
print(f"Code  ({len(code)} chars): {r2['count']} tokens -> {len(code)/r2['count']:.1f} chars/token")

# ── EXPERIMENT 5: Real cost calculation ─────────────────────────────────────
print("\n" + "=" * 60)
print("EXPERIMENT 5: Token cost calculator")
print("=" * 60)

# Claude Sonnet 4.6 pricing (as of 2025)
INPUT_PRICE_PER_1M  = 3.00   # USD per 1M input tokens
OUTPUT_PRICE_PER_1M = 15.00  # USD per 1M output tokens

texts = [
    ("Short prompt",     "Summarize this article."),
    ("Medium prompt",    "You are a helpful assistant. The user wants you to summarize the following article in 3 bullet points. Be concise and accurate. Article: " + "word " * 100),
    ("Long document",    "word " * 2000),
]

for label, text in texts:
    count = tokenize(text)["count"]
    cost  = (count / 1_000_000) * INPUT_PRICE_PER_1M
    print(f"\n{label}: {count:,} tokens -> ${cost:.6f} per call")

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)
print("""
1. Tokens != words. Common short words are often 1 token.
   Rare/long words get split into multiple tokens.

2. A leading space changes the token. 'token' and ' token' are different.
   This is why prompts sometimes behave differently with extra whitespace.

3. Code is token-dense. Natural language has more chars per token.

4. Every API call costs tokens. Input tokens + output tokens = total cost.
   Knowing token counts helps you optimize prompts for cost and speed.

5. The model never sees raw text -- it only ever sees a list of integers (token IDs).
   Understanding this explains why models can sometimes struggle with
   character-level tasks like counting letters or reversing strings.
""")
