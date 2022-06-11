package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
	"time"
)

var startDate time.Time
var endDate time.Time
var fileName string
var totalDays int
var doneDays int = 0

func main() {
	welcomeMessage()

	datesOrdered := getDates()
	totalDays = len(datesOrdered)

	scrapingStartTime := time.Now()
	symbolsOrdered, datesSymbolsRates := scrapeConcurrently(datesOrdered, updateProgressBar)
	scrapingDuration := time.Since(scrapingStartTime)

	convertionStartTime := time.Now()
	csvString := getCSVString(symbolsOrdered, datesOrdered, datesSymbolsRates)
	convertionDuration := time.Since(convertionStartTime)

	csvWriteStartTime := time.Now()
	writeCSVFile(csvString)
	csvWriteDuration := time.Since(csvWriteStartTime)

	successMessage()

	fmt.Printf("\nReports:")
	fmt.Printf("\nScraping took     %.2f seconds or %v milliseconds or %v microseconds or %v nanoseconds", scrapingDuration.Seconds(), scrapingDuration.Milliseconds(), scrapingDuration.Microseconds(), scrapingDuration.Nanoseconds())
	fmt.Printf("\nConvertion took   %.2f seconds or %v milliseconds or %v microseconds or %v nanoseconds", convertionDuration.Seconds(), convertionDuration.Milliseconds(), convertionDuration.Microseconds(), convertionDuration.Nanoseconds())
	fmt.Printf("\nCSV creation took %.2f seconds or %v milliseconds or %v microseconds or %v nanoseconds\n", csvWriteDuration.Seconds(), csvWriteDuration.Milliseconds(), csvWriteDuration.Microseconds(), csvWriteDuration.Nanoseconds())
}

func updateProgressBar() {
	doneDays++
	pbLength := 25
	doneLength := int(float32(doneDays) * (float32(pbLength) / float32(totalDays)))
	doneLengthString := strings.Repeat("█", doneLength)
	remainingLengthString := strings.Repeat("█", pbLength-doneLength)
	percentString := doneDays / totalDays * 100
	// https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
	fmt.Printf("\r\033[42;32m%v\033[41;31m%v\033[0m %v%% %v/%v", doneLengthString, remainingLengthString, percentString, doneDays, totalDays)
}

func welcomeMessage() {
	fmt.Print("Source code at: \033[34mhttps://github.com/bilguun-zorigt\033[0m\n")
}
func successMessage() {
	fmt.Printf(" => File \033[34m'%v' \033[0msaved.\n", fileName)
}

func writeCSVFile(csvString string) {
	fileName = fmt.Sprintf("BoM Rates %v-%v.csv", startDate.Format("20060102"), endDate.Format("20060102"))
	err := ioutil.WriteFile(fileName, []byte(csvString), 0644)
	if err != nil {
		log.Fatal(err)
	}
}

func getCSVString(symbolsOrdered []string, datesOrdered []time.Time, datesSymbolsRates datesSymbolsRatesType) string {
	var csvString = "Date"
	for _, symbol := range symbolsOrdered {
		csvString = csvString + "," + symbol
	}
	for _, date := range datesOrdered {
		dateString := date.Format("2006-01-02")
		csvString = csvString + "\n" + dateString
		for _, symbol := range symbolsOrdered {
			rateString := strconv.FormatFloat(datesSymbolsRates[date][symbol], 'f', -1, 64)
			if rateString == "0" {
				rateString = ""
			}
			csvString = csvString + "," + rateString
		}
	}
	return csvString
}

func getDates() []time.Time {
	var dates []time.Time
	startDate = getDateInput("Enter start date (yyyy-mm-dd): ")
	endDate = getDateInput("Enter end date (yyyy-mm-dd): ")
	for date := startDate; !date.After(endDate); date = date.AddDate(0, 0, 1) {
		dates = append(dates, date)
	}
	return dates
}

func getDateInput(message string) time.Time {
	for {
		var dateString string
		fmt.Print("\033[0m" + message + "\033[34m")
		fmt.Scan(&dateString)

		date, err := time.Parse("2006-01-02", dateString)
		if err != nil {
			fmt.Printf("\033[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\033[0m\n")
			continue
		}
		return date
	}
}
