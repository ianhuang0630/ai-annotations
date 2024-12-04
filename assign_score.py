from striprtf.striprtf import rtf_to_text

from tasksolver.common import Question, ParsedAnswer, TaskSpec
from tasksolver.gpt4v import GPTModel
from tasksolver.answer_types import TextAnswer, Number
from tasksolver.utils import docs_for_GPT4
import os

import json
from tqdm import tqdm


def assign(input_folder: str,
           output_folder: str,
           prompt_txt: str):

    analyze = TaskSpec(
            name="Analyze text and interviews for a clinical study about opioid abuse and recovery.",
            description="You're a helpful assistant that reads interviews and passages written by patients, and uses the passage to infer scores for different questions for the patient.",
            answer_type=TextAnswer,
            followup_func=None,
            completed_func=None
        )

    files = os.listdir(input_folder)
    files = [os.path.join(input_folder, f) for f in files]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(prompt_txt, "r") as f:
        mega_prompt = f.read()

    with open("openai_key.txt", "r") as f: 
        openai_key = f.readline().strip()


    ai = GPTModel(openai_key,
                task=analyze ,
                model="gpt-4o-mini")

    example_json_template = """
    ```json
    {
        "stigma": {
            "explanation" : "{your explanation for the rating for degree of external stigma they experienced. CITE excerpts in the passage.}"
            "rating" : "low"/"moderate"/"high"/"NA"
        },

        "role_of_self_in_recovery": {
            "explanation" : "{your explanation for the rating for role of self in recovery. CITE excerpts in the passage.}"
            "rating" : "low"/"moderate"/"high"/"NA"
        },
        
        "locus_of_control": {
            "explanation" : "{your explanation for the rating for locus of control. CITE excerpts in the passage.}"
            "rating" : "internal"/"moderate"/"external"/"NA"
        },
        
        "helplessness": {
            "explanation" : "{your explanation for the rating for degree of helplessness. CITE excerpts in the passage.}"
            "rating" : "low"/"moderate"/"high"/"NA"
        },
        
        "destiny": {
            "explanation" : "{your explanation for the degree to which they feel it is their destiny to become addicted. CITE excerpts in the passage.}"
            "rating" : "low"/"moderate"/"high"/"NA"
        }
    }
    ```
    """

    create_schema = Question([
        "You are to reach a passage (either an interview or a passage written by a person), and answer the following questions:",
        mega_prompt,
        f"-------------\n Suggest a json schemathat answers each of the questions. For instance, for an entirely different set of questions about stigma, locus of control etc, the following can be a valid json schema: {example_json_template}" 
    ])

    response, _, _, _ = ai.run_once(create_schema)
    json_string = response.data.split("```json")[1:][0].split("```")[0]
    json_schema = f"""
    ```json
    {json_string}
    ```
    """

    print("expecting the following json schema...")
    print(json_schema)


    done = False
    while not done:
        yesno = input("Continue? (Y/n)")
        yesno = yesno.strip().lower()
        if yesno == "y":
            done = True
            pass
        elif yesno == "n":
            print("exiting...")
            exit
        else:
            print(f"invalid option {yesno}")


    for f in files:
        try:
            with open(f, "r") as fi:
                raw_text = fi.read()

        except Exception as e:
            print(f"{f} gave the following error: \n{e}")
            exit()


    for f in tqdm(files):
        with open(f, "r") as fi:
            raw_text = fi.read() 
        text = rtf_to_text(raw_text)
        
        if "UON" in os.path.basename(f):
            preamble = "This is an interview done on a person who is suffering / suffered from opioid addiction. Infer who is the interviewer, and who is the interviewee:"
            preamble += "\n ==================================="

        else:
            preamble = "Here's a passage written by someone who is suffering / suffered from opioid addiction:" 
            preamble += "\n ==================================="
        
        
        evaluation_prompt = f""" 
    ====================================
    {mega_prompt}
    """
        evaluation_prompt += f"""
    At the end, please produce a json in the following format:   
    {json_schema}
    """

        done = False
        try_num = 0
        max_num_tries = 5
        while not done and try_num < max_num_tries:  
            
            question_to_ask = Question([
                preamble,
                text,
                evaluation_prompt
            ])

            # print(question_to_ask)
            
            p_ans, _, _, _ = ai.run_once(
                question_to_ask
                )

            # print("##############################") 
            # print(p_ans.data)

            try: 
                json_string = p_ans.data.split("```json")[1:][0].split("```")[0]
                data_dictionary = json.loads(json_string)
                done = True
            except: 
                try_num += 1
        
        # print(data_dictionary)
        # save it 

        save_to = os.path.join(output_folder,
                        os.path.basename(f)[:-len(".rtf")]+".json")
        
        with open(save_to, "w") as f:
            json.dump(data_dictionary, f)
        