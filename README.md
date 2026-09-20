# Puddle

A small marketplace web app built with Django and Tailwind CSS. Users can list items for sale, browse and search listings by category, and send direct messages to sellers.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create an admin user (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

To run the test suite:
```bash
python manage.py test core
```

## Project Structure

```text
Marketplace/
├── core/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── templates/core/
│       ├── base.html
│       ├── index.html
│       ├── browse.html
│       ├── detail.html
│       ├── form.html
│       ├── contact.html
│       ├── signup.html
│       ├── login.html
│       ├── inbox.html
│       └── conversation.html
├── marketplace/
│   ├── settings.py
│   └── urls.py
├── media/
├── manage.py
└── requirements.txt
```

## Data Models

- **Category**: Product category with a name and unique slug used for filtering listings.
- **Item**: Listed product containing a title, description, price, optional image, category reference, seller reference (Django `User`), and `is_sold` status flag.
- **Profile**: Extends Django's `User` model with `bio` and `avatar` fields via a `OneToOneField`. A `post_save` signal automatically instantiates a profile whenever a new user account is created.
- **Message**: Stores buyer-seller messages linked to a specific item, sender, receiver, and read status.

## Auth, Permissions, and Messaging

- **Authentication**: Built using Django's standard `User` model, `UserCreationForm`, and built-in `LoginView`/`LogoutView`.
- **Permissions**: Protected views use `@login_required`. Item editing and deletion views enforce `item.seller == request.user` so only item owners can modify or delete listings.
- **Direct Messaging**: Messages are grouped by item and interlocutor pair. The inbox lists active conversations with unread indicators, and opening a thread automatically marks incoming unread messages as read.