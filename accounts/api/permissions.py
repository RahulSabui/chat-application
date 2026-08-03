from rest_framework.permissions import IsAuthenticated


class IsLoggedIn(IsAuthenticated):
    pass