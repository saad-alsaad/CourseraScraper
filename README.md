### Coursera Scraper Script

<p>main.py script built to scrap courses from <a href="https://www.coursera.org">Coursera</a>. the script will return courses from the first page only</p>
<p>main.py script takes --keyword <value> argument to search for courses with specific keyword</p>
<p>tester.py script has some unit tests</p>

##### Commands:
<p>Install needed libraries: <span>`pip install -r requirements.txt`</span></p>
<p>To run the main.py: `python main.py --keyword "web Scraping"`</p>
<p>To run unit tests: `python tester.py`.</p>


### Argo WorkFlows:
<p>`argo_workflow.yaml` file has configuration of 4 tasks workflow with consideration of dependencies. each task is responsible of one action</p>
<p>The workflow scheduled to be run in weekly basis</p>