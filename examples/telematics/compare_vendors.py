"""Compare telematics vendors side by side.

API V5 has no comparison endpoint, so this calls
:meth:`Telematics.get_vendor_v5 <route4me.telematics.Telematics.get_vendor_v5>` once per vendor. Each
call sends ``GET /modules/api/v5.0/telematics/vendors`` with ``vendor_id`` in the query (API V5, on
``wh.route4me.com``). The vendors are then printed as a table, one column per vendor.

Run it with::

    python examples/telematics/compare_vendors.py --api_key <your key> --vendor_ids <ID>,<ID>[,<ID>...]
"""

import argparse

from route4me import Route4Me

#: Vendor fields compared as they are.
FIELDS = ("id", "name", "title", "is_enabled", "is_readonly")


def _summary(vendor):
    """Return the values to compare for one vendor.

    :param vendor: the vendor, as returned by ``get_vendor_v5``.
    :return: field name mapped to the text to print.
    """
    row = {field: str(vendor.get(field, "")) for field in FIELDS}
    row["credentials"] = ", ".join(c.get("name", "") for c in vendor.get("credentials") or [])
    row["sync_entities"] = ", ".join(e.get("title", "") for e in vendor.get("sync_entities") or [])
    return row


def _print_side_by_side(rows):
    """Print one line per field, with one column per vendor.

    :param rows: the summaries from :func:`_summary`, one per vendor.
    """
    labels = list(rows[0])
    label_width = max(len(label) for label in labels)
    widths = [max(len(row[label]) for label in labels) for row in rows]
    for label in labels:
        cells = "  ".join(row[label].ljust(width) for row, width in zip(rows, widths))
        print(f"{label.ljust(label_width)}  {cells}".rstrip())


def vendor_id_list(text):
    """Parse the ``--vendor_ids`` argument.

    :param text: comma-separated vendor IDs, e.g. ``"1,58,155"``.
    :return: the IDs as integers.
    """
    return [int(part) for part in text.split(",") if part.strip()]


def main(api_key, vendor_ids):
    """Fetch each vendor and print them side by side.

    :param api_key: Route4Me API key.
    :param vendor_ids: IDs of the vendors to compare.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    rows = []
    for vendor_id in vendor_ids:
        vendor = telematics.get_vendor_v5(vendor_id)
        if isinstance(vendor, dict) and "errors" in vendor.keys():
            print(f"Vendor {vendor_id}: {vendor['errors']}")
        else:
            rows.append(_summary(vendor))
    if rows:
        _print_side_by_side(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telematics Vendors Comparison")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--vendor_ids",
        dest="vendor_ids",
        help="Comma-separated IDs of the vendors to compare, e.g. 1,58,155",
        type=vendor_id_list,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.vendor_ids)
