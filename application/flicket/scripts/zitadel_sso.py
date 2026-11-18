#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
Single sign on via Zitadel (https://zitadel.com) using OpenID Connect.

The client is configured from the OIDC discovery document published by the
issuer, e.g. https://id.exam-studio.com/.well-known/openid-configuration.
"""

import base64
import datetime
import os
import re

from authlib.integrations.flask_client import OAuth
from sqlalchemy import func

from application import app, db
from application.flicket.models.flicket_user import FlicketUser, user_field_size
from application.flicket.scripts.hash_password import hash_password

oauth = OAuth()


def register_zitadel():
    """
    Registers the Zitadel OIDC client with Authlib. Endpoints are discovered
    from '<ZITADEL_ISSUER>/.well-known/openid-configuration'.

    Uses the authorization code flow with PKCE (S256) as recommended for web
    (confidential) clients.
    """
    if not app.config.get('ZITADEL_ENABLED'):
        return

    oauth.register(
        'zitadel',
        client_id=app.config['ZITADEL_CLIENT_ID'],
        client_secret=app.config['ZITADEL_CLIENT_SECRET'],
        server_metadata_url=app.config['ZITADEL_ISSUER'].rstrip('/') + '/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid profile email',
            'code_challenge_method': 'S256',
        },
    )


def _unique_username(username):
    """
    Returns a username based on the given one that doesn't collide with an
    existing account. Appends -2, -3 ... if required.
    """
    candidate = username[:user_field_size['username_max']]
    suffix = 1
    while FlicketUser.query.filter(func.lower(FlicketUser.username) == func.lower(candidate)).count() > 0:
        suffix += 1
        stem = username[:user_field_size['username_max'] - len(str(suffix)) - 1]
        candidate = '{}-{}'.format(stem, suffix)
    return candidate


def _locale_from_claim(locale):
    """ Maps the locale claim to a supported language, defaulting to en. """
    supported = app.config.get('SUPPORTED_LANGUAGES', {'en': 'English'})
    if locale and locale[:2] in supported:
        return locale[:2]
    return 'en'


def get_sso_user(userinfo):
    """

    Finds the local account belonging to a Zitadel identity and provisions it
    on first login:

    1. match by stored oidc_sub,
    2. fallback match by verified email address (account gets linked),
    3. otherwise auto create a new account with no groups.

    :param userinfo: dict of claims from the Zitadel user info endpoint.
    :return: FlicketUser or None when the account is disabled / can't be provisioned.
    """
    sub = userinfo.get('sub')
    email = userinfo.get('email')

    # only trust the email address when the provider says it is verified.
    if userinfo.get('email_verified') is False:
        email = None

    user = None
    if sub:
        user = FlicketUser.query.filter_by(oidc_sub=sub).first()

    if user is None and email:
        user = FlicketUser.query.filter(
            func.lower(FlicketUser.email) == email.lower()).first()

    if user is not None:
        # keep local data in sync with the identity provider.
        changed = False
        if sub and user.oidc_sub != sub:
            user.oidc_sub = sub
            changed = True
        name = userinfo.get('name') or userinfo.get('preferred_username')
        if name and user.name != name:
            user.name = name
            changed = True
        if changed:
            db.session.commit()
        return user if not user.disabled else None

    # unknown identity: only provision when we have an email to work with.
    if not email:
        return None

    name = userinfo.get('name') or userinfo.get('preferred_username') or email.split('@')[0]
    name = name[:user_field_size['name_max']]
    username = _unique_username(re.sub(r'[^a-zA-Z0-9._-]', '', email.split('@')[0]) or 'user')
    locale = _locale_from_claim(userinfo.get('locale'))

    # password hash of random bytes; the user never logs in with it.
    unusable_password = hash_password(base64.b64encode(os.urandom(24)).decode('utf-8'))

    new_user = FlicketUser(username=username,
                           name=name,
                           email=email,
                           password=unusable_password,
                           date_added=datetime.datetime.now(),
                           job_title=None,
                           locale=locale,
                           disabled=False)
    new_user.oidc_sub = sub
    db.session.add(new_user)
    db.session.commit()

    return new_user
