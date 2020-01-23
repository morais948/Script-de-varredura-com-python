from cx_Freeze import setup, Executable

# executable options
script = 'T10_GUI.py'
base = 'Win32GUI'       # Win32GUI para gui's e None para console
icon = 'icon_64.ico'
targetName = 'CivCom Diagram Calculator.exe'

# build options
packages = ['matplotlib', 'atexit', 'PyQt4.QtCore', 'tkinter']
includes = []
include_files = ['icon_64.png', 'logo-90.png']

# shortcut options
shortcut_name = 'Diagram Calculator'

# bdist_msi options
company_name = 'CivCom UnB'
product_name = 'Diagram Calculator'
upgrade_code = '{66620F3A-DC3A-11E2-B341-002219E9B01E}'
add_to_path = False

# setup options
name = 'CivCom Diagram Calculator'
version = '0.1'
description = 'Bending moment diagram calculator'

"""
Edit the code above this comment.
Don't edit any of the code bellow.
"""

msi_data = {'Shortcut': [
    ("DesktopShortcut",         # Shortcut
     "DesktopFolder",           # Directory_
     shortcut_name,      # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]/{}".format(targetName),  # Target
     None,                      # Arguments
     None,                      # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     "TARGETDIR",               # WkDir
     ),

    ("ProgramMenuShortcut",         # Shortcut
     "ProgramMenuFolder",           # Directory_
     shortcut_name,      # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]/{}".format(targetName),  # Target
     None,                      # Arguments
     None,                      # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     "TARGETDIR",               # WkDir
     )
    ]
}

opt = {
    'build_exe': {'packages': packages,
                  'includes': includes,
                  'include_files': include_files
                  },
    'bdist_msi': {'upgrade_code': upgrade_code,
                  'add_to_path': add_to_path,
                  'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
                  'data': msi_data
                  }
}

exe = Executable(
    script=script,
    base=base,
    icon=icon,
    targetName=targetName,
    # shortcutName=shortcut_name,
    # shortcutDir='DesktopFolder'
)

setup(name=name,
      version=version,
      description=description,
      options=opt,
      executables=[exe]
      )
