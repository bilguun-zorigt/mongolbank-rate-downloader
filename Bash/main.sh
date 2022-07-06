#!/bin/bash
source ./scraper.sh

function main {
	welcomeMessage
    
    getDates
	totalDays=$(wc -w <<< "$datesOrdered")
    updateProgressBar

	# scrapingStartTime := time.Now()
	scrapeConcurrently "$datesOrdered"
	# scrapingDuration := time.Since(scrapingStartTime)

	# convertionStartTime := time.Now()
	getCSVString
	# convertionDuration := time.Since(convertionStartTime)

	# csvWriteStartTime := time.Now()
	writeCSVFile
	# csvWriteDuration := time.Since(csvWriteStartTime)

	successMessage

	printf "\nReports:\n"
	# printDuration("Scraping:    ", scrapingDuration)
	# printDuration("Convertion:  ", convertionDuration)
	# printDuration("CSV creation:", csvWriteDuration)
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
	csvString="Date"
# 	for _, symbol := range symbolsOrdered {
# 		csvString = csvString + "," + symbol
# 	}
# 	for _, date := range datesOrdered {
# 		dateString := date.Format("2006-01-02")
# 		csvString = csvString + "\n" + dateString
# 		for _, symbol := range symbolsOrdered {
# 			rateString := strconv.FormatFloat(datesSymbolsRates[date][symbol], 'f', -1, 64)
# 			if rateString == "0" {
# 				rateString = ""
# 			}
# 			csvString = csvString + "," + rateString
# 		}
# 	}
declare -A datesSymbolsRates

    for date in $datesOrdered; do {
        declare -A symbolsRates
        while read -a line; do
            local symbol=${line[0]}
            local rate=${line[1]}
            symbolsRates[$symbol]=$rate
        done <".temp/$date.txt"
        datesSymbolsRates[$date]=$symbolsRates
    }; done
    rm -rf .temp

    # for key in "${!datesSymbolsRates[@]}"; do echo $key; done
    # for val in "${datesSymbolsRates[@]}"; do echo $val$'\n'; done
}

function writeCSVFile {
    fileName="BoM Rates $(date -d "$startDate" +%Y%m%d)-$(date -d "$endDate" +%Y%m%d).csv"
	echo "$csvString" > "$fileName"
}

function successMessage {
	printf "\nFile saved: '\033[34m%s\033[0m'\n" "$fileName"
}

function printDuration {
    # local operationName="$1"
    # local durationTime="$2"
	# fmt.Printf("%v \033[34m%.2f\033[0m seconds or \033[34m%v\033[0m milliseconds or \033[34m%v\033[0m microseconds or \033[34m%v\033[0m nanoseconds\n", operationName, durationTime.Seconds(), durationTime.Milliseconds(), durationTime.Microseconds(), durationTime.Nanoseconds())
    echo "1"
}

main
