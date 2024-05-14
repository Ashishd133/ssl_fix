"""
Module for returning the current date and time in a string format with underscores
"""
import datetime
import logging

def time_now():
    """
    Returns the current date and time in a string format
    with underscores (_) replacing spaces, colons, and dots.

    Returns:
    str: A string representing the current date
    and time in the format YYYY-MM-DD_HH_MM_SS_microseconds.
    """
    try:
        now = str(datetime.datetime.now())
        now = now.replace(" ", "_")
        now = now.replace(":", "_")
        now = now.replace(".", "_")
        return now
    except Exception as e:
        logging.error(str(e))
        raise
