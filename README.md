# Employee Management System

This project is a web-based employee management system built using Flask. It includes features such as employee sign-up with OTP verification, punch-in and punch-out tracking, and face verification for employee identification.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [License](#license)

## Project Structure

```
my_flask_app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   ├── email_utils.py
│   ├── templates/
│   │   └── frontend.html
│   ├── static/
│   │   └── FRAS_logo.png
│
├── run.py
├── requirements.txt
├── .env
├── .flaskenv
├── README.md
├──dlib_face_recognition_resnet_model_v1.dat
├──LICENSE
├──shape_predictor_68_face_landmarks.dat
```

## Features

- **Employee Signup**: Employees can sign up with their ID, name, mobile number, email, and photos.
- **OTP Verification**: Email-based OTP verification during sign-up.
- **Punch In/Out**: Employees can record their punch-in and punch-out times.
- **Face Verification**: Verifies employee identity using face recognition technology.

## Requirements

- Python 3.x
- Flask
- MySQL
- Pillow
- face-recognition
- OpenCV

## Setup

### 1. Clone the repository

```bash
git clone <Repository Link>
cd my_flask_app
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the following:

```
SECRET_KEY=your_secret_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
```

### 5. Configure Flask environment

Create a `.flaskenv` file in the project root and add the following:

```
FLASK_APP=run.py
FLASK_ENV=development
```

### 6. Setup the MySQL database

1. **Create a Database**:
   ```sql
   CREATE DATABASE <your_database_name>;
   ```

2. **Update the Database Connection**:
   Ensure the `create_connection` function in `app/database.py` matches your MySQL setup:
   ```python
   connection = mysql.connector.connect(
       host="localhost",
       user="your_mysql_user",
       password="your_mysql_password",
       database="your_database_name",
       auth_plugin='mysql_native_password'
   )
   ```

## Running the Application

1. **Run the Flask application**:
   ```bash
   flask run
   ```

2. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

### Signup

1. Navigate to the signup page.
2. Fill in the employee details including ID, name, mobile number, email, and person name.
3. Click "Send OTP" to receive an OTP in the provided email.
4. Enter the OTP and upload photos.
5. Click "Signup" to complete the registration process.

### Punch In/Out

1. Use the endpoints `/punch_in` and `/punch_out` to record punch-in and punch-out times.

### Face Verification

1. Use the `/verify_face` endpoint to verify employee identity using face recognition.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
