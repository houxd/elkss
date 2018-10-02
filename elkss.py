#!/usr/bin/python
#elipse-linux-kernel-source-scan

import os
from lxml import etree 

def list_dir_entrys(path):
    dirs,files=[],[]
    for e in os.listdir(path):
        if e=='.' or e=='..':
            continue
        pe = os.path.join(path,e)
        if os.path.isdir(pe):
            dirs.append(pe)
        elif os.path.isfile(pe):
            files.append(pe)
    return dirs,files
    
def walk(path):    
    dirs,files = list_dir_entrys(path)
    is_empty = True
    emptys = []
    for f in files:
        name,ext = os.path.splitext(f)
        if ext=='.c' or ext=='.S' or ext=='.s':
            if files.__contains__(name+'.o'):
                is_empty = False
            else:
                emptys.append(f[2:])
    for d in dirs:
        _is_empty,_emptys=walk(d)
        if _is_empty:
            emptys.append(d[2:])
        else:
            is_empty = False
            emptys += _emptys
    return is_empty,emptys

excluding = ''
is_empty,emptys=walk('.')
for i in emptys:
    print(i)
    excluding += i + '|'
excluding = excluding[:-1]

xp = '/cproject/storageModule[@moduleId="org.eclipse.cdt.core.settings"]\
/cconfiguration/storageModule[@moduleId="cdtBuildSystem"]/configuration'
#/sourceEntries/entry'

parser = etree.XMLParser(encoding="utf-8", strip_cdata=False, remove_blank_text=True)
cproject = etree.parse('.cproject',parser)
configuration_s = cproject.xpath(xp)
if len(configuration_s)>1:
    print('More then one configuration be found.')
    exit(-1)
sourceEntries_s = configuration_s[0].xpath('sourceEntries')
if len(sourceEntries_s)==0:
    sourceEntries = etree.SubElement(configuration_s[0], 'sourceEntries')
else:
    sourceEntries = sourceEntries_s[0]    
sourceEntries.clear()
entry = etree.SubElement(sourceEntries, 'entry')
entry.set('excluding',excluding)
entry.set('flags','VALUE_WORKSPACE_PATH|RESOLVED')
entry.set('kind','sourcePath')
entry.set('name','')
cproject.write('.cproject',pretty_print=True)

print('done.')
exit(0)
