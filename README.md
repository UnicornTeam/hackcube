flask-file-uploader
===================

## Description
File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.


## Setup
- Install system package. See the `system_package.txt` file. (*Unix)

- Create virtual enviroment (use `virtualenv`) and activate it.

- Then install python packages:  
```
$ pip install -r requirements.txt
```

- Run it:

```
$ python app.py
```

- Go to http://127.0.0.1


Use gunicorn:
```
sudo gunicorn -w 4 -b 127.0.0.1:5000 app:app
```
or
```
DEBUG=0 authbind gunicorn -b 0.0.0.0:80 backend:app --access-logfile .log/access.log --error-logfile .log/general.log
```
