import java.io.IOException;
import java.time.*;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

interface ProgressCallback {
    void call();
}

class ScrapeConcurrently {
    LinkedHashSet<String> symbolsOrdered = new LinkedHashSet<>();
    HashMap<LocalDate, HashMap<String, Float>> datesSymbolsRates = new HashMap<>();

    ScrapeConcurrently(List<LocalDate> dates, ProgressCallback progressCallback) {
        dates.parallelStream().forEach(date -> {
            request(date, progressCallback);
        });
    }

    void request(LocalDate date, ProgressCallback progressCallback) {
        String urlParams = "?vYear=%s&vMonth=%s&vDay=%s"
                .formatted(date.getYear(), date.getMonthValue(), date.getDayOfMonth());
        String url = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx" + urlParams;

        try {
            Document doc = Jsoup.connect(url).get();
            parse(date, doc);
        } catch (IOException e) {
            e.printStackTrace();
        }
        progressCallback.call();
    }

    void parse(LocalDate date, Document doc) {
        String spanIDPrefix = "ContentPlaceHolder1_lbl";

        Elements elements = doc.select(".uk-comment-list span[id^=%s]".formatted(spanIDPrefix));

        HashMap<String, Float> symbolRates = new HashMap<>();

        for (Element element : elements) {
            String symbol = element.id().substring(spanIDPrefix.length());
            addIfNotExist(symbol);
            if (element.text() != "") {
                Float rate = Float.parseFloat(element.text().replace(",", ""));
                symbolRates.put(symbol, rate);
            }
        }
        datesSymbolsRates.put(date, symbolRates);
    }

    synchronized void addIfNotExist(String symbol) {
        if (!symbolsOrdered.contains(symbol)) {
            symbolsOrdered.add(symbol);
        }
    }
}
