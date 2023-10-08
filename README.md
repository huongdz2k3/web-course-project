Step 1: grab the code from the repository on GitHub:

git clone https://github.com/MinhHoan147/e-learning-django.git

Step 2: Create a new virtual environment and activate it:

$ cd LMS

$ python3 -m venv venv \&\& source venv/bin/activate

Step 3: Install the requirements and migrate the database:

(venv) $ pip install -r requirements.txt

(venv) $ python manage.py makemigrations

(venv) $ python manage.py migrate

Step 4: Run the server:

(venv) $ python manage.py runserver