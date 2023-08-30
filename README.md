USE control+c to kill terminal

create env 
```bash
conda create -n wineq python=3.11.4 -y 
#this env is not for this folder, but for all the laptop & its folder structure
# if we create multiple env:
# env1: laptop & its folder structure
# env2: laptop & its folder structure........
# Above created Python virtual env is a self-contained workspace that includes its own Python interpreter, libraries and site-package directory installed using pip install in this env

python --version # to see the verison installed for this env
```

activate env
```bash
conda activate wineq
```

create a req file and install the req
```bash
pip install -r requirements.txt
```

create template.py to generate folder(with .gitkeep) & files structures. Then run it with:
```bash
python template.py
```

download the data from 
https://drive.google.com/drive/folders/18zqQiCJVgF7uzXgfbIJ-04zgz1ItNfF5?usp=sharing
to data_given folder

```bash
git init
```
```bash
dvc init 
```
```bash
dvc add data_given/winequality.csv
```

```bash
git remote add origin https://github.com/oneplus-user/wineq.git #add remote repo given(name): origin and URL to specify remote [ONE TIME]
git branch -M main #in local, to change current branch name from master to main[ONE TIME]
```

```bash
git pull # to pull all the files in remote(NOTE: It will not alter changes made in local)
```
```bash
git add . && git commit -m "first commit"
#in local, add . means to add all files for versioning purpose
#in local, and commit to changes(Its like saying its final)
```
```bash
git push origin main #push all the changes commited in local
```

Next 
1. we generate params.yaml files.
2. we create file inside src named:get_data.py --> touch src/get_data.py
    Note:
    we tried to import pandas but currently pandas is not there. How we know this?
    In terminal@MLOps level:(for any python commands, first type python) like below and exit
        -> python
        -> import pandas (will give error, so exit)
        -> exit()
        Hence add pandas in requirements.txt and separately in terminal@MLOps level:
        -> pip install pandas
then add content of get_data.py
-> python src/get_data.py
to load from remote(s3) and return dataframe

3. we create file inside src named:load_data.py --> touch src/load_data.py
then add content of load_data.py 
-> python src/load_data.py
to recieve dataframe from get_data.py, process, and save to data/raw folder

[OPTIONAL] as git tracks it as well
4. then add stage in dvc.yaml for above
-> dvc repro     # to generate dvc.lock

5. we create file inside src named:split_data.py --> touch src/split_data.py
then add content of split_data.py 
-> python src/split_data.py
to take data from data/raw folder and split in train/test and save to data/processed folder

[OPTIONAL] as git tracks it as well
6. then add stage in dvc.yaml for above
-> dvc repro     # to generate dvc.lock

7. we create file inside src named:train_and_evaluate.py --> touch src/train_and_evaluate.py 
then add content of train_and_evaluate.py 
-> python src/train_and_evaluate.py
to take data from data/processed folder and fit model and print evaluation metrics and {save models to saved_models folder, score&model_parameters to report folder}

[OPTIONAL] as git tracks it as well
8. then add stage in dvc.yaml for above
-> dvc repro     # to generate dvc.lock

#####
NOTE:
a. Main use of DVC:
    Now make changes in params.yml, and run dvc repro: It will run from the part of code where it requires to start running. I don't have to re-run from start or think about it. Now:
    --> dvc metrics show (to see scores and params)
    --> dvc metrics diff (to see the change in scores and params)
b. U can go to commits in git and if you want to go back:
    --> git checkout ......(number in front of each commit)
####


9. (tox.ini + setup.py) run (pytest) to test assertions in (test_config.py)
10. EDA for putting up tests above and custom error generation in (test_config.py)

