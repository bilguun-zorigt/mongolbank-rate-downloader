package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
)

type symbolRatesType = map[string]float64
type datesSymbolsRatesType = map[time.Time]symbolRatesType

var symbolsOrdered []string
var symbols = make(map[string]bool)
var datesSymbolsRates = make(datesSymbolsRatesType)
var goRoutineWaitGroup = sync.WaitGroup{}

func scrapeConcurrently(dates []time.Time, progressCallback func()) ([]string, datesSymbolsRatesType) {
	for _, date := range dates {
		goRoutineWaitGroup.Add(1)
		go request(date, progressCallback)
	}
	goRoutineWaitGroup.Wait()
	return symbolsOrdered, datesSymbolsRates
}

func request(date time.Time, progressCallback func()) {
	url_params := fmt.Sprintf("?vYear=%v&vMonth=%v&vDay=%v", date.Year(), int(date.Month()), date.Day())
	url := "https://www.mongolbank.mn/dblistofficialdailyrate.aspx" + url_params

	response, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer response.Body.Close()
	if response.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", response.StatusCode, response.Status)
	}

	parse(date, response)
	progressCallback()
	goRoutineWaitGroup.Done()
}

func parse(date time.Time, response *http.Response) {
	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal(err)
	}

	span_id_prefix := "ContentPlaceHolder1_lbl"

	elements := doc.Find(fmt.Sprintf(".uk-comment-list span[id^=%v]", span_id_prefix))

	var symbolRates = make(symbolRatesType)

	elements.Each(func(_ int, element *goquery.Selection) {
		spanId, _ := element.Attr("id")
		symbol := strings.ReplaceAll(spanId, span_id_prefix, "")
		if value := symbols[symbol]; !value {
			symbols[symbol] = true
			symbolsOrdered = append(symbolsOrdered, symbol)
		}
		rate, err := strconv.ParseFloat(strings.ReplaceAll(element.Text(), ",", ""), 64)
		if err == nil {
			symbolRates[symbol] = rate
		}
	})
	datesSymbolsRates[date] = symbolRates
}
