# Accuknox-Django-Assignment-SJS

STEP - 1 : 

Download this project in Computer by  :

 	git clone https://github.com/MynaMeisKai/Accuknox-Django-Assignment-SJS.git
or by :
	goto the git repo of desire project inside that repo <>code - there we can download in zip file 

--------------------------------------------------------------------------------------------------------------------------------------
STEP - 2 :

open cmd in windows

if you need a virtual environment for this project just use this command -> -venv name- is "any name"

	python -m venv venv name

	<venv name>\Scripts\activate

---------------------------------------------------------------------------------------------------------------------------------------

STEP - 3 :

After completing step-1 goto the project folder in command prompt window , run tis command to install t rquird files in the venv

	pip install -r requirements.txt

----------------------------------------------------------------------------------------------------------------------------------------

STEP - 4 :

Inside the project file you find manage.py using cmd prompt, just run this line for migrations

	python manage.py makemigrations
	
 	python manage.py migrate

if you want your data in database just delete the migration file except __init__.py
then continue  the above command line 

admin=> sam@a.com , 123 



-----------------------------------------------------------------------------------------------------------------------------------------

Install the required Docker and docker Desktop in you're PC

then open Docker Desktop , leave it .

Then create Dockerfile and docker-compose.yml in the project folder  and write the requirements

in cmd cd / or cd .. to the project Dockerfile  and paste it

	docker build -t acc-social-app . 
 
		it takes time to build
  
	docker-compose up --build 

it will host your app in docker in given port to me 8000
if you give port like 9000 it runs in 9000

-----------------------------------------------------------------------------------------------------------------------------------------





API ENDPOINTS  COLLECTIONS =>  https://documenter.getpostman.com/view/29989056/2sAXjM5Bxz




 
