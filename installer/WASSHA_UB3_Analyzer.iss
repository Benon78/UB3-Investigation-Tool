#define MyAppName "WASSHA UB3 Analyzer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Benon Art & Technology"
#define MyAppExeName "WASSHA_UB3_Analyzer.exe"

[Setup]
AppId={{8F9D1E52-7C0B-4A5E-8D2C-123456789ABC}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

OutputDir=output
OutputBaseFilename=WASSHA_UB3_Analyzer_v1.0.0

Compression=lzma
SolidCompression=yes
WizardStyle=modern

SetupIconFile=..\assets\icons\app.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop Shortcut"; Flags: unchecked

[Files]
Source: "..\dist\WASSHA_UB3_Analyzer\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WASSHA UB3 Analyzer"; Filename: "{app}\WASSHA_UB3_Analyzer.exe"
Name: "{autodesktop}\WASSHA UB3 Analyzer"; Filename: "{app}\WASSHA_UB3_Analyzer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WASSHA_UB3_Analyzer.exe"; Description: "Launch WASSHA UB3 Analyzer"; Flags: nowait postinstall skipifsilent