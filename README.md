# Puddle Marketplace (Django Web Application)

A clean, idiomatic, fully-functional Django marketplace application built for technical interview demonstration. Buyers can browse, search, and inquire about items via a direct messaging system, while sellers can list, update, and manage their listings.

---

## 🚀 Quick Start (Local Setup)

1. **Clone & Navigate to Directory**
   ```bash
   git clone <repo-url>
   cd Marketplace
   ```

2. **Set Up Virtual Environment & Install Dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (Admin Access)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server & Access Application**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

6. **Run Automated Test Suite**
   ```bash
   python manage.py test core
   ```

---

## 📁 Project Architecture & Directory Structure

```text
Marketplace/
├── core/                       # Primary Django Application
│   ├── admin.py                # Admin site registrations & filters
│   ├── apps.py                 # Core app config
│   ├── forms.py                # Forms (SignUpForm, ItemForm, EditItemForm, ContactForm, MessageForm)
│   ├── models.py               # ORM Models (Category, Item, Profile, Message) & Signals
│   ├── tests.py                # Unit & Integration test suite
│   ├── views.py                # Request handling logic (index, browse, detail, item CRUD, inbox, auth)
│   └── templates/core/         # HTML Templates styled with Tailwind CSS
│       ├── base.html           # Master layout with navbar, alerts, and footer
│       ├── index.html          # Homepage with hero & recent listings
│       ├── browse.html         # Item search & category filter sidebar
│       ├── detail.html         # Item view with seller actions & buyer messaging
│       ├── form.html           # Reusable form template for New/Edit Item
│       ├── contact.html        # Contact form with validation & flash messages
│       ├── signup.html         # User registration form
│       ├── login.html          # User authentication login
│       ├── inbox.html          # Active buyer-seller conversations list
│       └── conversation.html   # Chat message history & reply box
├── marketplace/                # Django Project Root Configuration
│   ├── settings.py             # App settings, media roots, & auth redirects
│   ├── urls.py                 # Global URL dispatcher & dev media serving
│   ├── wsgi.py                 # WSGI gateway entrypoint
│   └── asgi.py                 # ASGI gateway entrypoint
├── media/                      # Uploaded user images (Item pictures, avatars)
├── manage.py                   # Django CLI management script
└── requirements.txt            # Dependency file (Django, Pillow)
```

---

## 💡 Plain-English Interview Explanation Guide

### 1. Database Models (`core/models.py`)
- **`Category`**: Stores marketplace product categories (e.g., *Electronics*, *Clothing*, *Books*). Uses `slug` for clean URL query filtering.
- **`Item`**: Represents products listed for sale. Includes title, description, price, optional image, `is_sold` flag, and ForeignKeys linking to `Category` and `seller` (`User`).
- **`Profile`**: Extends Django's built-in `User` model via a `OneToOneField`. Contains optional user bio and avatar picture.
- **`Message`**: Stores direct communications between buyers and sellers. Linked to a specific `Item`, `sender` (`User`), and `receiver` (`User`).

### 2. Django Signals (`post_save`)
- **Profile Auto-Creation**: Uses a `@receiver(post_save, sender=User)` signal. Whenever a new `User` account is registered, Django automatically triggers `create_user_profile` to instantiate a linked `Profile` record, ensuring 1:1 integrity without manual creation logic in views.

### 3. Authentication & Security
- Uses Django's built-in `UserCreationForm` wrapped in `SignUpForm` and built-in `LoginView` / `LogoutView`.
- Actions requiring login (such as listing an item, editing, deleting, or accessing inbox) are guarded with Django's `@login_required` decorator.
- Permission enforcement: Edit and delete item endpoints inspect `item.seller == request.user` via `get_object_or_404(Item, pk=pk, seller=request.user)` to guarantee users can only modify their own listings.

### 4. Forms & Validation (`core/forms.py`)
- **ModelForms** (`ItemForm`, `EditItemForm`, `MessageForm`): Map directly to database models, automatically converting HTML inputs into validated model fields.
- **Standard Forms** (`ContactForm`): Validates user inputs (Name, Email, Message) using Django's built-in field cleaning before triggering flash notifications with `messages.success()`.

### 5. Direct Messaging System (`inbox` & `conversation_detail`)
- Plain request/response chat system without websockets or third-party JS.
- Conversations are grouped dynamically by `(item, other_user)` pair. Unread message counters dynamically update when incoming messages arrive, and incoming unread messages automatically mark as `is_read=True` when viewed.