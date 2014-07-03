#! /usr/bin/env python



# ::::::::::::::::::::::::::::::
# IMPORT MODULES & PYTHON TASKS:
# ::::::::::::::::::::::::::::::

import sys
import os.path
import math

from pyraf import iraf
import pyfits

import filecheck
import reduction



# ::::::::::::::::::::::::::::::::::::
# STEP 1.1 DETERMINE ORDER/WAVELENGTH:
# ::::::::::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'WAVELENGTH OF INTEREST:                            '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'Please enter wavelength of interest in Angstroms:  '
print 'e.g. 6562.8                                        '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '

# Get wavelength from terminal and convert to a number from text for calculations:
wvlength = float(raw_input())

# If wavelength outside range of SALT HRS:
while True:
  if wvlength < 3700.0 or wvlength > 8900.0:
    print ' '
    print ' '
    print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
    print 'WAVELENGTH RANGE ERROR:                            '
    print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
    print 'Wavelength (' + str(wvlength) + ') must be between 3700.0 and 8900.0'
    print 'Angstroms. Please try again:                       '
    print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
    print ' '
    wvlength = float(raw_input())
  else:
    break

# Calculate order from wavelength:
order = (2.0 * ((1.0/41.59) * 10000000.0) * math.sin(math.radians(76))) / wvlength
order = str(round(order))
# Strip off extraneous decimal places:
order = order[:-2]

# If blue wavelength:
if wvlength >= 3700.0 and wvlength < 5550.0:
  colour = 'blue'

# If red wavelength:
elif wvlength >= 5550.0 and wvlength <= 8900.0:
  colour = 'red'



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# STEP 1.2: CONFIRM REDUCTION FRAMES, CALCULATE SETUPS & CHECK FILES:
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print str(colour).upper() + ' CCD WAVELENGTH:             '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'Wavelength (' + str(wvlength) + 'A) appears on the ' + str(colour) + ' HRS CCD in'
print 'order ' + str(order) + '.                          '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print str(colour).upper() + ' OBJECT FILE?                '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'Please enter the file name for the ' + str(colour) + ' object file'
print 'you wish to reduce, including the .fits extension  '
print 'e.g. ' + str(colour)[0].capitalize() + 'YYYYMMDD0001.fit.'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '

while True:
# Determine if file exists:
  image = filecheck.exists()

# Run file check on red input file to determine setup (amplifiers,
# HRS mode etc.):
  image, instrume, ccd, exptype, expmode, i2stage, \
    ccdamps, rospeed, ccdsum = filecheck.kw_check(image)

# Check if it is a red object file:
  if ccd[0] == colour and exptype[0] == "Science":
# Print settings to screen:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print str(colour).capitalize() + ' CCD SALT-HRS settings as follows:'
    print 'CCD: ' + instrume[0] + ' ' + str(ccd[0]).capitalize()
    print 'Exposure Type: ' + str(exptype[0])
    print 'HRS Mode: ' + str(expmode[0])
    print 'Iodine Cell Stage Setup: ' + str(i2stage[0])
    print 'No. Amplifiers: ' + str(ccdamps[0])
    print 'Read-out Speed: ' + str(rospeed[0]) + 'kHz'
    print 'CCD Binning: ' + str(ccdsum[0])
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
# Add DISPAXIS keyword to object file (if missing):
    image = str(image[0])
    filecheck.dispaxis(image)
    break
# Error if input is an existing, keyword acceptable file but which
# is not for an appropriate colour CCD and/or not an object file:
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'ERROR: From the file name and header, this does not'
    print 'appear to be a ' + str(colour).capitalize + ' file containing SCIENCE data.   '
    print 'Please try again:                                  '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '



# :::::::::::::::::::::::::::::::::
# STEP 2.1: SHOW MASTER BIAS FRAME:
# :::::::::::::::::::::::::::::::::

# Define default pre-existing combined_bias frame:
combined_bias = str("default_" + str(colour) + "_" + str(ccdamps[0]) + "_" + \
  str(rospeed[0]) + "_" + str(ccdsum[0]) + "_combined_bias.fit")
