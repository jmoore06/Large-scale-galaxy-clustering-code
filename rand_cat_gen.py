# -*- coding: utf-8 -*-
'''Programme to clone galaxies from a catalogue and generate a random,
unclustered catalogue to examine the effects of clustering on galaxy properties.
This is the full interface version, with a text prompt to generate a catalogue
when run as the main program. Note that this is currently set up only for flat 
cosmologies (FlatLambdaCDM).
'''

import os
import numpy as np
import reflwin
from astropy.cosmology import FlatLambdaCDM
from matplotlib import pyplot


#m_min    = 10.0          # Minimum apparent magnitude usable in the survey
#m_max    = 19.8          # Maximum apparent magnitude detectable in the survey
#n_clone  = 20            # The ratio of cloned-to-surveyed galaxies, typ. 400
#Sigma    = 0.389017e11

def boolean_raw_input(text):
    variable = -1
    while variable != True and variable != False:
        variable = raw_input(text)
        if variable.lower() in {"y", "ye", "yes", "true", "sure", "oui", "ja"}:
            variable = True
        elif variable.lower() in {"n", "no", "false", "non", "nein"}:
            variable = False
        elif variable != True and variable != False:
            print "Please answer with y/yes or n/no."
    return variable

if __name__=="__main__":
    H0     = float(raw_input("Hubble constant in kms^-1Mpc^-1: "))
    Om0    = float(raw_input("Matter density: "))
    print "Please wait while the cosmology is generated."
    print "Cosmology finished."
    cosmo  = FlatLambdaCDM(H0, Om0)
    
    m_min    = float(raw_input("Minimum apparent magnitude: "))
    m_max    = float(raw_input("Maximum apparent magnitude: "))
    sol_ang  = float(raw_input("Solid angle covered by the survey in " + \
                               "steradians: "))
    
    k_text = raw_input("Type in Python function for k-correction in terms " + \
                       "of redshift z: ")
    e_text = raw_input("Type in Python function for e-correction in terms " + \
                       "of redshift z: ")                   
    k_corr = lambda z: eval(k_text)
    e_corr = lambda z: eval(e_text)

    abs_mag = lambda z, m, univ: m - univ.distmod(z).value - k_corr(z) - \
                                  e_corr(z)
    obs_mag = lambda z, M, univ: M + univ.distmod(z).value + k_corr(z) + \
                                  e_corr(z)
    
    print "The generator accepts a text file with columns delimited " + \
               "by spaces. The columns must be ordered right ascension " + \
               "(in degrees), declination (in degrees), redshift, and " + \
               "apparent magnitudes, followed by any arbitrary properties. " + \
               "Alternatively, the properties can be input as separate " + \
               "text files in column format."

    separate = boolean_raw_input("Do you wish to input separate " + \
                                 "text files? (y/n): ")
                                 
    if separate == True:
        same_loc = boolean_raw_input("Is the Python file in the same " + \
                                     "location as the data files? (y/n): ")
        
        if same_loc == True:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), \
                           os.path.dirname(__file__)))
            
            angpos = boolean_raw_input("Are there angular positions (right " + \
            "ascensions or declinations) to input? (y/n): ")
            if angpos == True:
                ra_loc = raw_input("Type the name of the right ascension " + \
                                   "file: ")
                ra = np.loadtxt(os.path.join(__location__,ra_loc), \
                                delimiter=' ')
            
                dec_loc = raw_input("Type the name of the declination file: ")
                dec = np.loadtxt(os.path.join(__location__,dec_loc), \
                                 delimiter=' ')
            elif angpos == False:
                ra  = None
                dec = None
            
            z_loc = raw_input("Type the name of the redshift file: ")
            z = np.loadtxt(os.path.join(__location__,z_loc), delimiter=' ')
            
            absolute = boolean_raw_input("Are the input magnitudes " + \
                                         "absolute? (y/n): ")
            if absolute == True:
                mag_loc = raw_input("Type the name of the absolute " + \
                                    "magnitude file: ")
                mag = np.loadtxt(os.path.join(__location__,mag_loc), \
                                 delimiter=' ')
            elif absolute == False:
                mag_loc = raw_input("Type the name of the apparent " + \
                                    "magnitude file: ")
                mag = np.loadtxt(os.path.join(__location__,mag_loc), \
                                 delimiter=' ')
                for i in range(len(mag)):
                    mag[i] = abs_mag(z[i],mag[i],cosmo)
            
            att_loc = raw_input("Type the name of the additional " + \
                                "properties file: ")
            att = np.loadtxt(os.path.join(__location__,att_loc), delimiter=' ')
        
        elif same_loc == False:
            angpos = boolean_raw_input("Are there angular positions (right " + \
            "ascensions or declinations) to input? (y/n): ")
            if angpos == True:
                ra_loc = raw_input("Type the full file path of the right " + \
                               "ascension file: ")
                ra = np.loadtxt(ra_loc, delimiter=' ')
            
                dec_loc = raw_input("Type the full file path of the " + \
                                "declination file: ")
                dec = np.loadtxt(dec_loc, delimiter=' ')
            elif angpos == False:
                ra  = None
                dec = None
            
            z_loc = raw_input("Type the full file path of the redshift file: ")
            z = np.loadtxt(z_loc, delimiter=' ')
            
            absolute = boolean_raw_input("Are the input magnitudes " + \
                                         "absolute? (y/n): ")
            if absolute == True:
                mag_loc = raw_input("Type the full file path of the " + \
                                    "absolute magnitude file: ")
                mag = np.loadtxt(mag_loc, delimiter=' ')
            elif absolute == False:
                mag_loc = raw_input("Type the full file path of the " + \
                                    "apparent magnitude file: ")
                mag = np.loadtxt(mag_loc, delimiter=' ')
                for i in range(len(mag)):
                    mag[i] = abs_mag(z[i],mag[i],cosmo)
            
            att_loc = raw_input("Type the full file path of the additional " + \
                                "properties file: ")
            att = np.loadtxt(att_loc, delimiter=' ')
            
    elif separate == False:
        same_loc = boolean_raw_input("Is the Python file in the same " + \
                                     "location as the data file? (y/n): ")
        
        if same_loc == True:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), \
                           os.path.dirname(__file__)))
                           
            file_loc = raw_input("Type the name of the data file: ")
            data = np.loadtxt(os.path.join(__location__,file_loc), \
                              delimiter=' ')
                              
            ra  = data[:,0]
            dec = data[:,1]
            z   = data[:,2]
            mag = data[:,3]
            att = data[:,4:int(data.shape[1])]
            
            for i in range(len(mag)):
                mag[i] = abs_mag(z[i],mag[i],cosmo)
        
        elif same_loc == False:
            file_loc = raw_input("Type the full file path of the data file: ")
            data = np.loadtxt(file_loc, delimiter=' ')
            
            ra  = data[:,0]
            dec = data[:,1]
            z   = data[:,2]
            mag = data[:,3]
            att = data[:,4:int(data.shape[1])]  
            
            for i in range(len(mag)):
                mag[i] = abs_mag(z[i],mag[i],cosmo)  
    
       
    n_clone  = int(raw_input("The average number of galaxy clones (20 is " + \
                             "recommended): "))
    
    windowed = boolean_raw_input("Apply the Farrow window to the " + \
                                 "redistribution? (y/n): ")
    if windowed == True:
        Sigma    = float(raw_input("The standard deviation of the window " + \
                                   "in Mpc^3: "))
    
    zlim = boolean_raw_input("Is there a redshift limit to the " + \
                             "survey? (y/n): ")
    if zlim == True:
        zlim = float(raw_input("Input the redshift limit: "))
    elif zlim == False:
        zlim = None
        
    ralim = boolean_raw_input("Are there RA limits to the survey? (y/n): ")
    if ralim == True:
        ralim_lo = float(raw_input("Input the lower RA limit: "))
        ralim_hi = float(raw_input("Input the upper RA limit: "))
        ralim = (ralim_lo,ralim_hi)
    elif ralim == False:
        ralim = None
    
    declim = boolean_raw_input("Are there declination limits to the " + \
                               "survey? (y/n): ")
    if declim == True:
        declim_lo = float(raw_input("Input the lower declination limit: "))
        declim_hi = float(raw_input("Input the upper declination limit: "))
        declim = (declim_lo,declim_hi)
    elif declim == False:
        declim = None
        
    N  = int(raw_input("Input the number of iterations to perform (20 is " + \
                       "sufficient): "))
    dz = float(raw_input("Input the separation of the redshift bins the " + \
                         " overdenstity will be measured over (0.025 is " + \
                         "recommended): "))
    
    take_record = boolean_raw_input("Do you wish to obtain a record of the " + \
                                    "catalogue at each iteration? Note that" + \
                                    " this can be memory intensive. (y/n): ")

