# Image Storage
***Storage for uploading images.***

### Description

Description
This is an api site for storing images. You can upload your image to the site and depending on your subscription level (Base, Premium, Enterprise) get links of different resolutions on the site.
- Base level - height 200 px
- Premium - height 200 px, 400 px
- Enterprise - height 200 px, 400 px, and a link to the original image
- The admin can create links to images of different sizes, as well as change user subscription levels

### Technologies

- Python 3.9
- Django 3.2.9
- Django Rest Framework 3.12.4

### Quick start

1. Install and activate the virtual environment
2. Install all packages from [requirements.txt](https://github.com/nick-rebrik/image_store_api/blob/main/requirements.txt)<br>
  ```pip install -r requirements.txt```
3. Run in command line:<br>
  ```python manage.py makemigrations```<br>
  ```python manage.py migrate```<br>
  ```python manage.py runserver```
4. Visit the [homepage](http://127.0.0.1:8000/) and start using
