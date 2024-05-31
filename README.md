# Study Gymon

Study Gymon is a Django-based web application designed to help South African matriculants collaborate and study more effectively. It provides a platform where students can form study groups, share resources, schedule study sessions, and track their progress. The application uses MySQL as its database.

## Features

- **User Registration and Authentication**: Secure sign-up and login for students.
- **Profile Management**: Users can create and manage their profiles.
- **Study Groups**: Create and join study groups based on subjects and interests.
- **Resource Sharing**: Upload and share study materials like notes, past papers, and textbooks.
- **Study Session Scheduling**: Schedule and manage study sessions with reminders.
- **Progress Tracking**: Track individual and group study progress.
- **Discussion Forums**: Engage in subject-specific discussions.

## Getting Started

These instructions will help you set up the development environment on your local machine.

### Prerequisites

- Python 3.x
- Django 3.x
- MySQL
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/7irelo/Study_Gymon.git
   cd Study_Gymon
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python3 -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database**
   - Ensure MySQL is installed and running.
   - Create a database named `studygymon`.
   - Update the database settings in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'studygymon',
             'USER': 'your_mysql_user',
             'PASSWORD': 'your_mysql_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000`.

## Contributing

We welcome contributions! Here’s how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact us at tirelo.eric@gmail.com.

---

Thank you for using Study Gymon! We hope it helps you achieve your academic goals.