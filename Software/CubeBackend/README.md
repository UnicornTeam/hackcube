Cube Backend
===================

## Description
- Cube backend with many backend API.
- File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.
- Using python2.7

## Setup
- Install system package. See the `system_package.txt` file. (*Unix)

- Create virtual enviroment (use `virtualenv`) and activate it.

- Then install python packages:  
```
$ pip install -r requirements.txt
```

You can run it under debug mode:
```
python app.py --debug True
```
And the program will use file under `./data` as mock data.

Or just run it using product config by default:
```
$ python app.py
```

- Go to http://127.0.0.1:5000


Use gunicorn:
```
pip install gunicorn
gunicorn --reload -w 4 -b 0.0.0.0:5000 app:app --access-logfile log/access.log --error-logfile log/error.log
```

Use uwsgi:
```
uwsgi --socket 0.0.0.0:5000 --enable-threads --protocol=http -w app:app
```