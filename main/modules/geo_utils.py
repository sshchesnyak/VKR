import numpy as np
import main.modules.consts as c


def param_calc(angle):
    rho = (c.A * (1 - c.ECC)) / ((1 - c.ECC * (np.sin(angle) ** 2)) ** (3.0 / 2.0))
    nu = c.A / np.sqrt(1 - c.ECC * (np.sin(angle) ** 2))
    psi = nu / rho
    t = np.tan(angle)
    return rho, nu, psi, t


# function that allows the conversion of a transverse mercator to geographic coordinates - working!
def tm_to_gc(e, n):
    nm = n - c.N_CONST
    mn = c.M_PHI_CONST + nm / c.K_CONST
    sigma = mn/c.G
    phi_m = sigma + (3 * (c.N / 2) - 27 * (c.N ** 3 / 32)) * np.sin(2 * sigma) + (21 * (c.N ** 2 / 16) - 55 * (c.N ** 4 / 32)) * np.sin(4 * sigma) + 151 * (c.N ** 3 / 96) * np.sin(6 * sigma) + 1097 * (c.N ** 4 / 512) * np.sin(8 * sigma)
    rho_m, nu_m, psi_m, tm = param_calc(phi_m)
    em = e - c.E_CONST
    xm = em/(c.K_CONST * nu_m)
    # computing latitude
    coefficient = (tm*em)/(c.K_CONST * rho_m)
    c_phi_1 = coefficient*xm/2
    c_phi_2 = coefficient*(xm**3/24)*(-4*(psi_m**2)+9*psi_m*(1-tm**2)+12*(tm**2))
    c_phi_3 = coefficient*(xm**5/720)*(8*(psi_m**4)*(11-24*(tm**2))-12*(psi_m**3)*(21-71*(tm**2))+15*(psi_m**2)*(15-98*(tm**2)+15*(tm**4))+180*psi_m*(5*(tm**2)-3*(tm**4))+360*(tm**4))
    c_phi_4 = coefficient*(xm**7/40320)*(1385+3633*(tm**2)+4095*(tm**4)+1575*(tm**6))
    latitude = np.degrees(phi_m-c_phi_1+c_phi_2-c_phi_3+c_phi_4)
    # computing longitude
    sec_psi_m = 1/np.cos(phi_m)
    c_lambda_1 = sec_psi_m*xm
    c_lambda_2 = sec_psi_m*(xm**3/6)*(psi_m+2*(tm**2))
    c_lambda_3 = sec_psi_m*(xm**5/120)*(-4*(psi_m**3)*(1-6*(tm**2))+(psi_m**2)*(9-68*(tm**2))+72*psi_m*(tm**2)+24*(tm**4))
    c_lambda_4 = sec_psi_m*(xm**7/5040)*(61+662*(tm**2)+1320*(tm**4)+720*(tm**6))
    longitude = np.degrees(c.LAMBDA_CONST+c_lambda_1-c_lambda_2+c_lambda_3-c_lambda_4)
    return latitude, longitude


def gc_to_tm(lat, lon):
    latitude = np.radians(lat)
    longitude = np.radians(lon)
    rho, nu, psi, t = param_calc(latitude)
    omega = longitude-c.LAMBDA_CONST
    # Calculating m
    a_0 = 1-(c.ECC/4)-3*(c.ECC**2/64)-5*(c.ECC**3/256)
    a_2 = 3/8*(c.ECC+(c.ECC**2/4)+15*(c.ECC**3/128))
    a_4 = 15/256*(c.ECC**2+3*(c.ECC**3/4))
    a_6 = 35*(c.ECC**3/3072)
    m = c.A*(a_0*latitude-a_2*np.sin(2*latitude)+a_4*np.sin(4*latitude)-a_6*np.sin(6*latitude))
    # Northing calculation
    coefficient = nu*np.sin(latitude)
    n_1 = (omega**2/2)*coefficient*np.cos(latitude)
    n_2 = (omega**4/24)*coefficient*(np.cos(latitude)**3)*(4*(psi**2)+psi-t**2)
    n_3 = (omega**6/720)*coefficient*(np.cos(latitude)**5)*(8*(psi**4)*(11-24*(t**2))-28*(psi**3)*(1-6*(t**2))+(psi**2)*(1-32*(t**2))-psi*(2*(t**2))+(t**4))
    n_4 = (omega**8/40320)*coefficient*(np.cos(latitude)**7)*(1385-3111*(t**2)+543*(t**4)-(t**6))
    n = np.round(c.N_CONST+c.K_CONST*(m-c.M_PHI_CONST+n_1+n_2+n_3+n_4), 1)
    # Easting calculation
    e_1 = (omega**2/6)*(np.cos(latitude)**2)*(psi-t**2)
    e_2 = (omega**4/120)*(np.cos(latitude)**4)*(4*(psi**3)*(1-6*(t**2))+(psi**2)*(1+8*(t**2))-2*psi*(t**2)+(t**4))
    e_3 = (omega**6/5040)*(np.cos(latitude)**6)*(61-479*(t**2)+179*(t**4)-t**6)
    e = np.round(c.E_CONST+c.K_CONST*nu*omega*np.cos(latitude)*(1+e_1+e_2+e_3), 1)
    return e, n


def get_corner_xy(lat, lon):
    new_lat = lat + 20*c.LAT_1M
    new_lon = lon + 20 / (c.LON_1M * np.cos(np.deg2rad(new_lat)))
    x, y = gc_to_tm(new_lat, new_lon)
    return x, y


def get_corner_coords(lat, lon):
    new_lat = lat + 20*c.LAT_1M
    new_lon = lon + 20 / (c.LON_1M * np.cos(np.deg2rad(new_lat)))
    return new_lat, new_lon
