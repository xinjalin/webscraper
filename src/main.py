from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from time import sleep
import datetime

from data_item import DataItem


def main():
    url = "https://visualisations.aemo.com.au/aemo/apps/visualisation/index.html#/electricity/dashboard"
    region_id = "SA"
    formatted_data = []

    # date
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")

    # Initialize WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for initial page load
        sleep(5)

        try:
            # Wait for the dropdown to be present
            dropdown_element = wait.until(
                EC.presence_of_element_located((By.ID, "region-id"))
            )

            # Use Select class to change the region
            dropdown = Select(dropdown_element)
            dropdown.select_by_visible_text(region_id)

            print(f"Selected {region_id} region")

            # Wait for the page to update after selection
            sleep(5)

        except Exception as region_error:
            print(f"Error selecting region: {region_error}")

        # Find all summary rows
        summary_rows = driver.find_elements(By.CLASS_NAME, "summary-row")

        for row in summary_rows:
            try:
                # Extract data from each row
                title = row.find_element(
                    By.CLASS_NAME, "summary-row-label-title").text
                unit = row.find_element(
                    By.CLASS_NAME, "summary-row-label-unit").text
                value = row.find_element(
                    By.CLASS_NAME, "summary-row-value").text

                # Clean up the unit text (remove parentheses)
                unit = unit.strip('()')

                # Create a DataItem instance
                data_entry = DataItem(
                    name=title, unit=unit, value=value, region=region_id, time=formatted_date)

                formatted_data.append(data_entry)
                print(f"Extracted: {title} - {value} {unit}")

            except Exception as row_error:
                print(f"Error processing row: {row_error}")

        print("\nComplete formatted data:", formatted_data)

        spot_prices = [
            item for item in formatted_data if item.name == 'CURRENT SPOT PRICE']
        print(f"Spot Price slice: {spot_prices}")

    except TimeoutException:
        print("Timeout waiting for page elements to load")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()