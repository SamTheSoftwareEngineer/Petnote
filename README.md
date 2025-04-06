# 🐾 PetNote

**PetNote** is a pet care management app that helps pet owners stay organized and on top of their pet's daily needs. Users can log, track, and manage care activities like walks, feedings, and grooming — all in one place.

## 🚀 MVP Features

- User authentication (sign up, log in, log out)
- Add and manage multiple pets
- Track daily activities (e.g., walking, grooming, feeding)
- Mark activities as completed
- Dashboard view of pet activity status
- Mobile-responsive design with Tailwind CSS

## 🛠️ Tech Stack

**Frontend**
- Django Templates
- Tailwind CSS

**Backend**
- Django
- Django REST Framework

**Database**
- PostgreSQL

**Deployment**
- Heroku (or similar PaaS)

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/petnote.git
cd petnote
```

### 2. Create and activate a virtual environment 

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

### 3. Install dependencies 

```
pip install -r requirements.txt
```

### 4. Set up the database
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)
```
python3 manage.py createsuperuser
```

### 6. Run the development server 
```
python3 manage.py runserver
```

Visit http://localhost:8000 in your browser

✨ Coming Soon
Activity history & analytics

Reminders & notifications

Vet and medication tracking

Stripe integration for premium features

💡 Project Goals
PetNote aims to become a lightweight SaaS platform for pet owners who want a simple yet effective way to manage their pets' care routines. The MVP focuses on core features that address everyday needs, with room to grow into a community-driven and monetizable product.

🧪 Running Tests
python manage.py test

📂 Folder Structure (MVP)
petnote/
├── petnote/         # Django project settings
├── pets/            # Pets app
├── activities/      # Activities app
├── templates/       # HTML templates
├── static/          # Tailwind CSS & other static files
├── requirements.txt
└── README.md

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

📫 Contact
Made with ❤️ by Sam
Reach out on GitHub or via Linked in my profile!


