
import fetch from "node-fetch"
import { load } from "cheerio"

let symbolsOrdered = []
let datesSymbolsRates = {}

export default function scrapeAsynchronouslyPromise(dates, progressCallback) {
    return Promise.all(dates.map(date => requestPromise(date, progressCallback))).then(
        _ => ({
            symbolsOrdered: [...new Set(symbolsOrdered)],
            datesSymbolsRates
        })
    )
}

function requestPromise(date, progressCallback) {
    const urlParams = `?vYear=${date.getFullYear()}&vMonth=${date.getMonth() + 1}&vDay=${date.getDate()}`
    const URL = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx" + urlParams

    return fetch(URL)
        .then(response => response.text())
        .then(doc => {
            parse(date, doc)
            progressCallback()
        })
        .catch(err => { throw err })
}

function parse(date, doc) {
    const spanIDPrefix = "ContentPlaceHolder1_lbl"

    const elements = load(doc)(`.uk-comment-list span[id^=${spanIDPrefix}]`)

    let symbolsRates = {}

    elements.each((_, element) => {
        const symbol = element.attribs.id.slice("ContentPlaceHolder1_lbl".length)
        symbolsOrdered.push(symbol)
        const rate = parseFloat(element.children[0]?.data.replace(",", ""))
        if (!isNaN(rate)) {
            symbolsRates[symbol] = rate
        }
    })
    const dateString = date.toISOString().substring(0, 10)
    datesSymbolsRates[dateString] = symbolsRates
}