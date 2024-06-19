from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# Initialize the WebDriver for headless Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# Define the list of donor types
donor_types = [
    'All Donors by Donor Type',
    'Deceased Donors by Donor Age',
    'Deceased Donors by Donor Ethnicity',
    'Deceased Donors by Donor Gender',
    'Deceased Donors by Circumstance of Death',
    'Deceased Donors by Mechanism of Death',
    'Deceased Donors by Cause of Death',
    'Deceased Donors by DSA',
    'Living Donors by Donor Age',
    'Living Donors by Donor Ethnicity',
    'Living Donors by Donor Gender',
]

# Function to select a state and navigate through the steps
def select_state_and_navigate(state_value=None, state_name=None, donor_type=None):
    try:
        if state_value:
            # Select the state
            select = Select(driver.find_element(By.ID, 'selectArea'))
            select.select_by_value(state_value)
        
        # Click the "Go" button
        go_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'imgSubmit'))
        )
        go_button.click()
        
        # Wait for the new page to load
        time.sleep(0.5)
        
        # Select the "Donor" category
        category_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'category'))
        )
        Select(category_select).select_by_value("1;Donor")
        
        # Wait for the options to load
        time.sleep(0.5)
        
        # Select the "Kidney" organ
        organ_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'slice0'))
        )
        Select(organ_select).select_by_value("Kidney;Kidney;8;Organ;Organ")
        
        # Wait for the options to load
        time.sleep(0.5)
        
        # Click on the donor type link
        donor_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{donor_type}')]"))
        )
        donor_link.click()
        
        # Wait for the new page to load
        time.sleep(0.5)
        
        # Click the "Portrait" button
        portrait_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'tool_portrait'))
        )
        portrait_button.click()
        
        # Wait for the table to reload
        time.sleep(1)
        
        # Click the "Switch Axes" button to flip the data
        flip_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'tool_flip'))
        )
        flip_button.click()
        
        # Wait for the table to reload after flipping
        time.sleep(1)
        
        # Extract the table data
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'reportData'))
        )
        headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
        rows = []
        for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
            rows.append([cell.text for cell in row.find_elements(By.TAG_NAME, 'td')])
        
        # Create a DataFrame
        df = pd.DataFrame(rows, columns=headers)
        df['State'] = state_name  # Add a column for the state name
        
        return df

    except Exception as e:
        print(f"Error processing {state_name} for {donor_type}: {e}")
        return None

    finally:
        # Go back to the main page
        driver.get('https://optn.transplant.hrsa.gov/data/view-data-reports/state-data/')
        time.sleep(2)

# Open the website
driver.get('https://optn.transplant.hrsa.gov/data/view-data-reports/state-data/')

# Wait for the page to load
time.sleep(2)

# Process each donor type
for donor_type in donor_types:
    all_data = []
    print(f"Processing donor type: {donor_type}")
    
    # Process the initial state (Alabama) by just pressing "Go"
    print(f'Selecting Alabama for {donor_type}...')
    df = select_state_and_navigate(state_name='Alabama', donor_type=donor_type)
    if df is not None:
        cols = df.columns.tolist()
        cols[1] = 'Year'
        df.columns = cols
        df['Year'] = df['\xa0']
        df = df.drop(columns=['\xa0'])
        df.insert(0, 'State', df.pop('State'))
        
        all_data.append(df)
    
    # Iterate over each option in the drop-down menu starting from the second option 
    for i in range(1, len(Select(driver.find_element(By.ID, 'selectArea')).options)):
        # Reinitialize the select element and its options
        select_element = driver.find_element(By.ID, 'selectArea')
        select = Select(select_element)
        option = select.options[i]
        
        state_value = option.get_attribute('value')
        state_name = option.text
        
        print(f'Selecting {state_name} for {donor_type}...')
        df = select_state_and_navigate(state_value, state_name, donor_type)

        if df is not None:
            cols = df.columns.tolist()
            cols[1] = 'Year'
            df.columns = cols
            df['Year'] = df['\xa0']
            df = df.drop(columns=['\xa0'])
            df.insert(0, 'State', df.pop('State'))
            
            all_data.append(df)
    
    # Combine all DataFrames for the donor type into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.fillna('0')
    

    # Clean donor type name to use in the filename
    donor_type_clean = re.sub(r'\W+', '_', donor_type)
    
    # Save the combined DataFrame to a Parquet file
    combined_file_path = f'data/kidney/{donor_type_clean}.parquet'
    combined_df.to_parquet(combined_file_path, index=False)
    print(f"Saved data for {donor_type} to {combined_file_path}")

# Close the WebDriver
driver.quit()
