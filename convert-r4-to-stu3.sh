#!/bin/bash
#=====================================
# FHIR R4 to STU3 IG Integration Script
#=====================================
#
# This script integrates FHIR R4 to STU3 conversion 
# into the IG development workflow.

echo "====================================="
echo "FHIR IG R4-to-STU3 Integration"
echo "====================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to the converter directory
cd "$SCRIPT_DIR/util/r4-to-r3-converter/fhirconverter"

echo ""
echo "1. Checking R4 source directory..."
if [ ! -d "../../../R4/fsh-generated/resources" ] || [ -z "$(ls -A ../../../R4/fsh-generated/resources/*.json 2>/dev/null)" ]; then
    echo "❌ Error: No R4 resources found in R4/fsh-generated/resources/"
    echo "   Please run the R4 IG Publisher first: R4/_genonce.sh"
    echo ""
    exit 1
fi

echo "✅ R4 resources found"

echo ""
echo "2. Creating STU3 resources directory if needed..."
mkdir -p "../../../STU3/input/resources/"
echo "✅ STU3 resources directory ready"

echo ""
echo "3. Running R4 to STU3 conversion..."

# Check if Maven is available
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven not found. Please install Maven to continue."
    exit 1
fi

# Build and run converter
mvn clean compile dependency:copy-dependencies > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Maven build failed!"
    exit 1
fi

# Run the converter
java -cp "target/classes:target/dependency/*" FhirBatchConverter

if [ $? -ne 0 ]; then
    echo "❌ Conversion failed!"
    exit 1
fi

echo ""
echo "4. Running conversion analysis..."
cd ..
python3 analyze_conversion.py
if [ $? -ne 0 ]; then
    echo "⚠️  Analysis failed, but conversion completed successfully"
fi

echo ""
echo "====================================="
echo "✅ R4-to-STU3 Integration Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Review CONVERSION_ANALYSIS_REPORT.md for details"
echo "2. Build the STU3 IG: STU3/_genonce.sh"
echo "3. Compare R4 and STU3 implementation guides"
echo ""
