# ReAct Paper Implementation

A hands-on implementation of the paper **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (Yao et al., 2022).

This repo is purely a learning project. The goal isn't to build something production-ready — it's to deeply understand *why* ReAct works by implementing and comparing it against other prompting styles from scratch.

---

## What is ReAct?

ReAct is a prompting framework that interleaves **reasoning** (thinking through a problem) and **acting** (using tools like search) in a loop. The key insight from the paper is that combining thought and action outperforms doing either alone.

The loop looks like this:

```
Thought  →  Action  →  Observation  →  Thought  →  ...  →  Finish
```

---

## Prompting Styles

Each file in `styles/` implements a different way of prompting the same model (Nemotron Nano on OpenRouter), so I can compare how they behave on the same questions.

| File | Style | Description |
|------|-------|-------------|
| `styles/standard.py` | Standard | Model answers directly from its own knowledge. No tools, no reasoning steps. |
| `styles/c_o_t.py` | Chain-of-Thought | Model reasons step-by-step before answering, but takes no external actions. |
| `styles/actions_only.py` | Acting Only | Model can only use tools (search, lookup, finish). No reasoning or thought steps. |
| `styles/react.py` | ReAct | Full Thought → Action → Observation loop. Combines reasoning with tool use. |

---

## Observations

The `observations/` directory contains my personal notes and findings from running each style against real questions. These are written by me, not generated — just raw thoughts on what I noticed, what failed, and what surprised me.

| File | What it covers |
|------|----------------|
| `observations/acting.md` | How the acting-only agent handles questions — and where it falls short without reasoning |

More observations will be added as I experiment with each style.

---

## Setup

```bash
pip install requests python-dotenv ddgs
```

Create a `.env` file in the root:

```
OPENROUTER_API_KEY=your_key_here
```

Then run any style directly:

```bash
python styles/react.py
python styles/actions_only.py
python styles/c_o_t.py
python styles/standard.py
```

---

## Model

All styles use `nvidia/nemotron-3-nano-30b-a3b:free` via the OpenRouter API. A small free model was a deliberate choice — it's more interesting to see where a weaker model benefits most from structured prompting.