combined_bias = str(combined_bias)
print ' '
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Pre-existing default master bias to be used:       '
print str(combined_bias)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print ' '
# Check if default file exists:
if os.path.isfile(combined_bias) == False:
  print ' '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'Default master bias                                '
  print  str(combined_bias)
  print 'does not exist. Exiting script.                    '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print ' '
  print ' '
  sys.exit()



# :::::::::::::::::::::::::::::::::
# STEP 2.2: SHOW MASTER FLAT FRAME:
# :::::::::::::::::::::::::::::::::

# Define default pre-existing combined_flat frame:
combined_flat_b_n = str("default_" + str(colour) + "_" + str(ccdamps[0]) + "_" + \
  str(rospeed[0]) + "_" + str(ccdsum[0]) + "_combined_flat_b_n.fit")
combined_flat_b_n = str(combined_flat_b_n)
print ' '
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Pre-existing default master flat to be used:       '
print str(combined_flat_b_n)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print ' '
# Check if default file exists:
if os.path.isfile(combined_flat_b_n) == False:
  print ' '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'Default master flat                                '
  print  str(combined_flat_b_n)
  print 'does not exist. Exiting script.                    '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print ' '
  print ' '
  sys.exit()



# ::::::::::::::::::::::::::::::::::::::::::::::::
# STEP 2.3: SHOW FIRST REFERENCE EXTRACTION FRAME:
# ::::::::::::::::::::::::::::::::::::::::::::::::

# Define default pre-existing order_def frame:
order_def = str("default_" + str(colour) + "_" + str(ccdamps[0]) + "_" + \
  str(rospeed[0]) + "_" + str(ccdsum[0]) + "_order_def.fit")
order_def = str(order_def)
print ' '
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Pre-existing default order definition to be used   '
print str(order_def)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print ' '
# Check if default file exists:
if os.path.isfile(order_def) == False:
  print ' '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'Default order definition                           '
  print  str(order_def)
  print 'does not exist. Exiting script.                    '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print ' '
  print ' '
  sys.exit()



# ::::::::::::::::::::::::::::::::::::::::::::
# STEP 2.4: SHOW WAVELENGTH CALIBRATION FRAME:
# ::::::::::::::::::::::::::::::::::::::::::::

# Define default pre-existing wavelength reference frame:
wave_ref = str("default_" + str(colour) + "_" + str(ccdamps[0]) + "_" + \
  str(rospeed[0]) + "_" + str(ccdsum[0]) + "_wave_ref.fit")
wave_ref = str(wave_ref)
print ' '
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Pre-existing default wavelength reference to be    '
print 'used                                               '
print str(wave_ref)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print ' '
# Check if default file exists:
if os.path.isfile(wave_ref) == False:
  print ' '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'Default wavelength reference                       '
  print  str(wave_ref)
  print 'does not exist. Exiting script.                    '
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print ' '
  print ' '
  sys.exit()



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# STEP 3: SUBTRACT DEFAULT/CREATED COMBINED BIAS FRAME FROM OBJECT:
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'OBJECT FRAME BIAS SUBTRACTION:'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'The appropriate bias frame will now be subtracted  '
print 'from the user-defined object frame:                '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'

# Setup filenames:
addition = '_b'
object_b = filecheck.file_setup(image, addition)

# Determine if bias-subtracted object file would be over-written
# (this would cause an imarith error in sub_bias if unchecked):
filecheck.overwrite(object_b)

# Call IRAF task via reduction.py (if file deleted earlier or doesn't yet exist):
if os.path.isfile(object_b) == False:
  reduction.sub_bias(image, combined_bias, object_b)



# ::::::::::::::::::::::::::::::::
# STEP 4: FLAT FIELDING OF OBJECT:
# ::::::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'FLAT FIELDING OF OBJECT FRAME:                     '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'The bias-subtracted object frames are flat-fielded '
print 'by dividing by a normalized, bias-subtracted       '
print 'combined flat frame:                               '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'

