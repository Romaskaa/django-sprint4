#!/usr/bin/env python
"""Django command-line utility."""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            'Django is not installed or is unavailable in the active '
            'virtual environment.'
        ) from error
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
