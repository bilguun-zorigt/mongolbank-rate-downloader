import fetch from "node-fetch"
import { load } from "cheerio"
import promptSync from "prompt-sync"
import { writeFile } from "fs"

function parse(htmlString, dateString, URL) {
  const html = load(htmlString)
  const elements = html('.uk-comment-list span')

  let row = { "Date": dateString }
  elements.each((_, element) => {
    const symbol = element.attribs.id.slice("ContentPlaceHolder1_lbl".length)
    const rate = parseFloat(element.children[0]?.data.replace(",", ""))
    row[symbol] = rate
  })
  console.log("SCRAPED: ", URL)
  return row
}

function getRowPromise(date) {
  const URL = `https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=${date.getFullYear()}&vMonth=${date.getMonth() + 1
    }&vDay=${date.getDate()}`
  const dateString = date.toISOString().split('T')[0]
  const rowPromise = fetch(URL)
    .then(response => response.text())
    .then(htmlString => parse(htmlString, dateString, URL))
  return rowPromise
}

function getListOfDates() {
  const prompt = promptSync()
  const startDate = prompt("Enter date to download from (yyyy-mm-dd): ")
  const endDate = prompt("Enter date to download to (yyyy-mm-dd): ")

  let listOfDates = [];
  for (let d = new Date(startDate); d <= new Date(endDate); d.setDate(d.getDate() + 1)) {
    listOfDates.push(new Date(d));
  }
  return listOfDates
}

function convertToCSV(arr) {
  const array = [Object.keys(arr[0])].concat(arr)
  return array.map(it => {
    return Object.values(it).toString()
  }).join('\n')
}

function main() {
  const INFO = "Source code at: https://github.com/bilguun-zorigt\n"

  console.log(INFO)
  const listOfDates = getListOfDates()
  console.log("\n***** Starting...")

  Promise.all(listOfDates.map(d => getRowPromise(d)))
    .then(result => {
      writeFile(
        "rates.csv",
        convertToCSV(result),
        error => {
          if (error) return console.log("error: ", error)
          console.log("***** Done. File saved.\n")
          console.log(INFO)
        })
    })
}

main()
