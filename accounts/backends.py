from django.shortcuts import get_object_or_404
from .models import Vendor, User
import logging
from django.contrib.auth.backends import BaseBackend


class AuthUser(BaseBackend):
    def authenticate(self, request, name=None, password=None):
        try:
            user = get_object_or_404(User, name=name)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists ")
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None


class AuthVendor(BaseBackend):
    """ In case we want to do some additional
        stuff when authenticating
        a user, we have this. """
    def authenticate(self, request, name=None, password=None):
        try:
            user = get_object_or_404(Vendor, name=name)
            if user.check_password(password):
                return user
            else:
                return None
        except Vendor.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists ")
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = Vendor.objects.get(id=user_id)
            if user.is_active:
                return user
            return None
        except Vendor.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None
