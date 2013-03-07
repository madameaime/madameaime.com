from django.contrib.auth import get_user_model

import bcrypt


class V1BackwardCompatibilityBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            # check that old password format is valid
            if bcrypt.hashpw(password, user.password) == user.password:
                # store password using the django format
                user.set_password(password)
                user.save()
                return user

        except UserModel.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            UserModel = get_user_model()
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
