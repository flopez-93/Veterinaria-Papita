@echo off
setlocal

REM ============================================================
REM Papita Veterinaria - Iniciar API + Frontend
REM ============================================================

REM Usa la carpeta donde esta este archivo BAT
set "PROJECT_DIR=%~dp0"

REM Nombre del frontend
set "FRONT_FILE=papita_veterinaria_front_conectado_api_corregido_v3.html"

REM Buscar entorno virtual dentro del proyecto
if exist "%PROJECT_DIR%\.venv\Scripts\activate.bat" (
    set "VENV_ACTIVATE=%PROJECT_DIR%\.venv\Scripts\activate.bat"
) else if exist "%PROJECT_DIR%\venv\Scripts\activate.bat" (
    set "VENV_ACTIVATE=%PROJECT_DIR%\venv\Scripts\activate.bat"
) else (
    set "VENV_ACTIVATE="
)

echo.
echo ============================================
echo  Iniciando Papita Veterinaria
echo ============================================
echo Proyecto: %PROJECT_DIR%
echo Frontend: %FRONT_FILE%
echo.

if "%VENV_ACTIVATE%"=="" (
    echo AVISO: No se encontro entorno virtual .venv o venv.
    echo Se intentara ejecutar con Python instalado en el sistema.
    echo.
    start "Papita Veterinaria API" cmd /k "cd /d ""%PROJECT_DIR%"" && python -m uvicorn main:app --reload"
) else (
    echo Entorno: %VENV_ACTIVATE%
    echo Levantando API FastAPI en una ventana nueva...
    start "Papita Veterinaria API" cmd /k "cd /d ""%PROJECT_DIR%"" && call ""%VENV_ACTIVATE%"" && python -m uvicorn main:app --reload"
)

echo Esperando 5 segundos para que arranque la API...
timeout /t 5 /nobreak >nul

echo Abriendo frontend...

if exist "%PROJECT_DIR%\%FRONT_FILE%" (
    start "" "%PROJECT_DIR%\%FRONT_FILE%"
) else (
    echo.
    echo AVISO: No encontre el frontend:
    echo %PROJECT_DIR%\%FRONT_FILE%
    echo.
    echo Abro Swagger como respaldo.
    start "" "http://127.0.0.1:8000/docs"
)

echo.
echo Listo.
echo API: http://127.0.0.1:8000
echo Swagger: http://127.0.0.1:8000/docs
echo.
pause