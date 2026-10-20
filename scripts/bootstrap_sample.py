import os
import sys
from pathlib import Path

import django
from django.contrib.auth import get_user_model
from django.core.management import call_command


def _env(name: str, default: str) -> str:
    value = os.environ.get(name, default).strip()
    if not value:
        raise ValueError(f"Environment variable {name} cannot be empty.")
    return value


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings")
    django.setup()

    call_command("migrate", interactive=False)

    username = _env("DJANGO_SUPERUSER_USERNAME", "admin")
    email = _env("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = _env("DJANGO_SUPERUSER_PASSWORD", "change-me-admin-password")

    user_model = get_user_model()
    user = user_model.objects.filter(username=username).first()
    if user:
        if not user.is_superuser or not user.is_staff:
            user.is_superuser = True
            user.is_staff = True
            user.save(update_fields=["is_superuser", "is_staff"])
        print(f"Superuser already exists: {username}")
    else:
        user_model.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        print(f"Superuser created: {username}")

    if not _env_bool("SAMPLE_LOAD_FIXTURE", False):
        return

    from hierarchy.models import MPTTGroup

    if MPTTGroup.objects.exists():
        print("Skipping fixture load: hierarchy data already exists.")
        return

    fixture_path = project_root / "sample" / "fixtures" / "linux_hierarchy.json"
    call_command("loaddata", str(fixture_path))
    print("Loaded sample fixture: sample/fixtures/linux_hierarchy.json")


if __name__ == "__main__":
    main()
