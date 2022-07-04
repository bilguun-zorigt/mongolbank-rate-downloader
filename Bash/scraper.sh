#!/bin/bash

function scrapeConcurrently {
    local datesOrdered="$1"
    # local updateProgressBar="$2"
    for date in $datesOrdered; do request "$date" & done
    wait
    echo "1"
}

function request {
    local date="$1"

    year=$(date -d "$date" +%Y)
    month=$(date -d "$date" +%m)
    day=$(date -d "$date" +%d)

    html=$(curl "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=$year&vMonth=$month&vDay=$day" | hxnormalize -x)

    elements=$(echo $html | hxselect -s '\n' ".uk-comment-list span[id^=ContentPlaceHolder1_lbl]")

    old_IFS=$IFS
    IFS=$'\n'

    str="Date"
    for e in $elements; do
        id=$(echo $e | hxselect -c '::attr(id)')
        id=${id//ContentPlaceHolder1_lbl/}
        # rate=$(echo $e | hxselect -c 'span')
        # rate=${rate//,/}
        str+=",$id"
        # echo "$id $rate" >> "BoM Rates $(date +%Y%m%d)-$(date +%Y%m%d).csv"
    done
    echo $str  >> "BoM Rates $(date +%Y%m%d)-$(date +%Y%m%d).csv"

    str=$(date -d "$date" +%Y-%m-%d)
    for e in $elements; do
        # id=$(echo $e | hxselect -c '::attr(id)')
        # id=${id//ContentPlaceHolder1_lbl/}
        rate=$(echo $e | hxselect -c 'span')
        rate=${rate//,/}
        str+=",$rate"
        # echo "$id $rate" >> "BoM Rates $(date +%Y%m%d)-$(date +%Y%m%d).csv"
    done
    echo $str  >> "BoM Rates $(date +%Y%m%d)-$(date +%Y%m%d).csv"

    IFS=$old_IFS
}






# type symbolsRatesType = map[string]float64
# type datesSymbolsRatesType = map[time.Time]symbolsRatesType

# var symbolsOrdered []string
# var symbols = make(map[string]bool)
# var datesSymbolsRates = make(datesSymbolsRatesType)
# var goRoutineWaitGroup = sync.WaitGroup{}

# func scrapeConcurrently(dates []time.Time, progressCallback func()) ([]string, datesSymbolsRatesType) {
# 	for _, date := range dates {
# 		goRoutineWaitGroup.Add(1)
# 		go request(date, progressCallback)
# 	}
# 	goRoutineWaitGroup.Wait()
# 	return symbolsOrdered, datesSymbolsRates
# }

# func request(date time.Time, progressCallback func()) {
# 	urlParams := fmt.Sprintf("?vYear=%v&vMonth=%v&vDay=%v", date.Year(), int(date.Month()), date.Day())
# 	url := "https://www.mongolbank.mn/dblistofficialdailyrate.aspx" + urlParams

# 	response, err := http.Get(url)
# 	if err != nil {
# 		log.Fatal(err)
# 	}
# 	defer response.Body.Close()
# 	if response.StatusCode != 200 {
# 		log.Fatalf("status code error: %d %s", response.StatusCode, response.Status)
# 	}
# 	doc, err := goquery.NewDocumentFromReader(response.Body)
# 	if err != nil {
# 		log.Fatal(err)
# 	}

# 	parse(date, doc)
# 	progressCallback()
# 	goRoutineWaitGroup.Done()
# }

# func parse(date time.Time, doc *goquery.Document) {
# 	spanIDPrefix := "ContentPlaceHolder1_lbl"

# 	elements := doc.Find(fmt.Sprintf(".uk-comment-list span[id^=%v]", spanIDPrefix))

# 	var symbolsRates = make(symbolsRatesType)

# 	elements.Each(func(_ int, element *goquery.Selection) {
# 		spanId, _ := element.Attr("id")
# 		symbol := strings.ReplaceAll(spanId, spanIDPrefix, "")
# 		if value := symbols[symbol]; !value {
# 			symbols[symbol] = true
# 			symbolsOrdered = append(symbolsOrdered, symbol)
# 		}
# 		if element.Text() != "" {
# 			rate, err := strconv.ParseFloat(strings.ReplaceAll(element.Text(), ",", ""), 64)
# 			if err == nil {
# 				symbolsRates[symbol] = rate
# 			}
# 		}
# 	})
# 	datesSymbolsRates[date] = symbolsRates
# }
