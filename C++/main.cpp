#include <fstream>
#include <iomanip>
#include <math.h>
#include "scraper.hpp"

Date startDate;
Date endDate;
std::string fileName;
int totalDays;
int doneDays;

void welcomeMessage();
Date getDateInput(std::string message);
std::vector<Date> getDates();
void updateProgressBar();
void getCSVString(std::string *csvString, std::vector<std::string> *symbolsOrdered, std::vector<Date> *datesOrdered, std::map<std::string, std::map<std::string, float>> *datesSymbolsRates);
void writeCSVFile(std::string csvString);
void successMessage();
void printDuration(std::string operationName, int durationTime);

int main()
{
    welcomeMessage();

    auto datesOrdered = getDates();
    totalDays = datesOrdered.size();

    // scrapingStartTime = time.Now();
    auto scraped = scrapeConcurrently(datesOrdered, updateProgressBar);
    // scrapingDuration = time.Since(scrapingStartTime);

    // convertionStartTime = time.Now();
    std::string csvString;
    getCSVString(&csvString, &scraped.symbolsOrdered, &datesOrdered, &scraped.datesSymbolsRates);
    std::cout << "csvString: " << csvString << std::endl;
    // convertionDuration = time.Since(convertionStartTime);

    // csvWriteStartTime = time.Now();
    // writeCSVFile(csvString);
    // csvWriteDuration = time.Since(csvWriteStart; Time);

    // successMessage();

    // fmt.Print("\nReports:\n");
    // printDuration("Scraping:    ", scrapingDuration);
    // printDuration("Convertion:  ", convertionDuration);
    // printDuration("CSV creation:", csvWriteDuration);

    // return 0;
}

void welcomeMessage()
{
    std::cout << "Source code at: \033[34mhttps://github.com/bilguun-zorigt\033[0m\n";
}

Date getDateInput(std::string message)
{
    while (true)
    {
        std::string dateString;
        std::cout << "\033[0m" + message + "\033[34m";
        std::cin >> dateString;

        Date date;
        std::istringstream dateStringStream(dateString);
        dateStringStream >> std::get_time(&date, "%Y-%m-%d");

        if (getISODateString(date) != dateString)
        {
            std::cout << "\033[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\033[0m\n";
            continue;
        }
        return date;
    }
}

std::vector<Date> getDates()
{
    std::vector<Date> dates;
    Date startDate = getDateInput("Enter start date (yyyy-mm-dd): ");
    Date endDate = getDateInput("Enter end date (yyyy-mm-dd): ");
    for (Date date = startDate; mktime(&date) <= mktime(&endDate); ++date.tm_mday)
        dates.push_back(date);
    return dates;
}

void updateProgressBar()
{
    doneDays++;
    int pbLength = 25;
    int doneLength = (float)doneDays * ((float)pbLength / (float)totalDays);
    std::string doneLengthString = std::string(doneLength, ' ');
    std::string remainingLengthString = std::string(pbLength - doneLength, ' ');
    float percent = (float)doneDays / (float)totalDays * 100;
    // https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    std::cout << "\r\033[0mCurrent progress: \033[44;34m" << doneLengthString
              << "\033[41;31m" << remainingLengthString
              << "\033[0m\033[34m " << doneDays
              << "/" << totalDays
              << " " << std::fixed << std::setprecision(2) << percent
              << "%\033[0m";
}

void getCSVString(std::string *csvString, std::vector<std::string> *symbolsOrdered, std::vector<Date> *datesOrdered, std::map<std::string, std::map<std::string, float>> *datesSymbolsRates)
{
    *csvString = "Date";
    for (std::string symbol : *symbolsOrdered)
    {
        *csvString += "," + symbol;
    }
    for (Date date : *datesOrdered)
    {
        std::string dateString = getISODateString(date);
        *csvString += "\n" + dateString;
        auto *dateSymbolRates = &datesSymbolsRates->at(getISODateString(date));
        for (std::string symbol : *symbolsOrdered)
        {
            std::string rateString;

            auto search = dateSymbolRates->find(symbol);
            if (search != dateSymbolRates->end())
                rateString = std::to_string(search->second);
            else
                rateString = "";

            *csvString += "," + rateString;
        }
    }
}

// void writeCSVFile(std::string csvString)
// {
//     // fileName = fmt.Sprintf("BoM Rates %v-%v.csv", startDate.Format("20060102"), endDate.Format("20060102"))
//     // err := ioutil.WriteFile(fileName, []byte(csvString), 0644)
//     // if err != nil {
//     // 	log.Fatal(err)
//     // }
//     std::ofstream outFile;
//     outFile.open("output.txt");
//     outFile << str << std::endl;
//     outFile.close();
//     std::cout << "File saved" << std::endl;
// }

// void successMessage()
// {
//     fmt.Printf("\nFile saved: '\033[34m%v\033[0m'\n", fileName)
// }

// void printDuration(std::string operationName, int durationTime)
// {
//     fmt.Printf("%v \033[34m%.2f\033[0m seconds or \033[34m%v\033[0m milliseconds or \033[34m%v\033[0m microseconds or \033[34m%v\033[0m nanoseconds\n", operationName, durationTime.Seconds(), durationTime.Milliseconds(), durationTime.Microseconds(), durationTime.Nanoseconds())
// }
