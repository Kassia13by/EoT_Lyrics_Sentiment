# Song Lyrics Sentiment Analysis Project

This project leverages multiple AI roles as distinct experts (using the OpenAI GPT model as an example) to analyze the sentiment of song lyrics through the Exchange of Thought (EOT) method. The approach is inspired by the paper [Exchange-of-Thought: Enhancing Large Language Model Capabilities through Cross-Model Communication](https://aclanthology.org/2023.emnlp-main.936/).

## Project Structure

- **`main.py`**: The main script used to run the analysis.
- **`functions.py`**: Contains the primary functions for API calls, text processing, and EOT analysis.
- **`config.py`**: Includes the API key, role descriptions, and other configuration settings.
- **`requirements.txt`**: Specifies the required package versions.
- **`README.md`**: This project documentation.

## Setup

1. **Installation**: Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Setup**:  
   - **Option 1**: Directly update the API key in `config.py`.  
   - **Option 2 (Recommended)**: Set the environment variable `OPENAI_API_KEY` (this option is commented out in `config.py`):
     ```bash
     # Linux/Mac
     export OPENAI_API_KEY="your_api_key"
     
     # Windows
     set OPENAI_API_KEY=your_api_key
     ```

3. **Prepare the Input CSV File**: Create a CSV file containing the lyrics data. In this example, the file `lyrics.csv` includes a column named `lyrics` with 15 rows of song lyric segments.

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Read the lyrics from the input CSV file.
2. Process each lyric segment using the EOT sentiment analysis system.
3. Write the results and discussion logs to a new file named `lyrics_with_eot.json`.

## Methodology

The EOT process works as follows (In this project, only **Memory** communication is utilized):
1. Three expert roles (Amy, Lily, and John) independently analyze the sentiment of the lyrics.
2. They then share their perspectives and iterate multiple times to reach a consensus on the analysis.
3. The project is set to iterate a maximum of 3 times; if consensus is reached earlier, the iterations will terminate early.
4. If no consensus is reached after 3 iterations, a majority vote is taken.
5. If a majority decision cannot be made, Amy's answer is used by default.
6. The final sentiment label will be unified (0 indicates negative sentiment, 1 indicates positive sentiment).

## Customization Tips

You can modify:
- The role descriptions in `config.py`.
- The API parameters in `config.py`.
- The model name in `config.py`
- The input/output file paths in `main.py`.
- The number of iterations in the EOT process in `main.py`.
