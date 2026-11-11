# SkyLink Airlines Flight Ticketing System

## Project Overview
This project is a web-based Flight Ticketing System developed for SkyLink Airlines. It allows customers to search for flights, make reservations, retrieve booking details, and cancel bookings. It also includes an administrative dashboard for managing flights and viewing system metrics.

## Technologies Used
*   **Backend:** Python 3.8, Flask
*   **Frontend:** HTML5, CSS3, JavaScript (Jinja2 Templates)
*   **Database:** SQLite3
*   **Security:** Werkzeug (Password Hashing)

## Installation and Setup Instructions

1.  **Extract the Project:** Extract the submitted ZIP file to a local directory.
2.  **Navigate to the Directory:** Open your terminal and navigate to the project root:
    ```bash
    cd flight_ticketing_system
    ```
3.  **Set up a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
4.  **Install Dependencies:** Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Initialize the Database:** Run the database script to create the schema and populate it with sample flights and the default administrator account:
    ```bash
    python3 database.py
    ```

## Running the Application
1. Start the Flask development server:
  ```bash
  python3 app.py

2. Access the application in your web browser at: 
http://127.0.0.1:5000

## Administrator Credentials
To access the administrative dashboard (http://127.0.0.1:5000/admin/login), use the following fictional credentials:

- Username: admin

- Password: admin123