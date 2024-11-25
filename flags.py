
# Define possible GCC optimization flags
FLAGS = [
    '-O0', '-O1', '-O2', '-O3', '-Os', '-Ofast',
    '-fdata-sections', '-ffunction-sections',
    '-fno-exceptions', '-fno-rtti',
    '-fomit-frame-pointer', '-fno-inline',
    '-flto', '-fno-fat-lto-objects',
    '-foptimize-strlen', '-fdelete-null-pointer-checks',
    '-ffast-math', '-fno-builtin'
]
