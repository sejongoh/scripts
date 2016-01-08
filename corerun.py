import os
import subprocess
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('--verbose', action='store_true', help='Verbose dump')
parser.add_argument('--release', action='store_true', help='Run the release binary')
parser.add_argument('--ws', metavar='N', type=int, default='0', help='Workspace number')
parser.add_argument('--bty', metavar='BUILD_TYPE', default='Debug', help='Build type, Debug or Relase')
parser.add_argument('--dump', metavar='DUMP_FUNC_NAME', default='', help='A function name where COMPlus_JitDump=FUNC_NAME')
parser.add_argument('prog_and_args', nargs=argparse.REMAINDER)
args = parser.parse_args()


#
# Pick up a corerun binary
#
workspace = ''
if args.ws >= 0:
	workspace = 'ws' + str(args.ws)
else:
	workspace = 'origin'
	
coreclr_base_path='C:/Workspaces/' + workspace + '/coreclr'

os_name = ['Windows_NT', 'Linux']
build_types = ['Debug', 'Release', 'Checked']
target_cpu = ['x64']

build_type_idx = -1
if (args.bty.lower() == "debug") :
	build_type_idx = 0
elif (args.bty.lower() == "release") :
	build_type_idx = 1
elif (args.bty.lower() == "checked") :
	build_type_idx = 2
else :
	print ("Invalid build type:" + args.bty)

target_bin = os_name[0] + '.' + target_cpu[0] + '.' + build_types[build_type_idx]
coreclr_bin_rel_path = os.path.join('bin/Product/', target_bin)
coreclr_bin_rel_path = os.path.join(coreclr_bin_rel_path, 'CoreRun.exe')
coreclr_path = os.path.join(coreclr_base_path, coreclr_bin_rel_path)
# Final path pointing to corerun.exe
coreclr_path = os.path.normpath(coreclr_path)

#
# Set optional environment variables
#

env_dic = os.environ
env_dic['COMPlus_JitDump'] = args.dump

print (env_dic['COMPlus_JitDump'])
#
# Execute corerun.exe
#
process_args = [coreclr_path] + args.prog_and_args
print (process_args)


process = subprocess.Popen(process_args, stderr=subprocess.STDOUT)
stdout_str, stderr_str = process.communicate()
sys.stdout.flush()
#print ("Process return code", process.returncode)
#print (stdout_str)
