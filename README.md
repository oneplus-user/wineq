create env 

```bash
conda create -n wineq python=3.11.4 -y
python --version # to see the verison installed
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














tox command -
```bash
tox
```
for rebuilding -
```bash
tox -r 
```
pytest command
```bash
pytest -v
```

setup commands -
```bash
pip install -e . 
```

build your own package commands- 
```bash
python setup.py sdist bdist_wheel
```