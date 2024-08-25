# Install dependencies using uv
install:
	uv sync --frozen

activate:
	. .venv/bin/activate

deactivate:
	deactivate

install-dev:
	uv install --dev

# Run the bot
run:
	uv run python main.py

# Run linting
lint:
	uv run ruff check .
