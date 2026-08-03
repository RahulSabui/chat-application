from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:

    @staticmethod
    def generate_tokens(user):

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    @staticmethod
    def generate_tokens(user):

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def blacklist_token(refresh_token):

        token = RefreshToken(refresh_token)

        token.blacklist()