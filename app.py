import requests
from bs4 import BeautifulSoup
import csv

def scrape_yellow_pages(base_url):
    page_number = 1
    while True:
        url = f"{base_url}?page={page_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all('div', class_='row box foc')  # Adjust class name accordingly
            if not listings:
                break
            with open('yellow_pages_restaurants.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for listing in listings:
                    name = listing.find('h2', class_='cmp_name').text.strip()
                    location_tag = listing.find('span', itemprop='streetAddress')
                    location = location_tag.text.strip() if location_tag else "N/A"
                    city_tag = listing.find('strong', itemprop='addressLocality')
                    city = city_tag.text.strip() if city_tag else "N/A"
                    po_box_tag = listing.find('span', itemprop='postalCode')
                    po_box = po_box_tag.text.strip() if po_box_tag else "N/A"
                    phone_tag = listing.find('span', class_='phone')
                    phone = phone_tag.text.strip() if phone_tag else "N/A"
                    mobile_tag = listing.find('a', class_='ViewMobText')
                    mobile = mobile_tag.text.strip() if mobile_tag else "N/A"
                    company_page_link_tag = listing.find('a', class_='website')
                    company_page_link = company_page_link_tag['href'] if company_page_link_tag else "N/A"
                    logo_url_tag = listing.find('img')
                    logo_url = logo_url_tag['src'] if logo_url_tag else "N/A"

                    writer.writerow([name, location, city, po_box, phone, mobile, company_page_link, logo_url])

            print(f"Page {page_number} data successfully written to yellow_pages_restaurants.csv")
            page_number += 1
        else:
            print("Failed to retrieve the webpage")
            break

base_url = 'https://www.yellowpages-uae.com/uae/restaurant'

scrape_yellow_pages(base_url)
