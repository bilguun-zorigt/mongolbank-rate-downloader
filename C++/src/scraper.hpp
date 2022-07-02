#include <iostream>
#include <regex>
#include <set>
#include <algorithm>
#include <functional>
#include "cpr/cpr.h"          // https://github.com/libcpr/cpr
#include "BS_thread_pool.hpp" // https://github.com/bshoshany/thread-pool

typedef struct tm Date;

// Date makeDate(int year, int month, int day)
// {
//     Date ttm = {0};
//     ttm.tm_mday = day;
//     ttm.tm_mon = month - 1;
//     ttm.tm_year = year - 1900;
//     return ttm;
// }

std::string getISODateString(Date date, std::string separator)
{
    std::string year = std::to_string(date.tm_year + 1900);
    std::string month = std::to_string(date.tm_mon + 1);
    std::string day = std::to_string(date.tm_mday);

    return year + separator +
           std::string(2 - month.size(), '0').append(month) + separator +
           std::string(2 - day.size(), '0').append(day);
}

std::string getISODateString(Date date)
{
    return getISODateString(date, "-");
}

// bool operator<(const Date &d1, const Date &d2)
// {
//     if (d1.tm_year == d2.tm_year &&
//         d1.tm_mon == d2.tm_mon &&
//         d1.tm_mday == d2.tm_mday)
//         return true;
//     return false;
// };

std::map<std::tm, std::string> mapItem; // no need to pass any argument now!

class scrapeConcurrently
{
private:
    std::map<std::string, bool> symbolsMap;
    void request(Date date, std::function<void()> progressCallback);
    void parse(Date date, std::string doc);
    std::mutex mtx;

public:
    std::vector<std::string> symbolsOrdered;
    std::map<std::string, std::map<std::string, double>> datesSymbolsRates;
    scrapeConcurrently(std::vector<Date> dates, std::function<void()> progressCallback);
};

scrapeConcurrently::scrapeConcurrently(std::vector<Date> dates, std::function<void()> progressCallback)
{
    int num_of_threads = std::thread::hardware_concurrency();
    BS::thread_pool pool(num_of_threads);

    for (Date date : dates)
        pool.push_task(
            [this, date, progressCallback]
            { request(date, progressCallback); });
    pool.wait_for_tasks();
}

void scrapeConcurrently::request(Date date, std::function<void()> progressCallback)
{
    std::string urlParams = "?vYear=" + std::to_string(date.tm_year + 1900) +
                            "&vMonth=" + std::to_string(date.tm_mon + 1) +
                            "&vDay=" + std::to_string(date.tm_mday);
    std::string urlStr = "http://www.mongolbank.mn/dblistofficialdailyrate.aspx" + urlParams;

    cpr::Url url = cpr::Url{urlStr};
    cpr::Response response = cpr::Get(url);
    mtx.lock();
    parse(date, response.text);
    progressCallback();
    mtx.unlock();
}

void scrapeConcurrently::parse(Date date, std::string doc)
{
    std::regex elements("ContentPlaceHolder1_lbl(.*?)\".*?>(.*?)<");
    std::regex_iterator<std::string::iterator> elementsIter(doc.begin(), doc.end(), elements);
    std::regex_iterator<std::string::iterator> endOfString;

    std::map<std::string, double> symbolsRates;

    while (elementsIter != endOfString)
    {
        auto element = *elementsIter;
        std::string symbol = element[1];
        if (symbol != "Date")
        {
            if (!symbolsMap.contains(symbol))
            {
                symbolsMap[symbol] = true;
                symbolsOrdered.push_back(symbol);
            };

            std::string rateString = element[2];
            rateString.erase(std::remove(rateString.begin(), rateString.end(), ','), rateString.end());
            if (rateString != "")
                symbolsRates[symbol] = std::stod(rateString);
        }
        elementsIter++;
    }
    datesSymbolsRates[getISODateString(date)] = symbolsRates;
}