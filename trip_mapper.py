# Description: This script reads trip details from a CSV file and maps the trip using Google Maps.
# Usage: python trip_mapper.py <trip_num> <csv_path>
# Example: python trip_mapper.py 1 trips.csv

import argparse
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_locations_from_csv(csv_path, trip_num):
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i + 1 == trip_num:
                return [location.strip() for location in row if location.strip()]

def main(trip_num, csv_path):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/maps")

    # Wait for the page to load
    time.sleep(3)

    try:
        directions_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Directions')]"))
        )
        directions_button.click()

        # Wait for the directions panel to load
        time.sleep(3)
    except Exception as e:
        print("Error:", e)

    try:
        driving_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[contains(@aria-label, 'Driving')]/ancestor::button"))
        )
        driving_option.click()
    except Exception as e:
        print("Error:", e)

    # Get locations from CSV for the specified trip number
    locations = get_locations_from_csv(csv_path, trip_num)

    if not locations:
        print("Error: No locations found for the specified trip number.")
        return

    start_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Choose starting point, or click on the map...']"))
    )

    start_point = locations.pop(0)
    start_field.send_keys(start_point)
    print(start_point)
    for destination in locations:
        try:
            dest_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Choose destination, or click on the map...']"))
            )

            dest_field.clear()
            dest_field.send_keys(destination)

            dest_field.send_keys(Keys.ENTER)

            # Wait for the directions to load
            time.sleep(3)

            # Click the "Add destination" button
            add_destination_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.nhb85d.qTupT.fontTitleSmall"))
            )
            add_destination_button.click()

            start_point = destination

        except Exception as e:
            print("Error:", e)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process trip details from CSV")
    parser.add_argument("trip_num", type=int, help="Trip number to process")
    parser.add_argument("csv_path", type=str, help="Path to the CSV file containing trip details")
    args = parser.parse_args()

    main(args.trip_num, args.csv_path)
