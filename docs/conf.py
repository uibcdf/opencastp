"""Documentation configuration for the independent reference engine."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "OpenCASTp"
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]
html_theme = "alabaster"
exclude_patterns = ["_build"]
