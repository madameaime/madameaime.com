from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore as DefaultSessionStore

from emarket.models import ShoppingCartLog


class SessionStore(DefaultSessionStore):
    def cycle_key(self):
        """For security, when an anonymous user logs in, a new session is
        created and the old session content is copied to the new one. This way,
        if an attacker had access to the anonymous session id, he wouldn't be
        able to access to the newly created authenticated session.

        The problem is that by default, Django adds a ON DELETE CASCADE to all
        foreign keys. ShoppingCartLog has a foreignkey on a session and when
        the anonymous session is destroyed, the shopping cart is too.

        This function gets all ShoppingCartLog entries for the anonymous
        session, call the super method cycle_key() to generate a new session
        id, and re-populate the user ShoppingCart (note: with a resetted timer).
        """
        # Get the current session
        session = Session.objects.get(session_key=self.session_key)
        # Get shopping cart entries related to this session
        sales = [log.sale for log in
                 ShoppingCartLog.objects.filter(session=session)]

        # Generate a new session
        super(SessionStore, self).cycle_key()

        # Get the new session
        session = Session.objects.get(session_key=self.session_key)
        # For every old session's shopping cart entry, create one for the new
        # session
        for sale in sales:
            ShoppingCartLog(sale=sale, session=session).save()
