#! /usr/bin/env python

import pyfits
import os.path
import sys
from pyraf import iraf

import keywords



def exists():
# Prompt user file input:
  image = raw_input()
  while True:
    if os.path.isfile(image) == True:
      break
# Prompts for new file name if file does not exist and returns to start
# to start of procedure:
    else:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: ' + image
      print 'was not found. Please try again:                   '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return image



def kw_check(image):
# Convert input file or list of files from 'Himage.fit' or 'Himage.fit Rimage.fit'
# to [Himage.fit']  or ['Himage.fit','Rimage.fit']:
  image = image.replace(',',' ').split(' ')

# Define settings and errors list at same size as image input file list:
  instrume = [None] * len(image)
  ccd = [None] * len(image)
  exptype = [None] * len(image)
  expmode = [None] * len(image)
  i2stage = [None] * len(image)
  ccdamps = [None] * len(image)
  rospeed = [None] * len(image)
  ccdsum = [None] * len(image)

# Assign a value to settings/errors list:
  for i in range(len(image)):
    instrume[i] = 'Empty'
    ccd[i] = 'Empty'
    exptype[i] = 'Empty'
    expmode[i] = 'Empty'
    i2stage[i] = 'Empty'
    ccdamps[i] = 'Empty'
    rospeed[i] = 'Empty'
    ccdsum[i] = 'Empty'

# Get image name, setting and error (0 or 1) from keywords module:
  for i in range(len(image)):
    instrume[i] = keywords.instrume(image[i])
    ccd[i] = keywords.ccd(image[i])
    exptype[i] = keywords.exptype(image[i])
    expmode[i] = keywords.expmode(image[i])
    i2stage[i] = keywords.i2stage(image[i])
    ccdamps[i] = keywords.ccdamps(image[i])
    rospeed[i] = keywords.rospeed(image[i])
    ccdsum[i] = keywords.ccdsum(image[i])

# Returns arrays containing file name and associated keyword values:
# e.g. ['RObject.fit', 'HObject.fit'], ['HRS', 'HRS'], ['Red', Blue'] etc.
  return (image, instrume, ccd, exptype, expmode, \
    i2stage, ccdamps, rospeed, ccdsum)



def overwrite(image):
# Checks if file exists:
  if os.path.isfile(image) == True:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'ERROR: ' + image
    print 'already exists. Replace with newly created file    ' 
    print '(Y)? Or continue using existing file (N)?:         '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    while True:
# Prompt user to overwrite or not overwrite file (Y/N):
      overwrite_option = raw_input()
# Delete file if Y:
      if overwrite_option == "Y" or overwrite_option == "y" or overwrite_option == "Yes" or overwrite_option == "yes":
        iraf.images(_doprint=0)
        iraf.imutil(_doprint=0)
        iraf.imdelete(images=image, verify="No", default_action="Yes", go_ahead="Yes")
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print image
        print 'deleted. New file can now be created in its place. '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        break
# Do not delete file (with construct in hrs.py, the existing file is used):
      elif overwrite_option == "N" or overwrite_option == "n" or overwrite_option == "No" or overwrite_option == "no":
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print image
        print 'not deleted. Existing file will be used.           '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        break
# Return to start of procedure and request Y/N if non Y/N answer provided:
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: Please specify an option Y (Yes) or N (No): ' 
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '



def dispaxis(image):
  if os.path.isfile(image) == True:
# Opens image for keyword check/addition:
    hdulist = pyfits.open(image, mode='update')
# Look for keyword:
    try:
      hdulist[0].header['dispaxis']
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'DISPAXIS = 1 keyword and value present in file     '
      print image
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
# If keyword is not present, add DISPAXIS keyword with value of 1:
    except:
      prihdr = hdulist[0].header
      prihdr.update('dispaxis', 1)
      hdulist.flush()
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'DISPAXIS = 1 keyword added to file                 '
      print image
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print image
    print 'is absent. Cannot check for/add DISPAXIS keyword.  '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '



def refspec1(image):
  if os.path.isfile(image) == True:
