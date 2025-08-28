@echo off
setlocal enabledelayedexpansion

echo FHIR STU3 Resource Validation Script (Advanced)
echo ===============================================
echo.

REM Configuration
set VALIDATOR_JAR=input-cache\validator_cli.jar
set FHIR_VERSION=3.0.2
set RESOURCES_DIR=temp_files
set LOG_DIR=validation_logs
set TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

REM Create log directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Check if validator exists
if not exist "%VALIDATOR_JAR%" (
    echo ERROR: FHIR Validator not found at %VALIDATOR_JAR%
    echo.
    echo To download the validator:
    echo 1. Go to: https://github.com/hapifhir/org.hl7.fhir.core/releases
    echo 2. Download validator_cli.jar from the latest release
    echo 3. Place it in this directory: %CD%
    echo.
    pause
    exit /b 1
)

REM Parse command line arguments
set TARGET=%1
if "%TARGET%"=="" set TARGET=all

echo Validation target: %TARGET%
echo FHIR Version: %FHIR_VERSION%
echo Timestamp: %TIMESTAMP%
echo.

REM Set up file patterns based on target
if /i "%TARGET%"=="all" (
    set FILE_PATTERN=*.json
    set LOG_FILE=%LOG_DIR%\validation_all_%TIMESTAMP%.log
) else if /i "%TARGET%"=="profiles" (
    set FILE_PATTERN=StructureDefinition-*.json
    set LOG_FILE=%LOG_DIR%\validation_profiles_%TIMESTAMP%.log
) else if /i "%TARGET%"=="examples" (
    set FILE_PATTERN=*.json
    set LOG_FILE=%LOG_DIR%\validation_examples_%TIMESTAMP%.log
    REM Exclude StructureDefinitions, ValueSets, etc. for examples-only validation
) else if /i "%TARGET%"=="valuesets" (
    set FILE_PATTERN=ValueSet-*.json
    set LOG_FILE=%LOG_DIR%\validation_valuesets_%TIMESTAMP%.log
) else (
    REM Assume it's a specific file
    set FILE_PATTERN=%TARGET%
    set LOG_FILE=%LOG_DIR%\validation_single_%TIMESTAMP%.log
)

echo Validation started at %date% %time% > "%LOG_FILE%"
echo Target: %TARGET% >> "%LOG_FILE%"
echo File pattern: %FILE_PATTERN% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

set /a TOTAL_FILES=0
set /a VALID_FILES=0
set /a INVALID_FILES=0
set /a WARNING_FILES=0

echo Starting validation...
echo.

for %%f in ("%RESOURCES_DIR%\%FILE_PATTERN%") do (
    if exist "%%f" (
        set /a TOTAL_FILES+=1
        echo [!TOTAL_FILES!] Validating: %%~nxf
        echo ==================== %%~nxf ==================== >> "%LOG_FILE%"
        echo File: %%f >> "%LOG_FILE%"
        echo Validation started: !time! >> "%LOG_FILE%"
        echo. >> "%LOG_FILE%"
        
        REM Run validator with detailed output
        java -jar "%VALIDATOR_JAR%" "%%f" -version %FHIR_VERSION% -tx n/a -output-style compact >> "%LOG_FILE%" 2>&1
        
        REM Check return code and analyze output
        if !errorlevel! equ 0 (
            REM Check for warnings in the output
            findstr /C:"Warning" "%LOG_FILE%" >nul 2>&1
            if !errorlevel! equ 0 (
                echo   [VALID with WARNINGS] %%~nxf
                echo   STATUS: VALID WITH WARNINGS >> "%LOG_FILE%"
                set /a WARNING_FILES+=1
                set /a VALID_FILES+=1
            ) else (
                echo   [VALID] %%~nxf
                echo   STATUS: VALID >> "%LOG_FILE%"
                set /a VALID_FILES+=1
            )
        ) else (
            echo   [INVALID] %%~nxf - Check log for details
            echo   STATUS: INVALID >> "%LOG_FILE%"
            set /a INVALID_FILES+=1
        )
        
        echo Validation completed: !time! >> "%LOG_FILE%"
        echo. >> "%LOG_FILE%"
    )
)

if !TOTAL_FILES! equ 0 (
    echo No files found matching pattern: %FILE_PATTERN%
    echo Check that files exist in: %RESOURCES_DIR%
    goto :end
)

echo.
echo ===============================================
echo Validation Summary
echo ===============================================
echo Target: %TARGET%
echo Total files processed: !TOTAL_FILES!
echo Valid files: !VALID_FILES!
echo Files with warnings: !WARNING_FILES!
echo Invalid files: !INVALID_FILES!
echo ===============================================
echo.
echo Detailed results saved to: %LOG_FILE%

if !INVALID_FILES! gtr 0 (
    echo.
    echo ⚠️  WARNING: !INVALID_FILES! files have validation errors.
    echo Please check the log file for details.
)

if !WARNING_FILES! gtr 0 (
    echo.
    echo ℹ️  INFO: !WARNING_FILES! files have warnings.
    echo Review the log file for potential issues.
)

:end
echo.
echo Usage examples:
echo   %~nx0           - Validate all resources
echo   %~nx0 profiles  - Validate only StructureDefinitions
echo   %~nx0 valuesets - Validate only ValueSets
echo   %~nx0 examples  - Validate example instances
echo   %~nx0 Patient-*.json - Validate specific file pattern
echo.
echo Press any key to exit...
pause >nul
