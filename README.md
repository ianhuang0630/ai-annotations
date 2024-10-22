# AI interview/monologue annotation 

## Installation and Setup 

Clone this repository first by running in your terminal:
```bash
git clone []
cd 
```

Then run the following to set up the important
```bash
conda create -n ai-analyze python=3.10
conda activate ai-analyze

git clone git@github.com:ianhuang0630/TaskSolver.git
cd TaskSolver
pip install -e .
cd ../
pip install striprtf tqdm 
```

Paste your openai API key into a file named `openai_key.txt` at the root level of this repository.


## Quick Start

Put your data in a folder. Remember the relative path to that folder (let's say it's `input_data/` )
Write your prompts in a .txt, following theformat in the current prompts shown under `prompts/`. Remember the path to that .txt (let's say it's `prompts/new_prompt.txt`)

The last things you wanna decide are :
- the output file of the csv (this is the spreadsheet that the process outputs.). Let's say it is `new_analysis.csv`
- the output directory of the annotations. This isn't so important. It's an intermediate step, useful if you want to inspect the analysis of the LLM . Let's say it's a folder named `tmp/`.


You can then run 
```bash
python main.py --input-dir input_data --annotation-dir tmp/ --prompt prompts/prompt5.txt --output-csv new_analysis.csv
```

Almost immediately after running, the system will  recommend a schema for the output CSV based on the questions you're asking in the prompts. You can type Y + Enter to continue if it looks good, or quit the program (N + Enter) if it doesn't.

