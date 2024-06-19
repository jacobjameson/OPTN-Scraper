from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# Initialize the WebDriver for Safari
driver = webdriver.Safari()

# Initialize an empty list to collect DataFrames
all_data = []

# Function to select a state and navigate through the steps
def select_state_and_navigate(state_value=None, state_name=None):
    if state_value:
        # Select the state
        select = Select(driver.find_element(By.ID, 'selectArea'))
        select.select_by_value(state_value)
        
    # Click the "Go" button
    go_button = driver.find_element(By.ID, 'imgSubmit')
    go_button.click()
    
    # Wait for the new page to load
    time.sleep(1)
    
    # Select the "Donor" category
    category_select = Select(driver.find_element(By.ID, 'category'))
    category_select.select_by_value("1;Donor")
    
    # Wait for the options to load
    time.sleep(1)
    
    # Select the "Kidney" organ
    organ_select = Select(driver.find_element(By.ID, 'slice0'))
    organ_select.select_by_value("Kidney;Kidney;8;Organ;Organ")
    
    # Wait for the options to load
    time.sleep(1)
    
    # Click on the "Deceased Donors by Circumstance of Death" link
    link = driver.find_element(By.XPATH, "//a[contains(text(), 'Deceased Donors by Circumstance of Death')]")
    link.click()
    
    # Wait for the new page to load
    time.sleep(1)
    
    # Click the "Switch Axes" button to flip the data
    driver.find_element(By.ID, 'tool_flip').click()
    
    # Wait for the table to reload after flipping
    time.sleep(1)
    
    # Extract the table data
    table = driver.find_element(By.ID, 'reportData')
    headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
    rows = []
    for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
        rows.append([cell.text for cell in row.find_elements(By.TAG_NAME, 'td')])
    
    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)
    df['State'] = state_name  # Add a column for the state name
    
    # Append the DataFrame to the list
    all_data.append(df)
    
    # Go back to the main page
    driver.get('https://optn.transplant.hrsa.gov/data/view-data-reports/state-data/')
    time.sleep(0.1)

# Open the website
driver.get('https://optn.transplant.hrsa.gov/data/view-data-reports/state-data/')

# Wait for the page to load
time.sleep(2)

# Process the initial state (Alabama) by just pressing "Go"
print(f'Selecting Alabama...')
select_state_and_navigate(state_name='Alabama')

# Iterate over each option in the drop-down menu starting from the second option
for i in range(1, len(Select(driver.find_element(By.ID, 'selectArea')).options)):
    # Reinitialize the select element and its options
    select_element = driver.find_element(By.ID, 'selectArea')
    select = Select(select_element)
    option = select.options[i]
    
    state_value = option.get_attribute('value')
    state_name = option.text
    
    print(f'Selecting {state_name}...')
    select_state_and_navigate(state_value, state_name)

# Close the WebDriver
driver.quit()

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(all_data, ignore_index=True)
cols = combined_df.columns.tolist()
cols[1] = 'Year'
combined_df.columns = cols
combined_df['Year'] = combined_df['\xa0']
combined_df = combined_df.drop(columns=['\xa0'])
combined_df.insert(0, 'State', combined_df.pop('State'))

# Save the combined DataFrame to a CSV file
combined_file_path = '/data/kidney/state_transplant_data_combined.csv'
combined_df.to_csv(combined_file_path, index=False)

# Update the README file with the last updated date
readme_file_path = 'README.md'
with open(readme_file_path, 'r') as file:
    readme_contents = file.read()

last_updated_date = datetime.now().strftime('%Y-%m-%d')
readme_contents = readme_contents.replace('LAST_UPDATED_PLACEHOLDER', last_updated_date)

with open(readme_file_path, 'w') as file:
    file.write(readme_contents)
