from django.contrib.auth.models import BaseUserManager

from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, password, **extra_fields):
        if not first_name:
            raise ValidationError("Ism bo'lishi shart")

        if not last_name:
            raise ValidationError("Familiya bo'lishi shart")

        if not phone_number:
            raise ValidationError("Telefon raqam bo'lishi shart")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, phone_number, password, **extra_fields):
        user = self.create_user(first_name, last_name, phone_number, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
