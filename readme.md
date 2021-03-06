Сервер для хранения фотографий, которые вы хотите видеть в приложении Blynk. 

Принцип работы
==============
1. Устройство шлёт изображение в POST запросе, сервер сохраняет её и возвращает уникальный URL.
2. Устройство шлёт в Blynk этот URL
3. Blynk обновляет изображение в своем приложении

![Принцип работы blynk_image_widget_server](https://github.com/dontsovcmc/blynk_image_widget_server/blob/master/assets/diag.png)

Использование
=============
1. Добавляем в проект Blynk виджет «Image Gallery»

2. В прошивке:

а. Отправляем изображение на сервер POST запросом:

Отправка esp_http_client (отрывок!):

```
# image_buffer - буфер с изображением
# image_size - размер изображения в байтах

esp_http_client_set_post_field(http_client, (const char *)image_buffer, image_size);
esp_http_client_set_header(http_client, "Content-Type", "image/jpg");
esp_http_client_set_header(http_client, "Content-Length", String(data.frame_size).c_str());
esp_http_client_set_header(http_client, "Blynk-Token", settings.blynk_key);  //добавится к имени файла
```


б. Шлем в Blynk новую ссылку:

```
Blynk.virtualWrite(V20, 1); 
Blynk.setProperty(V20, "urls", image_url);  //image_url - полный URL к изображению
Blynk.virtualWrite(V20, 1);
```

3. Открываем приложение и видим новое изображение. Profit!
