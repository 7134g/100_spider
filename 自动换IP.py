#!/usr/bin/env python
#-*- encoding:gb2312 -*-
# Filename: IP.py
import sitecustomize
import _winreg
import ConfigParser
from ctypes import *
print '���ڽ���������������⣬���Ժ�'
print
netCfgInstanceID = None
hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, \
r'System\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}')
keyInfo = _winreg.QueryInfoKey(hkey)
# Ѱ��������Ӧ������������ netCfgInstanceID
for index in range(keyInfo[0]):
hSubKeyName = _winreg.EnumKey(hkey, index)
hSubKey = _winreg.OpenKey(hkey, hSubKeyName)
try:
hNdiInfKey = _winreg.OpenKey(hSubKey, r'Ndi\Interfaces')
lowerRange = _winreg.QueryValueEx(hNdiInfKey, 'LowerRange')
# ����Ƿ�����̫��
if lowerRange[0] == 'ethernet':
driverDesc = _winreg.QueryValueEx(hSubKey, 'DriverDesc')[0]
print '��⵽��������������', driverDesc
netCfgInstanceID = _winreg.QueryValueEx(hSubKey, 'NetCfgInstanceID')[0]
print '��⵽����������ID��', netCfgInstanceID
if netCfgInstanceID == None:
print 'û���ҵ������������������˳�'
exit()
break
_winreg.CloseKey(hNdiInfKey)
except WindowsError:
print r'Message: No Ndi\Interfaces Key'
# ѭ��������Ŀǰֻ�ṩ�޸�һ������IP�Ĺ���
_winreg.CloseKey(hSubKey)
_winreg.CloseKey(hkey)
# ͨ���޸�ע�������IP
strKeyName = 'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\' + netCfgInstanceID
print '������������ע����ַ�ǣ�\n', strKeyName
hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, \
strKeyName, \
0, \
_winreg.KEY_WRITE)
config = ConfigParser.ConfigParser()
print
print '���ڴ�IP.ini�����ļ���'
config.readfp(open('IP.ini'))
IPAddress = config.get("school","IPAddress")
SubnetMask = config.get("school","SubnetMask")
GateWay = config.get("school","GateWay")
DNSServer1 = config.get("school","DNSServer1")
DNSServer2 = config.get("school","DNSServer2")
DNSServer = [DNSServer1,DNSServer2]
print '�����ļ����趨����Ϣ���£���˶ԣ�'
print
print 'IP��ַ��', IPAddress
print '�ӹ����룺', SubnetMask
print 'Ĭ�����أ�', GateWay
print '��DNS��������', DNSServer1
print '��DNS��������', DNSServer2
print
res = raw_input('���ڣ���������������1���������ļ�д��ϵͳ������2�������е�ϵͳ�趨��ԭΪȫ���Զ���ȡ����������˳���')
if str(res) == '1':
try:
_winreg.SetValueEx(hkey, 'EnableDHCP', None, _winreg.REG_DWORD, 0x00000000)
_winreg.SetValueEx(hkey, 'IPAddress', None, _winreg.REG_MULTI_SZ, [IPAddress])
_winreg.SetValueEx(hkey, 'SubnetMask', None, _winreg.REG_MULTI_SZ, [SubnetMask])
_winreg.SetValueEx(hkey, 'DefaultGateway', None, _winreg.REG_MULTI_SZ, [GateWay])
_winreg.SetValueEx(hkey, 'NameServer', None, _winreg.REG_SZ, ','.join(DNSServer))
except WindowsError:
print 'Set IP Error'
exit()
_winreg.CloseKey(hkey)
print '�л��ɹ�����������󼴿���Ч'
elif str(res) == '2':
try:
_winreg.SetValueEx(hkey, 'EnableDHCP', None, _winreg.REG_DWORD, 0x00000001)
_winreg.SetValueEx(hkey, 'T1', None, _winreg.REG_DWORD, 0x00000000)
_winreg.SetValueEx(hkey, 'T2', None, _winreg.REG_DWORD, 0x00000000)
_winreg.SetValueEx(hkey, 'NameServer', None, _winreg.REG_SZ, None)
_winreg.SetValueEx(hkey, 'DhcpConnForceBroadcastFlag', None, _winreg.REG_DWORD, 0x00000000)
_winreg.SetValueEx(hkey, 'Lease', None, _winreg.REG_DWORD, 0x00000000)
_winreg.SetValueEx(hkey, 'LeaseObtainedTime', None, _winreg.REG_DWORD, 0x00000000)
_winreg.SetValueEx(hkey, 'LeaseTerminatesTime', None, _winreg.REG_DWORD, 0x00000000)
except WindowsError:
print 'Set IP Error'
exit()
_winreg.CloseKey(hkey)
print '�л��ɹ�����������󼴿���Ч'
else:
print '�û��ֶ�ȡ���������˳�'
exit('')
