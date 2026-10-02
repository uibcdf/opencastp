# Source provenance and release qualification

The initial Python reference implementation was extracted from uibcdf/topomt,
whose repository declares MIT licensing. Retain the inherited copyright notice
and the source hashes in devguide/extraction_manifest.json. This records the
declared source license; it does not certify the provenance of every historical
algorithmic adaptation.

The reconstruction was developed using CAST/CASTp literature and consultation
of historical Alpha Shape/MKALF/VOLBL implementations. The historical Alpha
Shape package has specific academic/internal-business, redistribution,
derivative-notification and commercial-use terms. Its conditions must not be
represented as MIT merely because the consumer repository declares MIT.

No historical C sources, PDB2ALF parameter file, server archives or molecular
fixtures are included in this initial extraction. The Python numerical source
still needs a file-by-file adaptation/provenance review before public package
release, owned by uibcdf/opencastp#2. No clean-room claim is made.

Scientific references and the pyCAST/pyCASTa predecessor must be credited in
future scientific comparisons. Adapting a published method is distinct from
claiming a new original cavity-detection algorithm.
