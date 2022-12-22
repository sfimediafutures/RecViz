## Personalized Reranker Demo
### About
This demo is aimed at demonstrating how a personalized approach can be utilized to adjust the recommendation popularity to the preference of each particular user. Two example users have been selected - one has strong affinity towards "mainstream" and highly popular movies, while the other one is gravitating more towards less popular and niche movies. Traditionally popularity bias mitigation approaches have been exposing every user to less popular items in the same manner to promote less known content. This approach, however, takes into consideration every viewer's watching history attempting to gauge their interest towards popular/unpopular movies and only adjust the recommendation accordingly. Since classic recommender systems are known for recommending mostly popular items to every user, the reranker is expected to have less influence on popularity-aligned users, while the strongest changes are predicted to be observed in the recommendation for the niche items. The algorithm will attempt to lower the general popularity of recommended items, while still retaining an acceptable relevance and accuracy. Note: The users with extremely niche preferences are unfortunately practically treated as outliers - the algorithm has a hard time of finding highly relevant niche items to safely recommend without a significant loss in accuracy.

This Demo is based on the research of PHD Candidate Anastasiia Klimashevskaia @ SFI MediaFutures, UIB, who provided the recommendations and recommender system, and Developed by Research Assistant Snorre Alvsvåg @ SFI MediaFutures, UIB, who provided the full stack application. 

### contact: 
**Anastasiia Klimashevskaia** \
PHD, SFI MediaFutures, University of Bergen \
anastasiia.klimashevskaia@uib.no

**Snorre Alvsvåg** \
Research Assistant, SFI MediaFutures, University of Bergen \
snorre.alvsvag@uib.no

## Setup Guide for Demo:
Following is a guide on how to setup this Demo 


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

### Enviournment Variables:
In the **root** of the project, add a .env file, and add the following lines:

You'll need a TMDB API key for this project to run, you can find information about this here:
https://developers.themoviedb.org/3/getting-started/introduction
```bash
TMDB_KEY=''
DJANGO_SECRET_KEY=''
DJANGO_DEBUG=True
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


#### Developers note:
At the current iteration of this Demo, images are slow to load, this is simply due to how we find our posters. This is currently a slow process of multiple fetch calls, as no poster nor poster links have been crawled and cached, and therefore results in live crawl and fetch for every movie.  


#### Acknowledgements:
We utilize TMDB API calls for all images in this DEMO and thank TMDB for issuing their API, read more about them here: https://www.themoviedb.org/about