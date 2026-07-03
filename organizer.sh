
#!/bin/bash

set -e

if [ ! -f .venv ]; then
    echo "Creating virtual environment"
    python3 -m venv .venv
fi  
echo "Activating virtual environment"
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Check if LLM is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed."
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

MODEL_NAME="llama3.1:8b"

echo "Checking model: $MODEL_NAME"

if ! ollama list | grep -q "$MODEL_NAME"; then
    echo "Pulling model: $MODEL_NAME"
    ollama pull "$MODEL_NAME"
else
    echo "Model already available: $MODEL_NAME"
fi

python agents/normalizer.py
