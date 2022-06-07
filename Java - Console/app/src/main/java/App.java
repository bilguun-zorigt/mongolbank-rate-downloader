import java.io.FileWriter;
import java.io.IOException;
import java.time.*;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Scanner;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class App {
    static Boolean headerWritten = false;

    public static void main(String[] args) {
        Scanner reader = new Scanner(System.in);
        System.out.println("Enter date to download from (yyyy-mm-dd): ");
        String startDateInputString = reader.nextLine();
        System.out.println("Enter date to download to (yyyy-mm-dd): ");
        String endDateInputString = reader.nextLine();
        reader.close();

        LocalDate startDate = LocalDate.parse(startDateInputString);
        LocalDate endDate = LocalDate.parse(endDateInputString);
        List<LocalDate> dates = startDate.datesUntil(endDate.plusDays(1)).toList();

        String fileName = "Rates " + startDate.toString().replace("-", "") + "-" +
                endDate.toString().replace("-", "") + ".csv";

        dates.parallelStream().forEach(date -> {
            Request request = new Request(date);
            LinkedHashMap<String, String> row = request.scrape();
            writeRowToCSV(fileName, row);
        });
    }

    public static void writeRowToCSV(String fileName, LinkedHashMap<String, String> row) {
        try {
            FileWriter pw = new FileWriter(fileName, true);
            if (!headerWritten) {
                String fieldsRowString = String.join(",", row.keySet()) + "\n";
                pw.append(fieldsRowString);
                headerWritten = true;
            }
            String rowString = String.join(",", row.values()) + "\n";
            pw.append(rowString);
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}

class Request {
    private String url;
    private LinkedHashMap<String, String> row;

    Request(LocalDate date) {
        url = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=%s&vMonth=%s&vDay=%s"
                .formatted(date.getYear(), date.getMonthValue(), date.getDayOfMonth());
        row = new LinkedHashMap<String, String>();
        row.put("Date", date.toString());
    }

    public LinkedHashMap<String, String> scrape() {
        try {
            Document doc = Jsoup.connect(url).get();
            parse(doc);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return row;
    }

    public void parse(Document doc) {
        String span_id_prefix = "ContentPlaceHolder1_lbl";
        Elements elements = doc.select(".uk-comment-list span[id^=%s]".formatted(span_id_prefix));

        for (Element element : elements) {
            String symbol = element.id().substring(span_id_prefix.length());
            String rate = element.text().replace(",", "");// Float rate = Float.parseFloat();
            row.put(symbol, rate);
        }
    }
}