Phistar_z0 = 9.4e-3 * cosmo.h ** 3 # The normalization density for the LF at z0
Alpha      = -1.26                 # The power law coefficient for the LF
Magstar_z0 = -20.7                 # The characteristic luminosity for the LF at z0
Phistar    = lambda z: Phistar_z0 * 10 ** (0.4*1.8*z)
Magstar    = lambda z: Magstar_z0 + 0.7 * (z-0.1)

def truncate_by_mag(app_m, z, abs_m, min_app_mag, vmaxs=None, \
                    vmaxcut=(False,-23.,-22.5)):
    '''
    Truncates a catalogue's data according to either a minimum apparent 
    magnitude, or a specified magnitude window.
    
    An input catalogue of apparent magnitudes app_m, absolute magnitudes abs_m, 
    and redshifts z have galaxies removed according to either an apparent
    minimum magnitude min_app_mag, or so that only galaxies within an absolute 
    magnitude window vmaxcut remain. Optionally, the analytical V_max values 
    vmaxs can be trucated as well. If no such values exist, use None.
    

    Parameters
    ----------
    app_m : array_like
       An array of apparent magnitude values.
    z : array_like
       An array of redshift values, where z[x] and app_m[x] refer to the same 
       galaxy.
    abs_m : array_like
       An array of absolute magnitudes, where abs_m[x] and app_m[x] refer to 
       the same galaxy.
    min_app_mag : float
       Minimum apparent magnitude of the catalogue.
    vmaxs : array_like or NoneType, optional
       An array of analytic V_max values, where vmaxs[x] and app_m[x] refer to 
       the same galaxy. If no V_max values are available, use None.
    vmaxcut : array_like (Boolean, float, float), optional
       Apparent magnitude window the function will cut the catalogue to, 
       removing all galaxies that lie outside of it, with three packed 
       variables: a Boolean that is True if the window is to be cut, the lower
       limit of apparent magnitude, and the upper limit of apparent magnitude.

    Returns
    -------
    app_m_cut : array_like
       An array of the apparent magnitudes after the cut.
    z_cut : array_like
       An array of the redshifts after the cut.
    abs_m_cut : array_like
       An array of the apparent magnitudes after the cut.
    vmax_cut : array_like
       An array of the V_max values after the cut. Only produced if vmaxs is not
       None.

    '''

    mag_run    = np.copy(app_m)
    z_run      = np.copy(z)
    absmag_run = np.copy(abs_m) 
    order      = []
    
    if vmaxcut[0] == True:
        if vmaxs is None:
            for i in range(len(abs_m)):
                if absmag_run[i] < vmaxcut[1] or absmag_run[i] > vmaxcut[2]:
                    order.append(i)
            app_m_cut = np.delete(mag_run, order)
            z_cut     = np.delete(z_run, order)
            abs_m_cut = np.delete(absmag_run, order)
            return app_m_cut, z_cut, abs_m_cut
        
        else:
            vmax_run   = np.copy(vmaxs)
            for i in range(len(abs_m)):
                if absmag_run[i] < vmaxcut[1] or absmag_run[i] > vmaxcut[2]:
                    order.append(i)
            app_m_cut = np.delete(mag_run, order)
            z_cut     = np.delete(z_run, order)
            abs_m_cut = np.delete(absmag_run, order)
            vmax_cut  = np.delete(vmax_run, order)
            return app_m_cut, z_cut, abs_m_cut, vmax_cut
        
    elif vmaxs is None:
        
        for i in range(len(abs_m)):
            if mag_run[i] < min_app_mag:
                order.append(i)
        app_m_cut = np.delete(mag_run, order)
        z_cut     = np.delete(z_run, order)
        abs_m_cut = np.delete(absmag_run, order)
        return app_m_cut, z_cut, abs_m_cut
        
    else:
        vmax_run   = np.copy(vmaxs)
        for i in range(len(abs_m)):
            if mag_run[i] < min_app_mag:
                order.append(i)
        app_m_cut = np.delete(mag_run, order)
        z_cut     = np.delete(z_run, order)
        abs_m_cut = np.delete(absmag_run, order)
        vmax_cut  = np.delete(vmax_run, order)
        return app_m_cut, z_cut, abs_m_cut, vmax_cut

