### Coursera Scraper Script

<h4>A Python Script implemented to scrap courses from Coursera. The script will return courses based on keywords passed to the script and generate results.csv that contains the course name, URL, rating, tag, and description.</h4>

<p>main.py script built to scrap courses from <a href="https://www.coursera.org">Coursera</a>. the script will return courses from the first page only</p>
<p>main.py script takes --keyword <value> argument to search for courses with specific keyword</p>
<p>tester.py script has some unit tests</p>
<p>used python version is 3.10.1</p>

##### Commands:
<p>If you don't have python installed, install from <a href="https://www.python.org/downloads/release/python-3101/">here</a> </p>
<p>Install needed libraries: <span>`pip install -r requirements.txt`</span></p>
<p>To run the main.py: `python main.py --keyword "web Scraping"`</p>
<p>To run unit tests: `python tester.py`.</p>


### Argo WorkFlows:
<p>`argo_workflow.yaml` file has configuration of 4 tasks workflow with consideration of dependencies. each task is responsible of one action</p>
<p>The workflow scheduled to be run in weekly basis</p>
