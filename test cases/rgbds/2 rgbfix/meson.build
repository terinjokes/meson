project('rgbds-test', 'rgbds')

rgbds = import('rgbds')

rom = executable('rgbdstest', 'src/main.asm',
                 include_directories: ['include'],
                 link_language: 'rgbds')

rgbds.fix('rgbdstest.gb', rom,
         title: 'EXAMPLE',
         mbc_type: 'ROM',
         fix_spec: 'lhg')
