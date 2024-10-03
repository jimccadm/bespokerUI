# bespokerUI
A simple interface to help analysts experiment with the bespoke-minicheck LLM on Ollama. 

# Yes/No Question Answering App

This Streamlit application uses the Ollama AI model to answer yes/no questions based on provided context with special focus on one LLM that purely generates Yes and No responses, vice typical "chatty" LLM responses. It's designed to work with the `bespoke-minicheck` model but can be adapted for other Ollama models (not recommended, use a proper UI that is not so highly restricted).

## Features

- Uses Ollama AI for question answering (functionality is for bespoke-minicheck testing ONLY).
- Provides yes/no answers based on given context
- Displays debug information including the full prompt and API response
- Shows real-time status of the analysis process
- Supports model refresh and listing of available models

## Prerequisites

- Python 3.7+
- Streamlit
- Ollama (installed and running on your system)
- `bespoke-minicheck` model (or another compatible Ollama model)
- Made on Ubuntu, good luck with other OSes.

## Installation

1. Clone this repository:
   ```bash
   git@github.com:jimccadm/bespokerUI.git
   cd yes-no-question-answering-app
   ```

2. Install the required Python packages:
   ```bash
   pip install streamlit requests ollama
   ```

3. Ensure Ollama is installed and running on your system.

4. Make sure you have the `bespoke-minicheck` model installed:
   ```bash
   ollama pull bespoke-minicheck
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run st_bespokerUI.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. In the app:
   - The left column shows the Ollama configuration and available models.
   - The middle column is where you input your context and question.
   - The right column displays debug information after running a query.

4. Enter your context in the first text area.

5. Enter your yes/no question in the second text area.

6. Click the "Check" button to get the answer.

7. The app will display "Analysing" while processing and show the result as "YES", "NO", or "UNCLEAR" when complete.

## Customization

To use a different Ollama model, change the `MODEL_NAME` variable at the top of the `app.py` file.

## Troubleshooting

- If you encounter issues with Ollama not being found, ensure it's properly installed and running on your system.
- If the specified model is not available, use the "Refresh Models" button to update the list of available models.

## Contributing

No requirement, intended for Single use Project but freely available to others who want to experiment with Yes/No LLMs.
## License
None
