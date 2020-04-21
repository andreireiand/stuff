# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os, sys, fcntl, time, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--bootstrapFile", default='bootstrap.xml')
parser.add_argument("--mxIP1", default='127.0.0.1')
parser.add_argument("--mxIP2", default='127.0.0.1')


def RemoveAdminIPs(lines):
    newLines = []
    for line in lines:
        if "admin-ip" not in line.strip().lower():
            newLines.append(line)
    return newLines

def  AddAdminIPs(f, IP1, IP2):
    f.write("<admin-ips>\n")
    f.write(' <admin-ip ip=\"' + IP1 + '\"/>\n')
    f.write(' <admin-ip ip=\"' + IP2 + '\"/>\n')        
    f.write("</admin-ips>\n")        
    
def IsEmpty(line):
    return line.strip() != ''

try:
    args = parser.parse_args()
    
    if args.bootstrapFile and args.mxIP1 and args.mxIP2:
        print("fixing bootstrapfile ... ")
        
        f = open(args.bootstrapFile, "r+")
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        
        lines = list(filter(IsEmpty,f.readlines()))
        assert("</bootstrap>" in lines[-1].strip().lower()) # file must be properly formatted upon opening
        lines = RemoveAdminIPs(lines)        
        f.seek(0)
        f.writelines(lines[:-1])
        
        AddAdminIPs(f, args.mxIP1, args.mxIP2)
        
        f.write(lines[-1])
            
        f.truncate()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        f.close()
        print("file changed successfully ... ")
        
    else:
        raise ValueError("Not all args provided for Mx ActionSet and Action!")
        
except NameError:
    f.write(lines[-1])
    print("Unexpected NameError:", sys.exc_info()[0])
except:
    print("Unexpected error:", sys.exc_info()[0])
    
finally:
    if not f.closed:
        f.truncate()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        f.close()        

