from rauth import OAuth2Service
from flask import current_app, url_for, request, redirect
import json


def register():
    try:
        user_role = UserRole.get_or_create(name="user")
        current_time = rethink.now()
        new_user = User.create(
            userName=session["username"],
            password="",    # None, because it's required for
                            # Flask-Login's auth key setup,
            email=session["email"],
            confirmed_at=current_time,
            roles=[user_role[0]["name"]],
            provider_id="{pid}${uid}".format(pid=session["provider"],
                                             uid=session["user_id"]),
            active=True
        )

        new_user.save()

        user = User.get(provider_id="{}${}".format(
            session["provider"],
            session["user_id"]
        ))

        if user is not None:
            login_user(user, True)
            return True, None
        else:
            return False, None
    except Exception as e:
        return False, e


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['CLIENT_ID']
        self.consumer_secret = credentials['CLIENT_SECRET']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class BeamSignIn(OAuthSignIn):

    def __init__(self):
        super(BeamSignIn, self).__init__("beam")
        self.service = OAuth2Service(
            name="beam",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://beam.pro/oauth/authorize",
            access_token_url="https://beam.pro/api/v1/oauth/token"
        )
        # self.callback_url = self.

    def authorize(self):
        params = {
            "redirect_uri": self.get_callback_url(),
            "response_type": "code",
            "scope": "user:details:self"
        }
        return redirect(self.service.get_authorize_url(**params))

    def callback(self):
        if "code" not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                "code": request.args["code"],
                "grant_type": "authorization_code",
                "redirect_uri": self.get_callback_url(),
                "client_id": self.consumer_id,
                "client_secret": self.consumer_secret
            },
            decoder=lambda b: json.loads(b.decode('utf-8'))
        )
        me = oauth_session.get("https://beam.pro/api/v1/users/current").json()

        return me