#-------------------------------------------------------------------------------

def schechter(magnitude, phiStar=Phistar_z0, alpha=Alpha, mStar=Magstar_z0, \
              z=False):
    '''
    Returns the value of the Schechter luminosity function specified by the 
    input properties at a given absolute magnitude, in units of cubic 
    megaparsecs. An evolving definition of the function can be given by 
    entering a redshift z and lambda functions for phiStar and mStar.
    

    Parameters
    ----------
    magnitude : float
       An absolute magnitude value the Schechter function is evaluated at.
    phiStar : float or lambda_like, optional
       The normalisation number density for the Schechter function, in units of
       lunminous bodies per cubic megaparsec. Can be an evolving function if a 
       redshift is specified.
    alpha : float, optional
       The unitless coefficient for the power law term for the Schechter 
       function.
    mStar : float or lambda_like, optional
       The characteristic luminosity for the cutoff point of the Schechter 
       function, in units of magnitudes. Can be an evolving function if a 
       redshift is specified.
    z : float or bool, optional
       The redshift at which the evolving Schechter function is measured. If the
       function is constant, use False.

    Returns
    -------
    float
       The value of the Schechter function at the input magnitude.

    '''
    if type(phiStar)!=float and type(mStar)!=float and type(z)==float:
        w = 0.4 * (mStar(z) - magnitude)
        return 0.4 * np.log(10) * phiStar(z) * 10.0**(w * (alpha + 1.0)) \
                * np.exp(-10.0**w)
    else:
        w = 0.4 * (mStar - magnitude)
        return 0.4 * np.log(10) * phiStar * 10.0**(w * (alpha + 1.0)) \
                * np.exp(-10.0**w)
    
    
