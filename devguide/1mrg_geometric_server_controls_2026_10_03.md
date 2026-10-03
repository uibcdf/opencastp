# 1MRG independent geometry and live-server controls — 2026-10-03

Owner: [OpenCASTp #6](https://github.com/uibcdf/opencastp/issues/6), still open.
The 89-input corpus remains at 3729/3729 exact regions, 14911/14916 regional
SA/MS scalars and 26103/26103 additional aggregate descriptors. These controls
do not fix a residual or add three distinct molecular benchmark systems.

## Question and independence boundary

For closed void 22 in 1MRG, the server prints SA volume 0.004 cubic angstroms;
OpenCASTp calculates 0.0034996378073546275. Its five original atom IDs are
1261, 1496, 1612, 1797 and 1834, and the native domain contains two tetrahedra.
This unusually small domain permits an independent measurement algorithm.

`devtools/section_volume_oracle.py` integrates planar sections of a supplied
tetrahedron minus an explicit union of spheres. Green's theorem integrates
exposed polygon segments and circular arcs, including interior holes; SciPy
QUADPACK integrates the section areas along the third axis. It imports no
CASTp metric primitive, visibility predicate or alpha predicate. Nine analytical
tests cover clipped disks, disk overlap, nesting, collective coverage, an
interior hole, transformations and tetrahedron/sphere volumes.

The tetrahedra, prepared coordinates and expanded `castp3_protor` radii remain
shared native inputs. This independently checks their SA measurement, not
molecular preparation, region detection or the exact server model. In particular,
it does not independently establish that server radii equal our radii.
All lengths passed to the developer tool use one explicitly declared common
unit; these controls use angstroms and report squared/cubed angstroms.
The tool is a developer reference, not a public molecular frontend.

Tiny uncovered domains require a conservative enclosure. Independently solve
for the four vertex spheres' weighted center c and common power q. For a point
x with tetrahedral barycentric weights lambda, the weighted sum of its vertex
powers is q minus the squared distance from c. Outside all vertex balls every
power is nonnegative, so the uncovered domain lies inside the sphere centered
at c with radius sqrt(q). Its padded bounding box narrows integration without
discarding the target domain. All molecular spheres that can intersect that
box remain candidates. This floating-point enclosure is not interval-certified;
axis changes, refinements and a wider padding test sensitivity.

## Independent volume and area results

| Section control | SA volume (cubic angstroms) | Estimated quadrature error |
| --- | ---: | ---: |
| z, 32 subdivisions | 0.003499637801168008 | 8.70e-11 |
| z, 64 subdivisions, tighter tolerance | 0.003499637802087797 | 3.86e-13 |
| x, 32 subdivisions | 0.003499637800870780 | 6.72e-11 |
| y, 32 subdivisions | 0.003499637800614780 | 7.64e-11 |
| z, wider enclosure padding | 0.003499637802571413 | 9.34e-11 |

Every result is within 7e-12 cubic angstroms of native integration and stays
below the 0.0035 three-decimal boundary. The agreement is strong evidence for
the chosen geometric measurement. It does not reproduce the server's 0.004.
The unchanged raw comparison tolerance is 0.00050001 cubic angstroms.

The negative derivative of uncovered volume under uniform sphere-radius growth,
holding the tetrahedra fixed, independently checks SA area. Central differences
at steps 0.001, 0.0005 and 0.00025 angstroms converge with approximately
second-order error. Richardson extrapolation gives 0.19945025506412162 square
angstroms, within 1.42e-10 of native 0.199450255206024. All three area estimates
pass the comparison with the server's printed 0.199. This checks SA area;
the molecular/rolling-probe surface is not the bare-sphere boundary.

QUADPACK returns an [estimated absolute error](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html),
not a certified bound. Convergence messages are retained, and none occurred in
these controls. Finite-difference truncation is separate from quadrature error.
No rigorous interval proof, independent geometry reconstruction or server bug
is claimed.

## Three fresh CASTpFold jobs

The retained TopoMT `CastpFoldClient` submitted the original ATOM records and
two integer-angstrom translations, with the same 1.4-angstrom probe. Inputs
keep ATOM/TER records and append END, excluding HETATM and unrelated headers.
The submitted PDB has 2395 ATOM rows, including 455 hydrogens. Each downloaded
contribution CSV has the same 1932 atom IDs as native protein/peptide preparation.
These are different counts at different preparation stages.

| Input | Translation (angstroms) | CASTpFold job | Native raw matches | Exploratory float32-coordinate matches |
| --- | --- | --- | ---: | ---: |
| Baseline | (0, 0, 0) | j_6ac12c1f0ccb4 | 115/116 | 110/116 |
| Near origin | (-44, -108, 5) | j_6ac12c1fa0333 | 115/116 | 114/116 |
| Shifted | (64, -64, 32) | j_6ac12c205bd51 | 115/116 | 111/116 |

All three jobs completed and returned validated ZIPs on 2026-10-03. Each has
29 regions with exact archived atom memberships, all 116 regional SA/MS values
and all seven additional cavity descriptors per region unchanged. Returned PDB
ATOM coordinates match the uploads at their exact millangstrom values. All
365 archived exported orthospheres match the translated exports, with unchanged
radii and coordinate differences below 3e-14 angstroms.

The server still prints 0.004 for void 22 in all three jobs. The fixed-domain
float64 native predictions preserve the same sole failed quantity. Simple
float32 coordinate materialization creates other discrepancies and does not
repair this one. This rejects that particular conditional precision explanation;
it does not exclude centered precision choices or coupled internal conventions.
These are live CASTpFold jobs only; no new CASTp3 job was submitted in this slice.

## Evidence, reproducibility and next gate

The [input-free evidence](artifacts/1mrg_section_rigid_controls_2026_10_03.json)
retains source commits, actual installed metadata, Python 3.14.7, NumPy 2.4.6,
SciPy 1.18.1, private input hashes, job identities, metrics, estimates and six
exact own-code collector snapshots. No PDB, server ZIP, original C source or
private geometry cache is redistributed. Editable installed version metadata
lags source commits and is retained as observed rather than relabelled.
Volume/area collectors ran against fcc823c; the final live comparison ran against
be30b78, whose intervening change only synchronized governance guidance.

To reproduce locally, restore the documented private archive/cache paths and
copy snapshot collectors back to their recorded `/tmp` filenames. Run the
volume collector before the area collector; the latter imports the former's
enclosure helper. Server submissions are separate explicit actions; stored
state prevents duplicate submission. The comparison collector reads completed
local downloads and performs no submissions. Snapshot filenames/hashes retain
the code actually executed rather than claiming a portable automated benchmark.

Evidence guards distinguish physical-model agreement from the still-failed
server comparison and verify collector hashes. No production numerical source,
public compatibility option or tolerance changed. Attribution integration and
new optional-engine contracts are not applicable to this developer-reference
slice; the existing server client was reused unchanged.

The next investigation should separate modern-server input materialization,
regional metric assembly and field-specific export. Full historical reader and
metric assembly execution remains uncompleted; historical code is an algorithmic
reference, not recovered modern server code. Neither the independent reference
nor translation invariance proves a server defect or a particular rounding rule.
The other four original residuals and individual multi-mouth server qualification
remain open; a public exact-equivalence recipe is still unavailable.


## Local validation

All 93 OpenCASTp tests pass with Pytest Receptor in
`molsyssuite@uibcdf_3.14` (Python 3.14.7), including the enabled local 1STP/8RAT
molecular guards and twelve added oracle/evidence tests. The existing TopoMT
Pint-registry-cache warning occurs once and does not change numerical results.
Ruff check and format check, developer-guide index verification and Sphinx HTML
with warnings treated as errors pass. TopoMT's changed benchmark inventory
passes its two reporting-protocol tests and index verification; its numerical
engine was not rerun or changed in this slice. Hosted CI is a separate gate;
ordinary push coverage does not certify the deferred full Python matrix.


## Later checkpoint

The [probe and original regional assembly controls](1mrg_probe_assembly_controls_2026_10_03.md)
execute the previously pending original C regional correction bodies on shared
native domains; the full historical reader/pipeline remains unexecuted. Five
new completed probe jobs support a conditional six-decimal hypothesis locally
and reject its uniform whole-corpus adoption. The original failures remain open.
