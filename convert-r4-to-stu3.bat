@echo off
REM =====================================
REM FHIR R4 to STU3 IG Integration Script
REM =====================================
REM
REM This script integrates FHIR R4 to STU3 conversion 
REM into the IG development workflow.

echo =====================================
echo FHIR IG R4-to-STU3 Integration
echo =====================================

REM Navigate to the converter directory
cd /d "%~dp0\util\r4-to-r3-converter\fhirconverter"

echo.
echo 1. Checking R4 source directory...
if not exist "..\..\..\R4\fsh-generated\resources\*.json" (
    echo ❌ Error: No R4 resources found in R4\fsh-generated\resources\
    echo    Please run the R4 IG Publisher first: R4\_genonce.bat
    echo.
    pause
    exit /b 1
)

echo ✅ R4 resources found

echo.
echo 2. Creating STU3 resources directory if needed...
if not exist "..\..\..\STU3\input\resources\" mkdir "..\..\..\STU3\input\resources\"
echo ✅ STU3 resources directory ready

echo.
echo 3. Running R4 to STU3 conversion...
call convert.bat
if errorlevel 1 (
    echo ❌ Conversion failed!
    pause
    exit /b 1
)

echo.
echo 4. Running conversion analysis...
cd ..
python analyze_conversion.py
if errorlevel 1 (
    echo ⚠️  Analysis failed, but conversion completed successfully
)

echo.
echo =====================================
echo ✅ R4-to-STU3 Integration Complete!
echo =====================================
echo.
echo Next steps:
echo 1. Review CONVERSION_ANALYSIS_REPORT.md for details
echo 2. Build the STU3 IG: cd STU3 ^&^& _genonce.bat
echo 3. Compare R4 and STU3 implementation guides
echo 4. Commit your changes to git
echo.
pause
