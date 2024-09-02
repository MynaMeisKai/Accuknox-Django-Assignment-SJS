# Accuknox-Django-Assignment-SJS






open cmd in windows

	python -m venv <venv name>

	<venv name>\Scripts\activate

create folder <Acc-social>

 	in cmd run -> pip install -r requirements.txt


After creating Dockerfile and docker-compose.yml and write the requirements

open Docker Desktop 

in cmd cd / or cd .. to the project Dockerfile  and paste it
	docker build -t acc-social-app . 
		it takes time to build
	docker-compose up --build 

	it will host your app in docker in given port to me 8000
		if you give port like 9000 it runs in 9000


 
