mod scrape;

use chrono::{Duration, NaiveDate};
use linked_hash_map::LinkedHashMap;
use std::{
    io::{stdin, Write},
    str::FromStr,
    sync::atomic::{AtomicUsize, Ordering},
};

static TOTAL_DAYS: AtomicUsize = AtomicUsize::new(0);
static DONE_DAYS: AtomicUsize = AtomicUsize::new(1);

fn main() {
    welcome_message();

    let dates_ordered = get_dates();
    TOTAL_DAYS.store(dates_ordered.len(), Ordering::Relaxed);

    let file_name = format!(
        "BoM Rates {}-{}.csv",
        dates_ordered.first().unwrap().to_string().replace('-', ""),
        dates_ordered.last().unwrap().to_string().replace('-', "")
    );

    let scraping_start_time = std::time::Instant::now();
    let dates_symbols_rates = scrape::scrape_concurrently(&dates_ordered, &update_progress_bar);
    let scraping_duration = scraping_start_time.elapsed();

    let convertion_start_time = std::time::Instant::now();
    let csv_string = get_csv_string(&dates_symbols_rates);
    let convertion_duration = convertion_start_time.elapsed();

    let csv_write_start_time = std::time::Instant::now();
    write_csv_file(csv_string, &file_name);
    let csv_write_duration = csv_write_start_time.elapsed();

    success_message(&file_name);

    println!("Reports:");
    print_duration("Scraping:    ", scraping_duration);
    print_duration("Convertion:  ", convertion_duration);
    print_duration("CSV creation:", csv_write_duration);
}

fn welcome_message() {
    println!("Source code at: \x1b[34mhttps://github.com/bilguun-zorigt\x1b[0m")
}

fn get_date_input(message: &str) -> chrono::NaiveDate {
    loop {
        print!("\x1b[0m{}\x1b[34m", message);
        std::io::stdout().flush().expect("");
        let mut date_string = String::new();
        stdin()
            .read_line(&mut date_string)
            .expect("Failed to read line");

        let date = NaiveDate::from_str(&date_string);

        match date {
            Ok(date) => return date,
            Err(_) => {
                println!(
                    "\x1b[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\x1b[0m"
                );
                continue;
            }
        }
    }
}

fn get_dates() -> Vec<chrono::NaiveDate> {
    let start_date = get_date_input("Enter start date (yyyy-mm-dd): ");
    let end_date = get_date_input("Enter end date (yyyy-mm-dd): ");

    let mut dates: Vec<chrono::NaiveDate> = Vec::new();
    let mut date = start_date;
    while date <= end_date {
        dates.push(date);
        date += Duration::days(1);
    }
    dates
}

fn update_progress_bar() {
    let done_days: usize = DONE_DAYS.fetch_add(1, Ordering::Relaxed);
    let total_days: usize = TOTAL_DAYS.load(Ordering::Relaxed);
    const PB_LENGTH: usize = 25;
    let done_length: usize = (done_days as f64 * (PB_LENGTH as f64 / total_days as f64)) as usize;
    let done_length_string: String = "█".repeat(done_length);
    let remaining_length_string: String = "█".repeat(PB_LENGTH - done_length);
    let percent_string: f64 = done_days as f64 / total_days as f64 * 100.0;
    // https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    print!(
        "\r\x1b[0mCurrent progress: \x1b[44;34m{}\x1b[41;31m{}\x1b[0m\x1b[34m {}/{} {:.2}%%\x1b[0m",
        done_length_string, remaining_length_string, done_days, total_days, percent_string,
    );
}

fn get_csv_string(
    dates_symbols_rates: &LinkedHashMap<chrono::NaiveDate, LinkedHashMap<String, f64>>,
) -> String {
    let mut csv_string: String = "Date".to_string();

    let mut symbols_ordered = Vec::new();
    if let Some((_, symbols_rates)) = dates_symbols_rates.back() {
        for (symbol, _) in symbols_rates.into_iter() {
            csv_string = csv_string + "," + symbol;
            symbols_ordered.push(symbol);
        }
    };

    for (date, symbols_rates) in dates_symbols_rates.into_iter() {
        csv_string = csv_string + "\n" + &date.to_string();
        for symbol in symbols_ordered.as_slice() {
            let rate_string = match symbols_rates.get(*symbol) {
                Some(rate) => rate.to_string(),
                None => "".to_string(),
            };
            csv_string = csv_string + "," + &rate_string;
        }
    }

    csv_string
}

fn write_csv_file(csv_string: String, file_name: &String) {
    std::fs::write(file_name, csv_string).expect("Unable to write file");
}

fn success_message(file_name: &String) {
    println!("\nFile saved: '\x1b[34m{:#}\x1b[0m'\n", file_name);
}

fn print_duration(operation_name: &str, duration_time: std::time::Duration) {
    println!("{} \x1b[34m{:.2}\x1b[0m seconds or \x1b[34m{}\x1b[0m milliseconds or \x1b[34m{}\x1b[0m microseconds or \x1b[34m{}\x1b[0m nanoseconds", operation_name, duration_time.as_secs_f32(), duration_time.as_millis(), duration_time.as_micros(), duration_time.as_nanos())
}
