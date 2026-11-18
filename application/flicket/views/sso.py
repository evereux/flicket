#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
Views for single sign on via Zitadel (OIDC authorization code flow + PKCE).
"""

from urllib.parse import urlencode

from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_babel import gettext
from flask_login import login_user
from flask_principal import Identity
from flask_principal import identity_changed

from application import app, db, flicket_bp
from application.flicket.scripts.zitadel_sso import get_sso_user, oauth, register_zitadel

register_zitadel()

# session keys used to remember the login across the redirect round trip.
_next_session_key = '_sso_next_url'
_id_token_session_key = '_sso_id_token'


def _base_url():
    """ Configured base url or fallback derived from the current request. """
    base = app.config.get('base_url')
    if base:
        return base.rstrip('/')
    return request.url_root.rstrip('/')


def _redirect_uri():
    """ Absolute callback url. Uses the configured base url when available. """
    path = url_for('flicket_bp.sso_callback')
    if app.config.get('base_url'):
        return _base_url() + path
    return url_for('flicket_bp.sso_callback', _external=True)


def _end_session_endpoint():
    metadata = oauth.zitadel.load_server_metadata()
    return metadata.get('end_session_endpoint')


@flicket_bp.route(app.config['WEBHOME'] + 'login/sso')
def login_sso():
    """
    Kicks off the OIDC authorization code flow by redirecting the user to Zitadel.
    """
    if not app.config.get('ZITADEL_ENABLED'):
        abort(404)

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('flicket_bp.index'))

    # imported here to avoid a circular import (login.py imports this module).
    from application.flicket.views.login import is_safe_url

    # remember where the user wanted to go (validated on the way back).
    next_url = request.args.get('next')
    if next_url and is_safe_url(next_url):
        session[_next_session_key] = next_url

    return oauth.zitadel.authorize_redirect(_redirect_uri())


@flicket_bp.route(app.config['WEBHOME'] + 'login/sso/callback')
def sso_callback():
    """
    Exchanges the authorization code for tokens, provisions / matches the local
    account and logs the user in.
    """
    if not app.config.get('ZITADEL_ENABLED'):
        abort(404)

    next_url = session.pop(_next_session_key, None)

    try:
        token = oauth.zitadel.authorize_access_token()
        userinfo = oauth.zitadel.userinfo(token=token)
    except Exception:
        flash(gettext('SSO login failed. Please try again or use your username and password.'),
              category='danger')
        return redirect(url_for('flicket_bp.login'))

    user = get_sso_user(userinfo)

    if user is None:
        flash(gettext('Unable to sign you in via SSO. Your account may be disabled '
                      'or missing an email address.'), category='danger')
        return redirect(url_for('flicket_bp.login'))

    identity_changed.send(app, identity=Identity(user.id))
    login_user(user, remember=True)
    # authentication token is required for api use.
    user.get_token()
    db.session.commit()

    # id token kept only for as long as the session lives; used for single logout.
    session[_id_token_session_key] = token.get('id_token')

    flash(gettext('You were logged in successfully.'), category='success')
    if next_url:
        return redirect(next_url)
    return redirect(url_for('flicket_bp.index'))


def current_sso_session():
    """ True when the current session was established via SSO. """
    return session.get(_id_token_session_key) is not None


def sso_logout():
    """

    Ends the Zitadel session after the local logout. Returns a redirect response
    to the identity provider end session endpoint, or None when the current
    session wasn't an SSO login.

    Call after logout_user() has been executed.
    """
    if not app.config.get('ZITADEL_ENABLED') or not current_sso_session():
        session.pop(_id_token_session_key, None)
        return None

    id_token = session.pop(_id_token_session_key, None)

    end_session = _end_session_endpoint()
    if not end_session:
        return None

    params = {'post_logout_redirect_uri': _base_url() + app.config['WEBHOME']}
    if id_token:
        params['id_token_hint'] = id_token

    return redirect(end_session + '?' + urlencode(params))
