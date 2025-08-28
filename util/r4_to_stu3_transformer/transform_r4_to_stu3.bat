@echo off
REM FHIR R4 to STU3 Transformer - Convenience shortcut for PZP project
REM Automatically discovers and transforms all supported resources

echo === FHIR R4 to STU3 Transformer (PZP Project) ===
echo.

REM Check if input directory exists
if not exist "..\..\R4\fsh-generated\resources" (
    echo ERROR: R4 output directory not found
    echo Please ensure R4 IG has been built first
    pause
    exit /b 1
)

echo Transforming resources from R4 to STU3...
echo Input: ..\..\R4\fsh-generated\resources
echo Output: ..\..\STU3\input\resources
echo.
echo Auto-discovering available transformers...
echo.

REM Run the Python transformer (auto-discovers all transformers)
python fhir_r4_to_stu3_transformer.py "..\..\R4\fsh-generated\resources" "..\..\STU3\input\resources"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Transformation failed with exit code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo SUCCESS: Transformation completed!
echo Converted files are in: ..\STU3\input\resources\
echo.
echo TIP: To transform other resources, use:
echo   python fhir_r4_to_stu3_transformer.py input_dir output_dir --resources ResourceType
echo.
pause
