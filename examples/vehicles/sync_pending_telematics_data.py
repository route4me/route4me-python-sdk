r"""Sync a pending vehicle from a telematics connection.

Calls :meth:`VehiclesV5.sync_pending_telematics_data
<route4me.vehicles_v5.VehiclesV5.sync_pending_telematics_data>`, which sends
``POST /modules/api/v5.0/vehicles/sync/pending`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/sync_pending_telematics_data.py --api_key <your key> \
        --connection_id <connection ID> --telematics_vehicle_id <telematics vehicle ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, connection_id, telematics_vehicle_id):
    """Sync the pending telematics vehicle and print the reply.

    :param api_key: Route4Me API key.
    :param connection_id: Route4Me telematics gateway connection ID.
    :param telematics_vehicle_id: Route4Me telematics gateway vehicle ID.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.sync_pending_telematics_data(
        vehicle_alias="Example van",
        r4m_telematics_gateway_connection_id=connection_id,
        r4m_telematics_gateway_vehicle_id=telematics_vehicle_id,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync a Pending Telematics Vehicle")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--connection_id",
        dest="connection_id",
        help="Route4Me telematics gateway connection ID",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--telematics_vehicle_id",
        dest="telematics_vehicle_id",
        help="Route4Me telematics gateway vehicle ID",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.connection_id, args.telematics_vehicle_id)
