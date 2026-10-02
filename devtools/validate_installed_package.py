"""Verify a non-editable installed package without source-checkout shadowing."""

import sys
from importlib import metadata
from pathlib import Path

import numpy as np

import opencastp


def main() -> None:
    """Check package origin and execute the independent numerical engine."""
    print(f"Runtime Python {sys.version.split()[0]}")
    origin = Path(opencastp.__file__).resolve()
    if not origin.is_relative_to(Path(sys.prefix).resolve()):
        raise RuntimeError(f"Package is not installed in this environment: {origin}")
    distribution = metadata.distribution("opencastp")
    direct_url = distribution.read_text("direct_url.json") or ""
    if '"editable": true' in direct_url:
        raise RuntimeError("Installed-package evidence cannot use an editable install")
    points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    result = opencastp.analyze(points, np.full(4, 0.25), length_unit="angstrom")
    assert result.features[0]["feature_type"] == "void"
    assert "topomt" not in sys.modules
    assert "molsysmt" not in sys.modules
    print(
        f"Installed OpenCASTp {distribution.version}: independent closed-void smoke passed"
    )


if __name__ == "__main__":
    main()
