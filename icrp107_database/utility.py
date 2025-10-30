import pathlib
import numpy as np
import json

icrp107_source_path = pathlib.Path(__file__).parent.resolve()

icrp107_emissions = [
    "alpha",
    "beta-",
    "beta+",
    "gamma",
    "X",
    "neutron",
    "auger",
    "IE",
    "alpha recoil",
    "annihilation",
    "fission",
    "betaD",
    "b-spectra",  # beta spectras, both beta+ and beta-
]

DEFAULT_SPECTRUM_TYPE = "gamma"


def get_icrp107_spectrum(rad_name: str, spectrum_type=DEFAULT_SPECTRUM_TYPE):
    """
    Get the spectrum of a given radionuclide according to ICRP107 recommendations.

    Parameters
    ----------
    rad_name : str
        The name of the radionuclide in Gate format, e.g. "Tc99m", "Lu177"

    spectrum_type : str
        The type of spectrum to retrieve. Must be one of "gamma", "beta-", "beta+", "alpha", "X",
        "neutron", "auger", "IE", "alpha recoil", "annihilation", "fission", "betaD", "b-spectra"

    Returns
    -------
    dict
        A dictionary with two keys: "energies", "weights", "half_life" and "time unit". The first contains the energy of
        each emission, the second contains the weight of each emission (summing to 1).

    Raises
    ------
    fatal
        If the radionuclide or spectrum type is not valid.
    """
    rad = rad_name
    path = icrp107_source_path / "icrp107" / f"{rad}.json"

    if not path.exists():
        raise Exception(f"get_icrp107_spectrum: {rad} is not contained in the icrp 107 database")

    if spectrum_type not in icrp107_emissions:  # Convert particle name to spectrum type
        spectrum_type = (
            spectrum_type.lower().replace("e-", "beta-").replace("e+", "beta+")
        )

    if spectrum_type not in icrp107_emissions:
        raise Exception(f"get_icrp107_spectrum: {spectrum_type} is not valid")

    with open(path, "rb") as f:
        data = json.loads(json.load(f))

        data_extracted = {
            "energies": np.array(
                [v[0] for v in data["emissions"][spectrum_type]]  # in MeV
            ),
            "weights": np.array(
                [v[1] for v in data["emissions"][spectrum_type]]
            ),
            "half_life": data["half_life"],
            "time_unit": data["time_unit"]
        }
        return data_extracted
