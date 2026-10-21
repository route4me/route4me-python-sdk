# Advanced Constraints Examples

Each example runs an `ADVANCED_CVRP_TW` optimization of nine New York
addresses with two groups of drivers, set with
`Optimization.advanced_constraints` and `AdvancedConstraint` objects. A driver
serves only the stops whose tags match the group's, inside the group's time
windows (seconds from midnight).

| Example | Test case |
| --- | --- |
| `advanced_constraint_test_case_1.py` | Tags and fleets with different time windows |
| `advanced_constraint_test_case_2.py` | Some addresses without tags |
| `advanced_constraint_test_case_3.py` | A driver's shift with a break: two time windows for one group |

Run one from the repository root:

```
python examples/advanced_constraints/advanced_constraint_test_case_1.py --api_key <your key>
```
