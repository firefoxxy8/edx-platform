"""
Take the list of states from settings.RETIREMENT_STATES and forces the
RetirementState table to mirror it.

We use a foreign keyed table for this instead of just using the settings
directly to generate a `choices` tuple for the model because the states
need to be configurable by open source partners and modifying the
`choices` for a model field causes new migrations to be generated,
with a variety of unpleasant follow-on effects for the partner when
upgrading the model at a later date.
"""
from __future__ import print_function

import copy
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from openedx.core.djangoapps.user_api.models import UserRetirementRequest, UserRetirementStatus


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Implementation of the populate command
    """
    help = 'Cancels the retirement of a user who has requested retirement - but has not yet been retired.'

    def add_arguments(self, parser):
        parser.add_argument('email_address',
                            help='Email address of user whose retirement request will be cancelled.')

    def handle(self, *args, **options):
        """
        Execute the command.
        """
        email_address = options['email_address']

        # Load the user retirement status.
        retirement_status = UserRetirementStatus.objects.get(original_email=email_address)

        # Load and update the user record using the retired email address.
        user = User.objects.get(email=retirement_status.retired_email)

        # Delete the user retirement status record.
        retirement_status.delete()

        # Delete the "permanent" retirement request record.
        retirement_request = UserRetirementRequest.objects.get(user=user)
        retirement_request.delete()

        print("Successfully cancelled retirement request for user with email address '{}'.")
