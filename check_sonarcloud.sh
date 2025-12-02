#!/bin/bash

# Script untuk cek settings SonarCloud project
# Usage: ./check_sonarcloud.sh <SONAR_TOKEN>

if [ -z "$1" ]; then
    echo "❌ Error: SONAR_TOKEN required"
    echo "Usage: ./check_sonarcloud.sh <SONAR_TOKEN>"
    echo ""
    echo "Cara dapat token:"
    echo "1. Login ke https://sonarcloud.io"
    echo "2. Account > Security > Generate Token"
    exit 1
fi

TOKEN="$1"
PROJECT_KEY="Posind-HCIS_hrms_custom"
ORG="posind-hcis"

echo "🔍 Checking SonarCloud project settings..."
echo "Project: $PROJECT_KEY"
echo "Organization: $ORG"
echo ""

# Check project existence
echo "📊 Project Info:"
curl -s -u "$TOKEN:" \
    "https://sonarcloud.io/api/projects/search?projects=$PROJECT_KEY" | \
    jq '.components[] | {key: .key, name: .name, visibility: .visibility}'

echo ""
echo "⚙️ Project Settings:"
curl -s -u "$TOKEN:" \
    "https://sonarcloud.io/api/settings/values?component=$PROJECT_KEY" | \
    jq '.settings[] | select(.key | contains("sonar")) | {key: .key, value: .value}'

echo ""
echo "🔧 Analysis Settings:"
curl -s -u "$TOKEN:" \
    "https://sonarcloud.io/api/settings/values?component=$PROJECT_KEY&keys=sonar.autoscan" | \
    jq '.settings[]'

echo ""
echo "✅ Done! Check output above for 'sonar.autoscan' setting"
echo "If sonar.autoscan=true, that's the problem!"
