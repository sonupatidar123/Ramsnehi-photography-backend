# Ramsnehi Photography — Django Backend

A Django + DRF backend powering the Ramsnehi Photography portfolio site.

---

## Project Structure

```
ramsnehi_backend/
├── gallery/
│   ├── migrations/
│   ├── admin.py          ← Admin panel configuration
│   ├── apps.py
│   ├── models.py         ← GalleryItem, Film, Testimonial, Inquiry
│   ├── serializers.py    ← DRF serializers
│   ├── views.py          ← ViewSets
│   └── urls.py           ← App-level router
├── ramsnehi/
│   ├── settings.py       ← All configuration (DRF, CORS, Media)
│   ├── urls.py           ← Project-level URL dispatcher
│   └── wsgi.py
├── media/                ← Uploaded images (auto-created)
├── requirements.txt
└── manage.py
```

---

## Quick Start

### 1. Clone & create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Create a superuser (for Admin access)
```bash
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

---

## API Endpoints

| Method | Endpoint                    | Description                          | Auth Required |
|--------|-----------------------------|--------------------------------------|---------------|
| GET    | `/api/gallery/`             | List all gallery photos              | No            |
| GET    | `/api/gallery/{id}/`        | Single gallery photo detail          | No            |
| GET    | `/api/films/`               | List all cinematic films             | No            |
| GET    | `/api/films/{id}/`          | Single film detail                   | No            |
| GET    | `/api/testimonials/`        | List all testimonials                | No            |
| GET    | `/api/testimonials/{id}/`   | Single testimonial detail            | No            |
| POST   | `/api/inquiries/`           | Submit a contact/booking inquiry     | No            |

### Filtering Examples

```
# Filter gallery by category
GET /api/gallery/?category=Wedding
GET /api/gallery/?category=Pre-Wedding

# Filter films by type
GET /api/films/?type=Cinematic+Film
GET /api/films/?type=Viral+Reel

# Fetch only featured testimonials
GET /api/testimonials/?is_featured=true

# Search
GET /api/gallery/?search=reception

# Pagination
GET /api/gallery/?page=2
```

### Sample Inquiry POST Body
```json
{
    "full_name": "Priya Sharma",
    "email": "priya@example.com",
    "inquiry_type": "Wedding Photography",
    "event_date": "2025-12-15",
    "vision": "We are looking for candid, emotional shots from our wedding in Udaipur."
}
```

---

## Admin Panel

Visit **http://localhost:8000/admin/** and log in with your superuser credentials.

You'll see:
- **Gallery Items** — Add/edit/delete photos with category tags and image preview
- **Films** — Manage YouTube-linked cinematic films and reels
- **Testimonials** — Toggle featured status with inline editing
- **Inquiries** — View-only client submissions (cannot be modified to preserve integrity)

---

## Connecting to the React Frontend

In your React app, replace mock data fetch calls like:

```js
// Before (mock data)
const photos = MOCK_GALLERY_DATA.filter(p => p.category === 'Wedding');

// After (live API)
const res = await fetch('https://ramsnehi-photography-backend.onrender.com/api/gallery/?category=Wedding');
const data = await res.json();
const photos = data.results;   // DRF pagination wraps results in .results
```

For the contact form:
```js
await fetch('http://localhost:8000/api/inquiries/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
});
```

---

## Production Checklist

- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Replace `SECRET_KEY` with a strong random value (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Switch database to PostgreSQL
- [ ] Configure media file storage (AWS S3 recommended via `django-storages`)
- [ ] Add your production domain to `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
- [ ] Remove `BrowsableAPIRenderer` from `DEFAULT_RENDERER_CLASSES`
- [ ] Set up HTTPS and configure `SECURE_SSL_REDIRECT = True`