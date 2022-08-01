// use reqwest::{self, header};
// #[tokio::main]
// async fn main() -> Result<(), Box<dyn std::error::Error>> {
//     let mut headers = header::HeaderMap::new();
//     headers.insert(
//         header::USER_AGENT,
//         header::HeaderValue::from_static("Mozilla/5.0...."),
//     );

//     let client = reqwest::Client::builder()
//         .default_headers(headers)
//         .build()?;

//     let res = client
//         .get("https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=2022&vMonth=2&vDay=7")
//         .send()
//         .await?;
//     println!("{:#?}", res.text().await);
//     Ok(())
// }

// }
extern crate reqwest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=2022&vMonth=2&vDay=7";

    let client = reqwest::Client::new();
    let response = client
        .get(url)
        .header("User-Agent", "Mozilla/5.0....")
        .send()
        .await? // ? == .unwrap()
        .text()
        .await?; // ? == .unwrap()

    let document = scraper::Html::parse_document(&response);

    let title_selector = scraper::Selector::parse(".uk-comment-list span").unwrap();

    let titles = document
        .select(&title_selector)
        .map(|x| (x.value().attr("id").unwrap(), x.inner_html()));

    titles.for_each(|(id, rate)| println!("{} {}", id, rate));

    Ok(())
}
