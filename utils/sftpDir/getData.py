#!/usr/bin/python
# coding:utf-8

import uuid, platform, os ,psutil

class GetData:
    def __init__(self):
        self.result = {}
        self.sys = os.name

    def get_hostname(self):
        hostname = platform.node()
        return hostname

    def get_sys_version(self):
        sys_version = ''
        with open('/etc/issue') as fd:
            for line in fd:
                sys_version = line.strip()
                break
        return sys_version

    def get_sys_type(self):
        sys_type = platform.system()
        return sys_type

    def get_mac(self):
        uid = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ":".join([uid[e:e + 2] for e in range(0, 11, 2)])
        return mac

    def get_cpu(self):
        num = 0
        cpu_model = ''
        with open('/proc/cpuinfo') as fd:
            for line in fd:
                if line.startswith('processor'):
                    num += 1
                if line.startswith('model name'):
                    cpu_model = line.split(':')[1].strip().split()
                    cpu_model = cpu_model[0] + ' ' + cpu_model[2]  + ' ' + cpu_model[-1]
        cpu =  cpu_model + ' ' + str(num) + '核'
        return cpu

    def get_memory(self):
        mem = 0
        with open('/proc/meminfo') as fd:
            for line in fd:
                if line.startswith('MemTotal'):
                    mem = int(line.split()[1].strip())
                    break
        mem = '%.f' % (mem / 1024.0) + ' MB'
        return mem

    def get_disk(self):
        disk = psutil.disk_usage('/').total/1024/1024/1024
        disk = str(disk).split('.')[0] + 'G'
        return disk

    def getData(self):
        data_method = GetData.__dict__
        for key,value in data_method.items():
            if 'get_' in key and callable(value):
                self.result[key.split('_',1)[-1]] = value(self)
        return self.result

if __name__ == "__main__":
    mydata = GetData()
    res = mydata.getData()
    print(res)
