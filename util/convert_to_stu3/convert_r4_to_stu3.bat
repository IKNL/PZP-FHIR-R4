@echo off
setlocal

:: --- User Configuration ---

:: 1. Set the path to the official FHIR Validator JAR file.
set "VALIDATOR_JAR=./validator_cli.jar"

:: 2. Set the path to the directory containing the R4 to STU3.map files.
::    This should be the 'r4' folder from the interversion download.
set "MAPS_ROOT_DIR=C:\git\iknl-pzp-fhir-r4\util\convert_to_stu3\interversion-r4to3\r4\R4toR3"

:: 3. Set the name of the specific.map file to use for the transformation.
::    This should be the official name from the interversion repository.
set "MAP_FILE=StructureDefinition.map"

:: 4. Set the specific R4 input file to transform.
set "INPUT_FILE=../../fsh-generated/resources/StructureDefinition-ACP-Encounter.json"

:: 5. Set the output file name for the STU3 resource.
set "OUTPUT_FILE=StructureDefinition-ACP-Encounter-STU3.json"


:: --- Script ---

:: Get the directory where this script is located
set "BASE_DIR=%~dp0"

:: Define full paths
set "FULL_MAP_FILE_PATH=%MAPS_ROOT_DIR%\%MAP_FILE%"
set "FULL_INPUT_FILE=%BASE_DIR%%INPUT_FILE%"
set "FULL_OUTPUT_FILE=%BASE_DIR%fsh-generated-stu3\%OUTPUT_FILE%"

:: Parameter check...
if not exist "%VALIDATOR_JAR%" (
    echo ERROR: Validator JAR not found at "%VALIDATOR_JAR%". Please edit the script.
    goto :eof
)
if not exist "%FULL_MAP_FILE_PATH%" (
    echo ERROR: The specified map file was not found at "%FULL_MAP_FILE_PATH%". Please check the MAPS_ROOT_DIR and MAP_FILE variables.
    goto :eof
)
if not exist "%FULL_INPUT_FILE%" (
    echo ERROR: Input file not found at "%FULL_INPUT_FILE%". Please edit the script.
    goto :eof
)
if not exist "%BASE_DIR%fsh-generated-stu3" mkdir "%BASE_DIR%fsh-generated-stu3"

echo Starting FHIR R4 to STU3 conversion...
echo ========================================
echo Input file: %FULL_INPUT_FILE%
echo Map file:   %FULL_MAP_FILE_PATH%
echo Output file:  %FULL_OUTPUT_FILE%
echo.

:: Construct and execute the transformation command
:: -transform must be the canonical URL of the map.
:: -version specifies the source file's FHIR version.
:: -ig tells the validator where to load the map file from.
:: -ig also loads the target FHIR specification (STU3).
java -Xmx2g -jar "%VALIDATOR_JAR%" "%FULL_INPUT_FILE%" -transform "http://hl7.org/fhir/StructureMap/StructureDefinition4to3" -version 4.0.1 -ig "%MAPS_ROOT_DIR%" -output "%FULL_OUTPUT_FILE%"

if errorlevel 1 (
    echo ERROR: Conversion failed!
) else (
    echo SUCCESS: Conversion completed!
)

echo.
echo ========================================
echo Your STU3 file is at: %FULL_OUTPUT_FILE%
echo.

endlocal
pause
goto :eof