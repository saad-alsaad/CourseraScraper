import json
from collections import defaultdict
import pandas as pd
import requests as requests
from bs4 import BeautifulSoup as bs
import argparse
from requests import Session


COURSERA_URL = 'https://www.coursera.org/'


def parse_arguments():
    """
    This function return parsed arguments from the command line
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='Scraper Options.', prog='SCRIPT')
    parser.add_argument('--keyword', type=str, nargs=1, metavar='<Course Name>', help='Course keyword to look for', required=True)
    args = parser.parse_args()

    args.keyword = args.keyword[0]
    return args


class CourseraCourses:
    _base_url: str = None
    _session: Session = None
    query_url = ''
    keyword = ''
    csv_file_name: str = 'results'
    search_results = []

    def __init__(self, base_url):
        self._base_url = base_url
        self._session = requests.session()
        self.query_url = f'{self._base_url}search?query='

    @staticmethod
    def get_response(url: str, session: Session) -> requests.Response:
        """
        This method return the source code for the provided URL.
        :param: url: URL of the page to scrape.
        :return: response object: HTTP response object from requests_html.
        """

        try:
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(f'Error happened when creating a request for {url}\nError Msg: {e}')

    def _get_content(self, url: str) -> list:
        """
        This method return a JSON text for the Coursera page data
        :param url: url for a specific page
        :return: json text for page data
        """

        response = self.get_response(url, self._session)
        soup = bs(response.text.encode('utf-8'), 'html.parser')
        rate = soup.find(class_="_16ni8zai m-b-0 rating-text number-rating number-rating-expertise")
        soup = soup.find_all("script")
        if rate:
            rate = rate.next

        return [soup[11].get_text(), rate]

    def _get_courses_urls(self, url: str, page: int) -> list:
        """
        This method allow us to search courses in self._base_url using a keyword and return list of courses urls
        :param page: page number that we need to fetch results from
        :param url: base URL and query
        :return: list of courses url
        """

        content = self._get_content(f'{url}&page={page}&index=prod_all_products_term_optimization&entityTypeDescription=Courses')

        text = content[0]
        data = text.split("window.App=")[1]
        json_data = json.loads(data.split("window.appName=")[0][:-6])
        results_state = json_data['context']['dispatcher']['stores']['AlgoliaResultsStateStore']['resultsState']
        courses = results_state[2]['content']['_rawResults'][0]['hits']

        courses_url = [self._base_url + course['objectUrl'][1:] for course in courses]

        return courses_url

    def get_course_details(self, url: str) -> dict:
        """
        This method get the data for a specific course from self._base_url
        :param url: a url for specific course
        :return: a dictionary of course details, dictionary has (Name, Url, Rate, Tag, Description)
        """

        result = defaultdict()

        content = self._get_content(url)

        text = content[0]
        rate = content[1]

        json_data = json.loads(text)['@graph']
        course_content = json_data[1]

        result['Name'] = course_content['name']
        result['Url'] = url
        result['Rating'] = rate

        if not rate and 'aggregateRating' in course_content:
            rate_value = course_content['aggregateRating'].get('ratingValue')
            if rate_value:
                result['Rating'] = rate_value

        result['Tag'] = [tag['item']['name'] for tag in json_data[0]['itemListElement'][1:]]
        result['Description'] = course_content['description']

        return result

    def get_coursera_courses(self, keyword: str):
        """
        This method implemented to get all courses details in the first page based on the passed keyword
        :param keyword: a string to search for specific subject
        :return: a list of courses details
        """

        self.keyword = keyword
        urls = self._get_courses_urls(f'{self.query_url}{keyword}', 1)
        self.search_results = [self.get_course_details(url) for url in urls]

        return self.search_results

    def export_to_csv(self):
        pd.DataFrame(self.search_results).to_csv(f'{self.keyword}_{self.csv_file_name}.csv', index=False, encoding='utf_8_sig')

    def close_session(self):
        if self._session:
            self._session.close()


if __name__ == '__main__':
    parse = parse_arguments()
    coursera = CourseraCourses(COURSERA_URL)
    results = coursera.get_coursera_courses(parse.keyword)
    coursera.export_to_csv()
    coursera.close_session()
