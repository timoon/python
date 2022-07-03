#!/usr/bin/python

# file comparision utility
# for byte-wise file comparision between source and destination directory
#
# version history
# 0.1	first try, does what it is supposed to do but no error handling nor info and help messages
#
# 0.2	added exception handling
#	added the standard info and help messages
#	added summary of checked, ok, and nonok files
#
# 0.3	converted to python 3 compatibility (print with indents / brackets)
#
#	TODO recursive file searching in destination directory
#	BUG checking files with more then one extension / dot in filename, it is checking both which are not the same files and there is error (this does not happen in v0.1

import filecmp,os,sys,errno,traceback,glob,time

count_ok=0

def file_compare(f):
  dir2 = sys.argv[1]
  print ("\nComparing subdir \'"+f+"\'")

  dir1_contents = [ f.name for f in os.scandir('./'+f) if f.is_dir() ]
  if len(dir1_contents)>0: foldercheck(f)

#  time.sleep(1)

  # Determine the items that exist in both directories
  #dir1_contents = set(os.listdir('.'))
  #print (dir2)
  dir1_contents=[]
  dir2_contents=[]
  dir1_contents = [ f.name for f in os.scandir('./'+f) if f.is_file() ]
  dir2_contents = [ f.name for f in os.scandir(dir2+''+f) if f.is_file() ]
#  print
#        print (files)
#        time.sleep(1)
  dir1_contents=set(dir1_contents)
  dir2_contents=set(dir2_contents)

  print (len(dir1_contents))
  print (len(dir2_contents))
#  time.sleep(5)

#for arg in dir2:
# try:
#  dir2_contents2 = filter(os.path.isfile, os.listdir(dir2))
#dir2_contents = set(os.listdir(dir2))
# except OSError as e:
#  print (e)
#  print (e.errno)
#  print (e.filename)
#  print (e.strerror,"-- '"+e.filename+"'")
#  sys.exit(2)
# except:
#  print "jo"
#  print (sys.exc_info()[2])
#  sys.exit(2)

# check for files not in destination (dir2) and, if any, print them out
  list1=[]
  list2=[]
  list3=''
  i=0
#for f in dir1_contents:
#  if not(f in dir2_contents):
#    print (f)
#    list2 = list2 +'\n'+ f
#    i=i+1
#	list1[i] = f
#	print i
  dirlist= glob.glob(dir2+f+'/**/*') #, recursive=True)
#  print (dirlist)
#  time.sleep(1)
  dirlist1= glob.glob('.'+'/**/*', recursive=True)

#for f in dirlist1:
#  print (f)

  for a in dir1_contents:
#  print (f)
    if not a in str(dir2_contents):
      list2.append(a)
      i=i+1
#for f in dir2_contents:
#  print(f)
#print ("\n\nw/o:")
#for f in dir2_contents:
#  print(f)

  if i>0:
    print ('\nWARNING: These',i,'files are not in destination:')
    print('\n'.join(sorted(list2)))
# if any, print all files that are not in destination

# determine common files and folders in both directories
  common = dir1_contents.intersection(dir2_contents)
#common = dir1_contents.intersection(dir2_contents)
#common = list(dir1_contents & dir2_contents)
#print (dir1_contents, 'and\n',dir2_contents,"\n")

#print os.path.join('.','tim')

  common_files = [ f 
    for f in common
#        print f
    if os.path.isfile(os.path.join('.', f))
]
#print (common)
#print (common_files)

  count_all=0
  count_ok=0
  count_error=0

# Compare the directories
#match, mismatch, errors = filecmp.cmpfiles(dir1,dir2,common_files,shallow=False)

# File Comparision
  print ('\nStart comparision of',len(dir1_contents)-i,'files:')
#  time.sleep(1)
  for a in dir1_contents:
#    print ("jo:"+f)
#  if os.path.isdir(f): continue
#  if not searchpattern in str.lower(f): continue
#  count_all=count_all+1
    res = [k for k in dir2_contents if a in k]
