from requests_html import HTMLSession
import os
import re
from sqlalchemy.orm import Session
from models import SubwayOutlet
from database import SessionLocal, init_db


os.environ['PYPPETEER_EXECUTABLE_PATH'] = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

url = 'https://subway.com.my/find-a-subway'

s = HTMLSession()


def clean_address(address):
    address = address.strip()
    address = address.replace('\xa0', ' ')
    address = re.sub(r'\s+', ' ', address)
    return address

def clean_operating_hours(hours):
    hours = hours.strip()
    hours = hours.replace('\xa0', ' ')
    hours = hours.replace(' - ', '-')
    hours = hours.replace('–', '-')  # Replace en dash
    hours = hours.replace('—', '-')
    return hours


def extract_subway_data(r):
    print('running extract subway data function...')
    
    # r = s.get(url)
        

    # r.html.render(sleep=1)
    outlets_data = []
    outlets = r.html.xpath('//*[@id="fp_locationlist"]/div/div[contains(@class, "fp_list_marker")]')

    # print(f"Found {len(outlets)} outlets in Malaysia: ")
    for outlet in outlets:
        # print(outlet)
        names = outlet.find('h4', first=True).text if outlet.find('h4', first=True) else "No name found"
        
        infobox = outlet.find('.infoboxcontent', first=True) 
        latitude = outlet.attrs.get('data-latitude')
        longitude = outlet.attrs.get('data-longitude')
        
        if infobox:
            paragraphs = infobox.find('p')
            address = clean_address(paragraphs[0].text) if len(paragraphs) > 0 else 'No Address Found'
            days_check = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for p in paragraphs:
                if any(day in p.text for day in days_check):
                    operating_hours = clean_operating_hours(p.text)
                    break
            
            
        else:
            address = "No address found."
            operating_hours = "No operating hours found."
            
        directionButton = outlet.find('.directionButton', first=True)
        
        if directionButton:
            links = directionButton.absolute_links
            wazelink = next((link for link in links if 'waze.com' in link), 'No waze link found.')
        else:
            wazelink = 'No waze link found'
        
        
       
        
        if 'Kuala Lumpur' in address:
            outlets_data.append(
                {
                    'name': names, 
                    'address': address, 
                    'operating_hours': operating_hours, 
                    'waze_link': wazelink, 
                    'latitude': latitude, 
                    'longitude': longitude
                 }
                )
            
    return outlets_data
    
        
    
    
# Function to navigate to through all pages
def scrape_pagination(url):
    print('running pagination function...')
    all_data = []
    while url:
        r = s.get(url)
        r.html.render(sleep=1)
        page_data = extract_subway_data(r)
        all_data.extend(page_data)
        
        # next page link
        next_page = r.html.find('a.next', first=True)
        if next_page and 'href' in next_page.attrs:
            url = next_page.attrs['href']
        else:
            url = None
    
    return all_data



# function to insert data into db
def insert_data(db_session: Session, outlets):
    for outlet in outlets:
        existing_outlet = db_session.query(SubwayOutlet).filter_by(name=outlet['name'], address=outlet['address']).first()
        if not existing_outlet:
            db_outlet = SubwayOutlet(
                name=outlet['name'],
                address=outlet['address'],
                operating_hours=outlet['operating_hours'],
                waze_link=outlet['waze_link'],
                latitude=outlet['latitude'],
                longitude=outlet['longitude']
            )
            db_session.add(db_outlet)
        
    db_session.commit()
    

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    
    # check if the table is empty
    outlet_count = db.query(SubwayOutlet).count()   
    if outlet_count == 0:
        print('No data is found in database, scraping new data ...')
        all_outlets = scrape_pagination(url)
        insert_data(db, all_outlets)
        print(f"Inserted {len(all_outlets)} outlets into the database.")
    
    else:
        print("Data already exist in the database, skip scraping ...")
    
    db.close()