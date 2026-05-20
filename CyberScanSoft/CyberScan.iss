; CyberScan Dashboard - Inno Setup Installer
; Simple and clean installation like any professional software

[Setup]
AppName=CyberScan Dashboard
AppVersion=1.0.0
DefaultDirName={autopf}\CyberScan
DefaultGroupName=CyberScan
AllowNoIcons=yes
OutputDir=.\dist
OutputBaseFilename=CyberScan-Setup
Compression=lzma2
SolidCompression=yes
LicenseFile=.\LICENSE.txt
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Components]
Name: "main"; Description: "CyberScan Dashboard"; Types: full custom; Flags: fixed

[Files]
Source: "dist\CyberScan.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\scans"; Permissions: everyone-modify

[Icons]
Name: "{group}\CyberScan Dashboard"; Filename: "{app}\CyberScan.exe"; Comment: "Network Security Scanner"
Name: "{group}\Uninstall CyberScan"; Filename: "{uninstallexe}"
Name: "{autodesktop}\CyberScan Dashboard"; Filename: "{app}\CyberScan.exe"; Comment: "Network Security Scanner"

[Run]
Filename: "{app}\CyberScan.exe"; Description: "Launch CyberScan Dashboard"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"

