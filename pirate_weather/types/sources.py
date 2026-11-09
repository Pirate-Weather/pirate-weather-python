"""Model sources used by the API."""

from enum import StrEnum


class Sources(StrEnum):
    """Model sources that can be passed to ``exclude`` to force a fallback source."""

    HRRR = "hrrr"
    NBM = "nbm"
    GEFS = "gefs"
    GFS = "gfs"
    RTMA_RU = "rtma_ru"
    ECMWF_IFS = "ecmwf_ifs"
    DWD_MOSMIX = "dwd_mosmix"
    ECMWF_AIFS = "ecmwf_aifs"
    AIGEFS = "aigefs"
    AIGFS = "aigfs"
    RAQDPS = "raqdps"
    SILAM = "silam"
    HRDPS = "hrdps"
    GDPS = "gdps"
    REPS = "reps"
    GEPS = "geps"
    CMC = "cmc"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
