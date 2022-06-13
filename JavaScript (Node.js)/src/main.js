import promptSync from "prompt-sync"
import { writeFile } from "fs"
import scrapeAsynchronouslyPromise from "./scraper.js"

let startDate
let endDate
let fileName
let totalDays
let doneDays = 0;

(async function main() {
    welcomeMessage()

    const datesOrdered = getDates()
    totalDays = datesOrdered.length

    const scrapingStartTime = performance.now()
    const { symbolsOrdered, datesSymbolsRates } = await scrapeAsynchronouslyPromise(datesOrdered, updateProgressBar)
    const scrapingDuration = performance.now() - scrapingStartTime

    const convertionStartTime = performance.now()
    const csvString = getCSVString(symbolsOrdered, datesOrdered, datesSymbolsRates)
    const convertionDuration = performance.now() - convertionStartTime

    const csvWriteStartTime = performance.now()
    writeCSVFile(csvString)
    const csvWriteDuration = performance.now() - csvWriteStartTime

    successMessage()

    console.log("Reports:")
    printDuration("Scraping:    ", scrapingDuration)
    printDuration("Convertion:  ", convertionDuration)
    printDuration("CSV creation:", csvWriteDuration)
})()

function welcomeMessage() {
    console.log("Source code at: \x1B[34mhttps://github.com/bilguun-zorigt\x1B[0m")
}

function getDateInput(message) {
    const prompt = promptSync()
    let date
    while (true) {
        const dateString = prompt(`\x1B[0m${message}\x1B[34m`)
        try {
            date = new Date(dateString)
            if (date.toISOString().substring(0, 10) !== dateString) {
                console.log("\x1B[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\x1B[0m")
                continue
            }
        } catch (error) {
            console.log("\x1B[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\x1B[0m")
            continue
        }
        break
    }
    return date
}

function getDates() {
    startDate = getDateInput("Enter date to download from (yyyy-mm-dd): ")
    endDate = getDateInput("Enter date to download to (yyyy-mm-dd): ")

    let dates = []
    for (let date = new Date(startDate); date <= endDate; date.setDate(date.getDate() + 1)) {
        dates.push(new Date(date))
    }
    return dates
}

function updateProgressBar() {
    doneDays++
    const pbLength = 25
    const doneLength = Math.round(doneDays * (pbLength / totalDays))
    const doneLengthString = "█".repeat(doneLength)
    const remainingLengthString = "█".repeat(pbLength - doneLength)
    const percentString = doneDays / totalDays * 100
    // https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    // https://stackoverflow.com/questions/17309749/node-js-console-log-is-it-possible-to-update-a-line-rather-than-create-a-new-l
    process.stdout.clearLine(0)
    process.stdout.cursorTo(0)
    process.stdout.write(`\r\x1B[0mCurrent progress: \x1B[34m${doneLengthString}\x1B[41;31m${remainingLengthString}\x1B[0m\x1B[34m ${doneDays}/${totalDays} ${percentString}%\x1B[0m`)

}

function getCSVString(symbolsOrdered, datesOrdered, datesSymbolsRates) {
    let csvString = "Date"
    symbolsOrdered.forEach(symbol => csvString += "," + symbol)
    datesOrdered.forEach(date => {
        const dateString = date.toISOString().substring(0, 10)
        csvString = csvString + "\n" + dateString
        symbolsOrdered.forEach(symbol => {
            let rateString = datesSymbolsRates[dateString][symbol]
            if (rateString === undefined) {
                rateString = ""
            }
            csvString = csvString + "," + rateString
        })
    })
    return csvString
}

function writeCSVFile(csvString) {
    fileName = `BoM Rates ${startDate.toISOString().substring(0, 10).replaceAll("-", "")}-${endDate.toISOString().substring(0, 10).replaceAll("-", "")}.csv`
    writeFile(
        fileName,
        csvString,
        error => { if (error) throw error }
    )
}

function successMessage() {
    console.log(`\nFile saved: '\x1B[34m${fileName}\x1B[0m'\n`)
}

function printDuration(operationName, durationTime) {
    console.log(`${operationName} \x1B[34m${(durationTime / 1000).toFixed(2)}\x1B[0m seconds or \x1B[34m${~~durationTime}\x1B[0m milliseconds or \x1B[34m${~~(durationTime * 1000)}\x1B[0m microseconds`)
}