def redshift_tabulator(univ, solid_Angle=4*np.pi, min_z=0.0, max_z=1.5, N=1e5):
    '''
    Tables redshifts and associated values in a reference table for finding 
    V_max and V_max_dc.
    
    The function tables N redshift bins between min_z and max_z in a Numpy 
    array. Using an AstroPy cosmology univ, values of various parameters are 
    calculated at each redshift bin, giving the following columns:
        
    1: Redshift bin (z)
    2: Distance modulus (q), which is equivalent to both 5 * (lg(D_L) - 1) + k(z) 
       + e(z), and m - M
    3: The comoving volume (V_c) over the solid angle (solid_Angle) of the 
       surface at z
    4: The overdensity (Delta) of an associated catalogue at z. At generation, 
       this is set to Delta(z) = 1.0.
    5: The change in volume over the redshift bin (DeltaV_c)
    6: The sum of the multiple of overdensity and change in volume (Sum_dc), 
       from min_z to the current z bin.

    Parameters
    ----------
    univ : LambdaCDM
       An AstroPy cosmology.
    solid_Angle : float
        The solid angle over which the corresponding survey is taken, in 
        steradians. Standard value is 4 pi (i.e. the whole sky).
    min_z : float, optional
       The minimum redshift bin for the table. Standard value is 0.0.
    min_z : float, optional
       The maximum redshift bin for the table. Standard value is 1.5.
    N : float, optional
       The number of redshift bins in the table. Standard value is 1e5.

    Returns
    -------
    table : array_like
       A (N,6) array of redshift values and corresponding dependants.

    '''
    
    intvl = 1.0/N * (max_z - min_z)                      # Redshift bin interval
    table = np.zeros((int(N),6))
    for i in xrange(int(N)):
        z           = intvl + i * intvl
        table[i][0] = z                                  # z (1)
        table[i][1] = univ.distmod(z).value + \
                      k_corr(z) + e_corr(z)              # q (2)
        table[i][2] = (solid_Angle / (4.0 * np.pi * univ.h ** 3)) * \
                       univ.comoving_volume(z).value     # V_c (3)
        table[i][3] = 1.0                                # Delta (4)
        if i != 0:
            table[i][4] = table[i][2] - table[i-1][2]    # DeltaV_c (5)
            table[i][5] = (table[i][4]*table[i][3]) \
                           + table[i-1][5]               # Sum_dc (6)
        else:
            table[i][4] = 0.0                            # DeltaV_c for min_z
            table[i][5] = 0.0                            # Sum_dc for min_z
    
    return table
    
    
def v_max(table, M, lim=0.5):
    '''
    Estimates the maximum volume statistic for a galaxy of absolute magnitude M
    from a table.
    
    Finds the maximum volume for any given galaxy with absolute magnitude M
    to be translocated and still remain in survey parameters of observed 
    magnitude, using a redshift table. An absolute redshift limit for the 
    volume can be set, based on the redshift limits of the survey.

    Parameters
    ----------
    table : array_like
       A (N,6) array of redshift values and corresponding dependants. 
    M : float
       The absolute magnitude of the galaxy.
    lim : float or NoneType, optional
       The redshift limit on the maximum volume. Use None if no limit is used.

    Returns
    -------
    v : float
       The maximum volume statistic for the galaxy.
    v_mx : float
       The upper volume limit for the galaxy's maximum volume.
    v_mn : float
       The lower volume limit for the galaxy's maximum volume.

    '''
    
    q_min = m_min - M                                # Minimum distance modulus
    q_max = m_max - M                                # Maximum distance modulus
    
    index_z_min = np.searchsorted(table[:,1], q_min) # Binary search for min z
    index_z_max = np.searchsorted(table[:,1], q_max) # Binary search for max z
    
    if lim==None:
        return table[index_z_max][2] - table[index_z_min][2], \
               table[index_z_max][2], table[index_z_min][2]
    elif table[index_z_max][0] > lim:
        index_z_max = np.searchsorted(table[:,0], lim)
    
    return table[index_z_max][2] - table[index_z_min][2], \
           table[index_z_max][2], table[index_z_min][2]

