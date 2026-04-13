from PyInstaller import __main__

__main__.run([
    'Quake3_CFG_Generator.1.0.4.py',
    '--noconsole',
    '--onefile',
    '--windowed',
    '--distpath', 'dist',
    '--name', 'Quake3_CFG_Generator'
])
