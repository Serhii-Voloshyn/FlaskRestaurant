# FlaskRestaurant
Back end for managing lunch places.

## Installation

### Clone or Download

-  Clone this repo to your local machine using   
```
git clone https://github.com/Serhii-Voloshyn/FlaskRestaurant.git
```

### Required to install

- Project reqirements:
```
pip install -r /requirements.txt
```

### Environment

- Add the environment variables file (.env) to the project folder (/FlaskRestaurant/).
It must contain the following settings:
```
SECRET_KEY="Your secret key"
SQLALCHEMY_DATABASE_URI="Your uri"
```

### How to run locally

- Start the terminal.
- Go to the directory "your way to the project" / FlaskRestaurant /
- Run the following commands
```
flask init-db
flask run -p 8000
```

### How to run Docker

- Run project using Docker:
```
docker-compose up --build
```


## Flake8

- Run flake8:
```
flake8
```

## Tests

- Run project tests:
```
pytest ./tests/
```