9. Add pytest and tox in requirements.txt. But, separately in terminal@MLOps level:
        -> pip install pytest
        -> pip install tox

    
    [Without TOX, usage of PYTEST]
        Hence, Right now, we can run:
        ->pytest -v in terminal but we will get that "No test run".

        So, we make folder of tests and put test files to it:
            -> mkdir test
            -> touch tests/__init__.py tests/conftest.py tests/test_config.py
            add content to tests/conftest.py, tests/test_config
            In tests/test_config: we add our assertion which we want to test.
        
        ->pytest -v to run assertions mentioned in test_config.py but in existing env only


    [With TOX, usage of PYTEST]
    create tox.ini file in root directory
    -> touch tox.ini
    then add content to tox.ini where we create test env and command to run in it using pytest and flake8 tool.
    
       (a) -> tox (skipdist = True in tox.ini)
            It will first create temporary env .tox : which is fresh env with latest requirements and run assertions mentioned in test_config.py
            NOTE: with skipdist = False(default) in tox file, Tox will create a package like numpy for my code in temporary env before running assertions mentioned in test_config.py. This package in temporary env is built using setup.py.

       (b) so, let's create setup.py file.
            -> touch setup.py and add content to it.
            -> tox (skipdist = False in tox.ini)

    <!-- **********************************************************************************************
    *********** All action of setup.py in my working env, not temp env created by tox ************
    **********************************************************************************************
    Lets look at the folder structure given below:
    MLOps/
    ├── src/
    │   ├── __init__.py
    │   ├── module1.py
    │   ├── module2.py
    ├── setup.py
    ├── README.md
    Here, above structure denotes how package_directory(where source codes and setup.py reside). Hence, pwd is same as package directory.

    [DURING DEVELOPMENT]
    -> pip install -e . & "package_name.egg-info" folder will be created.
    [here we mention: "-e" for editable mode & "." as path for package directory==pwd] ; The package is installed to the Python environment with all the metadata taken from setup.py; over and above that, symlink is also created between the package directory and the Python environment's site-packages directory.
    then u can see the package newly generated in site-packages directory using 
    ->pip freeze
    U can also import src in python from any pwd, even if package name is wine_src but source code folder name is src because it has been added in this env as package

    [AFTER DEVELOPMENT]
    You would typically run:
    ->python setup.py sdist bdist_wheel
    to create dist folder where zip file of package will be there and can then be shared and installed using tools like pip
    ********************************************************************************************* -->

10. Now, we want to fill test_config.py as per my project data EDA. If we are making predictions, ranges of Xs can't be anything. It will be defined and if its beyond limits, we need to raise error. and this is what we want to achieve here.

For EDA,
in this working env, lets start jupyterlab:
-> pip install jupyterlab
-> jupyter-lab notebooks/
Jupyter lab notebook will open at @MLops/notebooks/ level. generate schema_in.json to check limits and raise error if payload is beyond the limit.

Also created NotInRange() custom error to raise error. Check in EDA.ipynb and test_config.py to raise error for test_generic2/3 in it.

11. create following files and folders:
-> mkdir -p prediction_service/model
-> touch prediction_service/__init__.py
-> touch prediction_service/prediction.py
-> mkdir webapp
-> mkdir -p webapp/static/css
-> mkdir -p webapp/static/script
-> mkdir -p webapp/templates
-> touch webapp/static/css/main.css
-> touch webapp/static/script/index.js #it is empty
-> touch webapp/templates/index.html
-> touch webapp/templates/404.html
-> touch webapp/templates/base.html
-> touch app.py

add content to: main.css, 404.html, base.html, index.html. It's very const stuff.

12. local deployment: app.py + prediction.py + POSTMAN/templates
13. global deployment: app.py + prediction.py + templates + Heroku

12. lets add content to app.py and transfer model to prediction_service
-> cp saved_models/model.joblib prediction_service/model
and set 
-> webapp_model_dir: prediction_service/model/model.joblib in params.yaml

-> python app.py for local deployment URL
& test deployment in local using POSTMAN or using template if you have any.

