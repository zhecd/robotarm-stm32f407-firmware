"""Reproduce offline checks from any workspace location; never connect a device."""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--firmware',action='store_true',help='also build/audit all seven Arm profiles');a=p.parse_args()
 cmake=shutil.which('cmake');ctest=shutil.which('ctest')
 if not cmake or not ctest:p.error('cmake and ctest must be on PATH')
 out=ROOT/'build/validation';out.mkdir(parents=True,exist_ok=True);records=[];native={}
 def run(name,args):
  with (out/(name+'.log')).open('w',encoding='utf-8') as f:
   proc=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
  records.append({'check':name,'exit_code':proc.returncode})
  print(name,proc.returncode,flush=True)
  if proc.returncode:
   print((out/(name+'.log')).read_text(encoding='utf-8',errors='replace')[-6000:]);raise RuntimeError(name+' failed')
 try:
  for name,preset in [('Debug','HostTests'),('Release','HostTestsRelease')]:
   run(name+'_configure',[cmake,'--preset',preset,'-DPython3_EXECUTABLE='+sys.executable])
   run(name+'_build',[cmake,'--build','--preset',preset,'--parallel','8'])
   junit=out/(name+'.xml');run(name+'_tests',[ctest,'--test-dir',str(ROOT/'build'/preset),'-j8','--output-on-failure','--output-junit',str(junit)])
   xml=ET.parse(junit).getroot();assert int(xml.attrib.get('failures','0'))==0 and int(xml.attrib.get('errors','0'))==0
   native[name]=int(xml.attrib['tests'])
  run('architecture',[sys.executable,'-B','scripts/check_architecture_dependencies.py'])
  if a.firmware:
   for tool in ['gcc','nm','objdump','objcopy']:
    if not shutil.which('arm-none-eabi-'+tool):raise RuntimeError('arm-none-eabi-'+tool+' missing from PATH')
   for name,preset,compiled,hold in [('ProductionLocked','ProductionLocked',0,0),('ProductionTrial','ProductionTrial',1,0),('ProductionHoldLocked','ProductionHoldLocked',0,10000),('ProductionHoldTrial','ProductionHoldTrial',1,10000),('ProductionDebug','ProductionDebug',None,0),('ProductionRelease','ProductionRelease',None,0),('ProductionLockedRelease','ProductionLocked',0,0)]:
    cmd=[cmake,'--preset',preset,'-B',str(ROOT/'build'/name)]
    if name=='ProductionLockedRelease':cmd+=['-DCMAKE_BUILD_TYPE=Release']
    run(name+'_configure',cmd);run(name+'_build',[cmake,'--build',str(ROOT/'build'/name),'--parallel','8'])
    cmd=[sys.executable,'-B','scripts/audit_firmware.py','--name',name,'--build-dir',str(ROOT/'build'/name),'--output',str(out/'firmware'),'--hold-ms',str(hold),'--home-period-ms','1']
    if compiled is not None:cmd+=['--compiled',str(compiled)]
    run(name+'_audit',cmd)
  run('release_tree',[sys.executable,'-B','scripts/check_release.py'])
 finally:
  (out/'results.json').write_text(json.dumps({'checks':records,'native_tests':native,'hardware_access':False},indent=2)+'\n',encoding='utf-8')
 print('Offline validation complete; details in build/validation/results.json')
 return 0
if __name__=='__main__':sys.exit(main())
