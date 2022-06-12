import java.io.FileWriter;
import java.io.IOException;
import java.time.*;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class Main {
    static LocalDate startDate;
    static LocalDate endDate;
    static String fileName;
    static int totalDays;
    static int doneDays = 0;
    static Scanner reader = new Scanner(System.in);

    public static void main(String[] args) {
        welcomeMessage();

        List<LocalDate> datesOrdered = getDates();
        totalDays = datesOrdered.size();

        long scrapingStartTime = System.nanoTime();
        ScrapeConcurrently scraped = new ScrapeConcurrently(datesOrdered, new ProgressCallback() {
            public void call() {
                updateProgressBar();
            }
        });
        long scrapingDuration = (System.nanoTime() - scrapingStartTime);

        long convertionStartTime = System.nanoTime();
        String csvString = getCSVString(scraped.symbolsOrdered, datesOrdered, scraped.datesSymbolsRates);
        long convertionDuration = (System.nanoTime() - convertionStartTime);

        long csvWriteStartTime = System.nanoTime();
        writeCSVFile(csvString);
        long csvWriteDuration = (System.nanoTime() - csvWriteStartTime);

        successMessage();
        System.out.print("\nReports:\n");
        printDuration("Scraping:    ", scrapingDuration);
        printDuration("Convertion:  ", convertionDuration);
        printDuration("CSV creation:", csvWriteDuration);
    }

    static void welcomeMessage() {
        System.out.print("Source code at: \033[34mhttps://github.com/bilguun-zorigt\033[0m\n");
    }

    static LocalDate getDateInput(String message) {
        LocalDate date;
        while (true) {
            System.out.print("\033[0m" + message + "\033[34m");
            String dateString = reader.nextLine();
            try {
                date = LocalDate.parse(dateString);
            } catch (Exception e) {
                System.out.printf("\033[31mDate entered is not valid. Must be formatted as yyyy-mm-dd\033[0m\n");
                continue;
            }
            break;
        }
        return date;
    }

    static List<LocalDate> getDates() {
        startDate = getDateInput("Enter start date (yyyy-mm-dd): ");
        endDate = getDateInput("Enter end date (yyyy-mm-dd): ");
        reader.close();
        List<LocalDate> dates = startDate.datesUntil(endDate.plusDays(1)).toList();
        return dates;
    }

    static synchronized void updateProgressBar() {
        doneDays++;
        int pbLength = 25;
        int doneLength = Math.round(doneDays * (pbLength / (float) totalDays));
        String doneLengthString = "█".repeat(doneLength);
        String remainingLengthString = "█".repeat(pbLength - doneLength);
        Float percentString = doneDays / (float) totalDays * 100;
        // https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
        System.out.printf("\r\033[0mCurrent progress: \033[34m%s\033[41;31m%s\033[0m\033[34m %s/%s %.1f%%\033[0m",
                doneLengthString, remainingLengthString, doneDays, totalDays, percentString);
    }

    private static String getCSVString(LinkedHashSet<String> symbolsOrdered, List<LocalDate> datesOrdered,
            HashMap<LocalDate, HashMap<String, Float>> datesSymbolsRates) {
        String csvString = "Date";
        for (String symbol : symbolsOrdered) {
            csvString = csvString + "," + symbol;
        }
        for (LocalDate date : datesOrdered) {
            csvString = csvString + "\n" + date;
            for (String symbol : symbolsOrdered) {
                String rateString = Float.toString(
                        ((HashMap<String, Float>) datesSymbolsRates.get(date)).getOrDefault(symbol, 0f));
                if (rateString.equals("0.0")) {
                    rateString = "";
                }
                csvString = csvString + "," + rateString;
            }
        }
        return csvString;
    }

    private static void writeCSVFile(String csvString) {
        fileName = "BoM Rates %s-%s.csv".formatted(
                startDate.toString().replace("-", ""),
                endDate.toString().replace("-", ""));
        try {
            FileWriter pw = new FileWriter(fileName);
            pw.append(csvString);
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static void successMessage() {
        System.out.printf("\nFile saved: '\033[34m%s\033[0m'\n", fileName);
    }

    static void printDuration(String operationName, long durationTime) {
        System.out.printf(
                "%s \033[34m%.2f\033[0m seconds or \033[34m%s\033[0m milliseconds or \033[34m%s\033[0m microseconds or \033[34m%s\033[0m nanoseconds\n",
                operationName,
                TimeUnit.MILLISECONDS.convert(durationTime, TimeUnit.NANOSECONDS) / (float) 1000,
                TimeUnit.MILLISECONDS.convert(durationTime, TimeUnit.NANOSECONDS),
                TimeUnit.MICROSECONDS.convert(durationTime, TimeUnit.NANOSECONDS),
                TimeUnit.NANOSECONDS.convert(durationTime, TimeUnit.NANOSECONDS));
    }
}
