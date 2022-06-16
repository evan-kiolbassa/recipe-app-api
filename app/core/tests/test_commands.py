# patch is used for mocking
from unittest.mock import patch
# Error raised when
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test Commands
    """

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database if database ready.
        Mock object has a check method that will be called.
        """
        patched_check.return_value = True
        # Executes commands from wait_for_db.py
        call_command('wait_for_db')
        # Assert mock was called once with specified args
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep,patched_check):
        '''
        Test waiting for database when OperationalError.

        The first two times the mock object is called, 
        psycopg2error should be raised. This is raised when the 
        database is not ready to accept conncections.

        Then, the next three calls will raise an OperationalError.
        This exception is raised from Django
        '''

        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count,6)

        patched_check.assert_called_with(databases = ['default'])