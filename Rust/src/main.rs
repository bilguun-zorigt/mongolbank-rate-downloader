mod scrape;

use chrono::{Duration, NaiveDate};
// use std::sync::{Arc, Mutex};
use std::{
    io::{stdin, Write},
    str::FromStr,
};

// let start_date=chrono::NaiveDate;
// let end_date= time.Time
// var fileName string
// var totalDays int
// var doneDays int = 0

fn main() {
    welcome_message();

    let dates_ordered = get_dates();
    let total_days = dates_ordered.len();
    println!("First: {:#?}\nSecond: {:#?}", dates_ordered, total_days);

    // scraping_start_time := time.Now()
    let dates_symbols_rates = scrape::scrape_concurrently(dates_ordered, &update_progress_bar);
    println!("Second: {:#?}", dates_symbols_rates);
    // let (symbols_ordered, dates_symbols_rates) = scrape_concurrently(dates_ordered, update_progress_bar);
    // scraping_duration := time.Since(scraping_start_time)

    // convertion_start_time := time.Now()
    // csv_string := get_csv_string(symbols_ordered, dates_ordered, dates_symbols_rates)
    // convertion_duration := time.Since(convertion_start_time)

    // csv_write_start_time := time.Now()
    // write_csv_file(csvString)
    // csv_write_duration := time.Since(csv_write_start_time)

    // success_message();

    // fmt.Print("\nReports:\n")
    // printDuration("Scraping:    ", scraping_duration)
    // printDuration("Convertion:  ", convertion_duration)
    // printDuration("CSV creation:", csv_write_duration)
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

// static counter: Arc<Mutex<i32>> = Arc::new(Mutex::new(0));

fn update_progress_bar() {
    // let counter = Arc::clone(&counter);
    // let mut num = counter.lock().unwrap();
    // *num += 1;

    // println!("Result: {}", *counter.lock().unwrap());

    println!("One down");

    // let doneDays += 1;
    // println!("{:?}", doneDays);
    // pbLength := 25
    // doneLength := int(float32(doneDays) * (float32(pbLength) / float32(totalDays)))
    // doneLengthString := strings.Repeat("█", doneLength)
    // remainingLengthString := strings.Repeat("█", pbLength-doneLength)
    // percentString := strconv.FormatFloat(float64(doneDays)/float64(totalDays)*100, 'f', 1, 64)
    // // https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    // fmt.Printf("\r\x1b[0mCurrent progress: \x1b[34m%v\x1b[41;31m%v\x1b[0m\x1b[34m %v/%v %v%%\x1b[0m", doneLengthString, remainingLengthString, doneDays, totalDays, percentString)
}

// func get_csv_string(symbolsOrdered []string, datesOrdered []time.Time, datesSymbolsRates datesSymbolsRatesType) string {
// 	var csvString = "Date"
// 	for _, symbol := range symbolsOrdered {
// 		csvString = csvString + "," + symbol
// 	}
// 	for _, date := range datesOrdered {
// 		dateString := date.Format("2006-01-02")
// 		csvString = csvString + "\n" + dateString
// 		for _, symbol := range symbolsOrdered {
// 			rateString := strconv.FormatFloat(datesSymbolsRates[date][symbol], 'f', -1, 64)
// 			if rateString == "0" {
// 				rateString = ""
// 			}
// 			csvString = csvString + "," + rateString
// 		}
// 	}
// 	return csvString
// }

// func writeCSVFile(csvString string) {
// 	fileName = fmt.Sprintf("BoM Rates %v-%v.csv", start_date.Format("20060102"), end_date.Format("20060102"))
// 	err := ioutil.WriteFile(fileName, []byte(csvString), 0644)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// }

// fn success_message() {
//     println!("\nFile saved: '\x1b[34m{:#}\x1b[0m'\n", fileName)
// }

// func printDuration(operationName string, durationTime time.Duration) {
// 	fmt.Printf("%v \x1b[34m%.2f\x1b[0m seconds or \x1b[34m%v\x1b[0m milliseconds or \x1b[34m%v\x1b[0m microseconds or \x1b[34m%v\x1b[0m nanoseconds\n", operationName, durationTime.Seconds(), durationTime.Milliseconds(), durationTime.Microseconds(), durationTime.Nanoseconds())
// }
