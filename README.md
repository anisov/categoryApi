# Categories Api use DRF

#### Configure and start project use docker.
1) export CURRENT_UID=$(id -u):$(id -g)
2) export PROJECT_DIR='path/to/project'
3) export CODE_FOLDER=categories_api
4) Create `docker/docker-compose.yml` based on `docker-compose.yml.sample`. 
5) Create `docker/dockerfiles/uwsgi.Dockerfile` based on `docker/dockerfiles/uwsgi.Dockerfile.sample`.
6) Create `docker/docker_data/nginx/nginx.conf `based on `docker/docker_data/nginx/nginx.conf.sample`.
7) Create `docker/docker_data/uwsgi/uwsgi.ini` based on `docker/docker_data/uwsgi/uwsgi.ini.sample`.
8) Create `categories_api/categories_api/local_settings.py` based on `categories_api/categories_api/local_settings.py.sample`.
9) docker-compose -f docker/docker-compose.yml build
10) docker-compose -f docker/docker-compose.yml up -d

#### Stop project.
docker-compose -f docker/docker-compose.yml down
***
#### Simple project start.
1) `cd ./categories_api`
2) `mkvirtualenv categories_api -p /usr/bin/python3`
3) `workon categories_api`
4) `pip install -r requirements.txt`
5) Create `categories_api/categories_api/local_settings.py` based on `categories_api/categories_api/local_settings.py.sample` and use sqlite3.
4) `./manage.py runserver`
***
#### Run tests.
py.test -s

## Project technical task

### Categories API

**Introduction**

Create a simple Categories API that stores category tree to database and returns category
parents, children and siblings by category id.

**Requirements**

Use Python 3 and Django Rest Framework.
Use of any other third-party libraries is prohibited.

**Categories Endpoint**

Create POST /categories/ API endpoint. Endpoint should accept json body (see example
Request), validate input data (see Request) and save categories to database (category name
should be unique).

**Example.**

Request:
```json
{
  "name": "Category 1",
  "children": [
    {
      "name": "Category 1.1",
      "children": [
        {
          "name": "Category 1.1.1",
          "children": [
            {
              "name": "Category 1.1.1.1"
            },
            {
              "name": "Category 1.1.1.2"
            },
            {
              "name": "Category 1.1.1.3"
            }
          ]
        },
        {
          "name": "Category 1.1.2",
          "children": [
            {
              "name": "Category 1.1.2.1"
            },
            {
              "name": "Category 1.1.2.2"
            },
            {
              "name": "Category 1.1.2.3"
            }
          ]
        }
      ]
    },
    {
      "name": "Category 1.2",
      "children": [
        {
          "name": "Category 1.2.1"
        },
        {
          "name": "Category 1.2.2",
          "children": [
            {
              "name": "Category 1.2.2.1"
            },
            {
              "name": "Category 1.2.2.2"
            }
          ]
        }
      ]
    }
  ]
}
```

**Category Endpoint**

Create GET /categories/<id>/ API endpoint. Endpoint should retrieve category name, parents,
children and siblings (see examples) by primary key (<id>) in json format.

**Example 1.**

GET /categories/2/

Response:
```json
{
  "id": 2,
  "name": "Category 1.1",
  "parents": [
    {
      "id": 1,
      "name": "Category 1"
    }
  ],
  "children": [
    {
      "id": 3,
      "name": "Category 1.1.1"
    },
    {
      "id": 7,
      "name": "Category 1.1.2"
    }
  ],
  "siblings": [
    {
      "id": 11,
      "name": "Category 1.2"
    }
  ]
}
```

**Example 2.**

GET /categories/8/

Response:
```json
{
  "id": 8,
  "name": "Category 1.1.2.1",
  "parents": [
    {
      "id": 7,
      "name": "Category 1.1.2"
    },
    {
      "id": 2,
      "name": "Category 1.1"
    },
    {
      "id": 1,
      "name": "Category 1"
    }
  ],
  "children": [],
  "siblings": [
    {
      "id": 9,
      "name": "Category 1.1.2.2"
    },
    {
      "id": 10,
      "name": "Category 1.1.2.3"
    }
  ]
}
```