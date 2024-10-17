# Flask API Project

This project is a Flask API that implements functionality for handling `Episode`, `Guest`, and `Appearance` data models based on the ER diagram provided. The relationships between these models are as follows:

- An `Episode` has many `Guests` through `Appearances`.
- A `Guest` has many `Episodes` through `Appearances`.
- An `Appearance` belongs to both a `Guest` and an `Episode`.

The API supports CRUD operations with appropriate validations, cascading deletes, and serialization rules to manage recursive relationships.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mikemunene16/lateshow
cd lateshow
```

### 2. Set Up the Python Environment

This project uses **Pipenv** for dependency management. Install Pipenv and create a virtual environment with the required dependencies from the `requirements.txt` file:

```bash
pipenv install && pipenv shell
```

### 3. Install Dependencies

Ensure that all project dependencies from `requirements.txt` are installed:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

The project uses a relational database. Before running the app, set up your database with migrations and seed the data.

#### Running Migrations

To create the necessary tables, run the migrations:

```bash
flask db upgrade
```

#### Seeding the Database

A seed file (which uses a CSV file) is provided to populate the database. If you encounter issues with the seed file, you may generate your own seed data for testing.

To seed the database:

```bash
python seed.py
```

### 5. Run the Application

To start the Flask API, use the following command:

```bash
python app.py
```

The API will now be running locally at `http://127.0.0.1:555/`.

## Deliverables

### Data Models

The following models are implemented:

- **Episode**: Represents an episode with attributes such as date and number.
- **Guest**: Represents a guest with attributes such as name and occupation.
- **Appearance**: Represents an appearance of a guest on an episode, along with a `rating`.

### Relationships

- An `Episode` has many `Guests` through `Appearances`.
- A `Guest` has many `Episodes` through `Appearances`.
- An `Appearance` belongs to both an `Episode` and a `Guest`.
- Cascading deletes are configured to remove related `Appearances` when an `Episode` or `Guest` is deleted.

### Validations

- The `Appearance` model has a validation to ensure the `rating` is between 1 and 5 (inclusive).

### Routes

The following API routes are implemented:

#### a. GET `/episodes`
Returns a list of all episodes.

```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

#### b. GET `/episodes/:id`
Returns a specific episode with associated appearances.

```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      },
      "guest_id": 1,
      "id": 1,
      "rating": 4
    }
  ]
}
```

If the `Episode` does not exist, the response will be:

```json
{
  "error": "Episode not found"
}
```

#### c. GET `/guests`
Returns a list of all guests.

```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  },
  {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
]
```

#### d. POST `/appearances`
Creates a new appearance associated with an existing episode and guest. Accepts a JSON object with the following fields:

```json
{
  "rating": 5,
  "episode_id": 100,
  "guest_id": 123
}
```

On success, returns the newly created appearance:

```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

If the appearance is not created successfully, the response will be:

```json
{
  "errors": ["validation errors"]
}
```