#  filter(lambda x: f in x, dirlist)
    n=0
    for i in res:
#      print (i)
      n=n+1
      if(len(f)>0): src='.'+f+'/'+a
      else: src=''+f+''+a
      dest=dir2+f+'/'+i
      print (src,":\t",n,"th:",dest,":",end="")
#      start_time = time.clock()
      if filecmp.cmp(src,dest,shallow=False):
        print ('\t\033[92mok\033[0m')
        count_ok=count_ok+1
      else:
        print ('\t\033[91merror\033[0m')
        count_error=count_error+1
#      print(time.clock() - start_time)

  print ("\nfinished comparing",count_all,"files,",count_ok,"file(s) were ok and",count_error,"file(s) were not ok.\n")

  print , "seconds"

def main():
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

  print ('\033[1mStarting to compare:\033[0m')

# if no parameter given
  if len(sys.argv) == 1:
    print ("Usage: "+sys.argv[0]+" [OPTION]... PATTERN [FILE]...\nTry '"+sys.argv[0]+" --help' for more information.")
    sys.exit(0)

# if parameter is --help
  if sys.argv[1] == "--help":
    print ("Usage: "+sys.argv[0]+" [OPTION]... PATTERN [FILE]...\n")
    print ("Compare files bytewise")
    sys.exit(0)

# if parameter is --file
  filelist=(sys.argv[2:-1])
#  print(sys.argv[2])
  print ()
  print(sys.argv[-1])
#  dirlist= glob.glob(sys.argv[2], recursive=True)
#  dirlist= glob.glob('202105*', recursive=True)
#  print(dirlist)
  if sys.argv[1] == "-f" or sys.argv[1] == "--file" :
#    common =
    match, mismatch, errors = filecmp.cmpfiles('.',sys.argv[-1],filelist,shallow=False)
    print (match,mismatch,errors)
#      print ('\tok')
#      count_ok=count_ok+1
#    else:
#      print ('\terror')
    sys.exit(0)

#d2 = sys.argv[2]

  if len(sys.argv)>2:
    searchpattern = str.lower(sys.argv[2])
  else:
    searchpattern = ""

  foldercheck('.')
  file_compare('/.')

def foldercheck(cur):
  if cur=='.': cur=''
  dir2 = sys.argv[1]
  dir_src_folders=[]
  dir_dest_folders=[]

  dir_src_folders= glob.glob('./'+cur+'/*/') #, recursive=True)

#  for root, dirs, files in os.walk('.'):
#    dir_src_folders+= dirs
  dir_src_folders = [ f.name for f in os.scandir('./'+cur) if f.is_dir() ]
  dir_dest_folders = [ f.name for f in os.scandir(dir2+'/'+cur) if f.is_dir() ]
#  print (":",dir_src_folders)
#  print (":",dir_dest_folders)
#  print ("glob: ",dirlist)
#  time.sleep(1)

  if(len(dir_src_folders))>0:
    print ("\nFollowing",len(dir_src_folders),"subdirs exist:")
#  for f in dir_src_folders:
#   print (f)

#  dir_dest_folders= glob.glob(dir2+'/*/') #, recursive=True)
#  print ("os.walk: ",dir_dest_folders)

#  for root, dirs, files in os.walk(dir2):
#    dir_dest_folders+= dirs

  dir_src_folders=set(dir_src_folders)
  dir_dest_folders=set(dir_dest_folders)

  common = sorted(dir_src_folders.intersection(dir_dest_folders))
  differ = sorted(dir_src_folders.difference(dir_dest_folders))
#  print (common)
  print (differ)
  time.sleep(1)

  print (len(common),"existing in dest")
  print (len(differ),"missing in dest")

  for f in common: #dir_src_folders:
    print (cur+' '+f)
    file_compare(cur+'/'+f)

if __name__ == "__main__":
  main()
