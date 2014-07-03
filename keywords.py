#! /usr/bin/env python

from pyfits import getval



def instrume(image):
# Check for INSTRUME keyword and HRS value:
  while True:
    try:
      instrume = getval(image,'INSTRUME',0)
      instrume = str(instrume)
      if instrume == 'HRS':
        instrume = instrume
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not appear to be a SALT-HRS file, as it does'
        print 'not contain the expected INSTRUME .fits keyword'
        print 'value of HRS. Please try again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the INSTRUME keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (instrume)



def ccd(image):
# Check for DETNAM keyword and appropriate CCD serial numbers
# and compare with CCD filenames:
  while True:
    try:
      ccd = getval(image,'DETSER',0)
      ccd = str(ccd)
      if ccd == "04434-23-02" and image[0] == "H":
        ccd = "blue"
        break
      elif ccd == "08443-03-01" and image[0] == "R":
        ccd = "red"
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed detector name (e.g.'
        print '08443-03-01 for the red CCD or 04434-23-02 for the'
        print 'blue CCD). Please try again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the DETSER keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (ccd)



def exptype(image):
# Check for EXPTYPE keyword and Bias/Science etc. values:
  while True:
    try:
      exptype = getval(image,'EXPTYPE',0)
      exptype = str(exptype)
      if exptype == "Bias" or exptype == "Science" or exptype == "Arc" \
        or exptype == "Dark" or exptype == "Flat field":
        exptype = exptype
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed exposure type (e.g.'
        print 'Bias, Dark, Flat field, Arc or Science). Please try'
        print 'again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the EXPTYPE keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (exptype)



def expmode(image):
# Check for EXPMODE keyword and appropriate exposure mode (LR, HR, Calibration etc.):
  while True:
    try:
      expmode = getval(image,'EXPMODE',0)
      expmode = str(expmode)
      if expmode == "LOW RESOLUTION":
        expmode = "LR"
        break
      elif expmode == "MEDIUM RESOLUTION":
        expmode = "MR"
        break
      elif expmode == "HIGH RESOLUTION":
        expmode = "HR"
        break
      elif expmode == "HIGH STABILITY":
        expmode = "HS"
        break
      elif expmode == "INT CAL FIBRE":
        expmode = "CF"
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed exposure mode (e.g. LR,'
        print 'MR, HR, HS or Calibration). Please try again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the EXPMODE keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (expmode)



def i2stage(image):
# Check for I2STAGE keyword and appropriate stage mode (I2Cell, ThArFibre->P etc.):
  while True:
    try:
      i2stage = getval(image,'I2STAGE',0)
      i2stage = str(i2stage)
      if i2stage == "Nothing In Beam" or i2stage == "ThAr->Fibre O" or i2stage == \
        "ThAr->Fibre P" or i2stage == "I2 Cell In Beam" or i2stage == "Calibration":
        i2stage = i2stage
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed SALT-HRS setup (e.g.'
        print 'Nothing in Beam, ThAr->Fibre O, ThAr->Fibre P,'
        print 'I2 Cell In Beam, Calibration). Please try again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the I2STAGE keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (i2stage)



def ccdamps(image):
# Check for CCDAMPS keyword and appropriate number of read-out ports
# taking in to account which colour CCD is in use too
  while True:
    try:
      ccdamps = getval(image,'CCDAMPS',0)
      ccdamps = str(ccdamps)
      if ccdamps == "1" or ccdamps == "2" and image[0] == "H":
        ccdamps = ccdamps
        break
      elif ccdamps == "1" or ccdamps == "4" and image[0] == "R":
        ccdamps = ccdamps
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed number of CCD read-out'
        print 'amplifiers (e.g. 1/4 for the red CCD and 1/2 for'
        print 'the blue CCD). Please try again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the CCDAMPS keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (ccdamps)



def rospeed(image):
# Check for ROSPEED keyword and appropriate number of read-out ports:
  while True:
    try:
      rospeed = getval(image,'ROSPEED',0)
      rospeed = str(rospeed)
      if rospeed == "1000000.000000" or rospeed == "400000.000000":
        rospeed = rospeed[:-10]
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed CCD read-out speed'
        print '(e.g. 1000000kHz or 400000kHz). Please try again:  '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the ROSPEED keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input()
  return (rospeed)



def ccdsum(image):
# Check for CCDSUM keyword and appropriate number of read-out ports:
  while True:
    try:
      ccdsum = getval(image,'CCDSUM',0)
      ccdsum = str(ccdsum)
      if ccdsum == "1 1" or ccdsum == "2 2" or ccdsum == "3 1" or ccdsum == "3 3":
        ccdsum = ccdsum.replace(' ','x')
        break
      else:
        print ' '
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'ERROR: File ' + image
        print 'does not contain an allowed CCD binning format'
        print '(e.g. 1 1, 2 2, 3 1 or 3 3). Please try again:'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print ' '
        image = raw_input()
    except:
      print ' '
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print 'ERROR: File ' + image
      print 'does not contain the CCDSUM keyword. Please try'
      print 'again:'
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print ' '
      image = raw_input() 
  return (ccdsum)
