import requests
from bs4 import BeautifulSoup
import json

# URL of Analytics Vidhya Free Courses page
url = "https://courses.analyticsvidhya.com/collections/courses"

# Make an HTTP GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    print("Response content:", response.text[:500])  # Print the first 500 characters of the response
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    print("Response:", response.text)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find course details
courses = []

# Loop through all the course cards on the page
course_cards = soup.find_all('a', class_='course-card course-card__public published')

if not course_cards:
    print("No course cards found. Please check the HTML structure and class names.")

for course in course_cards:
    # Extract the course title from the <h3> tag directly
    title_tag = course.find('h3')  # Extracts the title from the <h3> tag

    # Extract the course link (href)
    link_tag = course['href'] if course.has_attr('href') else None

    # Extract the image URL
    image_tag = course.find('img', class_='course-card__img')  # Adjust if the class is different
    image_url = image_tag['src'] if image_tag else None

    # Extract the course price (assuming 'Free' text in price span)
    price_tag = course.find('span', class_='course-card__price')
    price = price_tag.text.strip() if price_tag else None

    # Collect course data if title and link are present
    if title_tag and link_tag:
        course_data = {
            "title": title_tag.text.strip() if title_tag else None,  # Get text inside <h3>
            "link": f"https://www.analyticsvidhya.com{link_tag}" if link_tag else None,
            "image_url": image_url,
            
            "price": price
        }
        courses.append(course_data)

# Check if courses are scraped successfully
if courses:
    # Save the scraped data to a JSON file
    with open('courses.json', 'w') as f:
        json.dump(courses, f, indent=4)
    print("Scraped and saved course data successfully!")
else:
    print("No course data found.")

# Load the courses data from the scraped JSON
try:
    with open("courses.json", "r") as f:
        courses = json.load(f)
    print(f"Successfully loaded {len(courses)} courses.")
except Exception as e:
    print(f"Error loading courses data: {str(e)}")
