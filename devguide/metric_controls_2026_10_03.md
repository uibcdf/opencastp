# Historical metric and precision controls — 2026-10-03

Owner: uibcdf/opencastp#6. This is a bounded diagnostic, not complete server equivalence.

## Historical metric and precision controls — 2026-10-03

The original 1996 volbl/metric.c does contain analytical tetrahedron, spherical
sector, cap and overlap calculations. The neighboring volbl.c assembles these
terms for SA quantities and probe-shrunk MS quantities. The original C source
was compiled unchanged outside the package with GCC 13.3.0, -O2, double
Vol_real and the explicitly pinned legacy headers. Only a separately authored
bridge supplies arrays and callbacks. No historical C source or binary is
redistributed in OpenCASTp.

Three controls hold each failing region's modern integration domain fixed:
accurate math.fsum accumulation of the Python terms; the compiled historical
C SA primitives; and evaluation of the same Python equations with mpmath at
40 and 80 decimal digits. The latter uses decimal strings of the modern
float64 coordinates/radii and reuses the native visibility/orientation decisions.
It tests precision of the same equations, not independently derived physics.

| Input / region | Field | Historical C | 80-digit evaluation, shortened | Strict comparison |
| --- | --- | ---: | ---: | --- |
| 1MRG / 22 | SA volume | 0.003499637802392569 | 0.003499637802067611 | fail |
| 1PSN / 13 | SA volume | 0.6854994934776033 | 0.6854994934778119 | fail |
| 1YPI / 6 | SA volume | 18.094500169285364 | 18.09450016928191 | fail |
| 1FBP / 3 | SA area | 299.2764954437971 | 299.2764954437971 | fail |
| 2FBP / 11 | SA volume | 36.26650173327073 | 36.26650173327425 | fail |

Every control retains every strict failure at 0.00050001. The compiled C
selected quantities differ from the Python production quantities by less than
7e-11; all historical correction/warning counters are zero. Forty/eighty-digit
selected quantities differ by less than 1e-30. These changes are over 100 times
smaller than the correction required to pass each fixed comparison. Simple
summation order, double-precision roundoff and an incorrect transcription of
these historical SA primitives do not explain the five observed residuals.

The exported bulb JSON independently constrains the integration domain for
these same five regions. All 247 printed orthospheres match one distinct
native supporting tetrahedron each: counts 2/13/42/141/49 respectively. Centers
and radii agree within half the four-decimal print quantum plus 1e-8; the
existing developer contact audit verifies four matching supports and no interior
atom. This is a five-region check, not qualification of every orthosphere in
the 89-input corpus. Printed orthospheres do not expose unrounded server inputs
or the server's metric implementation.

The C control deliberately feeds modern float64 arrays and native callbacks
into historical metric primitives. The original Alf_vect input type is float,
whereas Vol_real is double. The full historical reader, triangulation,
visibility and region pipeline was not run here. Consequently these results
neither certify full historical-pipeline equivalence nor demonstrate a bug or
large algorithmic change in CASTp3. Modern input materialization, metric
conventions and output/export precision remain candidate boundaries to inspect.
No production numerical source, radii or comparison tolerance changed.

Evidence: artifacts/historical_metric_controls_2026_10_03.json, with complete
selected values, 40/80-digit strings, orthosphere checks, producer versions,
compiler settings, legacy-source/header hashes and own collector hashes.
Historical source, server archives and frozen coordinate pickles remain
external. The regression in tests/test_comparison_evidence.py preserves all
five failures, control scope and collector integrity. The corpus status stays
84/89 passing systems; complete_server_equivalence remains false under #6.

### Replay the diagnostic

Copy the retained .py.txt collectors to their recorded /tmp Python names and
the .c.txt bridge to /tmp/opencastp_historical_metric_bridge.c. They record
absolute developer paths; adjust those paths when replaying elsewhere. In the
molecular developer environment, run opencastp_residual_diagnostic.py first to
rebuild the five private coordinate/term snapshots from the external ZIPs.
Pickle inputs are trusted local outputs of that collector, not a public API.
mpmath 1.3.0 is an explicitly used research-environment dependency; it is not
required by OpenCASTp's runtime or ordinary tests.

Compile the separately provided original source and own bridge as recorded:

```bash
gcc -fPIC -c -O2 \
  -I/path/to/Alphashape/castp/topomt_version/include \
  /path/to/Alphashape/castp/alpha-4.1-src/volbl/metric.c \
  -o /tmp/opencastp_historical_metric.o

gcc -shared -fPIC -O2 \
  -I/path/to/Alphashape/castp/topomt_version/include \
  -I/path/to/Alphashape/castp/alpha-4.1-src/volbl \
  /tmp/opencastp_historical_metric_bridge.c \
  /tmp/opencastp_historical_metric.o -lm \
  -o /tmp/opencastp_historical_metric.so

python /tmp/opencastp_residual_precision.py 1mrg 1psn 1ypi 1fbp 2fbp
python /tmp/opencastp_historical_metric_compare.py 1mrg 1psn 1ypi 1fbp 2fbp
python /tmp/opencastp_residual_orthospheres.py
python /tmp/opencastp_metric_controls_assemble.py
```

The diagnostic collectors exit zero when collection completes; their report
retains passed=false. Their exit is not a server-equivalence verdict. Historical
headers emit existing HIBITS/HIBITL redefinition warnings during compilation;
those are separate from the zero runtime metric correction/warning counters.
