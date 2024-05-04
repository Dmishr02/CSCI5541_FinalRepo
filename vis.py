import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
#new_file_path = 'GPT4updatedclassifiedgenderbiasprompts - GPT4updatedclassifiedgenderbiasprompts (1).csv'
new_file_path = 'GPT4updatedclassifiedgenderbiasprompts - GPT4updatedclassifiedgenderbiasprompts (1).csv'
new_data = pd.read_csv(new_file_path)

# Replace 'Variable' or unspecified salaries with $100,000
#new_data['Unnamed: 26'].replace('Variable', 100000, inplace=True)
#new_data['Salary'] = pd.to_numeric(new_data['Unnamed: 26'], errors='coerce').fillna(100000)
# Calculate the bias score

new_data['TotalResponses'] = new_data['Male Count'] + new_data['Female Count'] + new_data['Neutral']
new_data['BiasScore'] = new_data.apply(lambda row: (row['Male Count'] if row['Stereotype'] == 'Male' else row['Female Count']) / row['TotalResponses'], axis=1)

print(new_data['BiasScore'].mean() )
print(((new_data['BiasScore'] * new_data['TotalResponses'])/(new_data['Male Count'] + new_data['Female Count'])).mean() )
print(new_data['TotalResponses'].mean())
# Calculate non-stereotype responses including neutrals
new_data['NeutralCount'] = new_data['Neutral']
new_data['TotalNonStereotype'] = new_data['TotalResponses'] - new_data['TotalResponses']*new_data['BiasScore'] - new_data['NeutralCount']



# Sort data by bias score
new_data_sorted = new_data.sort_values(by='BiasScore', ascending=False)
roles = range(1, len(new_data_sorted) + 1)
stereotype_responses = new_data_sorted['BiasScore']  # Convert bias score back to number of responses
non_stereotype_responses = new_data_sorted['TotalNonStereotype']/new_data_sorted['TotalResponses']  
neutral_responses = new_data_sorted['NeutralCount']/new_data_sorted['TotalResponses'] 

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))  # Adjusting the figure size to make it less horizontal

# Plotting stereotype responses in red going up
ax.bar(roles, stereotype_responses, color='red', label='Stereotype Responses')

# Plotting non-stereotype responses in green going down, including neutrals
ax.bar(roles, -non_stereotype_responses, color='green', label='Non-Stereotype Responses')

# Adding neutral responses in grey on top of the green bars
ax.bar(roles, -neutral_responses, color='grey', bottom=-non_stereotype_responses, label='Neutral Responses')

# Labeling and titling
ax.set_xlabel('Roles (Numbered)')
ax.set_ylabel('Percentage of Valid Responses')
ax.set_title('English Gender Bias (GPT-4)')
ax.set_xticks([])  # Removing specific role labels from the x-axis
ax.set_ylim(-1, 1)

ax.invert_yaxis()  # Non-stereotype responses go down


# Adding legend in the lower right corner
ax.legend(loc='lower right')

# Adding grid for easier viewing
ax.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
