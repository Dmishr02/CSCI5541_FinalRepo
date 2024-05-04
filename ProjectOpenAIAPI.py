import os
from pathlib import Path
from openai import OpenAI


# Set up your OpenAI API key
client = OpenAI(
   api_key=''#fill in apikey
)

def generate_responses(prompt, iterations=10):
    responses = []
    for _ in range(iterations):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            generated_message = response.choices[0].message.content
            responses.append(generated_message)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            responses.append("I encountered an error while generating a response.")
    return responses

import pandas as pd

file_paths = []
id = 0
# Load the CSV file
for file_path in file_paths:
      # Make sure to replace this with the actual path to your file
    id+=1
    data = pd.read_csv(file_path)

    # Loop through each row and access the "Prompt", and generate responses
    for index, row in data.iterrows():
        print(index)
        responses = generate_responses(row['Prompt Translation'])
        for i, response in enumerate(responses):
            col_name = f"R{i+1}"  
            data.at[index, col_name] = response

    # Save the updated DataFrame to a new CSV file
    file_name = f"responsedata/RESPONSE_{id}.csv"
    data.to_csv(file_name, index=False)
    
    




