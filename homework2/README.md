# Homework 2 - CS4300/CS5300
## Student Information
**Name:** Mehak Hagemann  
**Course:** CS4300/CS5300
**GitHub Username:** mikki613  




# Movie Theater Booking System  
 Homework 2 using Django + Django REST Framework + Bootstrap

---

## Project Overview

This project is a full-stack Movie Theater Booking System built using Django and Django REST Framework (DRF).

The application provides:

- A RESTful API
- A Bootstrap-based web interface
- Authentication-protected booking
- Unit and integration tests
- BDD testing using Behave

Users can:
- View available movies
- View available seats
- Book seats for a movie
- View their booking history

---

## Repository Structure

This project is located inside the `homework2` directory of the main repository:

cs4300/
└── homework2/
├── manage.py
├── requirements.txt
├── behave.ini
├── bookings/
├── movie_theater_booking/
└── features/


---

##  Database Models

###  Movie
- title
- description
- release_date
- duration (minutes)

###  Seat
- seat_number

###  Booking
- movie (ForeignKey)
- seat (OneToOneField)
- user (ForeignKey)
- booking_date

Seats cannot be double-booked.

---

##  API Endpoints

Base URL (local development):

```bash

https://app-mhagema3-21.devedu.io/ 

```
## Base URL (Render deployment):

``` bash

https://cs4300-hw2-movie-booking.onrender.com

```



### Movies
- `GET /api/movies/`
- `POST /api/movies/`
- `GET /api/movies/<id>/`
- `PUT/PATCH/DELETE /api/movies/<id>/`

### Seats
- `GET /api/seats/`


### Bookings
- `GET /api/bookings/` *(Authentication required)*
- `POST /api/bookings/` *(Authentication required)*

Booking history only returns the logged-in user's bookings.

---

### Web Interface Routes

- `/` – Displays available movies  
- `/movies/<int:movie_id>/book/` – Book a seat for a movie (requires login)  
- `/history/` – Shows the logged-in user’s booking history  

### Authentication Routes

User authentication is handled using Django’s built-in system.

- `/accounts/login/` – Login page  
- `/accounts/logout/` – Logout  
- `/admin/` - Admin Panel

If a user tries to book a seat without being logged in, they are redirected to the login page.

### Features:
- Disabled seats once booked
- Success/error alerts
- Authentication required to book seats
- Bootstrap 5 styling

---

## Setup Instructions

### Clone the Repository

```bash

git clone https://github.com/mikki613/cs4300.git

cd cs4300/homework2

```
---

###  Create Virtual Environment

```bash

python3 -m venv hw2_env --system-site-packages
source hw2_env/bin/activate
```

---

###  Install Dependencies

```bash 
pip install -r requirements.txt
```

---

###  Apply Database Migrations

```bash
python3 manage.py migrate

```
---

###  Create Superuser

```bash
python3 manage.py createsuperuser

```
---

###  Run Development Server

```bash 
python3 manage.py runserver 0.0.0.0:3000

```

### Open in browser:

```bash

https://app-mhagema3-21.devedu.io/ 

``` 

---

### Live Deployment using Render:

This project has been deployed on Render and is publicly accessible at:

```bash

https://cs4300-hw2-movie-booking.onrender.com/

``` 

You can use this link to:

- View the movie listing page

- Book seats (after logging in)

- View booking history

The application was deployed using Render’s Web Service configuration with Gunicorn and environment variables for ADMIN_USER and ADMIN_PASS.

---

### Render Configuration:

This project is deployed using Render’s free tier Web Service.

Because the free tier uses ephemeral storage, the SQLite database does not persist permanently. This means:

- Any data added through the admin panel may be lost if the service restarts.

- Superusers created manually through the admin may not persist after a redeploy.

- Movies and bookings may disappear after inactivity or redeployment.

---

### Build Command:  

```bash

pip install -r requirements.txt && python manage.py migrate && python manage.py seed && python manage.py collectstatic --noinput

``` 

The custom `seed` management command creates:

A default superuser (using environment variables)

A sample movie if none exist

---

collectstatic is included in the build command because the project uses WhiteNoise for serving static files in production.

Ensure `ALLOWED_HOSTS` includes:
- DevEdu domain
- localhost
- 127.0.0.1
- testserver
- .onrender.com

### Start Command: 

```bash

gunicorn movie_theater_booking.wsgi:application

```



---

##  Testing

### Django Unit & Integration Tests

```bash
python3 manage.py test

``` 

These tests verify:
- API endpoints return correct status codes
- Booking requires authentication
- Seats cannot be double-booked
- Booking history is filtered per user

---

### BDD Testing with Behave

```bash

behave
```

BDD scenario verifies:
- BDD tests verify application behavior such as restricting access for unauthenticated users.

---


##  Security Considerations

- Authentication required for booking
- Booking history restricted per user
- Seat double-booking prevented
- CSRF protection enabled
- Proper ALLOWED_HOSTS configuration

---

##  AI Usage Disclosure

AI tools (ChatGPT) were used to assist with:

- Django project scaffolding
- Debugging configuration issues
- Structuring documentation/Grammar correction
- Render related questions and concerns.

All code was reviewed, tested, and modified to meet assignment requirements.

---

##  Assignment Requirements Covered

- Django project created inside homework2 directory
- Models implemented correctly
- DRF ViewSets implemented
- REST API endpoints functional
- Bootstrap-based UI implemented
- Booking logic enforced
- Unit & integration tests implemented
- BDD tests implemented
- Ready for deployment

