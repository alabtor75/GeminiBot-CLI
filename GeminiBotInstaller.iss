; Script d'installation GeminiBot CLI - Edition Soufianne Nassibi

[Setup]
AppName=GeminiBot CLI
AppVersion=1.0
DefaultDirName={pf}\GeminiBot_CLI
DefaultGroupName=GeminiBot CLI
OutputDir=install
OutputBaseFilename=GeminiBotInstaller
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
SetupIconFile=icon.ico
LicenseFile=LICENSE.txt

AppPublisher=Soufianne Nassibi
AppPublisherURL=https://github.com/alabtor75
AppSupportURL=https://github.com/alabtor75
AppUpdatesURL=https://github.com/alabtor75
AppCopyright=© 2025 Soufianne Nassibi

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le bureau"; GroupDescription: "Options supplémentaires :"

[Files]
Source: "dist\gemini_cli.exe"; DestDir: "{app}"; Flags: ignoreversion replacesameversion restartreplace
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "INSTALL.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\history"

[Icons]
Name: "{group}\GeminiBot CLI"; Filename: "{app}\gemini_cli.exe"; Flags: createonlyiffileexists
Name: "{commondesktop}\GeminiBot CLI"; Filename: "{app}\gemini_cli.exe"; Tasks: desktopicon; Flags: createonlyiffileexists

[Run]
Filename: "{app}\gemini_cli.exe"; Description: "Lancer GeminiBot CLI maintenant"; Flags: nowait postinstall skipifsilent shellexec unchecked

[Messages]
WelcomeLabel1=Bienvenue dans l'installation de GeminiBot CLI
WelcomeLabel2=Cet assistant va vous guider pour installer GeminiBot CLI sur votre ordinateur.
FinishedLabel=GeminiBot CLI a été installé avec succès. Merci pour votre confiance !

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\GeminiBot_CLI"
Type: filesandordirs; Name: "{app}\history"
Type: filesandordirs; Name: "{app}"
