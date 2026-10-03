# Joint precision and individual-mouth controls — 2026-10-03

Owner: uibcdf/opencastp#6. Native numerical production source, declared radii,
preparation and comparison tolerances are unchanged. Complete equivalence
remains false; the five regional failures remain open. These controls run in
Python 3.14.7 with the editable packages in molsyssuite@uibcdf_3.14.

## What the rounding hypothesis does and does not establish

The candidate formats each native value to four decimal places, converts it
back to a binary float, then applies NumPy rounding to the field precision:
two decimals for atom areas, three for atom volumes and cavity totals. This
includes binary tie behavior; it is not a proof of the modern server's exact
decimal or floating-point export implementation. The inspected historical
CHECKING output used four decimals, motivating the atom hypothesis. Its full
reader/triangulation pipeline and modern server post-processing remain unknown.

The preceding 89-system replay introduces 742 regional mismatches while
explaining four of five original failures. This rejects applying that uniform
transformation to the current computed cavity values. It does **not** prove
every upstream input, primitive, domain or numerical convention correct, or
exclude a different upstream calculation combined with an export stage.
Likewise, a raw value passing the print-quantum interval does not guarantee
its formatted output will equal the server string.

Earlier unchanged historical metric primitives, high-precision evaluation and
complete printed orthosphere sets constrain the alternatives. They do not
recover the modern engine or establish its exact unrounded geometry. A useful
replacement must have an independently motivated convention and survive
passing controls as well as repair the five residuals. Per-case or per-atom
fitting, larger tolerances and selective rounding are not qualification.

## Joint intermediate-precision ablation

This fresh control measures every SA/MS cavity area and volume in all 384
regions of 1STP, 8RAT, 1MRG, 1PSN, 1YPI, 1FBP and 2FBP. It uses the trusted
geometry caches prepared in the preceding checkpoint; this is new integration,
not a fresh molecular parse or triangulation. Coordinates, expanded
castp3_protor radii, 1.4 angstrom probe, exact filtration/predicates, castp3
region domains and cusp=False are fixed. The raw tolerance is 0.00050001 with
rtol=0. All failures and the five original residual values are retained.

Each non-baseline variant converts the output vector of the named metric
primitive to float32 and back to float64 before downstream use. These are
exploratory ablations, **not** a recovered modern-server policy or the original
historical Vector type, which uses Vol_real=double in the inspected source.
No production method is patched: wrappers are local to diagnostic contexts.
The second verdict applies the same four-to-three-decimal export candidate
to each variant's newly calculated totals, testing the combined hypothesis.

| Materialized vectors | Raw matches / 1536 | New raw failures | Export matches / 1536 | New export failures against raw baseline |
| --- | ---: | ---: | ---: | ---: |
| Baseline float64 | 1531 | 0 | 1460 | 75 |
| center2 | 1509 | 25 | 1452 | 83 |
| center3 | 1478 | 53 | 1418 | 117 |
| triangle_dual | 1523 | 8 | 1456 | 79 |
| center2 and triangle_dual | 1508 | 26 | 1453 | 82 |
| All three | 1464 | 70 | 1419 | 116 |

center2 float32 repairs 1MRG region 22, 1YPI region 6 and 2FBP region 11,
but introduces 25 failures elsewhere. None of the variants improves the
panel or repairs all five residuals, either raw or with the export stage.
No variant is promoted. This demonstrates why a local improvement cannot
establish a missing convention. Whole-corpus region counts stay 14911/14916.
The separate 1OKM formatted-output boundary remains outside this seven-case
panel and open in the preceding replay; it is not a sixth raw failure.

## Independent mouth partition reference

The reusable developer auditor devtools/audit_castp_mouths.py builds connected
tetrahedral fans around each open edge, then connects mouth seeds lying on the
same fan. Shape edges block connectivity; inactive tetrahedra split fans.
This graph calculation calls neither the native Fnext rotation nor native
mouth union routine. It preserves face multiplicity and checks seed coverage
and the whole mouth-partition multiset without relying on mouth IDs or order.

The weighted mesh, alpha filtration, pocket domains and seed selection remain
shared with the numerical engine. This is an independent **partition** check
on those fixed inputs, not independent validation of all prior geometry,
domain selection, analytical integration or regional mouth ownership.

