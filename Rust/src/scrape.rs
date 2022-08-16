use chrono::Datelike;
use futures::future::join_all;
use linked_hash_map::LinkedHashMap;

#[tokio::main]
pub async fn scrape_concurrently(
    dates: &Vec<chrono::NaiveDate>,
    progress_callback: &dyn Fn(),
) -> LinkedHashMap<chrono::NaiveDate, LinkedHashMap<String, f64>> {
    let mut requests = Vec::new();
    for date in dates {
        requests.push(request(*date, progress_callback))
    }

    let results = join_all(requests).await;

    let mut dates_symbols_rates: LinkedHashMap<chrono::NaiveDate, LinkedHashMap<String, f64>> =
        LinkedHashMap::new();
    for (k, v) in results {
        dates_symbols_rates.insert(k, v);
    }
    dates_symbols_rates
}

async fn request(
    date: chrono::NaiveDate,
    progress_callback: &dyn Fn(),
) -> (chrono::NaiveDate, LinkedHashMap<String, f64>) {
    let url = format!(
        "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear={}&vMonth={}&vDay={}",
        date.year(),
        date.month(),
        date.day()
    );

    let client = reqwest::Client::new();
    let response = client
        .get(url)
        .header("User-Agent", "Mozilla/5.0....")
        .send()
        .await
        .unwrap()
        .text()
        .await
        .unwrap();

    let doc = scraper::Html::parse_document(&response);
    let symbols_rates = parse(doc);
    progress_callback();
    (date, symbols_rates)
}

fn parse(doc: scraper::Html) -> LinkedHashMap<String, f64> {
    const SPAN_ID_PREFIX: &str = "ContentPlaceHolder1_lbl";
    let selector_str = format!(".uk-comment-list span[id^={}]", SPAN_ID_PREFIX);
    let elements_selector = scraper::Selector::parse(selector_str.as_str()).unwrap();
    let elements = doc.select(&elements_selector);

    let mut symbols_rates: LinkedHashMap<String, f64> = LinkedHashMap::new();
    for element in elements {
        let symbol = element
            .value()
            .attr("id")
            .unwrap()
            .replace(SPAN_ID_PREFIX, "");

        if let Ok(rate) = element.inner_html().replace(',', "").parse::<f64>() {
            symbols_rates.insert(symbol, rate);
        }
    }

    symbols_rates
}
