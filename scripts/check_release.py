"""离线检查发布树：文件、协议文档链接、固件哈希和明显本机/凭据痕迹。"""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','build','out','dist','.venv','venv','__pycache__','.pytest_cache'}
REQUIRED=['README.md','LICENSE','NOTICE','THIRD_PARTY_NOTICES.md','CONTRIBUTING.md','CHANGELOG.md','AGENTS.md','CMakeLists.txt','CMakePresets.json','.gitignore','.gitattributes','.github/workflows/ci.yml','Core/Src/main.c','RobotArm/App/app_runtime.c','docs/architecture.md','docs/serial-protocol.md','docs/build-and-test.md','docs/hardware.md','docs/control.md','docs/validation.md','docs/validation-summary.json','firmware/ProductionRelease.hex','firmware/ProductionRelease.bin','firmware/VisionStationRelease.hex','firmware/VisionStationRelease.bin','firmware/SHA256SUMS','Drivers/CMSIS/LICENSE.txt','Drivers/STM32F4xx_HAL_Driver/LICENSE.txt','Drivers/CMSIS/Device/ST/STM32F4xx/LICENSE.txt']
def main():
 errors=[]
 for n in REQUIRED:
  if not (ROOT/n).is_file():errors.append('missing: '+n)
 files=[p for p in ROOT.rglob('*') if p.is_file() and not EXCLUDED.intersection(p.relative_to(ROOT).parts)]
 for p in files:
  rel=p.relative_to(ROOT).as_posix()
  if p.suffix in {'.claim','.zip','.log','.elf'} or p.name in {'before_flash.bin','after_flash.bin','before_ram.bin','authorization.json'}:errors.append('local artifact: '+rel)
  if p.stat().st_size>10*1024*1024:errors.append('large file: '+rel)
  if p.suffix.lower() in {'.md','.py','.ps1','.json','.yml','.yaml','.cmake','.txt','.cfg','.ioc'} or p.name in {'CMakeLists.txt','AGENTS.md'}:
   text=p.read_text(encoding='utf-8-sig',errors='replace')
   if re.search(r'\b[A-Za-z]:[\\/]',text):errors.append('absolute Windows path: '+rel)
   if re.search(r'(?:/Users/|/home/)[A-Za-z0-9_.-]+/',text):errors.append('personal Unix path: '+rel)
   # Common actual credential formats; not a guarantee that arbitrary secrets are absent.
   if re.search(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',text):errors.append('credential-like data: '+rel)
  if p.suffix=='.md':
   text=p.read_text(encoding='utf-8')
   for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
    target=href.strip('<>').split('#',1)[0]
    if not target or re.match(r'^[a-z]+://',target):continue
    if not (p.parent/target).is_file():errors.append('broken link: '+rel+' -> '+target)
 sums=ROOT/'firmware/SHA256SUMS'
 if sums.is_file():
  for line in sums.read_text().splitlines():
   expected,name=line.split(None,1);path=ROOT/'firmware'/name.strip()
   if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:errors.append('firmware hash mismatch: '+name)
 result={'files_checked':len(files),'errors':errors,'pass':not errors,'hardware_access':False,'scan_scope':'selected obvious paths and credential patterns; no complete secret-detection guarantee'}
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