| Input | Compared mouths | Compared mouth triangles | One-mouth regions | Multi-mouth regions |
| --- | ---: | ---: | ---: | ---: |
| 1STP | 7 | 28 | 5 | 1 |
| 8RAT | 13 | 76 | 11 | 1 |
| 1MRG | 19 | 83 | 14 | 2 |
| 1PSN | 23 | 132 | 20 | 1 |
| 1YPI | 35 | 171 | 29 | 3 |
| 1FBP | 51 | 269 | 34 | 8 |
| 2FBP | 55 | 300 | 45 | 4 |
| Total | 203 | 1059 | 158 | 20 |

All partitions and seeds match. 1STP region 7 retains two mouths with two and
one triangles respectively, instead of collapsing its channel into one mouth.
The graph reference is tested first on synthetic fans, including interior
tetrahedra with no seed, blocked edges and interrupted fans.

## What can be validated against the archived server

The archive mouthInfo describes totals per cavity. Its mouth atom records
carry cavity IDs; neither exported file supplies an individual mouth ID,
individual triangle set or individual measurement for multi-mouth regions.

For each of the 158 one-mouth regions, the total is necessarily individual:
all 632 SA/MS area/perimeter values match at the original printed precision,
with exact rim atom sets and mouth-triangle counts. This directly compares
the native individual mouth calculation, not a replay of old aggregate rows.
It does not recover the server's individual triangle geometry.

For the 20 multi-mouth regions, the independent graph validates the native
partition on shared inputs. The server verifies only cavity totals, combined
rim atoms, mouth counts and total triangle counts; all pass here. Per-mouth
scalar/rim/triangle equivalence to CASTp3/CASTpFold remains **unqualified**.
The official [CASTpFold tutorial](https://cfold.bme.uic.edu/castpfold/infos/allabout/tutorial.html)
also illustrates separate mouths in 2IWV, but that illustration is not a
numerical per-mouth oracle for the jobs audited here.

## Evidence and replay

artifacts/joint_precision_mouth_controls_2026_10_03.json preserves actual
runtime and installed versions, source/archive/cache hashes, every failed
precision comparison, reference/native partitions and per-mouth measurements.
Collector snapshots are our own code. No historical C/header/binary, PDB,
server ZIP or coordinate pickle is redistributed. Pickles are trusted private
developer caches, not supported public input or a portable interchange format.
The original preparation/source identities remain in the preceding records.

Recreate the private caches with the preceding
[characterization collectors](metric_characterization_controls_2026_10_03.md).
Copy the pinned joint_precision_metric_runner.py.txt and
assemble_joint_precision_mouth.py.txt to their recorded /tmp paths, adapting
absolute checkout paths if needed. Run from the OpenCASTp checkout in the
configured Python 3.14 environment:

```bash
python /tmp/opencastp_joint_precision_controls.py
python -m devtools.audit_castp_mouths \
  --archive-dir /path/to/topomt/topomt/data/CASTpFold_server \
  --geometry-cache-dir /tmp \
  --cases 1stp 8rat 1mrg 1psn 1ypi 1fbp 2fbp \
  --output /tmp/opencastp_individual_mouth_controls.json
python /tmp/opencastp_assemble_joint_precision_mouth.py
```

For exact historical replay restore the pinned individual_mouth_auditor.py.txt
in a separate checkout's devtools/audit_castp_mouths.py; inspect future source
changes before substituting the current tool. The collector exits normally
with failed comparisons preserved. Completion is separate from equivalence;
the passing mouth panel does not close #6.

## Next qualification steps

Trace the remaining five regional boundaries and the separate atom/export
boundaries through input materialization, primitive selection, integration
terms and export conventions. Evaluate a motivated joint convention on passing
controls before expanding the full 89-system panel. Seek a genuine per-mouth
oracle for multi-mouth server jobs; retain unavailable evidence as unavailable.
Extend the bounded mouth/orthosphere/atom controls across the remaining corpus.
Only after these gates pass can a public server-equivalence recipe be certified.

## Local engineering verification

Python 3.14.7 passes 81 tests with pytest-receptor, including both enabled
1STP/8RAT molecular guards. The seven new auditor tests first failed for the
absent tool; three evidence guards first failed for the absent artifact. One
pre-existing TopoMT Pint-registry cache warning remains visible. Ruff lint and
format checks, generated devguide-index checks and warning-free Sphinx HTML
build pass. These are local checks; no new four-minor corpus qualification or
complete modern-server equivalence is claimed. TopoMT numerical source is
retained and unchanged.
