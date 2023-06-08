from enum import Enum


class Units(Enum):
    """The units for a given column/endpoint

    Taken from stardrop/libs/models/ContModelUnits.h
    """
    OTHER = 0
    MICROMOLAR = 1
    LOGMICROMOLAR = 2
    NANOMOLAR = 3
    LOGNANOMOLAR = 4
    PKI = 5
    RATIO = 6
    LOGRATIO = 7
    PERCENT = 8
    SECOND = 9
    MINUTE = 10
    HOUR = 11
    DAY = 12
    RADIAN = 13
    DEGREE = 14
    PARTS_PER_MILLION = 15
    PARTS_PER_BILLION = 16
    PARTS_PER_TRILLION = 17
    MILLIMOLAR = 18
    LOGMILLIMOLAR = 19
    PICOMOLAR = 20
    LOGPICOMOLAR = 21
    MILLIGRAM_PER_MILLILITRE = 22
    MICROGRAM_PER_MILLILITRE = 23
    NANOGRAM_PER_MILLILITRE = 24
    MICROGRAM_HOURS_PER_MILLILITRE = 25
    NANOGRAM_HOURS_PER_MILLILITRE = 26
    PICOMOLAR_PER_MINUTE_PER_MILLIGRAM = 27
    MILLILITRE_PER_MINUTE_PER_KILOGRAM = 28
    MICROLITRE_PER_MINUTE_PER_MILLIGRAM = 29
    METRES_PER_SECOND = 30
    CENTIMETRES_PER_SECOND = 31
    MILLIGRAM_PER_KILOGRAM = 32
    MILLIGRAM_PER_KILOGRAM_PER_MILLILITRE = 33
    MILLIVOLTS = 34
    MILLILITRE_PER_KILOGRAM = 35
    LITRE_PER_KILOGRAM = 36
    KILOGRAM_PER_HECTARE = 37
    KILOGRAM_PER_ACRE = 38
    KILOGRAM_PER_SQUARE_METRE = 39
    MOLAR = 40
    LOGMOLAR = 41
    CELSIUS = 42
    KELVIN = 43
    LOGMILLIGRAM_PER_MILLILITRE = 44
    LOGMICROGRAM_PER_MILLILITRE = 45
    LOGNANOGRAM_PER_MILLILITRE = 46
    MICROGRAM_MINUTES_PER_MILLILITRE = 47
    NANOGRAM_MINUTES_PER_MILLILITRE = 48


def parse_unit(unit: str) -> Units:
    """Parse unit string

    :param unit: The unit string
    :return: The unit enum
    """
    unit_lookup = {
        "%": Units.PERCENT,
        "percent": Units.PERCENT,
        "Percent": Units.PERCENT,
        "µM": Units.MICROMOLAR,
        "uM": Units.MICROMOLAR,
        "log(µM)": Units.LOGMICROMOLAR,
        "log(uM)": Units.LOGMICROMOLAR,
        "nM": Units.NANOMOLAR,
        "log(nM)": Units.LOGNANOMOLAR,
        "M": Units.MOLAR,
        "log(M)": Units.LOGMOLAR,
        "pKi/pIC50": Units.PKI,
        "pKi": Units.PKI,
        "pIC50": Units.PKI,
        "ratio": Units.RATIO,
        "Ratio": Units.RATIO,
        "log(ratio)": Units.LOGRATIO,
        "log(Ratio)": Units.LOGRATIO,
        "seconds": Units.SECOND,
        "minutes": Units.MINUTE,
        "hours": Units.HOUR,
        "days": Units.DAY,
        "s": Units.SECOND,
        "min": Units.MINUTE,
        "h": Units.HOUR,
        "d": Units.DAY,
        "rad": Units.RADIAN,
        "radian": Units.RADIAN,
        "degrees": Units.DEGREE,
        "ppm": Units.PARTS_PER_MILLION,
        "ppb": Units.PARTS_PER_BILLION,
        "ppt": Units.PARTS_PER_TRILLION,
        "mM": Units.MILLIMOLAR,
        "log(mM)": Units.LOGMILLIMOLAR,
        "pM": Units.PICOMOLAR,
        "log(pM)": Units.LOGPICOMOLAR,
        "mg/mL": Units.MILLIGRAM_PER_MILLILITRE,
        "ug/mL": Units.MICROGRAM_PER_MILLILITRE,
        "ng/mL": Units.NANOGRAM_PER_MILLILITRE,
        "ug hr/mL": Units.MICROGRAM_HOURS_PER_MILLILITRE,
        "ng hr/mL": Units.NANOGRAM_HOURS_PER_MILLILITRE,
        "ug min/mL": Units.MICROGRAM_MINUTES_PER_MILLILITRE,
        "ng min/mL": Units.NANOGRAM_MINUTES_PER_MILLILITRE,
        "pM/min/mg": Units.PICOMOLAR_PER_MINUTE_PER_MILLIGRAM,
        "pmol/min/mg": Units.PICOMOLAR_PER_MINUTE_PER_MILLIGRAM,
        "mL/min/kg": Units.MILLILITRE_PER_MINUTE_PER_KILOGRAM,
        "uL/min/mg": Units.MICROLITRE_PER_MINUTE_PER_MILLIGRAM,
        "m/s": Units.METRES_PER_SECOND,
        "cm/s": Units.CENTIMETRES_PER_SECOND,
        "mg/kg": Units.MILLIGRAM_PER_KILOGRAM,
        "mg/kg/mL": Units.MILLIGRAM_PER_KILOGRAM_PER_MILLILITRE,
        "mV": Units.MILLIVOLTS,
        "mL/kg": Units.MILLILITRE_PER_KILOGRAM,
        "L/kg": Units.LITRE_PER_KILOGRAM,
        "kg/ha": Units.KILOGRAM_PER_HECTARE,
        "kg/ac": Units.KILOGRAM_PER_ACRE,
        "kg/m^2": Units.KILOGRAM_PER_SQUARE_METRE,
        "K": Units.KELVIN,
        "C": Units.CELSIUS,
        "log(ng/mL)": Units.LOGNANOGRAM_PER_MILLILITRE,
        "log(ug/mL)": Units.LOGMICROGRAM_PER_MILLILITRE,
        "log(mg/mL)": Units.LOGMILLIGRAM_PER_MILLILITRE,
        "log(g/ha)": Units.LOGRATIO,
        "ml": Units.OTHER,
    }

    return unit_lookup.get(unit, Units.OTHER)

