from config import settings
import urllib.parse
import secrets

from auth.state_storage import state_storage


def generate_google_oauth_redirect_uri() -> str:
    random_state = secrets.token_urlsafe(16)
    state_storage.add(random_state)

    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(
            [
                settings.GOOGLE_DRIVE_SCOPE,
                settings.GOOGLE_CALENDAR_SCOPE,
                settings.GOOGLE_PROFILE_SCOPE,
                settings.GOOGLE_EMAIL_SCOPE,
                settings.GOOGLE_OPENID_SCOPE,
            ]
        ),
        "access_type": "offline",
        "state": random_state,
    }
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"
