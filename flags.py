
# Define possible GCC optimization flags
FLAGS = [
    '-Os',
    '-faggressive-loop-optimizations', '-falign-functions', 
    '-falign-loops', '-fassociative-math', 
    '-fdata-sections', '-ffunction-sections',
    '-fno-exceptions', '-fno-rtti',
    '-fomit-frame-pointer', '-fno-inline',
    '-flto', '-fno-fat-lto-objects',
    '-foptimize-strlen', '-fdelete-null-pointer-checks',
    '-ffast-math', '-fno-builtin', '-fassume-phsa', 
    '-fasynchronous-unwind-tables', '-fauto-inc-dec', 
    '-fbit-tests', '-fbranch-count-reg', '-fbranch-probabilities' , 
    '-fcaller-saves', '-fcode-hoisting', '-fcombine-stack-adjustments', 
    '-fcompare-elim', '-fconserve-stack', '-fcprop-registers', 
    '-fcrossjumping',
 '-floop-interchange',
  '-floop-nest-optimize',
  '-floop-parallelize-all',
  '-floop-unroll-and-jam',
  '-flra-remat',
  '-fmath-errno',
  '-fmodulo-sched',
  '-fmodulo-sched-allow-regmoves',
  '-fmove-loop-invariants',
  '-fnon-call-exceptions',
  '-fnothrow-opt',
  '-fomit-frame-pointer',
  '-fopt-info',
  '-foptimize-sibling-calls',
  '-foptimize-strlen',
  '-fpack-struct',
  '-fsched2-use-superblocks',
'-fschedule-fusion',
'-fschedule-insns',
'-fschedule-insns2',
'-fsection-anchors',
'-fsel-sched-pipelining',
'-fsel-sched-pipelining-outer-loops',
'-fsel-sched-reschedule-pipelined',
'-fselective-scheduling',
'-fselective-scheduling2',
'-fshort-enums',
'-fshort-wchar',
'-fshrink-wrap',
'-fshrink-wrap-separate',
'-fsignaling-nans',
'-fsigned-zeros',
 '-fstrict-volatile-bitfields',
'-fthread-jumps',
'-fno-threadsafe-statics',
'-ftoplevel-reorder',
'-ftracer',
'-ftrapping-math',
'-ftrapv',
'-ftree-bit-ccp',
'-ftree-builtin-call-dce',
'-ftree-ccp',
'-ftree-ch',
'-ftree-coalesce-vars',
'-ftree-copy-prop',
'-ftree-cselim',
'-ftree-dce',
'-ftree-dominator-opts',
'-ftree-dse',
'-ftree-forwprop',
'-ftree-fre',
 '-ftree-loop-distribute-patterns',
'-ftree-loop-distribution',
'-ftree-loop-if-convert',
'-ftree-loop-im',
'-ftree-loop-ivcanon',
'-ftree-loop-optimize',
'-ftree-loop-vectorize',
'-ftree-lrs',
  '-ftree-partial-pre',
  '-ftree-phiprop',
  '-ftree-pre',
  '-ftree-pta',
  '-ftree-reassoc',
  '-ftree-scev-cprop',
  '-ftree-sink',
  '-ftree-slp-vectorize',
  '-ftree-slsr',
  '-ftree-sra',
  '-ftree-switch-conversion',
  '-ftree-tail-merge',
  '-ftree-ter',
  '-ftree-vectorize',
  '-ftree-vrp',
  '-funconstrained-commons',
  '-funroll-completely-grow-size',
  '-funroll-loops',
  '-funsafe-math-optimizations',
  '-funswitch-loops',
  '-funwind-tables',
  '-fvar-tracking',
  '-fvar-tracking-assignments',
  '-fvar-tracking-assignments-toggle',
  '-fvar-tracking-uninit',
  '-fvariable-expansion-in-unroller',]


