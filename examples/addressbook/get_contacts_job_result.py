r"""Get the result of a finished background address book job.

Calls :meth:`AddressBookV5.get_contacts_job_result
<route4me.address_book_v5.AddressBookV5.get_contacts_job_result>`, which sends
``GET /modules/api/v5.0/address-book/job-tracker/result/{job_id}`` (API V5, on ``wh.route4me.com``),
and prints the job result.

Run it with::

    python examples/addressbook/get_contacts_job_result.py --api_key <your key> --job_id <job ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, job_id):
    """Print the job result.

    :param api_key: Route4Me API key.
    :param job_id: ID of the job.
    """
    route4me = Route4Me(api_key)

    response = route4me.address_book_v5.get_contacts_job_result(job_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get an Address Book Job Result (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--job_id", dest="job_id", help="Job ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.job_id)
