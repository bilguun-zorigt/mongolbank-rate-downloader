#!/bin/bash
source ./scraper.sh

function main {
	welcomeMessage
    
    getDates
	totalDays=$(wc -w <<< "$datesOrdered")
    updateProgressBar

	local scrapingStartTime=$(date +%s%N)
	scrapeConcurrently "$datesOrdered"
	local scrapingDuration=$(( $(date +%s%N) - $scrapingStartTime ))

	local convertionStartTime=$(date +%s%N)
	getCSVString
	local convertionDuration=$(( $(date +%s%N) - $convertionStartTime ))


	local csvWriteStartTime=$(date +%s%N)
	writeCSVFile
	local csvWriteDuration=$(( $(date +%s%N) - $csvWriteStartTime ))

	successMessage

	printf "\nReports:\n"
	printDuration "Scraping:    " $scrapingDuration
	printDuration "Convertion:  " $convertionDuration
	printDuration "CSV creation:" $csvWriteDuration
}

function welcomeMessage {
	printf "Source code at: \033[34mhttps://github.com/bilguun-zorigt\033[0m\n"
}

function getDateInput {
    local message="$1"
	while true; do 
        read -p $'\033[0m'"$message"$'\033[34m' dateString
		local date=$(date -d "$dateString" +%Y-%m-%d)
		if [ "$dateString" != "$(date -d "$date" +%Y-%m-%d)" ]; then 
			echo  $'\033[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\033[0m' > $(tty)
			continue
        fi
        echo $date
        break
	done
}

function getDates {
    startDate=$(getDateInput "Enter start date (yyyy-mm-dd): ")
	endDate=$(getDateInput "Enter end date (yyyy-mm-dd): ")

    local d=
    local n=0
    until [ "$d" = "$endDate" ]; do  
        d=$(date -d "$startDate + $n days" +%Y-%m-%d)
		datesOrdered+=" $d"
        ((n++))
    done
}

function updateProgressBar {
	# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
	printf "\033[0mCurrent progress: "
}

function getCSVString {
    symbolsOrdered=()
    while read -a line; do
        symbolsOrdered+=(${line[0]})
    done <".temp/$startDate.txt"
    
	csvString="Date"
	for symbol in ${symbolsOrdered[@]}; do {
		csvString+=",$symbol"
	}; done

    for date in $datesOrdered; do {
		csvString+=$'\n'"$date"

        declare -A symbolsRates
        while read -a line; do
            local symbol=${line[0]}
            local rate=${line[1]}
            symbolsRates[$symbol]=$rate
        done <".temp/$date.txt"

        for symbol in ${symbolsOrdered[@]}; do {
		    csvString+=",${symbolsRates[$symbol]}"
        }; done
    }; done
    rm -rf .temp
}

function writeCSVFile {
    fileName="BoM Rates $(date -d "$startDate" +%Y%m%d)-$(date -d "$endDate" +%Y%m%d).csv"
	echo "$csvString" > "$fileName"
}

function successMessage {
	printf "\nFile saved: '\033[34m%s\033[0m'\n" "$fileName"
}

function printDuration {
    local operationName="$1"
    local nano="$2"
    local micro="$(( $nano / 1000 ))"
    local milli="$(( $micro / 1000 ))"
    local seconds="$(( $milli / 1000 ))"
	printf "%s \033[34m%s\033[0m seconds or \033[34m%s\033[0m milliseconds or \033[34m%s\033[0m microseconds or \033[34m%s\033[0m nanoseconds\n" "$operationName" $seconds $milli $micro $nano
}

main
