# 🌐 ConnectHub — Social Media Platform

A full-featured social media web application built with Django, Django REST Framework, Bootstrap 5, and SQLite. Includes user authentication with JWT, profiles, posts with image upload, likes, comments, follow system, user search, and dark mode.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📸 Features

### 👤 User System
- Register & login with JWT authentication
- Profile pages with bio, profile picture, location, website
- Edit profile with live image preview
- Follow / unfollow users with AJAX (no page reload)
- Followers & following lists

### 📝 Posts
- Create posts with text and/or image upload
- Edit and delete your own posts
- Image preview before posting
- Character counter (500 limit)

### ❤️ Social Interactions
- Like / unlike posts with AJAX
- Comment on posts
- Delete your own comments
- Post detail page with full comment thread

### 🔍 Discovery
- Search users by username
- Suggested users sidebar
- Home feed showing posts from followed users
- People You May Know section

### 🌙 UI/UX
- Dark mode toggle (persists across sessions)
- Fully responsive — works on mobile, tablet, desktop
- Colorful gradient design
- Smooth animations and transitions
- Auto-dismiss flash messages

### ⚙️ Admin Panel
- Manage users and profiles
- View and moderate posts and comments
- Inline profile editing on user page
- Image previews in admin

### 🧪 Testing
- Seed command to generate fake users and posts
- Faker-powered realistic test data

---

## 🗂️ Project Structure

```
connecthub/
├── connecthub/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                   # Users & profiles app
│   ├── models.py            # Profile, Follow system
│   ├── views.py             # Auth, profile, follow, search
│   ├── forms.py             # Register, login, profile forms
│   ├── urls.py              # User URL routes
│   ├── admin.py             # Admin configuration
│   └── signals.py           # Auto-create profile on register
├── posts/                   # Posts app
│   ├── models.py            # Post, Comment models
│   ├── views.py             # Feed, CRUD, likes, comments
│   ├── forms.py             # Post and comment forms
│   ├── urls.py              # Post URL routes
│   ├── admin.py             # Admin configuration
│   └── management/
│       └── commands/
│           └── seed_data.py # Fake data generator
├── static/
│   ├── css/style.css        # All styles + dark mode
│   └── js/main.js           # Dark mode, likes, previews
├── templates/
│   ├── base.html            # Base template with navbar
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── edit_profile.html
│   │   ├── search.html
│   │   ├── followers_list.html
│   │   └── suggested.html
│   └── posts/
│       ├── feed.html
│       ├── post_detail.html
│       └── edit_post.html
├── media/                   # Uploaded images
├── requirements.txt
└── manage.py
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/connecthub.git
cd connecthub
```

**2. Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Apply database migrations**
```bash
python manage.py migrate
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. (Optional) Seed with test data**
```bash
pip install faker
python manage.py seed_data --users 10 --posts 30
```

**7. Run the development server**
```bash
python manage.py runserver
```

**8. Open in browser**
```
http://127.0.0.1:8000/
```

---

## 📦 Requirements

```
django
djangorestframework
djangorestframework-simplejwt
pillow
django-cors-headers
faker
```

Install all at once:
```bash
pip install django djangorestframework djangorestframework-simplejwt pillow django-cors-headers faker
```

---

## 🌐 URL Reference

| Page | URL |
|------|-----|
| Home / Feed | `/` |
| Register | `/users/register/` |
| Login | `/users/login/` |
| Logout | `/users/logout/` |
| User Profile | `/users/profile/<username>/` |
| Edit Profile | `/users/edit-profile/` |
| Follow/Unfollow | `/users/profile/<username>/follow/` |
| Followers List | `/users/profile/<username>/followers/` |
| Following List | `/users/profile/<username>/following/` |
| Search Users | `/users/search/?q=name` |
| Suggested Users | `/users/suggested/` |
| Create Post | `/post/create/` |
| Post Detail | `/post/<id>/` |
| Like Post | `/post/<id>/like/` |
| Edit Post | `/post/<id>/edit/` |
| Delete Post | `/post/<id>/delete/` |
| Delete Comment | `/comment/<id>/delete/` |
| Admin Panel | `/admin/` |
| JWT Token | `/api/users/token/` |
| JWT Refresh | `/api/users/token/refresh/` |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Django 6.0 | Backend framework |
| Django REST Framework | REST API + JWT setup |
| SimpleJWT | JWT token authentication |
| django-cors-headers | CORS handling |
| SQLite | Database (development) |
| Pillow | Image processing |
| Bootstrap 5.3 | Frontend UI |
| Bootstrap Icons | Icon library |
| Faker | Test data generation |
| Google Fonts (Inter) | Typography |
| Vanilla JavaScript | Dark mode, AJAX likes, image preview |

---

## 🌙 Dark Mode

- Click the **Dark / Light** button in the navbar to toggle
- Preference is saved in localStorage — persists across sessions and page refreshes
- Smooth CSS transitions between modes

--


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Avinash Patel

Built with Django, DRF and Bootstrap 5 for internship project.

---

*Happy Connecting! 🌐*
