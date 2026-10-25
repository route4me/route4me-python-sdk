# Test fixtures

Recorded API payloads, captured once against the real Route4Me API and then
scrubbed before being committed:

- account and member identifiers replaced with obviously-fake values
- API keys removed entirely
- address data replaced with the public sample addresses used in `examples/`
- payloads trimmed to the fields the SDK and its tests actually read

Load them through the `load_fixture` fixture in `tests/conftest.py`:

```python
def test_something(mocked, load_fixture):
    mocked.add(responses.GET, URL, json=load_fixture("routes_list"))
```

To refresh one, capture the response from the live API outside the
repository, then re-scrub it. Never commit a payload straight from a real
account.