def v_max_dc(table, M, lim=0.5):
    '''
    Estimates the density corrected maximum volume statistic from Cole (2011) 
    for a galaxy of absolute magnitude M from a table.
    
    Finds the density corrected maximum volume for any given galaxy with 
    absolute magnitude M to be translocated and still remain in survey 
    parameters of observed magnitude, using a redshift table. An absolute 
    redshift limit for the volume can be set, based on the redshift limits of 
    the survey.

    Parameters
    ----------
    table : array_like
       A (N,6) array of redshift values and corresponding dependants, 
       including overdensity. 
    M : float
       The absolute magnitude of the galaxy.
    lim : float or NoneType, optional
       The redshift limit on the maximum volume. Use None if no limit is used.

    Returns
    -------
    v_dc : float
       The density corrected maximum volume statistic for the galaxy.
    v_mx : float
       The upper volume limit for the galaxy's maximum volume.
    v_mn : float
       The lower volume limit for the galaxy's maximum volume.

    '''
    
    q_min = m_min - M                                # Minimum distance modulus
    q_max = m_max - M                                # Maximum distance modulus
    
    index_z_min = np.searchsorted(table[:,1], q_min) # Binary search for min z
    index_z_max = np.searchsorted(table[:,1], q_max) # Binary search for max z
    
    if lim==None:
        return table[index_z_max,5] - table[index_z_min,5], \
        table[index_z_max][2] * table[index_z_max][3], table[index_z_min][2] * \
        table[index_z_min][3] 
    elif table[index_z_max][0] > lim:
        index_z_max = np.searchsorted(table[:,0], lim)
    
    return table[index_z_max,5] - table[index_z_min,5], table[index_z_max][2] \
    * table[index_z_max][3], table[index_z_min][2] * table[index_z_min][3] 
    
    
def lumin_func_est(z, m, table, dM=0.1, absolute=True, density_corr=True):
    '''
    Estimates the luminosity function of galaxies of magnitudes m and redshifts 
    z.

    This estimates the luminosity function for a collection of galaxies, given 
    as arrays of corresponding magnitudes and redshifts, over absolute magnitude 
    bins of size dM and using a redshift table.

    Parameters
    ----------
    z : array_like
       An array of redshift values.
    m : array_like
       An array of magnitude values, where z[x] and m[x] refer to the same 
       galaxy.
    table : array_like
       A (N,6) array of redshift values and corresponding dependants.
    dM : float, optional
       The size of the absolute magnitude bins over which luminosity function
       values are applicable.
    absolute : bool, optional
       True if the magnitudes m are absolute; False if they are apparent.
    density_corr : bool, optional
       True if the density corrected maximum volume is to be used; False if the
       classic density independent value is used.

    Returns
    -------
    M_bin : array_like
       An array of the lower limits of the luminosity bins.
    M_bincentres : array_like
       An array of the centres of the luminosity bins.
    lum_func : array_like
       The estimated luminosity function phi, a function of M_bincentre values.

    '''

    if len(m) != len(z):
        return 'The catalogue must consist of two ordered lists of ' + \
        'magnitudes m and redshifts z of equal length.'

    elif absolute == False:
        M = np.zeros(shape=(len(m),))
        for g in xrange(len(m)):
            M[g] = abs_mag(z[g], m[g])

    elif absolute == True:
        M = np.copy(m)
    
    binnum       = int(abs(max(M)-min(M))/dM)

    if density_corr == True:
        inv = 1.0/np.asarray([v_max_dc(table, M[i])[0] for i in range(len(M))])
    elif density_corr == False:
        inv = 1.0/np.asarray([v_max(table, M[i])[0] for i in range(len(M))])

    lum_func,M_bin = np.histogram(M, weights=inv, bins=binnum, \
                                  range=(min(M),max(M)))
    dM_true = M_bin[2]-M_bin[1]
    M_bincentres=(M_bin[1:]+M_bin[:-1])/2.0
    lum_func /= dM_true

    return M_bin, M_bincentres, lum_func

    

