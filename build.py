from PyInstaller import __main__

__main__.run([
    'Quake3_CFG_Generator.py',
    '--noconsole',
    '--onefile',
    '--windowed',
    '--distpath', 'dist',
    '--name', 'Quake3_CFG_Generator'
])