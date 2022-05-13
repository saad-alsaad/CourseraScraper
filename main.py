import json
from collections import defaultdict
import pandas as pd
import requests as requests
from bs4 import BeautifulSoup as bs
import argparse

COURSERA_URL = 'https://www.coursera.org/'
COURSERA_QUERY_URL = f'{COURSERA_URL}search?query='

session = requests.session()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Scraper Options.', prog='SCRIPT')
    parser.add_argument('--keyword', type=str, nargs=1, metavar='<Course Name>', help='Course keyword to look for', required=True)
    args = parser.parse_args()

    args.keyword = args.keyword[0]
    return args


def get_source(url: str) -> requests.Response:
    """
    Return the source code for the provided URL.

    :param: url: URL of the page to scrape.
    :return: response object: HTTP response object from requests_html.
    """

    try:
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_text_content(url: str) -> str:
    response = get_source(url)
    soup = bs(response.text.encode('utf-8'), 'html.parser')
    soup = soup.find_all("script")

    return soup[11].get_text()


def get_courses_urls(url: str, page: int) -> list:
    """
    This function allow us to search courses in COURSERA_URL using a keyword and return list of courses urls

    :param page: page number that we need to fetch results from
    :param url: base URL and query
    :return: list of courses url
    """

    courses_url = []

    text = get_text_content(f'{url}&page={page}&index=prod_all_products_term_optimization&entityTypeDescription=Courses')

    data = text.split("window.App=")[1]
    data = data.split("window.appName=")[0][:-6]
    json_data = json.loads(data)
    results_state = json_data['context']['dispatcher']['stores']['AlgoliaResultsStateStore']['resultsState']
    courses = results_state[2]['content']['_rawResults'][0]['hits']

    for course in courses:
        courses_url.append(COURSERA_URL + course['objectUrl'])

    return courses_url


def get_course_details(url: str) -> dict:
    """
    This function get the data for a specific course from  COURSERA_URL

    :param url: a url for specific course
    :return: a dictionary of course details, dictionary has (Name, Url, Rate, Tag, Description)
    """

    result = defaultdict()

    text = get_text_content(url)

    json_data = json.loads(text)['@graph']

    course_content = json_data[1]

    result['Name'] = course_content['name']
    result['Url'] = url

    result['Rating'] = None
    if 'aggregateRating' in course_content:
        rate_value = course_content['aggregateRating'].get('ratingValue')
        if rate_value:
            result['Rating'] = float(rate_value)

    result['Tag'] = []
    for tag in json_data[0]['itemListElement'][1:]:
        result['Tag'].append(tag['item']['name'])

    result['Description'] = course_content['description']

    return result


def get_coursera_courses(keyword: str) -> list:
    """
    This function implemented to get all courses details in the first page based on the passed keyword

    :param keyword: a string to search for specific subject
    :return: a list of courses details
    """

    courses_data = []
    urls = get_courses_urls(f'{COURSERA_QUERY_URL}{keyword}', 1)

    for url in urls:
        courses_data.append(get_course_details(url))

    return courses_data


if __name__ == '__main__':
    parse = parse_arguments()
    courses_data = get_coursera_courses(parse.keyword)
    pd.DataFrame(courses_data).to_csv('results.csv', index=False, encoding='utf_8_sig')
    if session:
        session.close()
