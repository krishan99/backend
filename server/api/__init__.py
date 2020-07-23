"""server APIs."""
from server.api.account_setup import test_signin # for testing
from server.api.account_setup import signing_in
from server.api.account_setup import signing_up
from server.api.account_setup import update_account
from server.api.account_setup import retrieve_account
from server.api.queue_setup import delete_q
from server.api.queue_setup import update_q
from server.api.queue_setup import retrieve_q
from server.api.queue_setup import make_q
from server.api.queue_setup import retrieve_all
from server.api.queue_user import get_form_q
from server.api.queue_user import post_form_q
from server.api.queue_manage import get_q
from server.api.queue_manage import pop