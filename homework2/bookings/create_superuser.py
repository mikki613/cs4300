import os
import django


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")
    django.setup()

    from django.contrib.auth import get_user_model

    # Only run when the flag is enabled
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
