# SI 201 HW4 (Library Checkout System)
# Your name: Neveah Stevenson, Amelia Nelson, Vanessa Amevor
# Your student id: 16185138, 87333562, 91481036
# Your email: neveahst@umich.edu, ameliane@umich.edu, vamevor@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    # Don't need to find link
# look for 'div' tags and move in
# eventually you'll hit a 'div' tag with class_ = 't1jojoys dir dir-ltr'
# using .get_text() you will be able to get the listing_title
# the listing id can be found with a regex pattern inside the 'id=listing_id'
  
    listings = []

    with open(html_path, 'r', encoding='utf-8') as f:
        file = f.read()
        soup = BeautifulSoup(file, 'html.parser')

        lists = soup.find_all('div', class_='c1l1h97y')

        for l in lists:
            title = l.find('div', class_='t1jojoys').text
            id = re.findall(r'\/(\d+)\?', l.find('a').get('href'))[0]
            listings.append((title,id))

        return listings

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "html_files", f"listing_{listing_id}.html")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File for listing {listing_id} not found")

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    host_name_tag = soup.find("div", class_="host-name")
    host_name = host_name_tag.get_text(strip=True) if host_name_tag else ""

    host_type = "Superhost" if soup.find(string=re.compile("Superhost", re.IGNORECASE)) else "regular"

    subtitle_tag = soup.find("div", class_="subtitle")
    subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else ""
    subtitle_lower = subtitle.lower()
    if "private" in subtitle_lower:
        room_type = "Private Room"
    elif "shared" in subtitle_lower:
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    policy_number = "Pending"
    policy_tag = soup.find(string=re.compile("Policy number", re.IGNORECASE))
    if policy_tag:
        policy_text = policy_tag.parent.get_text('', strip=True)
        match = re.search(r'(STR-\d+|Pending|Exempt)', policy_text, re.IGNORECASE)
        if match:
            policy_number = match.group(1)
    policy_number = policy_number if policy_number else "Pending"

    
    location_rating = 0.0
    rating_matches = re.findall(r"(\d\.\d)", soup.get_text())
    if rating_matches:
        location_rating = float(rating_matches[-1])

    return {
        listing_id: {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating,
        }
    }
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    tup_list = []
    listing_results_tup = load_listing_results(html_path)
    
    for listing_title, listing_id in listing_results_tup:
        try:
            listing_details = get_listing_details(listing_id)[listing_id]
            tup_list.append(
            (
                listing_title, 
                listing_id,
                listing_details['policy_number'],
                listing_details['host_name'],
                listing_details['host_type'],
                listing_details['room_type'],
                listing_details['location_rating']
            )
        )
        except FileNotFoundError:
            continue
    return tup_list

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_tuples = sorted(data, key=lambda x: x[6], reverse=True)
    with open(filename, 'w', newline = '', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = [
            'Listing Titles',
            'Listing ID',
            'Policy Number',
            'Host Type',
            'Host Name',
            'Room Type',
            'Location Rating'
        ]
        csv_writer.writerow(headers)
        csv_writer.writerows(sorted_tuples)

   
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    room_ratings= {}
    for row in data:
        room_type= row[5]
        rating=row[6]
        if rating ==0.0:
            continue
        if room_type not in room_ratings:
            room_ratings[room_type]= []
        room_ratings[room_type].append(rating)
    averages= {}
    for room_type in room_ratings:
        ratings= room_ratings[room_type]
        averages[room_type]= sum(ratings)/len(ratings)
    return averages
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    nomatch=[]
    match1= r'20\d{2}-00\d{4}STR'
    match2=r'STR-000\d{4}'
    for row in data:
        listing_id= row[1]
        policy_number= row[2]
        if policy_number == 'Pending' or policy_number== 'Exempt':
            continue
        if not (re.fullmatch(match1,policy_number) or re.fullmatch(match2, policy_number)):
            nomatch.append(listing_id)
    return nomatch
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(len(self.listings),18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))                

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = [get_listing_details(listing_id) for listing_id in html_list]
        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        combined = {}
        for d in results:
            combined.update(d)

        self.assertEqual(combined["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(combined["1944564"]["host_type"], "Superhost")
        self.assertEqual(combined["1944564"]["room_type"], "Entire Room")


        self.assertAlmostEqual(combined["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        self.assertEqual(len(self.detailed_data), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(self.detailed_data[-1], ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8))
       

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        output_csv(self.detailed_data, out_path)
        # TODO: Read the CSV back in and store rows in a list.
        row_list = []
        with open(out_path, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                row_list.append(row)
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        self.assertEqual(row_list[1], ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"])

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        results = avg_location_rating_by_room_type(self.detailed_data)
        rating = results.get('Private Room')
        self.assertAlmostEqual(rating, 4.9, places=1)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings =validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"])


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    main()