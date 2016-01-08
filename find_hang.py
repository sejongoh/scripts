import os

#num_total_finished_tests = 0
#num_total_fails = 0
stats_with_finished_test_suites = {"null" :  0}
# testname -> (started flag, success flag)
finish_check = {"null" : [0,0] }

def get_start(line_str):
	global finish_check
	start_str = "Starting:"
	begin = line.find(start_str)
	if begin == -1:
		return ""
	test_name = line[begin+len(start_str):].strip()
	#print ("Start: ", test_name)
	finish_check[test_name] = [1,0]
	return test_name
	
def get_end(line_str):
	global finish_check
	end_str = "Finished:"
	begin = line.find(end_str)
	if begin == -1:
		return ""
	test_name = line[begin+len(end_str):].strip()
	#print ("Finished: ", test_name)	
	entry = finish_check[test_name] 
	entry[0] = 0
	return test_name

def get_stat_num(line_str, stat_name):
	stat_name_len = len(stat_name)	
	begin = line_str.find(stat_name)
	begin = begin + stat_name_len
	end = line_str.find(",", begin)
	if (end == -1) :
		raise "Unexpected input syntax"
	#print ("DEBUG ", begin, " ", line_str[begin:end])
	num_tests = int(line_str[begin:end])
		
	return num_tests
	
def scan_stats_line(line_str):
	global stats
	
	total_str = "Total:" 
	begin = line.find(total_str)
	if (begin == -1) :
		return -1
	
	test_suite_name = line_str[0:begin-1].strip()
		
	stat_line = line_str[begin:]
	
	stat_names = ["Total:", "Failed:"]
	
	for stat_name in stat_names:
		test_nums = get_stat_num(stat_line, stat_name)
		if test_nums > 0 :
			if stat_name == "Failed:":
				finish_check[test_suite_name][1] = test_nums
			if stat_name in stats_with_finished_test_suites :
				stats_with_finished_test_suites[stat_name] += test_nums
			else:
				stats_with_finished_test_suites[stat_name] = test_nums
	
	return 1
	
filename = os.sys.argv[1]

print ("FileName: ", filename)

fp = open(filename)

for line in fp:
	#print ("CurrLine:", line)
	if scan_stats_line(line) != -1:
		continue
	if get_start(line) != "":
		continue
	if get_end(line) != "":
		continue		


num_finished = 0
hang_crash_or_assert_list = []
finished_but_failed_list = []
for name, data in finish_check.items():
	#print ("FinishCheck:", name, count)
	started_flag = data[0]
	fail_nums = data[1]
	if started_flag != 0:
		#print ("[HANG, CRASH, or ASSERT]:", name)
		hang_crash_or_assert_list.append(name)
	else :
		num_finished = num_finished + 1
	if fail_nums > 0:
		finished_but_failed_list.append((name, fail_nums))
		#print ("[FINISHED BUT FAILED]: ", name, " failed tests: ", fail_nums)
		#num_finished_but_failed = num_finished_but_failed + 1

print ("\n[HANG, CRASH, or ASSERT]: {0} test suites ".format(len(hang_crash_or_assert_list)))
for name in hang_crash_or_assert_list:
	print (' {0}'.format(name))

print ("\n[FINISHED BUT FAILED]: {0} test suites".format(len(finished_but_failed_list)))
for (name, fail_nums) in finished_but_failed_list:		
	print (' {0}: failed tests: {1}'.format(name, fail_nums))
		
num_finished_but_failed = len(finished_but_failed_list)		

print ("\n")
print ("=== Summary ==================================")	
print (" Started test suites: {0}".format(len(finish_check)))
print (" Finished test suites: {0}".format(num_finished))
print (" Failed (not crash) test suites: {0}".format(num_finished_but_failed))
print (" Passed test suites: {0}".format(num_finished - num_finished_but_failed))
print (" Passed/Started: {0}".format(float(num_finished - num_finished_but_failed)/len(finish_check)))
print (" Tests finished: {0}".format(stats_with_finished_test_suites["Total:"]))
print (" Tests failed: {0}".format(stats_with_finished_test_suites["Failed:"]))
print ("  --> Note that crashed or asserted tests are not included here")
print ("==============================================")	

#print ("F", finish_check['System.Xml.XPath.Tests'])
#print (finish_check)

#for e in finish_check:
#	print (e)

	
		
	