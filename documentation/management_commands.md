### Managemement commands

There is several new built in management commands you can call by running `python manage.py`, in this file you will find the documentation for all of them.

##### load-recommendations
`python manage.py load-recommendations file.json [--root-data-folder]`

The command looks in `/data/recommendations` folder for the specified `file.json`,
if the file is somewhere else in the `/data/` folder, you can specify it with the
optional argument `--root-data-folder`. (*NOTE: when specifying a filepath within /data,
always use `/data/` as the root, and not `/backend/` if running from withing the docker container.*)
 
**Expected Datastructure** for `file.json` 
```
[
    {
        "userId":"123123",
        "recommendations": {
          "original": {
            "movieIds": [
              123,
              412,
              2,
              12
            ]
          },
          "SVD": {
            "movieIds": [
              123,
              412,
              16,
              32
            ]
          },
          "SVD-Reranked": {
            "movieIds": [
              123,
              412,
              55,
              11
            ]
          }
        },
        "user_description_short":"short story",
        "user_description_long":"long story"
    },
  {
    "recommendations": {
      "original": {
        "movieIds": [
          6,
          412,
          512,
          71
        ]
      },
      "SVD": {
        "movieIds": [
          85,
          412,
          512,
          71
        ]
      },
      "SVD-Reranked": {
        "movieIds": [
          123,
          412,
          510,
          11
        ]
      }
    },
    "userId": "4123215",
    "user_description_long": "long story for second user",
    "user_description_short": "short story for second user"
  }
]

```

**Example usecase**

I have a file `users.json` with recommendations for a spesific user, and want to load these into the database:

`python manage.py load-recommendations users.json`

My users.json is located in `/data/other_recommendations`:

`python manage.py load-recommendations users.json --root-data-folder /data/other_recommendations`
