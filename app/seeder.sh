rm db.*
rm */migrations/ -r
python3 manage.py makemigrations
python3 manage.py migrate
