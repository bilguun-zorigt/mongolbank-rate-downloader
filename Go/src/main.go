package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
	// For Windows
	// "golang.org/x/sys/windows"
)

// For Windows
// func init() {
// 	stdout := windows.Handle(os.Stdout.Fd())
// 	var originalMode uint32

// 	windows.GetConsoleMode(stdout, &originalMode)
// 	windows.SetConsoleMode(stdout, originalMode|windows.ENABLE_VIRTUAL_TERMINAL_PROCESSING)
// }

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

	fmt.Print("\nReports:\n")
	printDuration("Scraping:    ", scrapingDuration)
	printDuration("Convertion:  ", convertionDuration)
	printDuration("CSV creation:", csvWriteDuration)

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Press Enter to exit...")
	for {
		lineBreak, _ := reader.ReadString('\n')
		// For Windows
		// if lineBreak != "\n" {
		// 	break
		// }
		if lineBreak != "\n" {
			break
		}
	}
}

func welcomeMessage() {
	fmt.Print("Source code at: \033[34mhttps://github.com/bilguun-zorigt\033[0m\n")
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

func getDates() []time.Time {
	var dates []time.Time
	startDate = getDateInput("Enter start date (yyyy-mm-dd): ")
	endDate = getDateInput("Enter end date (yyyy-mm-dd): ")
	for date := startDate; !date.After(endDate); date = date.AddDate(0, 0, 1) {
		dates = append(dates, date)
	}
	return dates
}

func updateProgressBar() {
	doneDays++
	pbLength := 25
	doneLength := int(float32(doneDays) * (float32(pbLength) / float32(totalDays)))
	doneLengthString := strings.Repeat("█", doneLength)
	remainingLengthString := strings.Repeat("█", pbLength-doneLength)
	percentString := strconv.FormatFloat(float64(doneDays)/float64(totalDays)*100, 'f', 1, 64)
	// https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
	fmt.Printf("\r\033[0mCurrent progress: \033[34m%v\033[41;31m%v\033[0m\033[34m %v/%v %v%%\033[0m", doneLengthString, remainingLengthString, doneDays, totalDays, percentString)
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

func writeCSVFile(csvString string) {
	fileName = fmt.Sprintf("BoM Rates %v-%v.csv", startDate.Format("20060102"), endDate.Format("20060102"))
	err := ioutil.WriteFile(fileName, []byte(csvString), 0644)
	if err != nil {
		log.Fatal(err)
	}
}

func successMessage() {
	fmt.Printf("\nFile saved: '\033[34m%v\033[0m'\n", fileName)
}

func printDuration(operationName string, durationTime time.Duration) {
	fmt.Printf("%v \033[34m%.2f\033[0m seconds or \033[34m%v\033[0m milliseconds or \033[34m%v\033[0m microseconds or \033[34m%v\033[0m nanoseconds\n", operationName, durationTime.Seconds(), durationTime.Milliseconds(), durationTime.Microseconds(), durationTime.Nanoseconds())
}
