from operator import add, floordiv, mul, sub
from typing import Callable, NamedTuple

Job0 = int
Job1 = tuple[Callable[[int], int], str]
Job2 = tuple[Callable[[int, int], int], str, str]
Job = Job0 | Job1 | Job2

def parse_job(input: str) -> Job0 | Job2:
  try:
    return int(input)
  except ValueError:
    [lhs, op, rhs] = input.split()
    match op:
      case '+': op = add
      case '-': op = sub
      case '*': op = mul
      case '/': op = floordiv
      case _: raise Exception()
    return (op, lhs, rhs)

def solve1(input: str):
  monkeys: dict[str, Job] = {}
  references: dict[str, set[str]] = {}
  def try_resolve(name: str):
    def resolve_step(job: Job) -> Job:
      match job:
        case (op, lhs, rhs):
          if lhs in monkeys:
            match monkeys[lhs]:
              case int(x):
                references[lhs].remove(name)
                return (lambda y: op(x, y), rhs)
              case _: pass
          if rhs in monkeys:
            match monkeys[rhs]:
              case int(x):
                references[rhs].remove(name)
                return (lambda y: op(y, x), lhs)
              case _: pass
        case (op, operand):
          if operand in monkeys:
            match monkeys[operand]:
              case int(x):
                references[operand].remove(name)
                return op(x)
              case _: pass
        case _: pass
      return job
    monkeys[name] = resolve_step(resolve_step(monkeys[name]))
    if isinstance(monkeys[name], int):
      referers = references.get(name)
      if referers == None: return
      for referer in list(referers):
        try_resolve(referer)
  for line in input.strip().splitlines():
    [name, job] = line.split(": ")
    job = parse_job(job)
    monkeys[name] = job
    if isinstance(job, tuple):
      for referent in job[1:]:
        references.setdefault(referent, set()).add(name)
    try_resolve(name)
  return monkeys['root']

class JobRoot(NamedTuple):
  lhs: str
  rhs: str
JobHuman = tuple[()]
JobPart2 = Job | JobRoot | JobHuman

def solve2(input: str):
  monkeys: dict[str, JobPart2] = {}
  references: dict[str, set[str]] = {}
  def try_resolve(name: str):
    match monkeys[name]:
      case (op, lhs, rhs) as job:
        if 'humn' in job: return
        if lhs in monkeys and rhs in monkeys:
          match monkeys[lhs], monkeys[rhs]:
            case int(x), int(y):
              references[lhs].remove(name)
              references[rhs].remove(name)
              monkeys[name] = op(x, y)
            case _: return
        else: return
      case int(_): pass
      case _: return
    referers = references.get(name)
    if referers == None: return
    for referer in list(referers):
      try_resolve(referer)
  for line in input.strip().splitlines():
    [name, job] = line.split(": ")
    job = parse_job(job)
    match name:
      case 'root':
        assert isinstance(job, tuple)
        monkeys[name] = JobRoot(*job[1:])
        continue
      case 'humn':
        monkeys[name] = ()
        continue
      case _:
        monkeys[name] = job
        if isinstance(job, tuple):
          for referent in job[1:]:
            references.setdefault(referent, set()).add(name)
        try_resolve(name)
  root = monkeys['root']
  assert isinstance(root, JobRoot)
  eqlhs = monkeys[root.lhs]
  eqrhs = monkeys[root.rhs]
  if isinstance(eqlhs, int):
    eqlhs, eqrhs = eqrhs, eqlhs
  assert isinstance(eqrhs, int)
  while True:
    match eqlhs:
      case (op, lhs, rhs):
        lhs = monkeys[lhs]
        rhs = monkeys[rhs]
        if isinstance(lhs, int):
          eqlhs = rhs
          if op == add: eqrhs -= lhs
          elif op == sub: eqrhs = lhs - eqrhs
          elif op == mul: eqrhs //= lhs
          else: eqrhs = lhs // eqrhs
        else:
          assert isinstance(rhs, int)
          eqlhs = lhs
          if op == add: eqrhs -= rhs
          elif op == sub: eqrhs += rhs
          elif op == mul: eqrhs //= rhs
          else: eqrhs *= rhs
      case (): return eqrhs
      case _: raise Exception

def solve(input: str):
  print(solve1(input), solve2(input))

solve("""
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""")

