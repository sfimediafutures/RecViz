## Setup Guide for Demo:

### Data for demo:
To download the necesarry datasets into the repo follow the following steps:
```bash
# From github root folder:

curl https://files.grouplens.org/datasets/movielens/ml-25m.zip --output backend/data/ml-25m.zip &&
unzip backend/data/ml-25m.zip
```
If you cannot use these terminal commands, you can manually download the dataset using the following link:
https://files.grouplens.org/datasets/movielens/ml-25m.zip and then unzip the folder. To add it to the project, add it into the `backend/data/...` folder so that it matches the following folder structure:

```
├── backend
│   └── data
│       └── ml-25m
│           ├── README.txt
│           ├── genome-scores.csv
│           ├── genome-tags.csv
│           ├── links.csv
│           ├── movies.csv
│           ├── ratings.csv
│           └── tags.csv

```

### Backend Cold start:
**Step 1:**
From the root of the folder, run `docker-compose up --build`

**Step 2:**
Before the Demo is ready to run locally, you'll need to do some adjustments:
Open a new terminal and enter into the web container with the following command:
`docker exec -it DJANGO /bin/bash`

**Step 3:**
Load data into database with the following command:
Here you can choose between script args 25m / 1m or no arguments (-latest-small)

`python manage.py runscript csv-input --script-args 25m`

ps: A few failed links are no problem, it happends.

**Step 4:**
For the Demo we need to populate the database with some users:
`python manage.py load-recommendations all_recs_and_rerank_2.json`

**Step 5:**
Create your super user:
`python manage.py createsuperuser`
Here just follow the prompts


The Demo is now live at 0.0.0.0


### Running Frontend for Development
Theres already a built and compiled version of the frontend served through the docker-compose file, so in theory you should not need to touch Node or the frontend. However if you want to make changes or poke around:
Ensure you have node installed, I've operated with node 18, but node 16 should also sufice.

from `/frontend` folder, run `npm install`

run: `npm run dev`

have fun!