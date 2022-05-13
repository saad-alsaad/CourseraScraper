import unittest
import requests
from main import get_coursera_courses, get_course_details


session = requests.session()


class CheckCoursera(unittest.TestCase):
    def test_get_coursera_courses(self):
        courses = get_coursera_courses('python')
        self.assertEqual(len(courses), 10)
        self.assertEqual(courses[0]['Name'], 'Python for Everybody')
        session.close()

    def test_get_course_details(self):
        result = get_course_details('https://www.coursera.org/learn/python-project-for-data-engineering')
        self.assertEqual(result['Name'], 'Python Project for Data Engineering')
        self.assertEqual(result['Url'], 'https://www.coursera.org/learn/python-project-for-data-engineering')
        self.assertEqual(len(result['Tag']), 2)
        self.assertIsNotNone(result['Rating'])
        session.close()


if __name__ == '__main__':
    unittest.main()