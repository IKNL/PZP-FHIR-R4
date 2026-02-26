@ECHO OFF
ECHO Installing mitmproxy certificate to Java truststore...

REM Get the certificate from the running Docker container
docker cp nts-proxy-nts-proxy-1:/root/.mitmproxy/mitmproxy-ca-cert.pem %TEMP%\mitmproxy-ca-cert.pem

IF NOT EXIST "%TEMP%\mitmproxy-ca-cert.pem" (
    ECHO Failed to extract certificate from Docker container
    ECHO Make sure the NTS proxy is running: docker-compose up -d
    PAUSE
    EXIT /B 1
)

REM Find Java installation
FOR /F "tokens=*" %%i IN ('java -XshowSettings:properties -version 2^>^&1 ^| findstr "java.home"') DO SET JAVA_HOME_LINE=%%i
FOR /F "tokens=2*" %%a IN ("%JAVA_HOME_LINE%") DO SET JAVA_HOME=%%b

IF NOT EXIST "%JAVA_HOME%\lib\security\cacerts" (
    ECHO Could not find Java cacerts file at "%JAVA_HOME%\lib\security\cacerts"
    PAUSE
    EXIT /B 1
)

ECHO Found Java at: "%JAVA_HOME%"
ECHO.
ECHO Removing old mitmproxy certificate if it exists...
"%JAVA_HOME%\bin\keytool" -delete -alias mitmproxy -keystore "%JAVA_HOME%\lib\security\cacerts" -storepass changeit -noprompt 2>nul

ECHO Importing new certificate to Java truststore...
ECHO This requires administrator privileges.
ECHO Default keystore password is: changeit
ECHO.

"%JAVA_HOME%\bin\keytool" -import -trustcacerts -alias mitmproxy -file "%TEMP%\mitmproxy-ca-cert.pem" -keystore "%JAVA_HOME%\lib\security\cacerts" -storepass changeit -noprompt

IF %ERRORLEVEL% EQU 0 (
    ECHO.
    ECHO Certificate installed successfully!
    ECHO You can now use the NTS proxy with HTTPS connections.
) ELSE (
    ECHO.
    ECHO Failed to install certificate. You may need to run this script as Administrator.
)

DEL "%TEMP%\mitmproxy-ca-cert.pem"
PAUSE
