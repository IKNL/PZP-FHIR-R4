@echo off
echo ========================================
echo FHIR R4 to STU3 Batch Converter
echo ========================================
echo.

cd /d "%~dp0"

if not exist "target\classes" (
    echo Compiling Java project...
    call mvn compile
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Compilation failed!
        pause
        exit /b 1
    )
    echo.
)

echo Starting FHIR conversion...
echo.

call mvn exec:java -Dexec.mainClass="FhirBatchConverter"

echo.
echo ========================================
echo Conversion complete!
echo ========================================
pause
