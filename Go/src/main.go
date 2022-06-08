package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
)

var wg = sync.WaitGroup{}

func main() {
	var startDateString string
	fmt.Println("Enter date to download from (yyyy-mm-dd): ")
	fmt.Scan(&startDateString)
	start, _ := time.Parse("2006-01-02", startDateString)

	var endDateString string
	fmt.Println("Enter date to download to (yyyy-mm-dd): ")
	fmt.Scan(&endDateString)
	end, _ := time.Parse("2006-01-02", endDateString)

	for d := start; !d.After(end); d = d.AddDate(0, 0, 1) {
		wg.Add(1)
		go request(d)
	}
	wg.Wait()
}

func request(date time.Time) {
	url_params := fmt.Sprintf("?vYear=%v&vMonth=%v&vDay=%v", date.Year(), int(date.Month()), date.Day())
	url := "https://www.mongolbank.mn/dblistofficialdailyrate.aspx" + url_params

	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	parse(res, date)
	wg.Done()
}

func parse(httpResponse *http.Response, date time.Time) {
	doc, err := goquery.NewDocumentFromReader(httpResponse.Body)
	if err != nil {
		log.Fatal(err)
	}

	span_id_prefix := "ContentPlaceHolder1_lbl"

	elements := doc.Find(fmt.Sprintf(".uk-comment-list span[id^=%v]", span_id_prefix))

	row := map[string]string{"Date": date.Format("2006-01-02")}
	elements.Each(func(_ int, element *goquery.Selection) {
		spanId, _ := element.Attr("id")
		symbol := strings.ReplaceAll(spanId, span_id_prefix, "")
		rate := strings.ReplaceAll(element.Text(), ",", "")

		row[symbol] = rate
	})
	fmt.Println(row)
}
