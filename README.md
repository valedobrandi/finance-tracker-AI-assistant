Finance Tracker — AI Assistant

This repository contains an AI-powered assistant to help track and classify financial transactions. The primary goal is to automate the tagging of transaction rows in CSV files using OpenAI models via LangChain.

This README focuses on the backend (scripts, dependencies, and how to run it).

## Backend overview

- Type: batch/worker script for tagging CSV transactions using a language model.
- Location: `backend/`
- Main file: `backend/src/main.py` — reads example CSVs, invokes the model, and writes a tagged CSV.
- Example tables: `backend/tables/09_2025.csv`, `backend/tables/10_2025_untagged.csv`, output: `backend/tables/10_2025_tagged.csv`.

The script compares a set of labelled examples against an unlabelled CSV and asks the model to return lines in the format `index:tag` (one line per entry). The script then applies the returned tags and writes a tagged CSV.

## Technologies & dependencies

- Python 3.8+ (recommended)
- Pandas — CSV and table handling
- LangChain (packages used in this project): `langchain-core`, `langchain-openai`, `langchain-text-splitters`
- OpenAI (via LangChain client)
- Docker / Docker Compose (containers for running the backend)

Dependencies are listed in `backend/requirements.txt`.

## Component contract (backend)

- Input: CSV files containing transaction columns. One CSV should be an examples file with a `tag` column and another the unlabelled CSV to process.
- Output: A CSV with a populated tag column (e.g. `10_2025_tagged.csv`).
- Errors/limits: The script expects each model response line to strictly follow `index:tag`. Responses that don't match are ignored.

Edge cases / considerations:
- Lines that reference indices not present in the input CSV are ignored.
- If the model returns a tag not present in the examples, the script can write `unknown` (the prompt instructs the model to use `unknown` when no match is found) or record what the model returned.
- Large datasets may require batching, pagination or rate limiting to avoid API limits.

## Local setup & run

1. Create and activate a virtual environment (optional, recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Set the required environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

4. Run the tagging script:

```bash
python backend/src/main.py
```

Notes:
- The script currently reads/writes files under `/app/src/tables/...` when running inside the container. When running locally (outside the container), either adjust the paths in the code or run from the repository root so relative paths match your environment.

## Running with Docker / Docker Compose

The repository includes a `Dockerfile` in `backend/` and a `docker-compose.yml` at the project root to orchestrate containers.

Examples:

```bash
# Build and run with Docker Compose (rebuilds images):
docker-compose up --build

# Or run only the backend service (if a 'backend' service exists in docker-compose):
docker-compose up --build backend
```

Before starting with Docker, ensure the `OPENAI_API_KEY` is available to the container (through an `.env` file, the system's environment, or configured in `docker-compose.yml`).

## Relevant file structure

- `backend/`
	- `Dockerfile` — image to run the backend
	- `requirements.txt` — backend Python dependencies
	- `src/main.py` — main tagging script
	- `tables/` — example and output CSVs

- `finance-tracker-frontend/` — frontend code (not covered here)

## Improvements / next steps

- Extract tagging logic into reusable functions/modules and add unit tests (e.g., tests that mock model responses and validate behavior).
- Add batching/queue support to process large CSVs reliably.
- Optionally expose the functionality as an HTTP service (FastAPI/Flask) to receive CSVs and return results.
- Normalize/validate model-returned tags against a controlled vocabulary.

## Contact

For questions or contributions, please open an issue or a pull request in this repository.
