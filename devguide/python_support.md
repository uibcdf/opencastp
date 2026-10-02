# Python support

OpenCASTp supports Python 3.11, 3.12, 3.13 and 3.14. Metadata and both Conda
environments declare >=3.11,<3.15. Routine development remains Python 3.13.
The full Linux matrix runs on PRs, weekly and manual events; direct pushes run
unfiltered Python 3.13 tests. Every numerical lane checks the actual interpreter
and a non-editable installed package before its unfiltered test suite.

The initial four-minor qualification is run 37058887654 at source
762db29693f030ac61baa423de0371993ad6a454. Runtime versions were 3.11.16,
3.12.14, 3.13.15 and 3.14.7; each passed its installed numerical smoke and
26 tests. Native step/runtime evidence is in
artifacts/hosted_python_matrix_2026_10_02.json. This is interpreter/runtime
evidence on Linux, not public channel or unobserved OS qualification.

The component-specific transition is tracked by uibcdf/opencastp#5 and central
admission #70. The published policy registry limitation remains central #73;
the explicitly pinned bootstrap exception does not imply policy-release adoption.
