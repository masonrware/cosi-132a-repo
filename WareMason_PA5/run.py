import os
import json
import subprocess
from subprocess import check_output

#TODO
# make this into a dict
# then make script to generate a table with that
outputs: list = [] 

with open ('pa5_data/pa5_queries.json', 'r') as f:
    data = json.load(f)
    #TODO
    #cycle through each type of thing which will be keys in dict
    for line in data['pa5_queries']:
        # outputs.append(subprocess.call(['run.sh', line['topic']], shell=True))
        outputs.append(float(check_output(['python3.9', 'evaluate.py', '--index_name', 
                                           'wapo_docs_50k', '--topic_id', line['topic'], 
                                           '--query_type', 'nl', '--top_k', '20', 
                                           '--search_type', 'vector', '--vector_name', 'sbert_vector'])))
        
print(outputs)

#run the flask app
subprocess.call(['python3.9', 'hw5.py', '--run'])