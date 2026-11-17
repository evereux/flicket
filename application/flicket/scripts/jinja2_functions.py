#! usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import re

import markdown
from markupsafe import Markup, escape


def now_year():
    return datetime.datetime.now().strftime('%Y')


# Dangerous URI scheme inside an href/src attribute that markdown links or
# images could emit.
_DANGEROUS_LINK = re.compile(
    r'(?i)(<[^>]*?\b(?:href|src)=")\s*(?:javascript|vbscript|data):[^"]*(")'
)


def render_markdown(text):
    if not text:
        return ""
    # Python-Markdown passes raw HTML straight through, so user supplied ticket
    # and comment content must be HTML escaped before rendering. Otherwise a
    # normal user can store <script>/<img onerror=...> that executes in every
    # viewer's browser (stored XSS). Markdown formatting still works on the
    # escaped text.
    html = markdown.markdown(str(escape(text)), extensions=['fenced_code', 'tables'])
    # Remove javascript:/vbscript:/data: URIs from any links or images markdown
    # may have produced.
    html = _DANGEROUS_LINK.sub(r'\1\2', html)
    return Markup(html)
