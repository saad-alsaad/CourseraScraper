import unittest
from main import CourseraCourses, COURSERA_URL


class CheckCoursera(unittest.TestCase):
    def setUp(self):
        self.coursera = CourseraCourses(COURSERA_URL)

    def test_get_coursera_courses(self):
        courses = self.coursera.get_coursera_courses('python')
        self.assertEqual(len(courses), 10)
        self.assertEqual(courses[0]['Name'], 'Python for Everybody')

    def test_get_courses_urls(self):
        urls = self.coursera._get_courses_urls(f'{self.coursera.query_url}{self.coursera.keyword}', 1)
        self.assertEqual(len(urls), 10)

    def test_get_course_details(self):
        result = self.coursera.get_course_details('https://www.coursera.org/learn/python-project-for-data-engineering')
        self.assertEqual(result['Name'], 'Python Project for Data Engineering')
        self.assertEqual(result['Url'], 'https://www.coursera.org/learn/python-project-for-data-engineering')
        self.assertEqual(len(result['Tag']), 2)
        self.assertIsNotNone(result['Rating'])
        self.coursera.close_session()


if __name__ == '__main__':
    unittest.main()