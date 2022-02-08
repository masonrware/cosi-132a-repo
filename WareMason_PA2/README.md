<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="description" content="PA1ReadMe">
        <meta name="keywords" content="ReadMe">
        <meta name="author" content="Mason Ware">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style='font-family:Arial, Helvetica, sans-serif'>
        <h1 style='border: 0; padding: 0; margin: 0;'>PA2</h1>
        <h1 style='border: 0; padding: 0; margin: 0'>COSI 132A -- Brandeis University</h1>
        <h4>Mason Ware</h4>
        <h5>Professor Peter Anick</h5>
        <h6>Date: 02/07/22</h6>
        <hr>
        <div id='description'>
            <h3>Description</h3>
            <p id='gen description'>This Program is used to search through a given corpra of WSJ articles, found at 
                <code>/pa2_data/wapo.jl</code> . On the backend, the program utilizes the Flask
                framework for Python to stand up a web server and application. Via the templates
                found at <code>/templates</code> , a ui was generated and the capability for
                user interaction for searching was achieved. Retaining the data the user inputs
                using Jinja2 and Python script in <code>hw2.py</code> , the program processes
                said info in <code>utils.py</code>.
            </p>
            <br>
            Within utils, there are three methods: 
            <ol id='methods'>
                <li><code>load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Dict[str, Dict]
                </code></li>
                    <p>The <code>load_wapo</code> method is used to open the data located at <code>/pa2_data/wapo.jl</code>.
                    The method opens the file using a <code>with open</code> statment and jsonifys it using the <code>json</code>
                    built-in python package.</p>
                    <p>Reading through the data line by line, or dictionary item by dictionary item, 
                    the program first grabs the content, that is represented in each article's dictionary by a list of separate
                    dictionaries of html ssections. Using the list comprehension, <code> [item['content'] for item in contents 
                    if item['type'] == 'sanitized_html']</code> , to retain all the proper html items as specified by the instructions
                    and join them together to create a string of all the contents.</p>
                    <p>Next, the program creates a dictionary object containing all of the relevant data fields within an article.
                    Once it has built this dictionary, it then saves it as a value in another dictonary with the id of the article as
                    the key. What is left is a dictionary, called <code>articles_dict</code> in the code that is ids to dictionary items
                    of articles.</p>
                <br>
                <li><code>look_up_by_id(doc_id: int) -> Dict[str, Dict]</code></li>
                    <p>This method is far shorter than the others in the file. It works to search for a given id in the overall dictionary
                    and return its dictionary value, should it exist in the data, otherwises it raises a <code>KeyError</code> along with
                    the message: <code>'ARTICLE NOT FOUND'</code>. 
                    </p>
                <bR>
                <li><code>def title_match(query: str, title: str) -> bool</code></li>
                    <p>This method is also relatively short. It works to compare a given query, entered by the user, against a 
                    given title of one of the articles in the data. Should a match be found, True is returned and otherwise, False.
                    </p>
                    <p>This method is used in <code>./hw2.py</code> to find the titles among the data set overall that match the user's
                    query</p>
            </ol>
        </div>
        <br>
        <div id='Dependencies'>
            <h3>Dependencies</h3>
            <ol id='Dependencies List'>
                <li><code>Flask==2.0.2</code></li>
            </ol>
            <small>All dependencies can be found in the <code>./requirements.txt</code> file. Moreover, they can be automatically installed
            using the shell command: <code>pip install -r requirements.txt</code> and the most up to date versions of the dependencies can be installed using 
            the shell command: <code>pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
            </code>.</small>
        </div>
        <br>
        <hr>
        <div id='build and run'>
            <h2>Build & Run</h2>
            <div id='Build Instructions'>
                <h3>Build Instrcutions</h3>
                <p>As priorly mentioned, the first command to run in the terminal for this project's build is <code>pip install -r requirements.txt</code>.
                Once all packages are installed, the next step in the build process is to ensure that the data is located at <code>/pa2_data/wapo.jl</code>
                and is named properly. Due to the local scope of this project, if the file is not located and named correctly, the data will not be processed
                The last step is to ensure that an environment is active on your machine to allow python to execute. In the development of this project, a
                conda environment was used. You can create your own, use a ported venv from an editor like PyCharm, or create the one specified in the 
                <code>./environment.yml</code> file using the command <code>conda env create -f environment.yml</code>.</p> 
            </div>
            <div id ='Run Instrcutions'>
                <h3>Run Instrcutions</h3>
                <p>Now, in order to run the program after having built the environment and ensured the conditions, the python script in <code>hw2.py</code>
                needs to be run. To do so, run the program in a debug environment either by running the file via an editor's GUI or via the shell using the
                command, <code>python hw2.py</code> from the root of the project. Once you've done that, the project should be running locally. If you navigate
                to the correct localhost port in a browser, you should see the home page and a search bar prompting for a query. As a note,
                there is no typing correction or start end matching on the query keyword, which means whatever the user enters will be mathced across the
                entirety of the title. A search of <code>'a'</code>, would result in all files with an a in their title being returned and displayed.</p>
            </div>
        </div>
        <hr>
        <div id='Testing'>
            <h3>Testing</h3>
            <p>In lieu of unit tests, I tested this program by entering the following inputs: </p>
            <ul>
                <li>"" <p>To recieve a result of all 50 documents on 7 pages</p></li> 
                <li>"d.c." <p>To recieve a result of 3 documents on 1 page</p></li>
                <li>"prince" <p>To recieve a result of 1 document on 1 page</p></li>
                <li>"b" <p>To recieve a result of 22 documents on 3 pages</p></li>
            </ul>
        </div>
    </body>
</html>