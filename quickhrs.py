import os
import math 

from pyraf import iraf
from iraf import pysalt

import saltsafeio as saltio
import saltsafekey as saltkey

import reduction

def calc_order(wavelength):
    """Calculate the order for the given wavlength

       Parameters
       ----------
       wavelength: float
            Wavelength in angstroms

       Notes
       ----- 
       This should be replaces with functionality from PySpectrograph

    """
    order = (2.0 * ((1.0/41.59) * 10000000.0) * math.sin(math.radians(76))) / wavelength
    return int(order)

def quickhrs(image, wavelength, log=None, verbose=True):
    """QUICKHRS is a tool to extract a single order from an HRS image. 


       Parameters
       ----------
       image: string
            Input image from which to extract the spectra. It assumes that the
            image has already been processed by the PySALT pipeline.

       wavelength: float
            Wavelength of order to be extracted

       Returns:
       --------
       spectra: string
            Name of output file containing the extracted spectra
  
    """
    #check that it is a valid file
    saltio.fileexists(image)

    #check that it is a valid wavelenght
    if wavelength < 3700.0 or wavelength > 8900.0:
        msg = 'Wavelength of %s is outside of the valid region for HRS' % (wavelength)
        raise ValueError(msg)

    #determine the order
    order = calc_order(wavelength)

    #get the he basic information about which CCD it is
    hdu = saltio.openfits(image, mode='update')
    detname=saltkey.get('DETNAM', hdu[0])

    if detname=='08443-03-01' or detname=='HRDET':
       arm = 'red'
    elif detname=='04434-23-02' or detname=='HBDET':
       arm = 'blue'
    else:
       raise SaltError('%s is not an HRS detector' % detnam)
    namps = saltkey.get('CCDAMPS', hdu[0])
    rospeed = saltkey.get('ROSPEED', hdu[0])
    rospeed = int(float(rospeed)/1000.0)
    xbin, ybin = saltkey.ccdbin(hdu[0])

    #setup  the default files to be used
    #TODO: This should be switched to pointing to the pysalt/data/
    #directory once it is integrated into the pkg
    order_def_file = "default_%s_%i_%i_%ix%i_order_def.fit" % (arm, namps, rospeed, xbin, ybin)
    saltio.fileexists(order_def_file)
    wave_ref_file = "default_%s_%i_%i_%ix%i_wave_ref.fit" % (arm, namps, rospeed, xbin, ybin)
    saltio.fileexists(wave_ref_file)


    #add keywords that are needed for processing
    if not saltkey.found('DISPAXIS', hdu[0]):
        hdu[0].header.update('DISPAXIS', 1)
        hdu.flush()

    if not saltkey.found('REFSPEC1', hdu[0]):
        hdu[0].header.update('REFSPEC1', wave_ref_file)
        hdu.flush()
        
    
    #extract the one-d spectrum
    if log is not None:
        log.message('Extracting 1-D spectrum from %s using %s' % (image, order_def_file))

    #TODO: Replace with python code and an aperture map
    image = os.path.basename(image)
    ex_image = 'e'+image
    reduction.oned_extract(image, ex_image, order_def_file, arm)

    #wavelength calibrate the extracted data
    #TODO: This could be replaced with a PySpectrograph model
    w_image = 'we'+image
    reduction.thar_ref(ex_image, wave_ref_file, arm)
    reduction.thar_cal(ex_image, w_image, arm)

    #plot the data 
    plot_order = str(-(int(order)) + 86)
    iraf.noao.onedspec.splot(images=w_image, line=plot_order)

 

if __name__=='__main__':
   import sys
   quickhrs(sys.argv[1], float(sys.argv[2]))
   
