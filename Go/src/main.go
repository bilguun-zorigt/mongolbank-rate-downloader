package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

func main() {
	// Request the HTML page.
	res, err := http.Get("https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=2022&vMonth=2&vDay=7")
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}
	parse(res)

}

func parse(httpResponse *http.Response) {
	doc, err := goquery.NewDocumentFromReader(httpResponse.Body)
	if err != nil {
		log.Fatal(err)
	}

	span_id_prefix := "ContentPlaceHolder1_lbl"

	elements := doc.Find(fmt.Sprintf(".uk-comment-list span[id^=%v]", span_id_prefix))

	elements.Each(func(_ int, element *goquery.Selection) {
		spanId, _ := element.Attr("id")
		symbol := strings.ReplaceAll(spanId, span_id_prefix, "")
		rate := strings.ReplaceAll(element.Text(), ",", "")

		fmt.Println(symbol, rate)
	})
}
