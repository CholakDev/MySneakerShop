package com.satoshidca.backend;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*") // Разрешаем нашему HTML-интерфейсу обращаться к серверу
public class PaymentController {

    // Спринг сам достанет токен из application.properties
    @Value("${cryptobot.api.token}")
    private String cryptoBotToken;

    @Value("${cryptobot.api.url}")
    private String cryptoBotUrl;

    // Этот метод сработает, когда кто-то обратится по адресу /api/create-invoice
    @PostMapping("/create-invoice")
    public ResponseEntity<String> createInvoice() {
        try {
            // Указываем, что мы хотим продать: 10 USDT за "Satoshi PRO"
            String jsonBody = "{\"asset\": \"USDT\", \"amount\": \"10.00\", \"description\": \"Подписка Satoshi PRO на 1 месяц\"}";

            // Собираем запрос к официальному серверу CryptoBot
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(cryptoBotUrl + "createInvoice"))
                    .header("Crypto-Pay-API-Token", cryptoBotToken)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                    .build();

            // Отправляем запрос и ждем ответ
            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            // Возвращаем ответ от CryptoBot (там будет готовая ссылка на оплату) обратно в наш интерфейс
            return ResponseEntity.ok(response.body());

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("{\"error\": \"Ошибка при создании счета\"}");
        }
    }
}