Lets see first commented part of app.py(don't need prediction.py which complement it):
    "Form format" and "JSON format" refer to two different ways of structuring data when sending information over HTTP request:
    (a) "Form format": key1=value1&key2=value2&key3=value3 sent from Postman/browser-based application
    (b) "JSON format": {"key1": "value1", "key2": "value2", "key3": "value3"} sent from Postman

    We have read_params() for model path, predict() to generate response using model, with
    any xyz function(at given path, here its root path) decorated by app. When request(<Request 'http://127.0.0.1:5000/' [POST/GET]>) comes to xyz function:
        POST:
        it checks whether it is 
         (a) request.form(call form_response and render_template("index.html", response=response))
         (b) request.json(call api_response and return json of response)
         (c) otw, render_template("404.html", error=error)
        GET:
         (a) render_template("index.html") without response

    Hence, you can just use just (POSTMAN and app.py) even if you don't have template.

Later on, we will make use of app.py(uncomment ones)+prediction.py+POSTMAN(if you don't have template).
<!-- POSTMAN -> Local Deployment testing-->

13. lets create workflow for github actions + Global Deployment:
-> mkdir -p .github/workflows
-> touch .github/workflows/ci-cd.yaml
add content to it.

 <!-- tox(only for python testing) ~ github actions(general version)
    (a) dvc repro: in working env, run src codes corresponding to changes in params.yaml using dvc.yaml where we have defined all 3 stages and also save model, then execute step 12 to transfer model for usage in app.py
    (b) tox: use tox.ini(create test env, install deps, run flake pytest) to test assertions in    test_config.py -> ONLY FOR TESTING, WORK WITH PYTHON SCRIPTS ONLY
    (c) github actions: use tox.ini(on ubuntu, create python&NodeJS env & fetch latest code, install deps, run flake pytest heroku) -> FOR BOTH TESTING AND autoDEPLOYMENT, WORK WITH BOTH PYTHON+JS FILES -->
 
<!-- Why Node.js?
 When you're working on a project that involves both Python and JavaScript (for example, a web application with a backend written in Python and a frontend written in JavaScript), you might need to set up Node.js alongside Python. This ensures that you have the right tools available for both languages. -->

 Use Heroku(Heroku -> Global Deployment) for universal deployment.
 So, create Proc file and content to it (its general content) which Heroku will use to start with for deployment.
 uncomment/add Heroku part of (ci-cd.yaml) for (13.c), thus auto-deploy. But before that we need to connect heroku with git and also add keys from Heroku to secrets in GitHub.
 
 14. 
 ****************************************************************
 *********************** SUMMARY TILL NOW ************************
Till here we had:
DVC Pipeline: load_data -> split_data -> train_and_evaluate
then, we could have tox for testing&linting
OR,   we could have github actions for testing&linting and then deployment to heroku.
So you see, we need github actions so that for any model generated through DVC pipeline, first testing will be done and then only deployment will be processed, otw, if test fails, prior model will continue to serve.

Overall: 
[DVC pipeline -> transfer model&schema_in to prediction service -> tox(testing)& app.py+POSTMAN(local deployment testing) -> github actions(testing & global deploy using Heroku)]

Now, 3 things are still left to update:
 (a) test_config.py for testing
 (b) app.py has all the functions for predict and raise error. we will keep app.py clean and transfer all the functions to predict and raise error to prediction.py
 <!-- CI(cont integration) & CT(cont testing) & CD(cont deployment) are being done. -->
 (c) We are still not doing model versioning, so will do using mlflow.
 ****************************************************************
 ****************************************************************

 15. 
 Part 14(b)
 copy schema_in.json created at notebooks folder to prediction service
 -> cp notebooks/schema_in.json prediction_service
add content to prediction.py.

<!-- How we are handling errors in prediction.py?
    ->  function: return True/ raise errors(e1, e2)
    ->  class ei(Exception):               #Exception is the parent class and ei is sub-class of it
        def __init__(self, message="message of ei"):    # constructor of subclass
            self.message = message
            super().__init__(self.message)         # return message if [except ei as e] is given

    (1) try block: will execute code or raise error using (code or function itself). The moment error is raised, either in function or code, control is transferred to except block
    (2) except ei: will be executed only if ei is raised in try block
    (3) except ei as e: will be executed only if ei is raised in try block & can be used to print(e) from ei
    (4) except: will be at last and will be run if None of mentioned errors(ei_s) are raised
    (5) except Exception as e:  will be at last and will be run if None of mentioned errors(ei_s) are raised & can be used to print(e)

    try:
        if a/function:
            do this
    except e1 as e:
        print(e)
        print(1)
    except e2 as e:
        print(e)
        print(2)
    except Exception as e:
        print(e)
        print(3) -->




