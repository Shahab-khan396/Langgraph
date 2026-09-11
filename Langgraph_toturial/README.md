# LangGraph with OpenRouter

Install the project dependencies with `uv sync`, then create a `.env` file:

```dotenv
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

Run the example with:

```bash
uv run python main.py
```

`OPENROUTER_MODEL` is optional. Use any OpenRouter model that supports tool
calling, such as `openai/gpt-4.1-mini`.