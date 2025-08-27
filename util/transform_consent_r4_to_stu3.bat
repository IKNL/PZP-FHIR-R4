@echo off
REM Consent R4 to STU3 Transformer
REM Transforms FHIR Consent resources from R4 to STU3 using Python

echo === Consent R4 to STU3 Transformer ===
echo.

cd /d "%~dp0"

REM Check if input directory exists
if not exist "..\R4\fsh-generated\resources" (
    echo ERROR: R4 output directory not found
    echo Please ensure R4 IG has been built first
    pause
    exit /b 1
)

REM Create output directory if it doesn't exist
if not exist "..\STU3\input\resources" (
    mkdir "..\STU3\input\resources"
)

echo Transforming Consent resources from R4 to STU3...
echo Input: ..\R4\output
echo Output: ..\STU3\input\resources
echo.

REM Run the Python transformer
python consent_r4_to_stu3_transformer.py "..\R4\fsh-generated\resources" "..\STU3\input\resources" --pattern "*Consent*.json"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Transformation failed with exit code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo SUCCESS: Consent transformation completed!
echo Converted files are in: ..\STU3\input\resources\
echo.
pause
