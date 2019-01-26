#!/usr/bin/env python3

"""This is a very simple script to verify
if the given Google credentials are valid"""
from google.auth.exceptions import DefaultCredentialsError

from dotenv import load_dotenv

load_dotenv()


def valid():
    from google.cloud import storage

    try:
        # If you don't specify credentials when constructing the client, the
        # client library will look for credentials in the environment.
        storage_client = storage.Client()
        # Make an authenticated API request
        buckets = list(storage_client.list_buckets())
    except DefaultCredentialsError as e:
        return False

    return True


if __name__ == '__main__':
    msg = "Valid credentials" if valid() else "Invalid credentials"
    print(msg)
