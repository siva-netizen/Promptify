# Promptify
![Promptify Banner](https://capsule-render.vercel.app/api?type=waving&color=0:00BFFF,100:00008B&height=300&section=header&text=Promptify&fontSize=90&fontColor=ffffff)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/siva-netizen/Promptify)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Transform vague ideas into professional engineering specifications using AI agents.**

## Introduction

**Promptify** is an advanced AI-powered extension and cli tool designed to bridge the gap between abstract user intent and concrete technical requirements. It employs a multi-agent architecture (Triage, Critic, Expert, and Prompt Smith) to iteratively refine, critique, and enhance your prompts, delivering production-ready specifications for software projects.

No more back-and-forth. Just **Promptify** and build.

## Features

*   **Multi-Agent Architecture**: 
    *   **Triage Agent**: Understands intent and routes to the right expert.
    *   **Critic Agent**: Identifies gaps, ambiguities, and missing context.
    *   **Expert Agent**: Provides domain-specific architectural advice.
    *   **Prompt Smith**: Synthesizes everything into a perfect final prompt.
*   **Dynamic Model Support**: Switch seamlessly between **Cerebras** (fast/free), **OpenAI** (GPT-4), **Anthropic** (Claude 3.5), or **Local LLMs**.
*   **Interactive CLI & TUI**: Beautiful terminal user interface built with `Textual` and `Rich`.
*   **Flexible Configuration**: Easy YAML-based configuration with environment variable support (`.env`).

## Packages

### [CLI](./cli/)
Python CLI tool for prompt engineering with multi-agent system.

```bash
pip install pfy
```

### [Browser Extension](./extension/)
Chrome and Firefox extensions for seamless prompt refinement.

- [Install from Chrome Web Store](#)
- [Install from Firefox Add-ons](#)

## Repository Structure

- `cli/` - Python CLI package (PyPI)
- `extension/` - Browser extensions (Chrome/Firefox)
- `docs/` - Shared documentation

## Development

### CLI Development
```bash
cd cli
pip install -e .
promptify refine "test query"
```

### Extension Development
```bash
cd extension/chrome
# Load in chrome://extensions (Developer Mode) as "Load unpacked"
```