solve("""
swbs: bwzr * swcj
dsch: rvqh + fwvg
nlbr: 2
drtz: btpb + lngc
nwff: vqlw + lsdd
zjzw: lbtj * whgf
rndt: tnjv - dtdg
hjjz: nrhq + dbss
tfng: 3
fjtw: nmvr + qmrl
dbwj: mplc + vbpc
gwgp: vljt + qnsw
djwh: 2
mlbf: tzch / cqdv
stcz: 2
gzrw: hwfp * fbrg
qjgp: 3
pgzl: 2
ltzh: ftwz + cwjt
wwnp: 4
bthj: 4
bmcq: grmh * lhbs
ltvb: gslf / pndc
rgfc: lwrs + jwsn
ljwn: 2
pqrd: tglb - rrbw
jhzr: 6
fbfd: pqrd + gfhw
ccqt: 10
vwgm: 8
jmtf: 20
pwhn: 6
wrcl: 3
qmmf: ztqj * rtsc
mwgc: ftnz + mlsj
rjvc: 2
nmzw: 2
wqgg: 4
zqzn: mhvn * jwzq
pjzp: qpfv - bdjw
cvdl: 4
rvhc: 2
tfzp: 10
nmcd: qpln + bzbq
dpjh: rjfb / pgzl
cnvf: cqln + qrbb
dgwj: ptsl + pfnm
nvwt: 1
nvqw: 2
hmld: 2
jsvm: 2
qpgb: 2
rhhm: 15
bqmg: vbcn * dwcd
btrv: ldrw + mwrh
snbz: pfrf * smqm
zrvw: zhcg * vmgw
bjdt: 2
ffdf: 6
vwrh: spvc + rwcp
rmfv: 8
hhpb: 4
jtzp: 20
hclm: 5
vwzs: mhcg + ltvb
mrdd: 4
rmwc: lqdh + vwgp
vsqj: mmwv + wcgb
bthc: 7
lmfv: 9
dhfl: 18
lchr: mdtn * vrsg
swtl: 11
jwdq: 2
mhbd: 3
hbqg: 17
hvpl: 4
vvcd: 16
tsjs: 4
fvbn: 5
pznb: 5
jgqh: 5
ztvw: 9
lmnp: nvvm - tmnt
vlpd: 2
mtdc: pgnc * ddzs
qpjd: 5
nnvz: wnzd / qpmq
pqpw: vprc * fhld
qthr: rllp + zszw
jftf: qjcb - vmsb
tdhr: 2
ngdg: 5
dlhc: 5
nszs: 2
vtjm: mjtz + fbqw
ssdq: 7
rspw: 6
pgwj: 9
tpjn: 5
ssmc: 3
lzql: zqgl * gsmn
rzjb: 14
ptpl: 3
nrfc: 2
vrll: sgnb + brmb
vncb: vwzs + vdvd
fnhm: qphs + fqpt
smqs: ztjh * mbtg
hvcr: srnq + fbss
btmp: 5
sbdc: 3
zbgh: 5
wvmt: 18
znjm: tgqt + wrzg
scsc: 2
dddl: 2
wctj: gvjh + ndhf
jqvb: mntp * gpmb
rcdc: lfvp * msbt
fcrt: lcgq + nmbw
stqb: lmqz + gpbf
stpp: 3
twfc: vtnq * mjgp
szhz: 3
ggcd: 1
ngpn: jjwn * cttr
mzqf: 4
dqdl: mhcv - mgdh
zvvr: 5
qsfl: bjzl + psbm
blsl: 2
fjjn: nrmn + bnlz
jjvn: 18
hdhh: 2
qptc: hpdv + zpcf
gfmr: 9
ssbc: 3
jvrj: 5
lwzh: 18
qpgf: lcdc + mwwd
mplt: 19
prpm: lhhm + jnrl
ghdb: rwzv - gdgv
pndh: srvp + svvr
mbql: 1
qpmq: 2
lwjg: 5
ngff: 4
gfgp: nggm * bwgm
fccf: 9
trfm: 4
qlcr: 13
lghs: 14
jldm: rpfz * qtzw
szht: 13
hqhd: rjvz * bngz
bdtz: fzct + qrpm
jsvv: 1
btsw: sgpp * lcrq
qjts: 2
mrcp: 1
hbbf: 4
nprf: 2
tzfd: wclj / qmzp
tvgg: 2
bfvt: 2
qbzj: cjvp + dlwc
szzr: vltb * vbfl
lsww: 4
rjtd: 13
jnvb: ncjj + jsnr
pvfg: hbhf * ghsw
nqpg: 2
gjjm: fcct * bcfn
mcrj: 6
lwcn: 2
pvdp: prtt * ddcq
hcjd: tclq - cccp
hjlt: nssw / jbjz
rrsp: 3
nwwz: 3
sfpl: 4
gnsz: ntmg * gbmr
mgtf: wjpf + bmmh
rtlb: 18
sphm: ndvz * bmbb
gvsr: 2
mcct: nbqr * shmh
cchc: hlld + ggrw
rvdq: dnjs + drpz
mggm: 2
hbvb: smwg + rbjc
vljj: jgjc * qdcs
qmsf: rwwf + bccn
ghds: hsfv + tmcb
pbzg: 9
nsgb: 2
sgdp: tfhz * vdqh
ljpw: qwsl * ttcp
bgcz: 15
bnzp: 4
tvpm: 2
wtzw: hnwh + ccmc
dbml: lcrd * tltn
lblf: wshv * htwm
gglg: zsdb * fwtq
dzvn: 7
dslb: 3
cnsb: zwqt * fdgq
vnbc: 4
stpf: ltrp * pqpb
mhcg: vbsw + llrj
tdnf: 14
dclr: 5
jwjh: 3
dzbw: 4
szwc: mhwz + vwqz
pqmv: djpj / gvsr
cjcn: 2
jwzq: 5
zjcd: hnhw + szvw
wcpl: ctbm * pcph
mqpc: 3
qtzw: 2
tcpq: 7
fsll: jcct * lblm
wvgc: tjwv + fgnv
mbmn: 2
cbnb: gwts + mqgp
gffh: 6
fpsr: 14
tfmr: 4
vzjl: 7
srvp: 5
dcdt: 11
lwnm: 2
thfc: 5
ttzp: 3
tcln: trjt - gjlh
bsmg: 13
bjfr: 3
njhr: pgbn * jhmb
ccnq: trbd + phcp
ppfs: tjdz * gvdb
tbvr: tmbt * nzwc
vbcf: 14
fmhs: rhnh * hrnt
vrqb: vgqv + mbql
mqcf: glcd * wvpz
gnsl: qcpd * qpzn
vzbv: 6
tzcv: jjbl + mfbh
rvmw: 3
gmpl: 4
gwgh: dfgm * pqft
rmmn: 3
cznv: 1
vlql: 5
ptsl: 1
fvgt: sfsr * ncvz
jgdv: 2
jcdc: qpgf - wngc
fhmm: ntgj + cnlq
nvth: 4
zgmb: vpbs + mdgv
hfrj: fjcd - nzzh
vdht: qmnc + qmgj
gppd: 5
bqvf: 18
qrjb: vgrt + gqwj
hhhp: dnsn - hzsg
qmnc: gwjs * snbz
hmbh: swtl + zchv
bvwq: 3
tcfm: btmp * lbfb
frbf: 2
vlqr: 13
wblq: 2
nbnv: 4
tptf: cqnz + btqg
qtzv: vqhd - ggld
nmwl: 4
jfrp: nwgh / zwmp
qwvl: dhqb - zsmz
ztjg: 2
grmv: 2
mtcv: zwcf + dldn
hfrn: ltwl - tvjg
glzr: ptqb * wbqg
tjwv: 4
gvqf: bfgs / wwcj
mcmz: mvgr + lrmd
vjcv: pptq * qczt
zlsv: 2
ppcd: cmnh * jfps
qcpd: 4
mpcq: vlcd - gsfz
lwbn: mcdp * csdg
gcsv: hqhw * nbrf
mvrf: pfjr + tgvz
pcsq: rtpb + csqh
vbfl: lchr / gjcr
ssmp: 2
crvm: 8
mpgh: 14
rrbw: zbch * qsvd
ctvr: ljpd * vzhg
ltrc: prmp * gqsp
hrzl: 3
vqvr: sgww - bplb
ltcd: lwcn * gsbt
gbjb: lphc - fbfd
nqsm: mcgw / gpbs
zhlw: sbrq * znbn
slrc: rwtl + bzmv
rbjs: 1
brnr: 5
trzh: qbzj * dmns
tbqp: hbsc * vdjg
mjhq: 7
scrg: bnzp * lpwj
hzcc: mwrw * bqft
grdg: zlwz + tvfq
cvcz: 9
fqzj: pnvh * tgdh
jjqw: rcwt * sdcm
cqnz: nprv / dstg
bvnh: 11
hzzb: tcfm + jhqt
plwd: 1
frvg: 3
wcgb: pwhn + djnb
rbcd: 3
jvvr: pnlm + lrmw
gdcv: 10
gjgv: 9
dnjs: vlrs + ghcl
nbrf: 2
mnfc: 2
gmlp: 2
rzpj: gglg * dbvl
pwdt: 2
lhjp: 5
ghpb: zlfl * qsgm
snbg: 19
nlnt: 2
swrv: scrg / gqtm
vczc: 8
qvvj: mtnz - nttd
cvrm: 4
ffrq: 2
lmqr: 3
lbdc: jngq + tvzd
mrgj: 17
bmld: 3
trmq: 3
trjq: 2
chgm: 9
vjll: 3
mnzg: 3
nlgs: cqsj * bmld
pmdp: dwst + mwhd
qdjt: sdgv + nzbr
vfnj: wbzh * bpfp
dbrt: 5
nqgd: ccmw * lvfn
csbp: wpfr + zsgt
lzml: 3
vszv: qdtf / mppg
dmlq: 2
gdpn: 1
jfsr: gbrc + hjft
tfwz: nlgs * dcdw
llgj: 2
dvpb: cfbh * jqvb
dbdj: 5
fjmh: djwd * cpcs
ssjd: rvgs * wwwf
whnw: 3
trmt: nwpl * qvvc
mgvl: trdc * gnbw
llrj: vqqj * dtwl
fhfw: tghn + hjpp
tvzd: 1
jfmm: fgcn * wtcf
vjnn: fmjf * mwgc
fggp: 5
qfvq: 13
pwnc: jltf / smcn
hgzm: ptww / fvpb
tvjg: swcp * vqzq
jntr: vnwr + lslv
pfgn: 3
zqnw: wwwj / tpjn
mwql: qvvj + qlsf
cljv: 4
djhj: 1
tztb: gpsv * vcqp
pqpb: 9
psrj: 2
root: pqpw + vqmv
pbfn: 3
thbm: 14
zhgw: 5
rmpt: wzhv * jgdv
cbhn: ffrl + phcm
pspf: grdg + qlcr
zsdt: 2
sgwp: vgtq * fnnd
qpdj: 2
mlsj: pdqw * ftqc
ndns: 3
tfhz: njqz + bwwf
wdpw: 3
cpzz: sprl * cjcn
wfwp: nzdw * fbzf
wssl: szqv + mgzb
lrtm: qzvp * hsdf
wsrp: dhzz + rnpm
gmgz: lvbf * jzct
lwml: 5
tfwp: ghhp - jphm
nmrj: vgjb * tsnf
tsrd: fqtb * ncfp
trmv: qhtw + mcth
lmqz: 3
szpt: 3
ncrh: qrrp * fbhh
rlcm: 7
jllp: dvpb + phcb
gjsn: 5
djpj: lzgr * znnw
hblg: lvdd + wsmf
czmz: 13
hthc: jvbq + zngp
lpwj: bnwc - btvj
mnqb: 2
lhdw: ssjd * pznc
msbn: rhvb + vszz
rwtl: spvl * lgph
rjhd: 2
jrzr: 1
znld: 3
ftrd: snrm / ssmp
rnpw: nlfj * nqsm
shls: gwgh + cdrv
zhqj: 4
bwgm: rtgn * lhzp
gcvz: 11
cbqr: vrjz * qblq
cdrv: zscf * lssf
bcrj: wwvz * pjzp
ncwf: mwww + vjln
vjvp: tspn * fljz
qltp: ntgn * nvth
ddcq: zhtl + ggcd
tpml: 5
zmcz: 9
dczq: pphf * mhtr
jvbn: 2
lpbt: ndbd * wntf
tptd: 2
fmjf: 2
trhb: 11
zvgf: vbcf * rcnw
rjvz: 2
gvjl: rgtv * pznl
wwmf: 2
nhjz: vtmt + wndr
dmns: 3
wdtv: 2
zhgl: 19
gmpg: dghv * ddvc
lhhr: 7
tmdf: znqh + bsvn
rljl: wbjc / pwdt
ggqd: 18
gzhn: 4
qtnz: 16
fzlz: 11
gslb: 4
fqvp: 13
djpc: 11
pnbn: 4
mfnw: rmsr * hpgb
mjlf: pffd * bzzz
rbjc: hzdp + fmhj
jwjv: sbgs + gmqc
mwrw: 2
gwmq: lzgc + brhd
sqvh: jddd + dbml
gpsp: 18
wjlc: dzbw * spnq
slgb: cshp + phls
rfqd: fsll + gjsn
hbqh: gmsp * nvqw
tvbj: 4
dmtn: 4
csfn: 18
cqjn: vfvl + mmtb
zmjg: vstl * ggqd
hqdh: 2
tphr: tvll * dbwj
zsjv: 14
nggj: qfdz * lqcr
pznp: vtfh + fcmf
jpqr: tfwz * dgrf
vmsb: 1
jnnp: 2
lnbm: 2
rpps: fcrt * qjts
nlfw: chpb * gwrm
swbm: 12
lgmd: 6
mslg: 2
jznf: 8
nqdm: tddz + ngbr
whgf: 11
qqgw: mcpl * jtnt
mdbc: 4
rfjq: 10
tdtj: qswh + hnqn
szhj: brnr + fdhb
nzbt: 6
ntjz: vqht / qbgw
mgrq: znpm * szss
fzcl: 11
ltwl: tlmf * nstb
fcrd: szdq * pdrr
tvbh: fqvp * ptbw
bfmm: 4
llpc: 5
jvcs: 3
gqtm: 2
jsqh: 3
rbch: 7
nsct: 2
dldn: hjjz * nmdh
bdfj: 13
vmfn: 4
znqh: qczj + lqnp
hzwf: lnzp * zdst
rlpb: hnlr * ghpt
pgrp: psvq + mnrt
qblq: 3
mznc: 5
qbwj: 4
schh: 5
mmhg: bvcg * jgqh
qpzn: 2
ljhz: dqdt + zjrz
tgtf: vthl * zjll
pncm: 4
vprc: 3
drnb: lqtr + trds
fjht: ngdg * vpjb
vbnh: vbpt * vzfh
chtq: sphf * wblq
cfjn: vrqb * hcnb
sgpp: vnbc + ssbc
cvct: qstc + mbjj
wgrj: 13
vmdd: zlff + hbqh
ndvb: hvpl + nlwj
tbpb: 2
ljpd: 5
ztqj: 11
ftnz: twqt - ftsd
tvsd: 3
jrhj: dlzc + fvgv
rsjf: vqvz * jmsq
wjpf: bmjw * fhrs
blcl: phbv + qnht
gfjh: bmbl + gvqf
ggfr: jsgp * zbdv
hmgp: mlbf * vqzn
hlzb: lqzw - pwwp
ccmc: 3
wqld: 17
dvbp: 5
tppg: bsct * cvcz
zwmp: 10
qglh: nhjz * ltrn
nwnm: jfrp - whzt
tzws: 2
stws: 3
sncb: vbld * tmgj
zltb: 8
rbmg: fzlz - nzcc
srfv: ghmr + ntcr
ttbm: cqjn + hqps
bmmv: gwdv * bthc
qgwj: 4
lfpb: fmhm + ltcd
hzsg: 12
mvjm: hqhd * ndln
gpvf: 7
btdm: fzhc - wrhd
gvcq: zvmv * jmnq
gvpn: flbj * drnb
lgpq: 14
rtgq: 9
wbdw: 2
zzzd: 1
lsrt: 3
tzch: pspf * jtrg
ddrh: 2
nzbr: smqb * shlv
ndwq: 4
znfd: pcsq * pvrp
fqsd: bszd / tptd
cshp: 3
djnl: 3
glcq: jfgg * thzv
fzjp: 10
qpln: 6
rtwv: 5
sfpd: 4
rtcb: 2
qzrj: 17
zdjp: zrmn + jwjv
fhbf: 2
fhld: fggv - rmct
vpcr: vbzz * tdnf
zlwz: 11
pbmr: dpqt + jlvm
lcdc: ntjz * ljwg
wrbm: 4
gqwj: 4
bvlg: 6
lmhh: 4
lvmb: 2
htwm: 4
qzvp: 2
hlbl: 3
mdgv: bntf * mvlh
rcld: 6
vrjs: 6
ctqp: 17
hzfc: mngq + whhl
vvdn: 5
dmsw: rhlg + btdm
dtdg: wvcw + fzvp
gwbc: 5
ptlh: bpnl * hdvb
lgph: gwbl * pnsp
zplr: jqpw * tcpq
tvlt: rzgt + lmpz
fhmg: 7
pwdq: 2
dcnn: cvdl * pwdq
tdds: chdt + wczl
gwts: rzjb + vvsd
vqqj: hnfs * dntv
dgzh: 2
rrsl: 2
mqfr: nzrr * lpnd
pfms: 2
ntcc: 8
jqzz: lljd * hvnt
frrs: lmnp / mzwd
rswg: mhfq + gdfp
qltd: bqvf + nlpc
pfjl: bhbm * vpdr
mhvn: dzmw + rtlb
qtdv: pgnq / zhqj
bcdw: 3
rmmf: pvtc * gcff
mvgl: 6
tzms: 2
cdzn: 3
hwdg: 2
fsdw: 2
ctpf: 2
vsht: tztb + snjm
dpmd: 3
gcgz: jrhj + sflw
tmgj: 3
hrgq: swbm + wlpn
cdsr: 6
qphs: mmmd * rlcm
rzcw: 2
tsvh: jnwb + zbpf
pcph: fdtl + hmcc
wqqd: 2
ctll: gnfp * mnzg
brdj: 7
fvtj: gmlp * njnl
phcd: 3
grtn: 20
vstl: 16
tjms: 5
pnfc: dcdt * qfzq
lwfw: vgvh + sshv
czmc: bnsn * ggbf
lrbp: 4
hqmh: lgnl + hcvc
wwbw: 4
dwvl: tptf * vtjm
nnjb: 1
wsjg: 6
qzqw: 3
jvbq: plhp + swtm
lvdd: 1
tzdq: 7
qswh: 16
gszj: 2
mrzv: 2
hdfj: 1
dwqp: 10
fjgm: bqmg / fdlv
tlcm: 10
hvbj: mslg * qbsm
vfqn: mtcq * swsd
pwsg: 3
qjcb: jjqv * hbbf
ztvf: qbqp + qsfl
jmph: chhc * zfrc
djjb: 2
djtf: mrdd * cchc
lblm: 4
pwjn: 3
qfzq: 5
tgpt: 5
fngj: 4
vvlg: ztvd + zdrh
hgmt: fqsd - btmn
jrll: gvrv + snng
gtfn: tpcs * chhr
vssg: 3
wclj: mgrq * qtms
zrmn: 6
flvd: zrrm + bvlg
plhp: whtj * ltvj
vrcq: hsvn / hjgw
lvrp: 6
jtsd: 3
mtcq: 3
wnzd: crhd + nqfh
gnbw: 10
nvzb: 2
nfpw: gpcz + wzcm
rfgt: 7
nzpn: wdjw * tpbf
dffz: hqwg + rtrs
zjll: jwjh * pbfd
bmbb: 5
tnsb: czbg * djwb
czst: pbgh + bzrh
nsqh: mcjd * zlvl
bnlz: 8
pznc: 12
fbbt: 13
rhfb: zwww * dbql
jdwd: ttgb * ptpd
cvgb: wwgq - pbzg
nbvp: 3
pjqt: pznb * sscf
nhqz: fgfs - gdpn
swcj: 3
ltpt: 5
fgnv: 10
gwwn: cjrg + cdvl
rrnr: 3
vpjd: 4
vrsg: lmzw / qgzb
btmv: rrjf + dmjf
lzpb: 4
ztct: hdhb + sbbz
pjtn: 10
ltrp: wffd + rrzz
qcgj: djnl * hmld
bjfh: 2
mmtb: tjms * rvhc
rgtv: 2
rgdr: 2
dzlt: hpgv * wpmt
rvrc: 2
mvhj: wmtb * jmvf
vdrs: 8
vbsw: 7
jfzf: gzzq / swch
zwcw: pcml - fqzj
jmvq: 3
vszz: crts * lpbm
vbqf: 5
zttm: gwdt - lwgt
tjdp: 6
sgcs: fvbn + pvfg
wnng: 13
rqqc: 3
ztpm: trhm + dfdj
tvvm: 4
tzdj: 2
jlhw: gdcv + jhbn
ptqb: 2
grfc: cznl * vgqb
djwb: nfsq / crgw
hgsj: 2
tczg: wmrq * qslq
hzdp: gmpd / vnfb
nrhq: tzjm * hdzl
lnlf: hcpn * qrlm
vmgw: 9
rzgd: 4
strm: tphr + fcrw
bmbl: tbnv * pwsg
fcjj: 17
sgcz: zcwd - lbdc
jlzg: nrrr * mtdc
szrw: 2
fjrm: 2
pntw: hcqn + qgfb
snnz: ghqq + ngff
gfhw: 7
pqdg: 2
pfhm: 6
llzh: hgsr - hlbc
mlmp: lhdw + hqmh
rztd: jpqr + rmpt
lprq: 2
qrqd: 5
gnfp: 3
wpmt: 2
zrzq: 5
pqsg: lmwl * rttf
wdhb: 3
srhp: zdjp + rgdr
cqsj: 2
tlzq: 2
jvdt: 10
rwzv: fdmf + gtwj
bwgc: 4
clzs: lwbn / ptpn
cnhz: pzmn / wtqg
hqwn: rfrr + gzdv
bszd: fwds * qpdj
ggrw: 6
zmpd: gfgp + dqdl
sccw: jhlw + bhjf
ffpz: cpzz + srbr
mlcj: gsbp * qtsd
twtm: 8
jnhw: cbnb * jvbn
jpsp: tgbh * ctpf
ztrd: 13
zwcf: nprf * rzdh
rlmp: njjn + dzvn
lbtj: nvfj + djhj
fwvg: lpbt * glqf
lqzw: zbqd * shbf
vpbs: nbvp * drtz
vzfh: 20
jddd: cvct + tngd
chmv: 3
lcbt: 5
gmqc: 4
rtpb: tbrb + csbp
pqgt: 4
vbld: dslb * fbmt
gsmd: qgvc + pbqj
vdtv: 5
wwvz: 7
wzcm: 4
hnqn: 15
jmnq: 5
fcqq: 3
sljs: 3
pzbn: 2
chhr: 2
zfrc: 3
tmsz: nzmt + twjw
tjdz: 3
bfjg: wssl + bsmg
qqdg: pbgd + qblh
jvvd: jfmm * csmz
ggdg: pdvg * zdrv
dbsd: hthc / rffv
jdls: 3
jwlm: vjnn / rhfs
vnsn: pzct / qbjb
jvvm: 11
gpsv: qptc / pdmm
nchv: zrbv * nvzb
jcdj: 4
vgqv: rmmn * jcdj
dmlf: gnsl - jrzr
rpqg: 8
pgbl: 2
gsbt: hmft + tgtf
drqz: jvvm * dnzg
qhtw: qpgb * mplt
gwdt: zsjv + rjjv
tcnw: 3
rpfz: wbvl * ddsd
wbqg: 5
wdvm: 3
nzwc: 2
rpvl: 15
ldrw: mpcq * blsl
srlj: 7
jsvw: rtlr + pqpr
djwc: nmvc * tccv
jwmd: ttts - zfmh
zgff: 1
rttf: 18
sbmc: 2
vwgp: 4
mzjn: 4
jtcz: sjqp + zbnt
dhtt: lgfg + vhcl
tsnf: 2
dlzc: wdtv * mrgj
cghq: 2
bwsp: tvcg * dvcr
mdcn: jvrj + cfjn
rtgn: 11
zfnr: 2
rclr: smvm / nlrj
spvc: dsch + dpnz
bpvd: ncrh * jvsh
vbpt: pdcw * tvrt
ggcn: 6
wrzg: zgff + qrsm
bzbw: jbfl * qzfd
bpnl: fcrd + lwjg
fqqn: jszt * ltzh
fplb: qjgc * vfqz
dmtz: 3
zvmv: 2
hrnt: qrch + fcwt
slbd: fzsz + pnfc
fgbq: 5
qpbj: gfrq * tsvh
qrpm: dbtn / trjq
ldzr: 3
psqs: lcrj / zsdt
vlvn: 19
gdfs: ndhp + nlbg
mwhd: vqhl * tvwp
ngmz: 3
njlz: gcdq + ggfr
vzwr: msds + jnvd
bnwc: pjrd * dfnw
tjjw: bmjh + jntr
mmsc: vdrs + vhzb
bplb: 10
htnc: 2
swch: 2
cnng: qtlp * tspl
mvgr: tczg * ccdz
npjf: 3
wgjs: rznl * mlmh
sllr: 7
sqsv: 17
lrmd: pzbn * fmhs
vdgr: 5
phzs: 10
mpbh: rcqt * qjrd
jjmq: grpp + vwrh
fgmh: 5
fcnf: tzfd + czpn
swqj: rbch * tjjw
whhl: vgfg + gdfs
trmr: 4
dqlg: 5
jhvz: sljs + lbqh
jjfd: 2
mcpl: 3
srsw: ghzz + djwh
ndvz: cnng + drqc
mdjz: bdfj * bpdb
hcvc: nvsm * ptpl
jttg: 2
dwtz: 2
wwll: 3
tjzj: tlzq * qbwj
lqfh: 2
lgnl: sbmc * sjsf
nqtb: ghjg * zfbs
dsph: 4
lstn: 2
mgct: bjpg + mrgg
bgrw: 4
vphz: 3
csqh: fhmm + trzh
hwfp: 5
pdqp: 3
tcll: 3
bdpl: rgfc * mlqd
lwpq: dbhz / lvng
rnpm: pfjl - lfzz
zfwl: 13
wzgb: shlr + jvvr
thgc: 2
cwsb: 5
qghj: flrd * jhnh
cjzz: 2
rcrd: gljf + ngmz
pgnq: vptl + fqqn
jzgt: fhbf * hmcm
vcsj: 13
ccwh: stqb + hcqr
trdc: 2
gzdv: ljwn + jsgg
qrlm: 3
lvqd: 2
fcdr: 6
drwv: 2
pgnc: 3
lzhw: 9
bzlv: 2
hspp: lrrt + ddrh
vlmm: 7
tzhs: vfbj * mbmn
cswb: 4
chlh: 9
bngz: wlhj / qjgp
trbd: jwmd + lgqz
hqps: 12
gfjp: 2
rzgt: nnpl + ppjh
lfnm: 2
szgp: qpjd * lstn
cprv: rpjw * thgc
sftz: wltq + nnvm
vqlw: 2
zcrp: wfwp * shqq
zmqh: nchv + wswv
ggjv: bzbw / bzlv
nbqr: 3
vccf: pqbq * bdps
lssr: 2
qsgm: 4
znbp: 4
rjvn: nwbv + jtzp
qngp: fpdc + wdvz
rjfb: ndsb * ztrz
svjf: 3
lpgc: nqrd * jhvz
swwz: 11
jmzf: 3
shqq: 2
ztvd: 4
nfsq: fjtw * pgbl
pbgd: jzzd * sbdc
vdmv: nwqt * ssrr
rtwg: jqlt * srsw
mtcd: 4
bjzl: wrcl * clrt
ddmj: 3
qbhd: qqcj / mnqb
qwmv: ftdw + pfjj
rrsd: 18
cwjt: 1
mfbh: qtrj - wrbm
csmz: 9
fqqg: jghw + dhbm
fhqw: 14
fcmf: llpc * slgb
qtrj: qmmf + zmfg
djdr: dqlg + ccvr
ftnt: pbbz - rhpq
fvwj: 5
nhdj: tqwv * zpsn
bzbq: 4
zwqt: 3
zjrz: 10
hgsr: vjvp * tfjq
thwj: sqjb * hpcj
zqgl: 3
lhhm: wmfc * vbfr
pwcb: 3
vqtg: jmms + rztd
fcrw: fzcl + fntb
hgqr: 4
zrft: 2
znqv: 8
qtth: 1
cwtz: 7
jvhm: 3
wlhj: phlb * tmsz
fbrg: 5
bdvd: czjj * ggjv
mmpj: lqfh + lzqp
jjbl: mtcd * brdj
qrcq: 2
hzrg: ffnj + sqsv
hpgg: tzms * mlcj
vvsd: 4
bpdb: 2
hmtq: 4
mfdr: 2
ntmg: mjhq * njzm
stgv: 17
hbzr: 9
szct: jjqw + wwhh
vdvd: dhrh - mmhg
qbbt: 3
bvhz: 3
vqhd: zdbv / hgcq
qdmd: lprq * rcrl
jhwq: 7
dvgh: mbmz * hztl
bhct: phcd * frhf
jhbn: csgg * vssg
ntgn: vbmm + gvtv
fnfr: 7
crhd: 1
bdll: phzs + cmrw
vzpf: phsj + nhbm
njqz: ztct + zchs
rvqh: mwql * tvzs
pmsd: 2
qrjz: wnlp + pqtb
lzcd: 15
tbgw: dwgn * rbtg
vrjz: 2
zdst: dhfl + bgzl
qlct: dgtz * mmpj
mtwb: 13
whzt: vzqc + mvrf
ddvc: 2
njwn: fhmg * cczh
mcjd: 16
djwd: 4
vgqb: 11
rdtb: cnjr * pgwj
ggph: vgbm * ltrc
hfnt: pwjn * tzdj
vjnj: 1
lghw: pfms * lmzl
nzzh: 19
bqft: csmh + tsrd
nzhw: 2
lvpr: rrmp - qfbr
lbqh: 14
zwnz: sddq + dhtt
gndz: 6
fnvh: rblr + ffrq
spzq: srfv + dvnn
jmjt: 2
plnn: 2
nzdw: djvf + npjg
mjtz: 4
lzqp: 9
rzvs: dbtz * glth
pstm: 11
rmsz: 13
frqq: 10
qtlp: 2
nfpg: psrj * pqgt
hbql: cnfp * hggz
mzwd: 3
cdlr: 4
shbf: 3
tgvq: 5
fbss: zlzc + lsrt
cmch: 4
whpn: 5
cpcs: 4
wmvh: hpmg * jqff
hqwg: 2
szzp: zmld + gmtq
gmpd: zjtp * ndwq
zsrr: 5
mdnp: lwpq * qcgj
glth: 20
qzwn: mbrg * ffdf
jgsc: 16
qcgg: ddmj * brjh
fzsz: jjvn + nvvr
ppnh: 2
fbwn: 6
hpgv: lzmc + rrts
vswv: qfhl + dpjr
rfwt: hhwn + trmv
fqmg: 6
znrp: 3
cgsv: 3
sgnb: qzhp * zsvt
wjzp: 4
vzhg: 5
dlwp: whpn * vzwr
jnwb: hsmr * zfnr
jqlt: vzjl * chmv
nlwz: 5
dwwn: 3
gsmn: lqcl + rqtg
fbmt: nsqh - nqmm
wmtb: btjv + lwqz
qrvp: 2
nzmt: jsqh * cdlz
mzpt: 3
twqf: 6
cttr: mvjm + rjvn
ghpt: 5
bctq: 5
jpcv: 2
dzns: lmfv * hdrh
crjq: sncr * qsph
cjdc: twdv + bgws
vwgt: hcrq * qzdt
mvth: 2
mvdn: njdr * frvg
hnfs: 3
pjrd: 11
tntj: vsmg + vsqj
ttmw: 5
bcwn: 7
dgrf: 3
hbsc: 2
sqfb: cdsr * dmrl
lzhl: 2
hflc: 11
zcwd: wgrj * mzpt
tpms: szzr * vjpl
pjpz: 5
rtvq: rhpb * jsvm
jnvd: 4
dnrv: 4
zfjr: 9
vnlm: schh * vjll
tgqt: 7
pbbz: lcjr + vczc
ssst: 5
bpgv: tgbt - zmcz
nllz: cnvf * wjlf
gdgv: 12
whtj: lzpb * vlql
jsfs: 6
szdq: jbft * jdls
qvgq: zjcd * lwnm
mvhs: 3
jhqt: 16
stpz: 2
ftzs: 2
mldt: llfc + cmch
zmld: rmwc * qslz
bnhv: 3
wshv: fqvj * tsjs
fbqw: bwnj - lcmm
sflw: dcnn * zltb
pqft: snjb * slnt
zsgt: 10
ncjj: bjwh * zmqh
fvgv: 3
hsvn: qdzm + hrvh
lwqt: mtqm / mvth
ftsd: 15
hvqt: bmzh * lmhh
grbp: cbfs * nrfc
jgjl: 3
mbmz: 2
wtns: vqtg + tvsd
tjds: gwtt + nhdj
ghjg: 5
dmjc: qdmd / swnj
zsvc: 2
clwl: 10
qnsw: rfqd * pvdp
rdpl: lmqr * fsmq
nhnd: 8
dffq: mqpc * znrj
nhvj: cvrm * grbp
vdjg: npsr + hjlt
zgmn: gffh * bhbj
slhl: gnsw / fwdj
hhwn: tnmn * bphg
ssqr: tfmt + wjlc
lzgr: jzzh + rjjf
zfrp: qhgn / ttcl
jszt: 2
ftnc: 4
wvpz: 2
spnq: 2
gtbw: 17
hvtb: ndvb * stcz
rcnw: 3
hzsw: lhlc * qfhm
mmmd: 4
szss: 2
ddvb: qjcs * zgmn
vfqz: 4
mngq: 12
pcjr: 8
bcwt: 2
fwds: hlrd - hbfc
snjb: 2
lmpz: gzhn + zhgl
pjmg: 20
hjft: szhz * jnnp
czjj: 2
dpjr: 2
wwwj: vpjd + npvn
pqpr: 13
rqtf: fhqw - vmfn
tngd: jmbg + gjjm
ndhp: gfnh * tvvm
cvmw: 11
qfhl: gvzc + zjzw
vhpg: 2
nnmr: ldwr * tcll
rsrp: znqv + hclm
lgdw: gmpg * ltpt
grgz: 2
dvmh: 10
phsj: mmrw * zhww
bpzp: jmtf + qcmb
bmjh: qfct - gwnh
mbrg: 3
mcpc: 2
cdlz: 2
phls: jttg * jwgh
pqdf: mfmt * wtzw
ljsm: 3
fnnn: rjml + mcmz
djnb: 1
lbfb: 3
fvgc: 3
lbrs: 5
gvzc: prqq * pjmq
mdps: 17
cccp: 5
cnlq: 6
twdv: 5
mbjj: sgwp / hfvv
zsmz: 2
pdvg: 4
sscf: mzqf * trmq
pfjr: djjb * mznc
qgvc: dsqq + vwmc
tzjm: 3
pdrr: 2
ccsm: 1
tglj: 2
wmqf: 5
ghzz: 13
fcgd: 2
bmmh: hzzc * dgvm
lgrl: dzlt / pzrm
fqtb: zhfq * bfnj
fsvg: 2
pmfp: 2
zdrv: vljj / dpmd
npvn: hgqr * wlvl
sphf: 9
ffcm: 15
jgjc: 3
jjcp: 11
qbls: znfd * snsp
qwqt: ggcn + vvdn
gbbw: 8
qsnr: nnvz * rmpm
gdzh: zpjf + bjjm
wmdg: svld * thfc
jnrj: trqt * qhhf
qbvv: 4
djln: 5
vnwg: wvmq * znjm
lwvd: 3
qlsq: szpt * strm
wnlp: ggph + vbgb
nnvn: nlnt * pvnr
sqjb: gndb + wzvr
bnbj: nmrj + rrrm
lwzf: 7
nqhb: wbqd * clwl
nqpv: 3
rsmp: 3
wsmf: cgsw * wmqf
zswj: nzwv * lwft
lfvp: 5
mcmw: 18
fzct: qmsf / gtwf
tvzs: 3
lsdd: lldd * dmlq
gmbc: 3
qrrp: 3
rhph: tsfj + dmsw
hsmr: 3
ncvz: cwtz * qrvp
tgbt: fsnz * rpcn
hnzj: dncv * tvgg
dlth: mpgh / zpqc
fmcd: 2
gcdq: dgfb + rpqg
hmcc: 4
hcqn: ztgp * cbzb
ggmq: hzwf + mqfr
rvgs: 2
vbfh: 2
jnmp: zrft * lwqt
vzqc: nlht * qhlt
cvbt: 3
mrsj: swrv * lfnm
dltf: rjtd * sllr
wvmq: 3
wbqd: zptn + tnbb
flbq: mfdr * fhfw
ffhd: 17
rhfs: 2
cfbq: hqwn + pqsg
ptpn: 2
pdhr: frbf * sfpl
spsz: pvsz * pfsg
ldwr: fvgt + thwj
zsbq: ppcd * gwvt
fwdj: 4
vbgb: cvfc * jfsr
zrcz: dpcw * vzmb
fdhb: bdcb * hfnt
wrzm: 12
dbql: 3
fzvp: jdrl * cfbq
tpcs: 14
sbgs: 7
fdtl: 2
sfjs: bfdn * mhdw
grfl: jgsc + blcl
vfvl: 7
vpdr: zqzn + bfll
dvdv: 6
gsfz: pntw * hspp
vjln: 2
vqmv: qvgq * sfqc
rhnh: 2
rflf: zlsv + pstm
vfvg: 2
zdrh: 3
zzgs: czmc / ttzp
dfgm: swsc * vqwb
qjgc: 8
rmrc: 4
rhlg: vzgc * lssj
mnrt: 6
rjml: rlpb + cvjq
mcsw: 2
hllr: 2
wmfc: 7
hnhw: zcrp * pltl
zbmd: 3
zchs: qdbn * ttmw
ttts: wmvh * gvml
nwnv: 1
vznm: zzzd + ntcc
gmnn: mjcr * tgpt
trbw: 3
hvnt: spsz + szht
lbtd: 6
sprb: pttb - wllf
zfbs: hvqm + tbhb
qcmh: 5
zmfg: 8
djvf: 2
gzzq: lpnp + fnfr
hcqr: 4
gtwj: fngj * whvc
nrrr: 3
srnq: pjmg + fgqr
pvtc: 2
fdmf: bcwn + rsjf
npsr: srjf * czmz
nbth: wttj * rlnc
njnl: 4
jwqm: 5
ljwg: 2
gbrc: 13
mgcw: gcgz * gwzd
hbhf: 4
ndhf: fpzf * bntv
mlqd: nqhb + gdds
tspn: 2
bccn: 4
rbpl: rrsl * vwjs
zszw: lbrs * llhb
bhvv: llzh / zrlg
zwsw: 2
rpnd: 5
gmtq: grmv * mgvl
gsbp: 2
vdrv: 20
sqph: 2
fqpt: 8
tbcs: 2
tlmf: bdrq + cpvn
lwgt: 4
bntv: gvcq + ctll
rrrm: dffz + dpjh
srzf: djdr * jgjl
qfbr: lbrm * vghl
ztjh: 13
smwg: jqjc * tdds
ltrn: brdg + vsmv
shlr: 12
jbfl: 2
zlfr: 4
rhpq: wtcz - cznv
flwr: 2
zzbh: 1
fjvr: 2
fgfs: nmzw * gdzh
qvbt: gjgv * jtvj
cjvf: 16
mhcv: qllv * sqlv
vhlb: vwhd * dmpm
fmqq: 10
vrmv: bthj * fqhq
qmzp: 2
gsdn: jbzl * fjvr
tltn: jwlm + czcd
njjn: wrzm * nszs
dwws: 2
zfvw: 3
hdrh: 2
ptww: wfvv * crjq
sshv: cnnr / bqjf
glqf: 3
rswz: 1
mnbl: 4
sbrq: qvbt + gssg
vqwb: 3
rhpb: bpvd / nmfp
nnpl: gnhp + lwfw
jlpj: vszv + qcgg
vghl: 3
spvl: nlcq * tdtj
tbnv: 9
phmj: cnsb / lzhl
fntb: fclw * bfqc
mqgp: ctpj + zmjg
bjjm: ggzj * jrdp
zrrm: 1
lpbm: 2
dqdc: 4
nlfs: 2
swtm: jznz + ctvr
snsp: 3
jndl: 3
glcd: rfwt + vrzj
fdlv: 2
jpsc: qzwn + ttcm
lldd: dbgp + twtm
dgdr: vcjp + mltm
qwhh: mvdn - jvvd
pvrp: 3
cbzb: 16
glnn: brqb * hflc
nlwj: hrsn + rcld
prwj: 4
vzql: 2
tfjq: zpjh + jpmc
rbtg: 17
wzsg: 14
vgfg: 4
qfct: dlvr * jtsd
stcm: vcsj * cgsv
pttb: cljv + jhzr
qsvd: 4
hfvv: 2
cljb: vvlg * rmmm
zpqc: 2
dbtz: 2
vvjw: 10
wndr: wdhb * dmtz
vbnq: 2
qmrl: 1
hzzc: 2
fgcn: 2
jjwn: 2
pzmn: cllr + lhhr
hbnv: 9
chhd: dbrt * tjlf
hpgb: 4
zbpf: 5
qhgn: vswv + lmrq
wzvr: 2
dlvr: jlgh + tzhs
zngp: lzlf + rtwg
vsnq: 4
pnnc: npmd + ccqt
lzgc: sfgd * svdm
jcpf: mdqj + fppn
mpcs: 13
fclw: 2
nzwv: 17
phcp: 4
nwpl: 4
vqhl: 7
cqwz: mpcs * bhjq
hmcm: 3
gwzd: 7
qpjm: ptct * grgz
jhgt: dgvh - cswb
chgp: tjds + rqtf
lgqz: gnzr + qngp
zchv: 2
mcgw: ghpb + pwvd
jtph: bwsp * gnfz
trhm: hzcc + hqbc
njdr: gpnc - ztvf
rffv: 2
lgfh: 15
wbvl: 2
jqpw: hgzm * dlth
cgsw: fjrm * gmpl
bdcb: 2
qzdt: 3
gjrz: lnbg * vphz
pnft: lrvv + nlwz
tsfj: 9
sfsr: pmrn + mrcp
dmrl: 2
mwww: rwnq - qrpb
lwqz: dqdc + qfpg
vwpn: 2
vvqz: 5
zwhr: 11
bfdn: vnlm + ftpc
ddhm: 2
vgvh: rmmf + wzgb
dbgp: 5
hrvc: cghq * zwcw
bffw: rfgt * tbqp
drqc: hvbj + zlsl
pdcw: rrmr * mzjn
jqjc: 10
njzm: 2
zctn: mrzv * mmzq
jhmb: snnz + hhbh
dmhc: 2
gddv: 10
pwvd: wdvm * wzsg
gdds: nqdm * sgms
lfjt: rmfv * nwvp
cfln: thbm * shnv
mbml: dmtn * bvhz
jmvf: ljht * cwwq
lqtr: jsvv + pfhm
zpsn: 2
tpbf: 4
lwft: 7
dgtz: 2
dhqb: vbqf + lgpq
qlsf: tvpm * jzwr
vtfh: pfnq * zljz
jfzj: jcpf * zlfr
sqbj: 5
swsd: nmcd - zgpd
hfmg: 4
czcd: lvrp * lsbc
mcdp: rsrp + lwzh
bsct: 20
wwgq: jjcp * gltp
mtqm: wwlr * vbcw
phjz: 2
lvbf: 4
gnwd: lhjp + mdnp
vzms: 3
jghj: 4
jlvm: 12
jmlb: 2
wngc: 1
ggld: bffw - sncb
nlrj: 2
gmhp: 8
hrzc: hhpb + chlh
vbcn: 2
rmmm: ssqr + qghj
rjjz: qqgw - hpnh
lgnb: 2
lpgs: gnsz * gjnb
prmp: tntj + lppt
lbzr: 6
hsdh: dvbp * qrlv
qzhp: 4
jmms: rhhm + mmjt
lngs: pjqt + fbbt
bnsn: pzvd + wcpl
fcct: fnnn / fsgc
jghw: 3
ppzn: chhd - gcsv
mrsn: 6
dbtn: zsbq + nhvj
mjcr: 6
ttcp: 2
nqrd: 2
jphm: rhml + bfjg
nwmm: 11
mdqj: pnbn * wwmf
lqdh: 5
ftdf: qlsq / qzqw
shnp: 1
qjlf: lvqd + zfjr
lmzw: vzpf / rrsp
vbpc: lwml + lssr
vbjj: rnpw - vfqn
btvj: dblw + dzfw
fqvh: 4
dpcw: tpmq * nqpv
pptq: 3
rpcn: 14
hgqz: nwff * tprp
wswv: vlbc + fqqg
pnqb: 13
tnbb: 20
nzcc: 1
qhhf: 5
cnnr: vbjj * jdtf
dngf: 4
sfqc: sbfs * wmlt
jfpp: ccwh * fcgd
fvpb: 8
lslv: 17
dntv: 6
fqhq: 3
cfwt: pfgn * qrcq
czrq: 2
pvsz: 18
jjqv: vscg * tfng
rqnb: dwqp + nvwt
hnss: wrcz + zjrg
pltl: zjdz * gbcv
mntd: qqvp + dcbh
fsmq: 2
csdg: 2
nvgt: 10
twjw: 5
lljd: rhcf * rbpl
nrrp: fmqq + fnvh
gncj: rrrv * mmrh
bzmv: rhfb + hslf
pbfd: 4
pfqb: pwcb + hvmm
dwgn: jznf + fgmh
rqzg: gtbw * qtgg
trtg: gbdf - cqbc
lbrm: jnmp / rvrc
vbvh: rqzg + cljb
zpjf: 12
vnfb: 4
gdfp: 16
hjgw: 2
llfc: 3
lzmn: 5
vlbc: dsph * vffr
cwlg: phmj * zrvw
lsqb: 8
pdmm: 2
vrdn: 7
jltf: dhfw * cwlg
tddz: jjfd * rbcd
dmjf: sgcs * hnbf
mplc: 10
llmf: 3
bpdd: tgvq + shbq
tbrb: ffhd + fllb
jvsh: 2
mqpv: 20
srjf: 2
mnsh: dngf + mvgl
nnpv: 4
zcww: pnft + dvdv
dzcq: qpbj + zhlw
wrtg: 3
vgjb: jhwq + tzbm
bfhw: 2
ccvr: 2
pzrm: 2
csmh: swht - tncw
qbnn: 3
qzvw: rvbr + jhlh
dbvl: ztvw + fhpf
fpdc: 5
fsgc: 2
rwwf: pwzv - flbq
pwwp: 8
lzmc: prwj * lzql
gqsw: 3
bqhv: 1
pfcv: 2
gjnb: 4
fjcz: fvtj * bnhv
pqcz: 3
tlhp: jdzv + wwbw
zrgh: sbvr * mcmw
pffd: 3
ghhp: jlpj * tdhr
pmnt: 3
qbwp: 3
tnjv: mtcv / sqbj
wcwd: llmf * mjsl
wzhv: nsbl + rvdq
hrvh: lblf * pdtl
vnps: zsdn + vngv
ztrz: 3
hqhw: 3
gfrq: 3
clrt: cbqr + fcnf
bfnj: 4
ltvj: lqvd + bhvv
wbzh: zfbf + qtnz
jvbd: 2
tvrt: 3
rcwt: ggdg + qhbm
wmlt: jcdc * fgbb
mwrh: dvmh * tbjb
lcrd: mclg * gppd
sdcm: dlqm / jjdw
smqm: 5
rcrl: vnwg + nfpw
dwcd: fqmg + nhnd
jsfz: 2
mjps: tzws * chtj
tjrc: pgrp + zctn
vbmm: bctq * plwt
fllb: hnqh * vzms
jwgh: 4
rvbr: 2
dvnn: lfjt * cjvf
hppz: zffb + trfj
ppnj: msbn - gbjb
tbjb: 6
vhcl: sqsz / znbp
jnrl: lrtm + ftnc
dblw: 2
bdjw: jlsb * mfnw
czpn: thhb + hgmt
cnpg: 15
zjrg: pncm + gmbc
ggbf: 3
chpb: 2
gwnh: 1
swsc: szwc + mqmz
mcth: rzvs + ftnt
zdbv: mrsj + zmpd
phcb: gcvz * dltf
jtrg: 4
thzv: 2
jsbb: ssdq * lqjp
nfdc: 5
swcp: znld * srlj
dpqt: rmsz - vbnq
pdqw: 3
ntgj: 2
fjpz: sfpd + jdsp
rcsj: nggj / vlpd
qllv: tvbh + frrs
ffrd: zzqv * nttf
nhbm: jgvd * zhgw
wrcz: 4
qblh: 4
lcrj: ndhs * rcsj
jvsw: qtdv * mqcf
pgbn: lfpb + btmv
rfrr: 12
mqmz: 3
nssw: ddvb / frlb
rbtf: jndl + jsvw
fmhj: nnpv * fszj
rrts: dvgh + vzrf
vqht: sznw * rlmp
dncv: 10
wlpn: jvdt + rbjs
jtzv: dffq * gfmm
nqfh: zcww + mdjz
vlgr: rpvl * bwgc
rdbm: qltd * bvdz
dnzg: vwgt * dwtz
dgfb: 9
rwnq: slmd + jzgt
rdtm: qbnn + lsqb
bwwf: 3
hlbc: ngpn - drqz
gpbs: 2
cqdv: 4
zlfl: fcqq + rfjq
zhjw: 3
vhbb: 8
vsbn: plnn + twfg
ggzj: nwqf - rqns
jsgg: pjtn + nlvg
mhfq: bflt * lzcd
jmbg: sphm + vdht
nqvb: 15
drsj: 3
cmnh: vnsn + nzpn
swnj: 2
rjsr: 3
pfnq: 2
shbq: 2
lnbg: djln + czrq
cldt: 17
jnqw: 7
chdt: 1
gvtv: bdll * hgsj
tqwv: 3
zfpt: phlc + nsbs
mjlv: 5
zmzc: 2
ptbw: mqbj * vdmv
rqtg: 6
qdcs: dmhc + zvvr
fbzf: 2
nvsm: 5
ddsd: nllz + cssv
rvmp: 3
prqq: 5
sznw: 3
fszj: dgdr * hlmm
lwgn: jgvl + fcdn
tncw: nwwz + lzmn
lcjr: zfvw * cbhn
cjhd: humn - vncb
fdms: 11
qfpg: lbzr + plwd
lhcs: 5
mdtn: hbnv + sqfb
vbcw: 2
jlgh: 3
lmrq: nphd * stlp
dmth: gncc * jjdm
ftdw: gsfq * hvtb
qzfd: tpms - tbfz
wllf: 3
tvtf: 2
ghlq: 3
fttg: 2
nwbv: 1
fwtq: 2
qgzb: 2
svvr: 2
shmh: 4
rhml: lvpr + gbwp
zsvt: 4
nstb: 2
psvq: 11
zmnp: 2
gwbl: 2
chfr: jftf + jlhw
qnmz: hnzj / vbfh
tgbh: 4
vcjp: 4
sbfs: btcm / tbpb
rhcf: 4
dqdt: 1
cczh: 2
chtj: hrzl * rdtm
qfdz: fdms + wsjg
smcn: 2
ddzs: 3
vlrs: 2
mhtr: 13
zlsl: znht + twdm
gzcn: 1
dfnw: lgfh + vsjb
zvgp: 13
qtsd: hdmf + vccf
prtt: 2
qpfv: nqvb * vrll
btbr: sgzs + jfzf
mhwz: sfjs / tlgh
nhcw: gsmd + ggmq
wczl: 8
jngq: 9
jtfb: tvbj * bchh
hnwh: fjhc * jpsp
dwst: 3
qvvc: zhjw * znrp
cbcr: lhcs + vcnm
fhrs: trtv + rqqc
rmpm: trmt + pznp
hslf: shls * swwz
ctgg: pqcz * qbvv
plwt: zbmd * qqrd
gpnc: zgmb / tglj
zpcf: hhhp * ppzn
jfhm: 1
grmh: hsdh + zrdl
sddq: bmcq + gncj
zcsh: bsqb * fttg
rcqt: 11
mbtg: 5
bphg: vznm + qlct
lvfn: zzbh + csfn
glgh: 3
qcmb: tfmr * tzdq
ncfp: 4
psbm: qrqd * wsvm
lcgq: hzrg - tqfv
nhcf: 4
bmjw: 5
mvlh: 11
jdlr: 2
rllp: nfpg * rtcb
qgwz: bvnh + lzhw
zhfq: 2
mgdh: dwvl + jtzv
ljht: qlcn + zfrp
vprq: 5
btqg: nmwl * hdhh
pbgh: mgcw - tppg
ddvd: fbqz * hzvm
gwdv: 2
gqnm: 2
zrlg: 8
zgpd: 3
jtnt: 3
tbfz: bcrj * pdqq
sqsz: dddl * tbvr
dcdw: 2
nnvm: 2
tvfq: rrsd + zsrr
bfqc: dzns - pjpz
sqlv: 10
pphf: tfzp + btsw
dbss: djtf + qjlf
gwvt: 3
btpb: gvjl + cvgb
tspl: pqmv * zzgs
vnwr: 12
grpd: 6
twqt: tdlb * gqnm
cznl: wjwz + dssr
hpnh: 2
gnzr: fgwj * tbcs
nnjh: 2
gcnm: wctj + hjhn
bhjf: qgbq * djsw
qjwl: 5
vltb: lgdw - bcjp
gbmr: 2
jzwr: rvdr + mldt
qfhm: 3
nzrr: zcsh + bgzw
jlsb: 4
wrhd: 5
wbsf: 2
vhts: qsnr * mvhj
qgbq: hblg * zhgg
cprj: 2
vnqt: 3
qdzm: jjpb * jnhw
tvcg: 2
fmpv: vqvr + lbzg
pnvh: 3
vtmt: 2
pfrf: 5
jqff: 3
gcls: mtwb * gljz
tlvz: 2
ndsb: 12
lrmw: 10
nwgh: pfvw - qpjm
grpp: jvsw + djwc
zqwc: 5
mvgw: 2
fcwt: rcrd + fnhm
rblr: 5
qrsm: 9
nsbl: 3
dlqm: snlw * mntd
pmrn: pcjr + glnn
rfth: hnss * fllm
hvts: 2
mdnj: chfr / ssmc
jdsp: nnmf * stgv
vdqh: gzcn + mrsn
njgb: zswj + vdrv
sbbz: zbgh + dnrv
lqcr: 2
rqns: 1
cqbc: djbd + lngs
wcqf: jfzj + ppfs
qqrd: 5
pvnr: pbpg * qbbt
gstw: jpsc - rjjz
zmwr: zrzq * jwdq
jdrl: 2
bvfp: 5
jcct: 6
twfg: 5
jtvj: nlbr * cldt
qrpb: 7
jzct: 3
fzhc: dmbm * hlbl
zptn: hmtq + bmmv
rwcp: wczm - mfrs
bvdz: 4
mvhf: qwmv * pssr
msbt: 7
hcrq: 3
hvmm: tcln * fbvh
vqvz: 6
mclg: 3
qdbn: 3
bpql: pfcv * pfqb
vthl: bgrw * lcns
nmvr: vbnh / lwvd
qwst: 3
bhbm: 3
bjwh: hqdh * rfvb
znnw: 2
jbjz: 6
qnht: 10
tlgh: 2
bcjp: 9
zcmt: 4
qwsl: fjzf / hnbr
sncr: 2
nlhj: cprv + hzjw
vwtf: nhjc * pbfn
rrjf: hvqt + gfmr
humn: 862
hrsn: 1
rtrs: vplq / svrs
lnzp: 4
ngbr: 17
qczj: tjdp * bvwq
fjhc: lgnb * rmrc
hlmm: 2
vhzb: 1
btmn: 7
znpm: 3
fgwj: 17
mhwd: 1
nmvc: fccf * frqq
lhbs: 2
bvcg: 5
gnsr: 3
qqhc: 11
cbhr: bjfh * zrcz
mtjt: slld * cdzn
vpjb: chtq + zcmt
lvhl: dmth + chgp
qmhw: gnsr * sbdq
dhbm: gtfn - gmhp
tccv: qzrj + hmgp
gnfz: 2
crfl: 2
dssr: 9
srbr: 8
qrbb: nnjh * dzpr
vcqp: ptlh / mnfc
lnsj: ngjl + zztn
tprp: 2
hdzl: nnvn / rjhd
rtlr: 10
dbws: 2
btjv: gggv + lbtd
jhlh: 4
jbft: 3
nvfc: fsvg * gtgb
hlld: flvd + bgcz
frlb: 4
ssrr: 3
gdfg: ccnq / llgj
svld: 5
sprl: 7
flbj: 3
nlcq: 7
hjpp: gwwn - nmcv
zhww: mwgt + vwpn
dcds: 4
ljvs: 9
hhbh: gdfg / tjzj
tznz: 5
jzzh: wwll * lbgq
chhc: 3
qmgj: wqpt + zplr
ftzb: 2
smgt: 8
zrbv: jllp + vnps
qqcj: tmcd * dbws
dfcv: nqgd - frsc
cnjr: 3
cnfp: 5
lrvv: nbnv * wcwd
wjwz: 8
qplm: tvlt + sgdp
ndhs: 2
ffnj: 9
dhrh: smvw * cwhw
hdmf: htzb * glwc
sbvr: fzhz + wmdg
bchh: 3
dfdj: mrsf + mpbh
gmsp: nqmj / nlfs
hggz: 11
ctpj: 11
lcmm: 1
snfr: vrdn * fqvh
nlvg: 1
pzct: dfcv + gvpn
qnvp: 2
jmfv: 16
gljf: 4
qlzh: rswz + mcrj
nmdh: 3
nnmf: 7
rrrv: rtvq / vzbv
jsgp: 6
ndln: hlbn * vprq
phbv: 3
gpmb: 4
mjgn: 5
dstj: hzfc * whcr
vwhd: ljvs * srhp
ttcm: 13
jfps: 2
wtvt: 2
qdtf: qdjt + hfrn
nvvm: bdtz * bfvt
fsnz: 2
nmcv: 10
hgcq: 3
dtmp: ppnh * mgtf
qstc: nqtb - dgvw
jfgg: 5
gnhp: rdbm + fplb
hzjw: 3
pndc: 2
pfsg: 3
nmbw: 4
tbhb: hbvb * twqf
sdgv: ppnj * mbpl
rqcl: 3
bgzl: 5
gwtt: 17
bpfp: 2
vhmg: 4
sgms: 5
wtcz: jfhm + gbbw
dcbh: jjmq + njhr
rfvb: jvwt * ghlq
trfj: 4
rpjw: 5
dzpr: 19
gljz: mjlf + vrmv
gbsj: wnng * wqgg
lppt: jsfz * trbw
fhpf: 15
dghv: 4
pzvd: 7
ghfj: 2
pjmq: dwws * jvhm
hzvm: vhmg + slhl
pghw: jldm + sgjq
smvm: ffrd + vwmv
rtsc: 3
lcrq: 3
lssj: 4
bwzr: qmfp + jtfb
jgvd: 5
qmdl: 8
rpgv: 3
pfnm: 5
mmrh: 2
vzmb: 2
rrmr: 3
vgrt: lwzf * njwn
ghmr: lpgs + stpf
gqsp: 2
szqv: 1
zdll: 4
ljng: 2
gbdf: gnwd * rrjh
fcdn: 3
cssv: ncwf + fgmb
pdqq: zwnz * pmfp
fbqz: 4
bhbj: 4
dgvh: vlmm * mgwh
mmjt: wdpw * lzml
shnv: 2
qqvp: swqj + nnmr
pfjj: hppz * mvhs
nqmj: jdlr * zfwl
qtnm: lghs + szhj
vzrf: 1
pnsp: rdpl + qtth
wgvv: 2
jdtf: 3
zqff: bdvd / vzql
whcr: pzfr * ddhm
ljst: 5
gjlh: 1
vbzz: 3
wbjc: rpps + gsdn
qslq: wjzp + bjfr
jvwt: 2
mjgp: cbhr + mdps
qtzh: mlmp * ndwc
vptl: rzpj / crvm
gvcr: 3
zffb: 5
tjlf: 5
mwgt: 5
qbjb: 2
jzzd: pndh * wgvv
tghn: mhbd * gzrw
ghcl: 5
bmvv: 3
dvcr: 4
bcfn: 2
fgbb: 3
ntsg: rswg + zvgp
crts: smqs + mjps
gjcr: dwwn + trmr
dgvw: spzq - qrjz
bfll: ghfj * dmbt
phcm: 2
bgws: gmgz + qmhw
jjpb: rspw + qcmh
zbch: 4
dmbt: lnsj + wwnp
shlv: rljl + vmdd
jrdp: dbdl - rrnr
hpcj: 3
tmbt: vfnj / rrnn
zjdz: vsht + vhts
slld: 7
hlbn: 5
bsjc: fcqz + jdwd
lqjp: 7
brdg: vcmd + zmwr
zlff: ljpw / cprj
pblg: 3
fqvj: jzvn * dldt
nvvr: lsww * ztjg
csgg: 2
dbhz: dgzh * qsfb
fggv: sftz * sccw
lfzz: jzfs / jmjt
rjjv: 3
tnmn: hfmg * mvgw
lbgq: 4
hdhb: dclr * tlcm
dstg: 2
rrzz: hmbh + nzbt
fjzf: qnvp * lfmv
znbn: 3
dlwc: mqsp + vhpg
hcnb: 2
wsvm: lnlf + qbrs
drpz: hbql - gpsp
pcml: hrzc * pblg
zflq: nbth + grtn
nwqf: 8
hpdv: zrgh + vrcq
tmcd: rcdc + cqwz
nlht: drwv * ljst
mbpl: 2
twdm: gcls + qplm
mntp: 2
ppjh: ljhz * qlzh
zjtp: 11
sgww: ldzr * rclr
vsjb: 4
hsdf: 14
thhb: 7
whvc: sgcz + nsgb
dhfw: wcqf + qltp
wdjw: dbdj * drsj
bntf: 11
lpgr: mpfl * ghds
pbqj: 1
mhdw: 2
zsdn: ncqz - rbmg
znht: snbg * vwtf
wgmc: 4
fbhh: ghdb / nfdc
gncc: 2
nmfp: 2
djbd: 6
bfgs: bnbj - pbmr
qbsm: wtcm + pnnc
rmct: czst / stpp
dpnz: wtvt * hfrj
vwmc: vhbb * rqcl
mlmh: 4
npjg: gvcr * tznz
cfbh: ddvd / sqlc
vjpl: vbvh + dzcq
mrgg: nlfw * zvgf
zbqd: 17
frhf: wpgn / fmcd
dpzp: pqdg * zqff
nlfj: 2
gwrm: jwqm + qgwj
zpmq: rqnb + mvhf
brqb: 2
vwjs: 11
lmwl: 3
tqwq: rnjv * rjsr
fllm: ftzb * ctqp
rrnn: 2
zhgg: dpzp / gszj
wtcm: nrrp + rtgq
mmzq: 13
phlb: 3
mmrw: jfpp + nwnv
lwrs: tpml * wvmt
twcq: ffpz / nqpg
gslf: 12
rrmp: qfvq * bpzp
cbfs: bsjc + dhjf
llhb: 5
svrs: 2
fbvh: 5
nlpc: jmfv - dlhc
hsfv: phjz * ntsg
zzqv: 2
tclq: fsdw * twcq
gssg: trtg / svjf
lhzp: 2
rvdr: mdbc * bfhw
rrjh: 2
ftqc: scsc * fcjj
pdtl: jrll + crfl
wjlf: 3
stlp: 3
fmhm: bqhc * tjrc
djsw: slrc - pqdf
gvpb: 3
bzzz: bfmm + whnw
fjcd: fpsr * vdgr
wntf: 3
vtnq: 3
lcns: 2
wmrq: 7
wvcw: 17
hwzz: 12
snjm: hpgg * wqld
tmcb: jmvq * qwqt
zztn: wtlc * jmlb
bsqb: npjf * gpvf
wtcf: qtnm - qdgd
zjmr: hrvc + mnbl
gbwp: nsvz * zwsw
mqsp: 7
tvwp: 3
vcmd: rhph + hwzz
ngjl: 19
nwvp: qmdl * stpz
rnjv: 3
hnlr: zqnw - shnp
jbzl: prpm * bmvv
gwjs: rfth - szzp
wpgn: gvgp * zmnp
zbnt: tgpd + cnhz
bjpg: qwhh * wbdw
hlrd: bpgv + trhb
mgwh: 5
ccdz: 5
pssr: 2
cllr: bhct - vjcv
tgpd: rvmw * zdll
cmrw: 1
ghsw: 3
hvqm: qglh + nhcw
lmzl: cvmw + rbtf
tdlb: gstw + mcsw
lssf: 5
jwsn: 11
wtqg: 2
brmb: cbcr - gqsw
hcpn: 2
cjrg: 3
zbdv: lrbp + rsmp
pzfr: zflq + tnsb
ndbd: srzf + fzjp
ztgp: 2
vfbj: 5
nggm: 5
ftwz: 6
jhlw: szct * wgjs
snrm: mqpv + flwr
bhjq: 2
tgdh: 2
qpqw: 8
wtlc: 3
hqbc: qrjb + zpmq
ttgb: tzcv / zqwc
pnlm: 7
jznz: vsnq * nhcf
mltm: 2
fljz: 4
gvml: prjh + dcds
jzvn: 2
bsvn: 9
pznl: rdtb + vccz
cwwq: 4
rvqj: 3
zfmh: vvcd * zmhj
wltq: 5
trds: 4
bwnj: 8
dzfw: 10
gggv: 3
tmnt: lgmd * qbhd
hpmg: 3
zfbf: 15
lvng: 2
wwhh: bhgw * fccs
bdrq: rbgm * rndt
sgjq: gbsj * gcnm
wdvz: tqpv + cjdc
trtv: cvbt + ssst
dsqq: stcm * pdhr
pfvw: sqph * btrv
vzgc: 4
qbrs: fjgm / hwdg
jjdw: 2
clfv: qwst * qpqt
qgfb: 2
flrd: 11
dhzz: tfwp / grpd
trqt: 5
svdm: jmzf * ndsc
dmbm: nvgt - tvtf
pqtb: njlz + cdlr
zlzc: 7
vlcd: pghw / bjdt
tqfv: 7
lqvd: nlhj * zttm
lngc: qtzv / hllr
qhbm: fvgc * mjlv
gpbf: 4
jdzv: csdp + cfwt
vsmg: psqs * bcdw
ngcc: 3
vqzq: lwgn + cnpg
zdlv: 2
nphd: 19
wwwf: 15
ftpc: 4
glwc: snfr + fmpv
tqpv: 8
crgw: 2
vsmv: mnsh + vsbn
pqbq: 2
ctbm: 12
fgmb: fjjn * tcnw
dbdl: 10
lfmv: grfl + mbml
pbpg: 4
lrrt: 5
zhcg: 3
bqhc: rzcw * qjwl
bmzh: jpcv + lcbt
bbsm: vlgr + vjnj
ncqz: pnqb * fcdr
jzfs: tlvz * nhqz
qrlv: 6
tzbm: hdfj + mtjt
hdvb: 2
sfgd: 3
vwmv: jnqw * cjzz
fpzf: 3
ntcr: njgb * lnbm
fccs: 12
frsc: gwbc + qjms
fcqz: nvfc / rjvc
ptct: dczq - fjht
qsph: 17
dmpm: 3
szvw: bdpl * sqvh
vscg: 2
fppn: hzzb * bphn
wpfr: 9
wwcj: 2
nttd: 11
mtnz: qwvl * pmsd
rmsr: 4
czbg: 2
qbgw: 3
bflt: 2
mmwv: cwsb * ljsm
ndwc: tbgw - fjcz
lpnd: 3
qsfb: vwgm + ftdf
smvw: 12
mjsl: 2
mpfl: 2
sjsf: 11
zmhj: 2
sjqp: hbqg * nwmm
vcnm: 5
wwlr: clfv + hvts
trjt: gvpb + zjdm
qslz: 5
qjms: 17
zjdm: 8
qtgg: 19
cjvp: 4
mfrs: qnmz * bbsm
gltp: 13
qhlt: rbzd * hrgq
npmd: clzs + vpcr
vwqz: ngcc + jghj
bqjf: 3
bdps: dtmp / vfvg
qjrd: 5
dtwl: 3
snng: 1
sgzs: lvmb * swbs
prjh: glzr - rvmp
vplq: qqhc * htnc
mppg: 3
rbgm: 4
jgvl: 5
fdgq: 16
nqmm: 3
nprv: 18
slmd: gndz * qzvw
snlw: 2
rznl: dstj + qtzh
wqpt: ztpm * qbwp
zljz: gddv + dmlf
qrch: wgmc * szgp
bgzw: zpdm + jhgt
znrj: 8
gtwf: 3
gfmm: 14
pwzv: wsrp * rbzl
hnqh: 8
qmfp: 1
lrlz: 2
mfmt: jsbb - fbwn
rbzd: 2
lbzg: mcct - gslb
bhgw: pwnc + jnvb
wttj: fggp + glcq
gpcz: 18
zlvl: 2
lgfg: 2
rzdh: dbsd - qbls
vgbm: 2
nsvz: rflf * vlqr
swht: hcjd + qgwz
vccz: hvcr * zsvc
ttcl: 2
zscf: 19
slnt: 3
gtct: szrw + gmnn
zsdb: 9
tvll: 2
cdvl: zjmr + ftrd
jhnh: 3
gtgb: rltj + pmnt
phlc: 5
brjh: gwmq + twfc
csdp: 5
dldt: 4
nsbs: 14
tpmq: 2
vbfr: 3
smqb: 2
hmft: jtph + bqhv
ghqq: 4
rbzl: 3
hnbr: 2
rhvb: bvfp * vvjw
zhtl: 6
cqln: 3
gnsw: lghw * wbsf
ndsc: fjmh + ccsm
hbfc: 7
cvfc: lrlz * zwhr
dhjf: ffcm + tlhp
rlnc: 3
gvjh: jnrj * bcwt
jsnr: gwgp * djpc
hztl: 8
hnbf: 5
nrmn: 5
fgqr: 7
jjdm: bpdd + dgwj
lsbc: 4
mwwd: hbzr - pdqp
qpqt: 13
lpnp: fvwj * jbnh
zpjh: grfc + jtcz
nwqt: 3
qbqp: zdlv + ttbm
nttf: 4
ffrl: 5
wlvl: 14
zwww: rtwv * hlzb
qlcn: 6
vngv: btbr - ztrd
ccmw: 5
qczt: mjgn + mhwd
rjjf: vdtv + ljng
wffd: gfjp * rpnd
gbcv: 4
vffr: jmph + mcpc
mqbj: 5
wfvv: 4
btcm: jvbd + pmdp
tfmt: 5
cwhw: nsct * rzgd
dzmw: 5
nvfj: 6
dnsn: gfjh - vlvn
gvgp: mdnj + jsfs
gfnh: 2
vqzn: 2
lqcl: jlzg + lpgc
ptpd: 2
msds: vnzz + rvqj
sqlc: 2
lnrq: 1
nlbg: ctgg + lnrq
gsfq: 2
tglb: hgqz + wrtg
lqnp: glgh + bpql
cvjq: qthr + nnjb
gndb: 9
brhd: 15
qjcs: fjpz / ndns
bphn: 3
vnzz: 4
zrdl: 1
jbnh: 3
tgvz: stws * vnqt
nhjc: 7
rltj: zfpt * ftzs
htzb: 11
lhlc: lgrl * tqwq
fzhz: 1
bzrh: mgct / rpgv
mrsf: vhlb - tmdf
dgvm: qqdg + dlwp
gvrv: wqqd * qpqw
jmsq: 6
vrzj: vrjs * wvgc
gvdb: slbd + cfln
fnnd: 2
vgtq: hzsw - jqzz
zpdm: mmsc + sprb
gcff: vvqz * fgbq
vljt: chgm * jvcs
hjhn: cjhd / nzhw
wczm: dmjc * wtns
lzlf: lvhl * mggm
mgzb: smgt + gjrz
qdgd: 8
jpmc: nwnm / trfm
sbdq: 3
lphc: lpgr / zmzc
qtms: 6
cpvn: mdcn * gtct
""")
