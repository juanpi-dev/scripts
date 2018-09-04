import platform
import json
import sys

print_default = True
print_cpu = False
print_memory = False
print_platform = False
print_load = False
print_uptime = False
print_all = False

# platform object, only for further declarations
platform_object = {
    'node': '',
    'distribution': '',
    'architecture': '',
    'machine': '',
    'system': '',
}

proc_info = {}

if '--all' in sys.argv or '-a' in sys.argv:
    print_all = True
    print_default = False
    proc_info = {
        'platform': platform_object,
        'processors': {},
        'loadavg': [],
        'memory': {},
        'uptime': 0,
    }
else:
    if '--cpu' in sys.argv or '-c' in sys.argv:
        print_cpu = True
        print_default = False
        proc_info['processors'] = {}

    if '--memory' in sys.argv or '-m' in sys.argv:
        print_memory = True
        print_default = False
        proc_info['memory'] = {}

    if '--platform' in sys.argv or '-s' in sys.argv:
        print_platform = True
        print_default = False
        proc_info['platform'] = platform_object

    if '--load' in sys.argv or '-l' in sys.argv:
        print_load = True
        print_default = False
        proc_info['loadavg'] = []

    if '--uptime' in sys.argv or '-u' in sys.argv:
        print_uptime = True
        print_default = False
        proc_info['uptime'] = 0

# default output info, if none of the options were passed
if print_default:
    proc_info = {
        'platform': platform_object,
        'loadavg': [],
        'memory': {},
        'uptime': 0,
    }

indent = None
if '--prettyprint' in sys.argv or '-p' in sys.argv:
    indent = 2

# processor
if print_all or print_cpu:
    with open("/proc/cpuinfo", "r") as f:
        info = f.readlines()

    cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    for index, item in enumerate(cpuinfo):
        proc_info['processors'][int(index)] = item.strip()


# node, architecture, machine, system, distribution
if print_all or print_default or print_platform:
    dist = platform.dist()
    dist = " ".join(x for x in dist)
    proc_info['platform']['distribution'] = dist.strip()
    proc_info['platform']['node'] = platform.node()
    proc_info['platform']['architecture'] = platform.architecture()[0]
    proc_info['platform']['machine'] = platform.machine()
    proc_info['platform']['system'] = platform.system()

# Load
if print_all or print_default or print_load:
    with open("/proc/loadavg", "r") as f:
        loadavg = f.read().strip()

    proc_info['loadavg'] = loadavg.split()
    proc_info['loadavg'][0] = float(proc_info['loadavg'][0])
    proc_info['loadavg'][1] = float(proc_info['loadavg'][1])
    proc_info['loadavg'][2] = float(proc_info['loadavg'][2])

# Memory
if print_all or print_default or print_memory:
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()

    proc_info['memory'] = {}
    proc_info['memory'][lines[0].split()[0]] = int(lines[0].split()[1])
    proc_info['memory'][lines[1].split()[0]] = int(lines[1].split()[1])
    proc_info['memory'][lines[2].split()[0]] = int(lines[2].split()[1])
    proc_info['memory'][lines[3].split()[0]] = int(lines[3].split()[1])
    proc_info['memory'][lines[4].split()[0]] = int(lines[4].split()[1])
    proc_info['memory'][lines[5].split()[0]] = int(lines[5].split()[1])
    proc_info['memory'][lines[6].split()[0]] = int(lines[6].split()[1])
    proc_info['memory'][lines[7].split()[0]] = int(lines[7].split()[1])
    proc_info['memory'][lines[14].split()[0]] = int(lines[14].split()[1])
    proc_info['memory'][lines[15].split()[0]] = int(lines[15].split()[1])

# uptime
if print_all or print_default or print_uptime:
    with open("/proc/uptime", "r") as f:
        proc_info['uptime'] = float(f.read().split(" ")[0].strip())

print(json.dumps(proc_info, ensure_ascii=False, indent=indent))
