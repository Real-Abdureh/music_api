# 🎵 Music API - README Guide
## 📌 Project Overview


Music API is a Django-based RESTful API that enables users to manage artists, events, and bookings. Organizers can create events and assign artists, while artists can manage their profiles. This API provides authentication, role-based access control, and proper data validation.



## 🛠 Tech Stack

- Backend: Django, Django REST Framework (DRF)
- Database: PostgreSQL (or SQLite for development)
- Authentication: Django's default authentication with role-based access control
- Storage: Django's media file handling for profile images
- Dependencies: Django, djangorestframework, Pillow, psycopg2 (for PostgreSQL)




## 🚀 Getting Started
## 1️⃣ Clone the Repository

```sh
git clone https://github.com/Real-Abdureh/music_api.git
cd music_api
```

## 2️⃣ Set Up a Virtual Environment


# Create a virtual environment
```sh
python -m venv env
```

# Activate the virtual environment
# Windows:
```sh
env\Scripts\activate
```

# macOS/Linux:
```sh
source env/bin/activate
```

# 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

# 4️⃣ Configure Environment Variables

Create a .env file in the project's root directory and add the following:

```sh
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://your-db-user:your-db-password@localhost:5432/music_api_db
```

# 5️⃣ Apply Database Migrations
```sh
python manage.py migrate
```


# 6️⃣ Create a Superuser (Admin)

```sh
python manage.py createsuperuser
```

# 7️⃣ Run the Development Server

```sh
python manage.py runserver
```




## 🎭 User Roles


| Role | Permissions |
| ------ | ------ |
| Artist | [Create & update profile, join events] |
| Organizer | [Create & manage events, invite artists] |
| Admin | [Full control (via Django Admin panel)] |


## 🔗 API Endpoints
🔹 Authentication


| Method | Endpoint | Description |
| ------ | ------ | ------ |
| POST | [/api/auth/register/] |           Register a new user       |
| POST | [/api/auth/login/] |               Authenticate & retrieve token|
| POST | [/api/auth/logout/] |              Log out & revoke token|

🔹 Artists


| Method | Endpoint | Description |
| ------ | ------ | ------ |
| POST | [/api/artists/create/] |           Create Artists       |
| GET | [/api/artists/genres/] |               GET Genre|
| POST | [/api/artists/genres/] |              Create a Genre|
| GET | [/api/artists/list/] |              Get artist List|
| GET | [/api/artists/profile/] |              Get artist Profile|
| PUT | [/api/artists/profile/id/] |              Update artist Profile|


🔹 Bookings


| Method | Endpoint | Description |
| ------ | ------ | ------ |
| POST | [/api/bookings/create/] |           Create Booking       |
| GET | [/api/bookings/list//] |               GET Booking List|
| GET | [/api/bookings/id/] |              Retrieve a booking|
| PUT | [/api/bookings/id] |              Update a booking|



🔹 Events

| Method | Endpoint | Description |
| ------ | ------ | ------ |
| POST | [/api/events/create/] |           Create Event       |
| GET | [/api/events/list/] |               GET Event List|
| GET | [/api/api/events/id/] |              Retrieve an Event|
| PUT | [/api/api/events/id//] |              Update an Event|
| DELETE | [/api/api/events/id/] |              Delete an Event|


## 🛡 Security Considerations
- Always use environment variables for secrets (SECRET_KEY, DATABASE_URL).
- Set DEBUG=False in production.
- Use ALLOWED_HOSTS to prevent unauthorized access.

