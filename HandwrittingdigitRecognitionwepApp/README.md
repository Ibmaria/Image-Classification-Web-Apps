# Author Ibrahim Koné 
# Image Classification Restful Api

Image Classification Restful Api .

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Ibmaria/Image-Classification-Web-Apps.git
$ cd Image-Classification-Web-Apps/HandwrittingdigitRecognitionwepApp
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Storage
$ pip3 install -r requirements.txt or pip install -r requirements.txt or recents.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```





<br />


## Download Video App Here
![App Video](https://github.com/Ibmaria/Image-Classification-Web-Apps/blob/master/HandwrittingdigitRecognitionwepApp/videoapp.gif)


## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |--cnn/                              
   |--tensor
   |--tensorf                     
   |--Procfile              
   |--requirements.txt  
   |--recents.txt 
   |--model_digits.h5
   |--manage.py
   |
   |-- ************************************************************************
```

<br />