#-------------------------------------------------------------------------------


def rand_cat_populator(z, M, ra, dec, attributes, table, win=False, sig=Sigma, \
                       z_lim=0.5, ra_lim=(0.,10.), dec_lim=(-7.5,7.5)):
    '''
    Populatates a random catalogue with clones from an initial catalogue (z, M,
    ra, dec, attributes), using a redshift table defined by redshift_tabulator.

    From a catalogue of galaxies of redshifts (z), absolute magnitudes (M), 
    right ascension (ra), declination (dec), and arbitrary properties 
    (attributes), a new random catalogue is generated by cloning the original
    galaxies. If win is set to True, the galaxies will be redistributed in V_max
    in a probabiity window with standard deviation sig, as used in Farrow 
    (2015). If not, it will be distributed uniformly. A maximum limit in 
    redshift (z_lim) can be set, in addition to upper and lower limits in right
    ascension (ra_lim) and declination (dec_lim).

    Parameters
    ----------
    z : array_like
       An array of redshift values for a catalogue of galaxies.
    M : array_like
       An array of absolute magnitude values for the catalogue of galaxies.
    ra : array_like or NoneType
       An array of right ascension values for the catalogue of galaxies. If no 
       values are given, use None.
    dec : array_like or NoneType
       An array of declination values for the catalogue of galaxies. If no 
       values are given, use None.
    attributes : array_like
       An array of arbitrary properties values for the catalogue of galaxies.
    table : array_like
       A (N,6) array of redshift values and corresponding dependants.
    win : bool, optional
       True if the Farrow window is to be used; False if a uniform 
       distribution is to be used.
    sig : float, optional
       The standard deviation of the Farrow window.
    z_lim : float or NoneType, optional
       The redshift limit of the redistribution. Use None if no limit is used.
    ra_lim : array_like (float, float) or NoneType, optional
       The right ascension limits (lower, upper) of the redistribution. Using 
       None will redistrbute in redshift alone.
    dec_lim : array_like (float, float) or NoneType, optional
       The declination limits (lower, upper) of the redistribution in degrees. 
       Using None will redistrbute in redshift alone.

    Returns
    -------
    rand_cat : array_like
       An array for a random catalogue (z, M, ra, dec, attributes)
    n_list : array_like
       An array of the number of clones of each original galaxy.
    lum_func : array_like
       An array of the redshift of each original galaxy.
       
    '''
    
    rand_cat  = []
    n_list    = []
    orgz_list = []
    ang_pos   = False
    
    if ra != None and dec != None and ra_lim != None and dec_lim != None:
        low_dec = np.radians(dec_lim[0])
        hi_dec  = np.radians(dec_lim[1])
        low_ra  = np.radians(ra_lim[0])
        hi_ra   = np.radians(ra_lim[1]) 
        ang_pos = True   
    
    if win == True:
        random_v = lambda w,x,y,z: reflwin.rand_refl_win(w,x,y,z)
    elif win == False:
        random_v = lambda w,x,y,z: np.random.random() * (y-x)
           
    for i in xrange(len(z)):
        v, v_mx, v_mn          = v_max(table, M[i], None)
        v_dc, v_mx_dc, v_mn_dc = v_max_dc(table, M[i], None)
        n                      = n_clone * v / v_dc
        centre                 = table[np.searchsorted(table[:,0], z[i])][2]
            
        prob_n = 1 - (n % 1)
        lot_n  = np.random.rand()
            
        if lot_n <= prob_n:
            n = np.floor(n)
        else:
            n = np.ceil(n)
            
        n_list.append(n)
        
        for j in xrange(int(n)):
            new_v   = v_mn + random_v(centre,v_mn,v_mx,sig)
            new_z   = table[np.searchsorted(table[:,2], new_v)][0]
            while new_z > z_lim:
                new_v = v_mn + random_v(centre,v_mn,v_mx,sig)
                new_z = table[np.searchsorted(table[:,2], new_v)][0]
            if ang_pos == True:
                new_ra  = np.random.random() * (hi_ra - low_ra)
                new_dec = np.arcsin(np.random.random() * \
                          (np.sin(hi_dec) - np.sin(low_dec)))
                rand_cat.append([new_z, M[i], new_ra, new_dec, attributes[i]])
            else:
                rand_cat.append([new_z, M[i], attributes[i]])
            orgz_list.append(z[i])
        
    return np.asarray(rand_cat), n_list, orgz_list
    
    
