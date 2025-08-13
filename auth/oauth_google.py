from config import settings
import urllib.parse


def get_query_string() -> str:
    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join([
            settings.GOOGLE_DRIVE_SCOPE,
            settings.GOOGLE_CALENDAR_SCOPE,
            settings.GOOGLE_PROFILE_SCOPE,
            settings.GOOGLE_EMAIL_SCOPE,
            settings.GOOGLE_OPENID_SCOPE,
        ]),
        "access_type": "offline",
        #     state: ...
    }
    return urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

def generate_google_oauth_redirect_uri():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{get_query_string()}"