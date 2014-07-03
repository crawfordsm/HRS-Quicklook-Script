#! /usr/bin/env python

import sys
import os.path
from pyraf import iraf

import filecheck



def sub_bias(image, combined_bias, image_b):
# Import IRAF modules:
  iraf.images(_doprint=0)
  iraf.imutil(_doprint=0)
  parList = "bias_subtraction_imarith.par"
# Check input file and combined_bias frame exists before proceeding:
  if os.path.isfile(image) == True:
    if os.path.isfile(combined_bias) == True:
      if os.path.isfile(parList) == True:
# Subtract combined bias frame from input frame (object or flat)
# using IRAF task imarithmetic:
        iraf.imarith.setParList(ParList="bias_subtraction_imarith.par")
        iraf.imarith(operand1=image, operand2=combined_bias, result=image_b)
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Bias frame ' + str(combined_bias) 
        print 'subtracted from input ' + str(image)
        print 'to create ' + str(image_b)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Bias frame subtraction IRAF .par file              ' 
        print str(parList)
        print 'does not exist. Exiting script.                    '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        print ' '
        sys.exit()
    else:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'Combined bias frame                                ' 
      print str(combined_bias)
      print 'does not exist. Exiting script.                    '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      print ' '
      sys.exit()
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Input frame                                        ' 
    print str(image)
    print 'does not exist. Exiting script.                    '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    print ' '
    sys.exit()



def flat_field(object_b, combined_flat_b_n, object_b_fn):
# Import IRAF modules:
  iraf.images(_doprint=0)
  iraf.imutil(_doprint=0)
# Check input file and combined_flat frame exist before proceeding:
  if os.path.isfile(object_b) == True:
    if os.path.isfile(combined_flat_b_n) == True:
# Divide bias-subtracted object frame by normalized, bias
# subtracted combined flat frame using IRAF task imarithmetic:
      iraf.imarith(operand1=object_b, op="/", operand2=combined_flat_b_n, result=object_b_fn)
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'Bias-subtracted object frame                       '
      print str(object_b)
      print 'successfully flat-fielded using division by        '
      print str(combined_flat_b_n)
      print 'to create bias-subtracted, normalized flat-fielded '
      print str(object_b_fn) + ' frame.'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
    else:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'Combined flat frame                                ' 
      print str(combined_flat_b_n)
      print 'does not exist. Exiting script.                    '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      print ' '
      sys.exit()
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Input frame                                        ' 
    print str(object_b)
    print 'does not exist. Exiting script.                    '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    print ' '
    sys.exit()



def oned_extract(object_b_fn, object_b_fn_ec, order_def, colour):
# Import IRAF modules:
  iraf.noao(_doprint=0)
  iraf.twodspec(_doprint=0)
  iraf.apextract(_doprint=0)
# Check input file and reference extraction exist before proceeding:
  if os.path.isfile(object_b_fn) == True:
    if os.path.isfile(order_def) == True:
# Extract one dimensional spectrum from bias- and background scatter-subtracted
# normalized flat-fielded red object frame using IRAF task apall:
      if colour == 'red':
        parList = "r_oned_extraction_apall.par"
        if os.path.isfile(parList) == True:
          iraf.apall.setParList(ParList = "r_oned_extraction_apall.par")
          iraf.apall(input=object_b_fn, output=object_b_fn_ec, references=order_def)
          print ' '
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print 'One dimensional spectral extraction of bias- and   '
          print 'background-subtracted, normalized flat-fielded     '
          print 'red object ' + object_b_fn
          print 'to create ' + object_b_fn_ec + '.'
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print ' '
        else:
          print ' '
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print 'One dimensional extraction IRAF .par file          ' 
          print str(parList)
          print 'does not exist. Exiting script.                    '
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print ' '
          print ' '
          sys.exit()
# Extract one dimensional spectrum from bias- and background scatter-subtracted
# normalized flat-fielded blue object frame using IRAF task apall:
      if colour == 'blue':
        parList = "b_oned_extraction_apall.par"
        if os.path.isfile(parList) == True:
          iraf.apall.setParList(ParList = "b_oned_extraction_apall.par")
          iraf.apall(input=object_b_fn, output=object_b_fn_ec, references=order_def)
          print ' '
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print 'One dimensional spectral extraction of bias- and   '
          print 'background-subtracted, normalized flat-fielded     '
          print 'blue object ' + object_b_fn
          print 'to create ' + object_b_fn_s + '.'
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print ' '
        else:
          print ' '
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print 'One dimensional extraction IRAF .par file          ' 
          print str(parList)
          print 'does not exist. Exiting script.                    '
          print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
          print ' '
          print ' '
          sys.exit()
    else:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'Order definition frame                             ' 
      print str(order_def)
      print 'does not exist. Exiting script.                    '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      print ' '
      sys.exit()
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Input frame                                        ' 
    print str(object_b_fn)
    print 'does not exist. Exiting script.                    '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    print ' '
    sys.exit()



def thar_ref(object_b_fn_ec, wave_ref, colour):
# Import IRAF modules:
  iraf.noao(_doprint=0)
  iraf.onedspec(_doprint=0)
#  iraf.echelle(_doprint=0)
  parList = "wavelength_calibration_refspectra.par"
  if os.path.isfile(object_b_fn_ec) == True:
    if os.path.isfile(wave_ref) == True:
      if os.path.isfile(parList) == True:
# Assign reference spectra to input object spectra using IRAF task refspectra:
        iraf.refspectra.setParList(ParList="wavelength_calibration_refspectra.par")
        iraf.refspectra(input=object_b_fn_ec, references=wave_ref)
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print colour.capitalize() + ' object spectrum             '
        print '(' + str(object_b_fn_ec) + ')                      '
        print 'assigned to ' + str(colour) + ' reference spectrum '
        print '(' + str(wave_ref) + ') successfully.              ' 
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Wavelength reference IRAF .par file                ' 
        print str(parList)
        print 'does not exist. Exiting script.                    '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        print ' '
        sys.exit()
    else:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ThAr reference frame                               ' 
      print str(wave_ref)
      print 'does not exist. Exiting script.                    '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      print ' '
      sys.exit()
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Input frame                                        ' 
    print str(object_b_fn_ec)
    print 'does not exist. Exiting script.                    '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    print ' '
    sys.exit()



def thar_cal(object_b_fn_ec, object_b_fn_ec_w, colour):
# Import IRAF modules:
  iraf.noao(_doprint=0)
  iraf.onedspec(_doprint=0)
# Check input file and reference extraction exist before proceeding:
  if os.path.isfile(object_b_fn_ec) == True:
# Perform dispersion correction:
    iraf.dispcor(input=object_b_fn_ec, output=object_b_fn_ec_w)
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print colour.capitalize() + ' object spectrum             '
    print '(' + str(object_b_fn_ec) + ')'
    print 'successfully wavelength calibrated in file         '
    print str(object_b_fn_ec_w) + '.'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Input frame                                        ' 
    print str(object_b_fn_ec)
    print 'does not exist. Exiting script.                    '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    print ' '
    sys.exit()



