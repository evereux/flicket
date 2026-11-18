Single Sign On with Zitadel
===========================

Flicket can delegate user authentication to `Zitadel <https://zitadel.com>`_
(or any other OpenID Connect provider) using the authorization code flow with
PKCE. Local username / password login remains available alongside SSO.

User accounts are provisioned automatically on first login:

1. The account is matched by the stored ``oidc_sub`` (the Zitadel user id).
2. If no match is found, an existing account with the same email address is
   linked to the Zitadel identity.
3. Otherwise a new account is created with no groups assigned.

Groups and roles continue to be managed within Flicket by the administrator.
Logging out of Flicket also ends the session at Zitadel (single logout).

Configuring Zitadel
-------------------

In your Zitadel instance (for example ``https://id.exam-studio.com``):

1. Create a new **Web** application within your project.
2. Set the redirect URI to ``<your-flicket-url>/login/sso/callback``.
3. Set the post logout URI to ``<your-flicket-url>/``.
4. Enable the authorization code method (PKCE is used automatically).
5. Note the **client id** and **client secret**.

Configuring Flicket
-------------------

Add the following keys to ``config.json`` (or re-run ``flask run-set-up``)::

    "ZITADEL_ENABLED": true,
    "ZITADEL_ISSUER": "https://id.exam-studio.com",
    "ZITADEL_CLIENT_ID": "<client id from Zitadel>",
    "ZITADEL_CLIENT_SECRET": "<client secret from Zitadel>"

Endpoints are discovered automatically from
``<ZITADEL_ISSUER>/.well-known/openid-configuration``, so no further URL
configuration is required.

After changing the configuration restart Flicket and run ``flask db upgrade``
to add the ``oidc_sub`` column used for linking accounts.

Running Behind a Reverse Proxy
------------------------------

The callback url is built from the configured base url, or - when unset -
from the incoming request. Make sure the proxy forwards ``X-Forwarded-Proto``
and ``Host`` correctly, or set the base url via ``flask run-set-up``, so that
https is not downgraded to http in generated redirects.
