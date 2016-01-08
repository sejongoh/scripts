#
# copy recursively all testResult.xml files to target_path with the same directory structure
# Notes:
# 
#  ~/git/corefx/bin/tests/Linux.AnyCPU.Release/System.Xml.XPath.Tests/dnxcore50
#

import os
import shutil

corefx_path = os.path.normpath(os.sys.argv[1])
test_conf = os.sys.argv[2]
target_base_path = os.path.expanduser(os.path.join('C:/Workspaces/rc2_result', test_conf))
print ("COREFX_PATH:", corefx_path)
print ("TEST_CONF:", test_conf)
print ("TARGET_BASE_PATH:", target_base_path)


test_rel_path = 'bin/tests/Windows_NT.AnyCPU.Release'

source_base_path = os.path.join(corefx_path, test_rel_path)
print ("COREFX_TEST_BASE_PATH:", source_base_path)

dir_list = os.listdir(source_base_path)

for dir in dir_list:
	full_dir_path = os.path.join(os.path.join(source_base_path, os.path.join(dir)),'dnxcore50')
	#print (full_dir_path)
	full_result_file_path = os.path.join(full_dir_path, 'testResults.xml')
	#print (full_result_file_path)
	if os.path.exists(full_result_file_path) == False :
		print ("Warning: cannot find", full_result_file_path)
		continue
		
	target_dir_path = os.path.join(target_base_path, dir)
	#print ("Copying", full_result_file_path, "to", target_dir_path)
	
	if not os.path.exists(target_dir_path):
		os.makedirs(target_dir_path)	
		
	shutil.copy(full_result_file_path, target_dir_path)
	
	
	
    