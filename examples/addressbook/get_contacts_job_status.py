r"""Get the status of a background address book job, such as an export.

Calls :meth:`AddressBookV5.get_contacts_job_status
<route4me.address_book_v5.AddressBookV5.get_contacts_job_status>`, which sends
``GET /modules/api/v5.0/address-book/job-tracker/status/{job_id}`` (API V5, on ``wh.route4me.com``),
and prints the job status.

Run it with::

    python examples/addressbook/get_contacts_job_status.py --api_key <your key> --job_id <job ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, job_id):
    """Print the job status.

    :param api_key: Route4Me API key.
    :param job_id: ID of the job: the last segment of the ``Location`` header of the reply that started it.
    """
    route4me = Route4Me(api_key)

    response = route4me.address_book_v5.get_contacts_job_status(job_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get an Address Book Job Status (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--job_id", dest="job_id", help="Job ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.job_id)
