"""Domain failures exposed by the independent CASTp engine."""


class CastpInputError(ValueError):
    """An input does not satisfy the numerical or physical contract."""


class CastpGeometryError(ValueError):
    """An input cannot produce the required weighted geometry."""
