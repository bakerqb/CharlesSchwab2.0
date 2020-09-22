# Charles Schwab 2.0

The goal of this program is to provide Charles Schwab users with a more flexible UI, as the current UI is limited in its abilities of what users can do on the site

## Installation

After cloning this repo, you will need to set up a virtual environment.

Additionally, you may have the incorrect version of chromedriver, so if you are having errors running, please go to https://chromedriver.chromium.org/downloads and ensure you have the correct version downloaded. Be sure to put chromedriver in this repo, and name the executable "chromedriver_2"

## Usage

To see your stock portolio value from a one date to another date, enter the following command:
```python
python3 positions_table_view.py --account_value <start_date (YYYY-MM-DD)> [end_date(YYYY-MM-DD)]
```
inputing a start date is enforced, but if you leave end date blank, it will default to today's date

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
