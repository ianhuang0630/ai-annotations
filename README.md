# AI interview/monologue annotation 

## Installation and Setup 

Clone this repository first by running in your terminal:
```bash
git clone git@github.com:ianhuang0630/ai-annotations.git
cd ai-annotations
```

Then run the following to set up the required packages. We use [conda](https://anaconda.org/anaconda/conda) here, so to run the following please make sure you've first installed Conda.
```bash
conda create -n ai-analyze python=3.10
conda activate ai-analyze

git clone git@github.com:ianhuang0630/TaskSolver.git
cd TaskSolver
pip install -e .
cd ../
pip install striprtf tqdm 
```

Next, paste your Openai API key into a file named `openai_key.txt` at the root level of this repository.


## Quick Start

This repo assumes that every record it must annotate is in one file under a folder. Remember the relative path to that folder (for the purposes of the demo below, let's say it's `input_data/` ).

Write your prompts in a .txt, following the format in the current prompts shown under `prompts/`. Remember the path to that .txt (for the purposes of the demo below, let's say it's `prompts/new_prompt.txt`)

The last things you wanna decide are :
- the output file of the csv (this is the spreadsheet that the process outputs.). Let's say it is `new_analysis.csv` for the demo below.
- the output directory of the annotations. This isn't so important. It's an intermediate step, useful if you want to inspect the analysis of the LLM . Let's say it's a folder named `tmp/`.

You can then run 
```bash
python main.py --input-dir input_data/ --annotation-dir tmp/ --prompt prompts/prompt5.txt --output-csv new_analysis.csv
```

Almost immediately after running, the system will recommend a schema for the output CSV based on the questions you're asking in the prompts. You can type Y + Enter to continue if it looks good, or quit the program (N + Enter) if it doesn't.

If you decide to proceed, you'll find that it'll show a progress bar of annotating each file in the `input_data/` folder, and once it's done, a .csv should appear by the name `new_analysis.csv` with the annotations in it.

