## Setup guide for RecSys Framework

### Backend Cold start:
When pulling this repo for the first time, ensure that the handler app URL call is commented out in `backend/web/web/urls.py`.

Step 1:
From the root of the folder, run `docker-compose up --build`

Step 2: 
Open a new terminal and enter into the web container with the following command:
`docker exec -it DJANGO /bin/bash`

Step 3:
Load data into database with the following command:
Here you can choose between script args 25m / 1m or no arguments (-latest-small)

`python manage.py runscript csv-input --script-args 25m`

Step 4:
Create your super user:
`python manage.py createsuperuser`
Here just follow the prompts

Step 5:
Uncomment handler app URL in `backend/web/web/urls.py`.

Done!

If you neeed random users, go into the django container:
`docker exec -it DJANGO /bin/bash`
and run:

`python3 manage.py runscript create-random-recs`

This will give you 10 users rating 30 random movies with a rating of 5.

### Running Frontend for Development
Ensure you have node installed, I've operated with node 18, but node 16 should also sufice.

from `/frontend` folder, run `npm install`

run: `npm run dev`

have fun!