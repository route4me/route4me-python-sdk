# Telematics Examples

Run each example from the repository root. Every example prints its own help
with `-h`.

## Vendors (API V5)

The vendor examples call API V5 on `wh.route4me.com`. The old vendor host,
`telematics.route4me.com`, is retired; `Telematics.get_vendors`, `get_vendor`,
`search_vendor` and `compare_vendors` still exist but warn and cannot succeed.

| Example | SDK method | Request |
| --- | --- | --- |
| `get_vendors.py` | `Telematics.get_vendors_v5()` | `GET /modules/api/v5.0/telematics/vendors/all` |
| `search_vendor.py` | `Telematics.get_vendors_v5(**filters)` | `GET /modules/api/v5.0/telematics/vendors/all` |
| `get_vendor.py` | `Telematics.get_vendor_v5(vendor_id)` | `GET /modules/api/v5.0/telematics/vendors?vendor_id=...` |
| `compare_vendors.py` | `Telematics.get_vendor_v5(vendor_id)`, once per vendor | `GET /modules/api/v5.0/telematics/vendors?vendor_id=...` |

`get_vendors_v5` returns the vendors under `data` and takes these optional
filters: `search`, `country`, `feature`, `features`, `size`, `is_integrated`,
`display_hidden`, `page` and `per_page`. API V5 has no comparison endpoint, so
`compare_vendors.py` fetches each vendor and prints them side by side.

```
python examples/telematics/get_vendors.py --api_key <your key>
python examples/telematics/search_vendor.py --api_key <your key>
python examples/telematics/get_vendor.py --api_key <your key> --vendor_id <vendor ID>
python examples/telematics/compare_vendors.py --api_key <your key> --vendor_ids <ID>,<ID>
```

## Connections (API V4)

A member's connections are reached with the member's telematics API token.
`register_member.py` prints it, and the examples that take `--member_id` get it
themselves with `Telematics.register_member`.

| Example | SDK method | Request |
| --- | --- | --- |
| `register_member.py` | `Telematics.register_member(member_id)` | `GET /api.v4/telematics/register.php` |
| `get_connections.py` | `Telematics.get_connections(api_token)` | `GET /api.v4/telematics/connections.php` |
| `get_vendors_connection_info.py` | `Telematics.get_vendors_info(api_token)` | `GET /api.v4/telematics/vendors.php` |
| `register_vendor_connection.py` | `Telematics.register_connection(api_token, ...)` | `POST /api.v4/telematics/connections.php` |
| `get_vendor_connection.py` | `Telematics.get_connection(api_token, connection_token)` | `GET /api.v4/telematics/connections.php` |
| `update_vendor_connection.py` | `Telematics.update_connection(api_token, connection_token, ...)` | `PUT /api.v4/telematics/connections.php` |
| `delete_vendor_connection.py` | `Telematics.delete_connection(api_token, connection_token)` | `DELETE /api.v4/telematics/connections.php` |

`register_vendor_connection.py` and `update_vendor_connection.py` read the
vendor credentials from a JSON file; `vendor_credentials.json` shows the shape,
with sample values.

```
python examples/telematics/register_member.py --api_key <your key> --member_id <member ID>
python examples/telematics/get_connections.py --api_key <your key> --member_id <member ID>
python examples/telematics/get_vendors_connection_info.py --api_key <your key> --member_id <member ID>
python examples/telematics/register_vendor_connection.py --api_key <your key> --member_id <member ID> \
    --vendor_credentials examples/telematics/vendor_credentials.json
python examples/telematics/get_vendor_connection.py --api_token <API token> --connection_token <connection token>
python examples/telematics/update_vendor_connection.py --api_token <API token> --connection_token <connection token> \
    --vendor_credentials examples/telematics/vendor_credentials.json
python examples/telematics/delete_vendor_connection.py --api_token <API token> --connection_token <connection token>
```

For general questions about the SDK and the API, see the
[examples FAQ](../README.md).
