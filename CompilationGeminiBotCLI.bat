@echo off
title Compilation de GeminiBot CLI - Edition by Soufianne Nassibi
color 0A

echo ==========================================
echo    Compilation GeminiBot CLI
echo ==========================================
echo.

:: Aller dans le dossier du script automatiquement
cd /d %~dp0

:: Nettoyer les anciens builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist gemini_cli.spec del gemini_cli.spec

:: Créer le dossier install\ si absent
if not exist install (
    mkdir install
    echo  Dossier install créé.
)

:: Compiler le .exe avec PyInstaller
pyinstaller --onefile --icon=icon.ico gemini_cli.py

if %errorlevel% neq 0 (
    echo  Erreur lors de la compilation avec PyInstaller !
    pause
    exit /b
)

echo.
echo ==========================================
echo    Compilation .exe terminée !
echo ==========================================
echo.

:: Lancer Inno Setup automatiquement
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo  Lancement de la création du setup avec Inno Setup...
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" GeminiBotInstaller.iss
) else (
    echo  Inno Setup non trouvé !
    pause
    exit /b
)

echo.
echo ==========================================
echo    Setup GeminiBotInstaller.exe généré !
echo ==========================================
echo.
pause
exit /b
