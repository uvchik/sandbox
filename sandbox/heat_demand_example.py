# -*- coding: utf-8 -*-
"""
Creating heat demand profiles using the bdew method.

Installation requirements
-------------------------
This example requires at least version v0.1.4 of the oemof demandlib. Install
by:
    pip install 'demandlib>=0.1.4,<0.2'
Optional:
    pip install matplotlib

"""

import pandas as pd
import demandlib.bdew as bdew
import os
from workalendar.europe import Germany

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# read example temperature series

datapath = os.path.join(os.path.dirname(__file__),
                        'TRY2015_541957091051_Jahr.dat')
try_weather = pd.read_csv(datapath, skiprows=34, sep='\t', header=None,
                          decimal=',')
temperature = try_weather[5]

cal = Germany()
holidays = dict(cal.holidays(2010))

# Create DataFrame for 2010
demand = pd.DataFrame(
    index=pd.date_range(pd.datetime(2010, 1, 1, 0),
                        periods=8760, freq='H'))

# Single family house (efh: Einfamilienhaus)
demand['efh'] = bdew.HeatBuilding(
    demand.index, holidays=holidays, temperature=temperature,
    shlp_type='EFH',
    building_class=1, wind_class=1, annual_heat_demand=25000,
    name='EFH').get_bdew_profile()

# Multi family house (mfh: Mehrfamilienhaus)
demand['mfh'] = bdew.HeatBuilding(
    demand.index, holidays=holidays, temperature=temperature,
    shlp_type='MFH',
    building_class=2, wind_class=0, annual_heat_demand=80000,
    name='MFH').get_bdew_profile()

# Industry, trade, service (ghd: Gewerbe, Handel, Dienstleistung)
# Valid values for slp_types are:
# GMK, GPD, GHA, GBD, GKO, GBH, GGA, GBA, GWA, GGB, GMF, GHD
# https://demandlib.readthedocs.io/en/latest/description.html#heat-profiles
demand['ghd'] = bdew.HeatBuilding(
    demand.index, holidays=holidays, temperature=temperature,
    shlp_type='ghd', wind_class=0, annual_heat_demand=140000,
    name='ghd').get_bdew_profile()

if plt is not None:
    # Plot demand of building
    ax = demand.plot()
    ax.set_xlabel("Date")
    ax.set_ylabel("Heat demand in kW")
    plt.show()
else:
    print('Annual consumption: \n{}'.format(demand.sum()))
