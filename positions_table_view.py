import requests
import os
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from dateutil.relativedelta import *
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import click
from pandas.plotting import register_matplotlib_converters
from getpass import getpass
from tqdm import tqdm
from progressbar import ProgressBar
register_matplotlib_converters()


@click.command()
# @click.option("--account_value", "-v")
@click.option("--account_value", "-v", nargs=0, required=False)
@click.argument("account_value", nargs=-1)
def main(account_value):
    account_value
    error_handling(account_value)
    
    print("\nPlease enter your Charles Schwab Login Info:")
    os.environ['SCHWAB_USERNAME'] = input("Username: ")
    os.environ['SCHWAB_PASSWORD'] = getpass()
    
    login_url = 'https://client.schwab.com/Login/SignOn/CustomerCenterLogin.aspx'
    account_url = 'https://client.schwab.com/clientapps/accounts/summary/'
    
    '''
    options = webdriver.ChromeOptions()
    options.setHeadless(true)
    '''
    
    driver = webdriver.Chrome('./chromedriver_2') # , options=options)
    
    login(driver)
    print("\nSucessfully logged in!\n")  
            
    if account_value:
        end_date = datetime.datetime.now()
        if len(account_value) == 2:
            end_date = datetime.datetime.strptime(account_value[1], '%Y-%m-%d')
        
        if account_value[0] == "week":
            start_date = end_date - datetime.timedelta(days=7)
        elif account_value[0] == "month":
            start_date = end_date - relativedelta(months=1)
        else:    
            start_date = datetime.datetime.strptime(account_value[0], '%Y-%m-%d')
        
        
            
        graph_account_value(driver, start_date, end_date)

    driver.quit()
    
    
def error_handling(account_value):
    if account_value:
        # Assert arguments are in format YYYY-MM-DD
        try:
            for date in account_value:
                if date != "week" and date != "month":
                    datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    
def login(driver):
    login_url = 'https://client.schwab.com/Login/SignOn/CustomerCenterLogin.aspx'
    
    # Navigate to login page
    driver.get(login_url)
    driver.implicitly_wait(10)

    # Login w/ environ variables
    driver.switch_to.frame('lmsSecondaryLogin')
    username_textbox = driver.find_element_by_id('LoginId')
    username_textbox.send_keys(os.environ['SCHWAB_USERNAME'])
    password_textbox = driver.find_element_by_id("Password")
    password_textbox.send_keys(os.environ['SCHWAB_PASSWORD'])
    login_button = driver.find_element_by_id("LoginSubmitBtn")
    login_button.submit()
    

def graph_account_value(driver, start_date, end_date):
    # Open Table View on account summary page
    driver.implicitly_wait(10)
    '''
    try:
        table_view_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Table View"))
        )
    finally:
        driver.quit()
    '''
    table_view_button = driver.find_element_by_partial_link_text("Table View")
    table_view_button.click()
    
    # Switch windows to the Table View
    table_window = driver.current_window_handle
    for window in driver.window_handles:
        if window != driver.current_window_handle:
            table_window = window
            break
    driver.switch_to.window(table_window)

    # Grab data from rows
    test = driver.find_elements_by_tag_name("tr")
    date_values = []
    dollar_values = []
    
    num_days = (end_date - start_date).days + 1
    
    now_til_end_date = (datetime.datetime.now() - end_date).days
    
    print("\nGenerating Graph...")
    pbar = ProgressBar()
    
    for row in pbar(test[now_til_end_date:now_til_end_date + num_days]):
        values = row.find_elements_by_tag_name("td")
        if len(values) == 2:
            date_str = ' '.join(values[0].text.split(', ')[1:])
            date_obj = datetime.datetime.strptime(date_str, '%B %d %Y')
            date_values.append(date_obj)
            dollar_amt = float(''.join(values[1].text[1:].split(',')))
            dollar_values.append(dollar_amt)

    # Show graph
    plt.plot(date_values, dollar_values)
    plt.show()
    return


if __name__ == "__main__":
    main()




