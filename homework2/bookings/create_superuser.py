"""
One-time helper script to create a Django superuser on Render (non-interactive).

"""

import os
import sys


def main():
    # Make sure the project root is on the Python path
    # (the folder that contains manage.py and movie_theater_booking/)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")

    import django
    django.setup()

    from django.contrib.auth import get_user_model

    if os.getenv("CREATE_SUPERUSER") != "1":
        print("CREATE_SUPERUSER not set to 1, skipping.")
        return

    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")

    if not username or not password:
        print("Missing DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD.")
        return

    User = get_user_model()

    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists.")
        return

    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"Created superuser '{username}' successfully!")


if __name__ == "__main__":
    main()
