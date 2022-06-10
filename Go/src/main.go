package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"time"
)

var startDate time.Time
var endDate time.Time
var fileName string

func main() {
	// TODO need to show progress
	// TODO welcome message hyperlink
	// TODO need to add timers (scraping time, converting time, )
	welcomeMessage()
	datesOrdered := getDates()
	symbolsOrdered, datesSymbolsRates := scrapeConcurrently(datesOrdered)
	csvString := getCSVString(symbolsOrdered, datesOrdered, datesSymbolsRates)
	writeCSVFile(csvString)
	successMessage()
}

func welcomeMessage() {
	fmt.Print("###########\nSource code at: https://github.com/bilguun-zorigt\nStarting...\n\n")
}
func successMessage() {
	fmt.Printf("\nSuccess: file saved as '%v'\nSource code at: https://github.com/bilguun-zorigt\n###########\n", fileName)
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
		fmt.Print(message)
		fmt.Scan(&dateString)

		date, err := time.Parse("2006-01-02", dateString)
		if err != nil {
			fmt.Printf("\n###########\nDate entered is not valid. Must be formatted as yyyy-mm-dd\n###########\n\n")
			continue
		}
		return date
	}
}