def overdensity_iter(z, M, ra, dec, attributes, table, N, dz=0.025, win=False, \
                     sig=Sigma, z_lim=0.5, ra_lim=(0.,10.), dec_lim=(-7.5,7.5),\
                     record=False):
    '''
    Populatates a random catalogue with clones from an initial catalogue using 
    rand_cat_populator for N iterations, correcting the overdensity array after 
    each run.

    From a catalogue of galaxies of redshifts (z), absolute magnitudes (M), 
    right ascension (ra), declination (dec), and arbitrary properties 
    (attributes), a new random catalogue is generated by cloning the original
    galaxies. If win is set to True, the galaxies will be redistributed in V_max
    in a probabiity window with standard deviation sig, as used in Farrow 
    (2015). If not, it will be distributed uniformly. A maximum limit in 
    redshift (z_lim) can be set, in addition to upper and lower limits in right
    ascension (ra_lim) and declination (dec_lim). This is then repeated N times,
    with the overdensity measured and recorded in a running version of table 
    with each iteration, over redshift bins of size dz. The final catalogue will
    then be made uniform according to the methods in Cole (2011) and/or Farrow
    (2015).


    Parameters
    ----------
    z : array_like
       An array of redshift values for a catalogue of galaxies.
    M : array_like
       An array of absolute magnitude values for the catalogue of galaxies.
    ra : array_like
       An array of right ascension values for the catalogue of galaxies.
    dec : array_like
       An array of declination values for the catalogue of galaxies.
    attributes : array_like
       An array of arbitrary properties values for the catalogue of galaxies.
    N : float
       The number of iterations of the generation loop.
    dz : float, optional
       The separation of redshift bins over which the overdensity is measured.
    table : array_like
       A (X,6) array of redshift values and corresponding dependants.
    win : bool, optional
       True if the Farrow window is to be used; False if a uniform 
       distribution is to be used.
    sig : float, optional
       The standard deviation of the Farrow window.
    z_lim : float or NoneType, optional
       The redshift limit of the redistribution. Use None if no limit is used.
    ra_lim : array_like (float, float) or NoneType, optional
       The right ascension limits (lower, upper) of the redistribution. Using 
       None will redistrbute in redshift alone.
    dec_lim : array_like (float, float) or NoneType, optional
       The declination limits (lower, upper) of the redistribution in degrees. 
       Using None will redistrbute in redshift alone.
    record : Boolean, optional
       True if a complete record of all returns at every iteration is needed,
       False if only the final iteration is needed (to limit memory cost).
       
       
    Returns
    -------
    run_table : array_like
       An array of the redshift values and corresponding dependants, with the
       overdensity acquired by iteration.
    run_cat : array_like
       An array for a random catalogue (z, M, ra, dec, attributes)
    run_delta : array_like
       An array of the obtained overdensties, equivalent to run_table[:,3].
    run_zbin : array_like
       An array of the redshift bins the overdensities were gathered over.
    run_n : array_like
       An array of the number of clones made of each original galaxy.
    run_orgz : array_like
       An array of the original redshifts of each original galaxy.
    table_rec : array_like, optional
       An array of the run_table arrays produced at each iteration. Only 
       produced if record is set to True.
    cat_rec : array_like, optional
       An array of the run_cat arrays produced at each iteration. Only 
       produced if record is set to True.
    delta_rec : array_like, optional
       An array of the run_delta arrays produced at each iteration. Only 
       produced if record is set to True.
    zbin_dec : array_like, optional
       An array of the run_zbin arrays produced at each iteration. Only 
       produced if record is set to True.
    n_rec : array_like, optional
       An array of the run_n arrays produced at each iteration. Only 
       produced if record is set to True.
    orgz_rec : array_like, optional
       An array of the run_orgz arrays produced at each iteration. Only 
       produced if record is set to True.

    '''
    
    run_table = table.copy()
    if record == True:
        table_rec = []
        delta_rec = []
        cat_rec   = []
        zbin_rec  = []
        n_rec     = []
        orgz_rec  = []
        table_rec.append(run_table)
    
    run_orgz  = []
    
    def ceilstep(a, hibound):
        'The floor of a with respect to step size hibound.'
        return np.ceil(np.array(a, dtype=float) / hibound) * hibound
            
    def floorstep(a, lowbound):    
        'The ceiling of a with respect to step size lowbound.'
        return np.floor(np.array(a, dtype=float) / lowbound) * lowbound

    for i in xrange(N):
        
        if record == True:
            run_cat, run_n, run_orgz = rand_cat_populator(z, M, ra, dec, \
                                                          attributes, \
                                                          table_rec[-1], win, \
                                                          sig, z_lim, ra_lim, \
                                                          dec_lim)
        elif record == False:
            run_cat, run_n, run_orgz = rand_cat_populator(z, M, ra, dec, \
                                                          attributes, \
                                                          run_table, win, \
                                                          sig, z_lim, ra_lim, \
                                                          dec_lim)
                                                          
        z_r      = run_cat[:,0]

        minz   = floorstep(min(z),dz)
        maxz   = ceilstep(max(z),dz)
        binnum = int(np.round((maxz-minz)/dz))

        n_g,z_bin   = np.histogram(z, bins=binnum, range=(minz,maxz))
        n_r,z_r_bin = np.histogram(z_r, bins=binnum, range=(minz,maxz))
        run_zbin    = (z_bin[1:]+z_bin[:-1])/2.0
        
        if 0 not in n_r and 0. not in n_r:
            run_delta = n_clone * n_g / np.asarray(n_r, dtype=float)
        else:
            run_delta = np.zeros_like(n_g, dtype=float)
            ind_nonzero = (n_r != 0)
            run_delta[ind_nonzero] = n_clone * n_g[ind_nonzero] / \
            np.asarray(n_r[ind_nonzero], dtype=float)
        
        for j in xrange(len(run_table)):
            
            j_z = run_table[j][0]    
                                            
            if j_z < maxz and j_z > minz:
                k = np.searchsorted(z_bin, floorstep(j_z, dz)) - 1
                run_table[j][3] = run_delta[k]
            else:
                run_table[j][3] = 1.0
            
            if j != 0:  
                run_table[j][5] = (run_table[j][4]*run_table[j][3]) + \
                run_table[j-1][5]  
            else:
                run_table[j][5] = 0.0
            
        run_table = run_table.copy()
        if record == True:
            table_rec.append(run_table)
            cat_rec.append(run_cat)
            n_rec.append(run_n)
            delta_rec = np.append(delta_rec, run_delta)
            zbin_rec  = np.append(zbin_rec, run_zbin)
            zbin_rec  = np.append(orgz_rec, run_orgz)
        
    if record == True:    
        return run_table, run_cat, run_delta, run_zbin, run_n, run_orgz, \
        table_rec, cat_rec, delta_rec, zbin_rec, n_rec, orgz_rec
    elif record == False:    
        return run_table, run_cat, run_delta, run_zbin, run_n, run_orgz


