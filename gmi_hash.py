

CRED    = u'\33[31m'
CGREEN  = u'\33[32m'
CYELLOW = u'\33[33m'
CBLUE   = u'\33[34m'

CEND = u'\033[0m'

UCHECK = CGREEN + u"v" + CEND
UCROSS = CRED + u"x" + CEND
URING = CYELLOW + u"o" + CEND

def _gethashoffile(file_name):
	import hashlib
	try:
		with open(file_name, 'r') as file_to_check:
			# read contents of the file
			data = file_to_check.read()
			# pipe contents of the file through
			md5_stage = hashlib.md5(data.encode('utf-8')).hexdigest()
	except:
		return -2

	return md5_stage


def _gethashofdirs(directory, verbose=0):
  import hashlib, os
  SHAhash = hashlib.md5()
  if not os.path.exists (directory):
    return -1

  try:
    for root, dirs, files in os.walk(directory):
      i = 0
      i_step = 150
      for names in files:
        if i == 0:
          print(u'2. [\] Effect of each tesseroid', end='\r', flush=True)
        elif i == i_step:
          print(u'2. [|] Effect of each tesseroid', end='\r', flush=True)
        elif i == i_step*2:
          print(u'2. [/] Effect of each tesseroid', end='\r', flush=True)
        elif i == i_step*3:
          print(u'2. [-] Effect of each tesseroid', end='\r', flush=True)
        elif i == i_step*4:
          print(u'2. [\] Effect of each tesseroid', end='\r', flush=True)
          i = -1
        else:
          pass

        if verbose == 1:
          print ('Hashing' + names)
        filepath = os.path.join(root,names)
        try:
          f1 = open(filepath, 'r')
        except:
          # You can't open the file for some reason
          f1.close()
          continue

        buf = f1.read()
        md5_stage = hashlib.md5(buf.encode('utf-8')).hexdigest()
        SHAhash.update(md5_stage.encode('utf-8'))
        f1.close()
        i += 1

  except:
    import traceback
    # Print the stack traceback
    traceback.print_exc()
    return -2

  return SHAhash.hexdigest()

def read_dict(dictname, runcheck=True):


    import gmi_misc
    import gmi_config

    gmi_config.read_config()

    import numpy as np

    stages = [0, 0, 0]
    try:
        read_dictionary = np.load(dictname,allow_pickle='TRUE').item()
    except:
        gmi_misc.warning("NO SCRIPTS WERE EXECUTED!")
        return stages, None

    import hashlib

    gmi_misc.info("Reading checksum file: "+ dictname)


    #STAGE 1 CHECKSUMS **************************************
    if runcheck:
        print(u'1. [ ] Tesseroid model', end='\r', flush=True)
    if (len(read_dictionary['stage1']) != 0):
        if runcheck:
            md5_stage = _gethashoffile('model.magtess')
            if md5_stage != read_dictionary['stage1']:
                print(u'1. [' + URING + u'] Tesseroid model: checksum in dictionary does not match the one of ' + CBLUE + 'model.magtess' + CEND)
                stages[0] = -1
            else:
                print(u'1. [' + UCHECK + u'] Tesseroid model: correct checksum')
                stages[0] = 1
        else:
            stages[0] = 1
    else:
        if runcheck:
            print(u'1. [' + UCROSS + u'] Tesseroid model: no checksum ')
        stages[0] = 0

    #STAGE 2 CHECKSUMS **************************************
    if runcheck:
        print(u'2. [ ] Effect of each tesseroid', end='\r', flush=True)
    if (len(read_dictionary['stage2']) != 0):
        if runcheck:
            md5_stage = _gethashofdirs('model', verbose=0)
            if md5_stage != read_dictionary['stage2']:
                print(u'2. [' + URING + u'] Effect of each tesseroid: checksum in dictionary does not match the one of the folder ' + CBLUE + 'model' + CEND)
                stages[1] = -1
            else:
                print(u'2. [' + UCHECK + u'] Effect of each tesseroid: correct checksum')
                stages[1] = 1
        else:
            stages[1] = 1

    else:
        if runcheck:
            print(u'2. [' + UCROSS + u'] Effect of each tesseroid: no checksum ')
        stages[1] = 0

    if runcheck:
        print(u'3. [ ] Design matrix', end='\r', flush=True)
    if (len(read_dictionary['stage3']) != 0):
        if runcheck:
            SHAhash = hashlib.md5()

            try:
                f1 = open('design_matrix_shcoeff.npy', 'rb')

                i = 0
                i_step = 6500
                while 1:
                    if i == 0:
                            print(u'3. [\] Design matrix', end='\r', flush=True)
                    elif i == i_step:
                            print(u'3. [|] Design matrix', end='\r', flush=True)
                    elif i == i_step*2:
                            print(u'3. [/] Design matrix', end='\r', flush=True)
                    elif i == i_step*3:
                            print(u'3. [-] Design matrix', end='\r', flush=True)
                    elif i == i_step*4:
                            print(u'3. [\] Design matrix', end='\r', flush=True)
                            i = -1
                    else:
                            pass

                    buf = f1.read(4096)
                    if not buf : break
                    SHAhash.update(hashlib.md5(buf).hexdigest().encode('utf-8'))

                    i += 1

                f1.close()

                i = 0
                f2 = open('design_matrix_ufilt_shcoeff.npy', 'rb')
                while 1:
                    if i == 0:
                            print(u'3. [\] Design matrix', end='\r', flush=True)
                    elif i == i_step:
                            print(u'3. [|] Design matrix', end='\r', flush=True)
                    elif i == i_step*2:
                            print(u'3. [/] Design matrix', end='\r', flush=True)
                    elif i == i_step*3:
                            print(u'3. [-] Design matrix', end='\r', flush=True)
                    elif i == i_step*4:
                            print(u'3. [\] Design matrix', end='\r', flush=True)
                            i = -1
                    else:
                            pass

                    buf = f2.read(4096)
                    if not buf : break
                    SHAhash.update(hashlib.md5(buf).hexdigest().encode('utf-8'))

                    i += 1


                f2.close()

                md5_stage = SHAhash.hexdigest()

            except:
                md5_stage = 'abc'


            if md5_stage != read_dictionary['stage3']:
                print(u'3. [' + URING + u'] Design matrix: checksum in dictionary does not match the one of the folder ' + CBLUE + 'model' + CEND)
                stages[2] = -1
            else:
                print(u'3. [' + UCHECK + u'] Design matrix: correct checksum ')
                stages[2] = 1

        else:
            stages[2] = 1
    else:
        if runcheck:
            print(u'3. [' + UCROSS + u'] Design matrix: no checksum ')
        stages[2] = 0

    return stages, read_dictionary


def write_stage1():
	import hashlib
	file_name = 'model.magtess'
	with open(file_name, 'r') as file_to_check:
		# read contents of the file
		data = file_to_check.read()
		# pipe contents of the file through
		md5_returned = hashlib.md5(data.encode('utf-8')).hexdigest()

	#Save
	dictionary = {'stage1':md5_returned,
		'stage2':'',
		'stage3':'',
		'stage4':'',
	}
	np.save('checksums.npy', dictionary)