# Opens image for keyword check/addition:
    hdulist = pyfits.open(image, mode='update')
    refspec = image.split('.')
    refspec = str(refspec[0])
    refspec_option = ''
# Look for keyword:
    try:
      hdulist[0].header['refspec1']
      if hdulist[0].header['refspec1'] == refspec:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'REFSPEC1 keyword present in file                   '
        print str(image)
        print 'with correct value of                              '
        print str(refspec)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'REFSPEC1 keyword present in file                   '
        print str(image)
        print 'with incorrect value of                            '
        print hdulist[0].header['refspec1'] + '.'
        print 'Update header value accordingly (Y)? Or exit (N)?  '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        while True:
# Prompt user to overwrite or not overwrite file (Y/N):
          refspec_option = raw_input()
# Delete file if Y:
          if refspec_option == "Y" or refspec_option == "y" or refspec_option == "Yes" or refspec_option == "yes":
            prihdr = hdulist[0].header
            prihdr.update('refspec1', refspec)
            hdulist.flush()
            print ' '
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print 'REFSPEC1 keyword updated to                        ' 
            print str(refspec)
            print 'in file                                            '
            print str(image)
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print ' '
            break
# Do not delete file (with construct in hrs.py, the existing file is used):
          elif refspec_option == "N" or refspec_option == "n" or refspec_option == "No" or refspec_option == "no":
            print ' '
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print 'REFSPEC1 keyword not updated in file               '
            print str(image)
            print 'Reduction cannot continue. Exiting script.         '
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print ' '
            sys.exit()
# Return to start of procedure and request Y/N if non Y/N answer provided:
          else:
            print ' '
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print 'ERROR: Please specify an option Y (Yes) or N (No): ' 
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print ' '
# If keyword is not present, add REFSPEC keyword with correct value:
    except:
#      if refspec_option == "N" or refspec_option == "n" or refspec_option == "No" or refspec_option == "no":
#         sys.exit()
#      else:
      prihdr = hdulist[0].header
      prihdr.update('refspec1', refspec)
      hdulist.flush()
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'REFSPEC1 = ' +str(refspec)
      print 'keyword added to file                              '
      print image
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print image
    print 'is absent. Cannot check for/add REFSPEC1 keyword.  '
    print 'Exiting script.                                    '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '
    print ' '
    sys.exit()



def file_setup(original_image, addition):
  original_image =str(original_image)
  addition = str(addition)
# Determine if filename has an extension (.fit) or not:
# If .fit extension, split filename from extension and insert addition:
  if original_image[-4:] == ".fit" or original_image[-5:] == ".fits":
# Splits filename at '.' e.g. RObject.fit becomes ['RObject', 'fit']:
    original_image = original_image.split('.')
# Adds addition in gap and recombines e.g. ['RObject', 'fit'] and addition='_b' becomes 'RObject_b.fit':
    new_image = str(original_image[0] + addition + '.' + original_image[1])
  else:
    new_image = original_image + addition + '.fit'
# Returns updated image name to higher level calling task:
  return new_image



def temp_files(files):
# Setup empty string to append to:
  temp_files = ''
  for i in files:
# Check if file exists:
    if os.path.isfile(i) == True:
# If so, append to temporary file list:
      temp_files = temp_files + ',' + str(i)
# Else skip over file:
    elif os.path.isfile(i) == False:
      temp_files = temp_files
# Trim first comma in temp_files list if necessary:
  if len(temp_files) > 0:
    if temp_files[0] == ",":
      temp_files = temp_files[1:]
  return temp_files



def temp_delete(temp_files):
# Delete all temporary files involved in the reduction process:
  iraf.imutil(_doprint=0)
  if len(temp_files) > 0:
    iraf.imdelete(images=temp_files, verify="No", default_action="Yes", go_ahead="Yes")
# Form list of deleted files from string for iterable display:
    temp_files = temp_files.split(',')
# Inform user of deletion and list files affected:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Temporary files permanently DELETED are as follows:'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    for i in temp_files:
      print i
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' 
    print ' '
  else:
    print ' '
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'No temporary files to delete.'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print ' '



