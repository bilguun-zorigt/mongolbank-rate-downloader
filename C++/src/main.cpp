#include <fstream>
#include <iomanip>
#include <math.h>
#include <chrono>
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
void getCSVString(std::string *csvString, std::vector<std::string> *symbolsOrdered, std::vector<Date> *datesOrdered, std::map<std::string, std::map<std::string, double>> *datesSymbolsRates);
void writeCSVFile(std::string csvString);
void successMessage();
void printDuration(std::string operationName, auto durationTime);

int main()
{
    welcomeMessage();

    auto datesOrdered = getDates();
    totalDays = datesOrdered.size();

    auto scrapingStartTime = std::chrono::steady_clock::now();
    auto scraped = scrapeConcurrently(datesOrdered, updateProgressBar);
    auto scrapingDuration = std::chrono::steady_clock::now() - scrapingStartTime;

    auto convertionStartTime = std::chrono::steady_clock::now();
    std::string csvString;
    getCSVString(&csvString, &scraped.symbolsOrdered, &datesOrdered, &scraped.datesSymbolsRates);
    auto convertionDuration = std::chrono::steady_clock::now() - convertionStartTime;

    auto csvWriteStartTime = std::chrono::steady_clock::now();
    writeCSVFile(csvString);
    auto csvWriteDuration = std::chrono::steady_clock::now() - csvWriteStartTime;

    successMessage();

    std::cout << "\nReports:\n";
    printDuration("Scraping:    ", scrapingDuration);
    printDuration("Convertion:  ", convertionDuration);
    printDuration("CSV creation:", csvWriteDuration);

    return 0;
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
        std::istringstream dateStringStream(dateString + " 15:15:15");
        dateStringStream >> std::get_time(&date, "%Y-%m-%d %H:%M:%S");

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
    startDate = getDateInput("Enter start date (yyyy-mm-dd): ");
    endDate = getDateInput("Enter end date (yyyy-mm-dd): ");
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

void getCSVString(std::string *csvString, std::vector<std::string> *symbolsOrdered, std::vector<Date> *datesOrdered, std::map<std::string, std::map<std::string, double>> *datesSymbolsRates)
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
            {
                rateString = std::to_string(search->second);
                rateString.erase(rateString.find_last_not_of('0') + 1, std::string::npos);
                rateString.erase(rateString.find_last_not_of('.') + 1, std::string::npos);
            }
            else
                rateString = "";

            *csvString += "," + rateString;
        }
    }
}

void writeCSVFile(std::string csvString)
{
    fileName = "BoM Rates " + getISODateString(startDate, "") + "-" + getISODateString(endDate, "") + ".csv";
    std::ofstream outFile;
    outFile.open(fileName);
    outFile << csvString << std::endl;
    outFile.close();
}

void successMessage()
{
    std::cout << "\nFile saved: '\033[34m" + fileName + "\033[0m'\n";
}

void printDuration(std::string operationName, auto durationTime)
{
    std::cout
        << operationName << " \033[34m"
        << std::fixed << std::setprecision(2) << std::chrono::duration<double>(durationTime).count() << "\033[0m seconds or \033[34m"
        << std::to_string(std::chrono::duration_cast<std::chrono::milliseconds>(durationTime).count()) << "\033[0m milliseconds or \033[34m"
        << std::to_string(std::chrono::duration_cast<std::chrono::microseconds>(durationTime).count()) << "\033[0m microseconds or \033[34m"
        << std::to_string(std::chrono::duration_cast<std::chrono::nanoseconds>(durationTime).count()) << "\033[0m nanoseconds\n";
}
