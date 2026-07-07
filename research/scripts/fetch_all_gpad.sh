#!/bin/bash
# Download each GPAD practice-level release, aggregate to practice x month, delete raw.
cd /sessions/bold-zealous-knuth/mnt/outputs
mkdir -p gpad_agg
declare -A URLS=(
 [Feb_26]="https://files.digital.nhs.uk/BC/A65BD0/Practice_Level_Crosstab_Feb_26.zip"
 [Nov_25]="https://files.digital.nhs.uk/7D/783CF6/Practice_Level_Crosstab_Nov_25.zip"
 [Aug_25]="https://files.digital.nhs.uk/39/0079F3/Practice_Level_Crosstab_Aug_25.zip"
 [May_25]="https://files.digital.nhs.uk/F4/911CA1/Practice_Level_Crosstab_May_25.zip"
 [Feb_25]="https://files.digital.nhs.uk/25/BE5D56/Practice_Level_Crosstab_Feb_25.zip"
 [Nov_24]="https://files.digital.nhs.uk/87/0DC7D3/Practice_Level_Crosstab_Nov_24.zip"
 [Aug_24]="https://files.digital.nhs.uk/47/0882D1/Practice_Level_Crosstab_Aug_24.zip"
 [May_24]="https://files.digital.nhs.uk/F4/75B274/Practice_Level_Crosstab_May_24.zip"
 [Feb_24]="https://files.digital.nhs.uk/4B/2F6C27/Practice_Level_Crosstab_Feb_24.zip"
 [Nov_23]="https://files.digital.nhs.uk/08/1CA799/Practice_Level_Crosstab_Nov_23.zip"
 [Aug_23]="https://files.digital.nhs.uk/68/2DEC89/Practice_Level_Crosstab_Aug_23.zip"
 [May_23]="https://files.digital.nhs.uk/4E/6F4774/Practice_Level_Crosstab_May_23.zip"
)
ORDER="Feb_26 Nov_25 Aug_25 May_25 Feb_25 Nov_24 Aug_24 May_24 Feb_24 Nov_23 Aug_23 May_23"
for rel in $ORDER; do
  out="gpad_agg/gpad_${rel}.csv"
  if [ -s "$out" ]; then echo "SKIP $rel"; continue; fi
  echo "=== $rel $(date +%T)"
  tmp="raw/tmp_${rel}"
  mkdir -p "$tmp"
  wget -q "${URLS[$rel]}" -O "raw/${rel}.zip" || { echo "DOWNLOAD FAIL $rel"; continue; }
  unzip -o -q "raw/${rel}.zip" -d "$tmp" || { echo "UNZIP FAIL $rel"; continue; }
  python3 aggregate_gpad.py "$out" "$tmp"/Practice_Level_Crosstab*.csv || echo "AGG FAIL $rel"
  rm -rf "$tmp" "raw/${rel}.zip"
done
echo "ALL DONE $(date +%T)"
