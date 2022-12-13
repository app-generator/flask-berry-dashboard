# [Flask Berry Bootstrap 5](https://github.com/app-generator/flask-berry-dashboard)

Open-source **Flask Dashboard** project crafted on top of **Berry**, an open-source `Boostrap 5` design from [CodedThemes](https://codedthemes.com/?ref=appseed)
The product is designed to deliver the best possible user experience with highly customizable feature-rich pages. `Berry` has easy and intuitive responsive design whether it is viewed on retina screens or laptops.

<br />

> Features

- ✅ `Up-to-date dependencies`
- ✅ Database: `SQLite`, MySql
- ✅ `DB Tools`: SQLAlchemy ORM, `Flask-Migrate`
- ✅ `Authentication`, Session Based
- ✅ `Dark Mode` (persistent)
- ✅ Docker, `Flask-Minify` (page compression)
- ✅ **UI Kit**: [Berry BS5](https://github.com/app-generator/cth-berry-bootstrap5) `v1.0.1` by CodedThemes
  - `Persistent` **Dark-Mode**

<br />

![Berry Bootstrap 5 - Dark-Mode ready, Open-source Template.](https://user-images.githubusercontent.com/51070104/207091062-e805b36c-663a-4a01-acb8-9c55ab914f4f.jpg)

<br />


## ✨ Start the app in Docker

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`) 

```bash
$ # Get the code
$ git clone https://github.com/app-generator/flask-berry-dashboard.git
$ cd flask-berry-dashboard
```

<br />

> 👉 **Step 2** - Edit `.env` and set `DEBUG=True`. This will activate the `SQLite` persistance. 

```txt
DEBUG=True
```

<br />

> 👉 **Step 3** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

## ✨ How to use it

> Download the code 

```bash
$ # Get the code
$ git clone https://github.com/app-generator/flask-berry-dashboard.git
$ cd flask-berry-dashboard
```

<br />

### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD 
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />

> Start the app

```bash
$ flask run
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

## ✨ Code-base structure

The project has a simple, intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- apps/__init__.py
   |-- apps/
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/
   |         |
   |         |-- includes/                 # Page chunks, components
   |         |    |
   |         |    |-- navigation.html      # Top bar
   |         |    |-- scripts.html         # JS scripts common to all pages
   |         |    |-- footer.html          # The common footer
   |         |
   |         |-- layouts/                  # App Layouts (the master pages)
   |         |    |
   |         |    |-- base.html            # Used by common pages like index, UI
   |         |
   |         |-- home/                     # UI Kit Pages
   |              |-- index.html           # default page
   |              |-- page-404.html        # 404 error page
   |              |-- *.html               # Used by common pages like index, UI
   |
   |-- requirements.txt
   |
   |-- run.py
   |
   |-- ************************************************************************
```

<br />

## Screenshots

![Berry Bootstrap 5 - Sign IN, Open-source Starter by AppSeed.](https://user-images.githubusercontent.com/51070104/207091198-2753246e-3d65-4aac-96de-0598a9a94788.jpg)

<br />

> [Flask Berry Bootstrap 5](https://github.com/app-generator/flask-berry-dashboard) - `Icons` Page

![Berry Bootstrap 5 - UI Icons page, Open-source Starter by AppSeed](https://user-images.githubusercontent.com/51070104/207091655-d5005e08-7ea0-4367-ab3a-2cd16934d2fd.jpg)

<br />

> [Flask Berry Bootstrap 5](https://github.com/app-generator/flask-berry-dashboard) - `Colors` page

![Berry Bootstrap 5 - Colors page, Open-source Starter by AppSeed](https://user-images.githubusercontent.com/51070104/207091441-942be542-2794-4bdb-a51d-85c75b5bc692.jpg)

<br />

---
[Flask Berry Bootstrap 5](https://github.com/app-generator/flask-berry-dashboard) - Minimal **Flask** starter provided by **[AppSeed](https://appseed.us/)**