# Setup filenames:
#addition = '_fn'
#object_b_fn = filecheck.file_setup(object_b, addition)

# Determine if bias-subtracted, normalized flat-fielded
# object would be over-written:
#filecheck.overwrite(object_b_fn)

# Call IRAF task imarithmetic via reduction.py (if file deleted earlier or doesn't yet exist):
#if os.path.isfile(object_b_fn) == False:
#  reduction.flat_field(object_b, combined_flat_b_n, object_b_fn)



# :::::::::::::::::::::::::::::::::::::::::::::::::::
# STEP 5: ONE DIMENSIONAL OBJECT SPECTRAL EXTRACTION:
# :::::::::::::::::::::::::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'ONE DIMENSIONAL SPECTRAL OBJECT EXTRACTION:        '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'A spectra for each order is extracted from the     '
print 'bias-subtracted, flat-fielded object frame, using  '
print 'the initial extraction as a reference:             ' 
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '

# Setup filenames:
addition = '_ec'
object_b_ec = filecheck.file_setup(object_b, addition)

# Determine if bias-subtracted, normalized flat-fielded,
# order extraction would be over-written:
filecheck.overwrite(object_b_ec)

# Add DISPAXIS keyword to bias-subtracted,
# normalized flat-fielded, object frame:
filecheck.dispaxis(image=object_b)

# Call IRAF task apall via reduction.py (if file deleted earlier or doesn't yet exist):
if os.path.isfile(object_b_ec) == False:
  reduction.oned_extract(object_b, object_b_ec, order_def, colour)



# :::::::::::::::::::::::::
# STEP 6: ThAr CALIBRATION:
# :::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'WAVELENGTH CALIBRATION:'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'The wavelength scale derived previously is now     '
print 'applied to the object spectra:                     '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '

# Ensure default frame contains REFSPEC1 keyword as its own filename
# (e.g. REFSPEC1 = default_red_1_1000_1x1_wave_ref fpr this file):
filecheck.refspec1(wave_ref)

# Assign reference red spectra to red object spectra:
reduction.thar_ref(object_b_ec, wave_ref, colour)

# Setup filenames for wavelength dispersion correction:
addition = '_w'
object_b_ec_w = filecheck.file_setup(object_b_ec, addition)

# Determine if bias-subtracted, normalized flat-fielded,
# wavelength-calibrated order extraction would be over-written:
filecheck.overwrite(object_b_ec_w)

# Call IRAF task dispcor via reduction.py (if file deleted earlier or doesn't yet exist):
# Apply dispersion correction functions to object spectra:
if os.path.isfile(object_b_ec_w) == False:
  reduction.thar_cal(object_b_ec, object_b_ec_w, colour)



# ::::::::::::::::::::::::::::
# STEP 7: PLOT RELEVANT ORDER:
# ::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'PLOTTING EXTRACTED SPECTRA:'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'The extracted, wavelength-calibrated spectrum      '
print str(object_b_ec_w)
print 'is now plotted at order ' + str(order) + ' for the user'
print 'specified wavelength at ' + str(wvlength) + 'A:'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '

plot_order = str(-(int(order)) + 86)

iraf.noao(_doprint=0)
iraf.onedspec(_doprint=0)
iraf.splot(images=object_b_ec_w, line=plot_order)



# :::::::::::::::::::::::::::::::
# STEP 8: REMOVE TEMPORARY FILES:
# :::::::::::::::::::::::::::::::

print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'TEMPORARY FILE REMOVAL:                            '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'Temporary files clean up:                          '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '

# Potential temporary file list:
files = object_b, object_b_ec, object_b_ec_w

# Check files and produce temporary file list for deletion:
temp_files = filecheck.temp_files(files)

# Delete files and print all files deleted:
#filecheck.temp_delete(temp_files)



print ' '
print ' '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'REDUCTION COMPLETE:                                '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print 'Quicklook reduction complete. Quiting PyHRS.py.    '
print ':::::::::::::::::::::::::::::::::::::::::::::::::::'
print ' '
print ' '

sys.exit()