#-------------------------------------------------------------------------------


if __name__=="__main__":
    print "Please wait while the table is generated."
    table = redshift_tabulator(cosmo)
    print "Table finished."
    
    
    print "Please wait while the random catalogue is generated."
    if take_record == True:
        run_table, rand_cat, run_delta, run_zbin, run_n, run_orgz, table_rec, \
        cat_rec, delta_rec, zbin_rec, n_rec, orgz_rec = \
        overdensity_iter(z, mag, ra, dec, att, table, N, dz, windowed, Sigma, \
                         zlim, ralim, declim, take_record)
    elif take_record == False:
        run_table, rand_cat, run_delta, run_zbin, run_n, run_orgz = \
        overdensity_iter(z, mag, ra, dec, att, table, N, dz, windowed, Sigma, \
                         zlim, ralim, declim, take_record)
    np.savetxt("rand_cat.txt", rand_cat, delimiter= ' ')
    np.savetxt("table.txt", table, delimiter= ' ')
    print "Random catalogue generated; saved as rand_cat.txt. Available as" + \
           " variable rand_cat. Table saved as table.txt."
    
    def finalplot():

        M = 200
        n, bins   = np.histogram(rand_cat[:,0], bins = M, normed=True)
        bincent   = (bins[1:]+bins[:-1])/2.0
        n2, bins2 = np.histogram(z, bins = M, normed=True)
        bincent2  = (bins2[1:]+bins2[:-1])/2.0

        corrn  = sum(n)
        corrn2 = sum(n2)
    
        pyplot.figure(1,figsize=(8.2677,11.6929))
        pyplot.subplots_adjust(left=0.2)
        pyplot.rcParams['xtick.major.pad'] = 6
        pyplot.rcParams['ytick.major.pad'] = 6
    
        pyplot.subplot(1,1,1)
        pyplot.xlabel(r'$z$',fontsize='48')
        pyplot.ylabel(r'$N(z)$',fontsize='48')
        pyplot.plot(bincent, n/corrn)
        pyplot.plot(bincent2, n2/corrn2)
        pyplot.legend(['Farrow (2015) Distribution', \
                       'Cole (2011) Distribution', \
                       'Analytic Distribution'], fontsize='xx-large')
    
        pyplot.show()
    
    
        return 0.0
        
    finalplot()
