# Kalite ve güvenlik — yaşayan belge

## Kanıt düzeyleri

| Kod | Anlam | Asgari kanıt |
| --- | --- | --- |
| E0 | İddia / retrospektif anlatı | Kaynak belge + sınırlama notu |
| E1 | Depoda gözlemlenen uygulama | Commit hash + dosya/satır veya diff |
| E2 | Otomatik doğrulama | Commit hash + tam komut + tarihli sonuç/CI |
| E3 | Hedef cihazda doğrulama | Build kimliği + anonim cihaz/OS + senaryo + sonuç + artefakt |
| E4 | İnsan kabulü / sürüm kanıtı | Açık kabul kaydı ve/veya yayımlanmış sürüm kimliği |

Düzey numaranın büyüklüğüne göre değil, iddiayı destekleyen kanıta göre seçilir.
Uygulandı → otomatik test geçti → cihazda doğrulandı → yayımlandı ayrı durumlardır.

## Otomatik testler neyi kanıtlamaz?

- Unit testler gerçek modelin yüklenmesini, MPS hızını veya ses kalitesini kanıtlamaz.
- Mock ile CPU fallback testi gerçek M4 üzerinde başarılı çıkarım anlamına gelmez.
- Derleme GUI yerleşimini, görsel hataları ve Tk etkileşimlerini kanıtlamaz.
- WAV/MP3 çözümleme testi İngilizce telaffuzun doğruluğunu kanıtlamaz.
- GUI açılışı play/pause'un işitilebilirliğini veya bütün dosya diyaloglarını kanıtlamaz.
- Hiçbir otomatik test insan nihai kabulü veya yayın kanıtı değildir.

## Hedef cihaz kabul senaryoları

Her senaryoda build/hash, anonim cihaz/OS, tarih, sonuç ve kontrollü artefakt kaydet.

| Senaryo | Beklenen |
| --- | --- |
| İngilizce test metni, ABD kadın ve Britanya erkek ses | Tam, anlaşılır ses; doğru seçim |
| Hız 0.5 / 1 / 2 | Ayar uygulanır; ses kalite kontrolü ayrıca |
| Model ilk yükleme, ardından önbellekli kullanım | Açıklayıcı durum, arayüz yanıt verir |
| MPS kullanılabilir / CPU zorlanmış | Başarı veya anlaşılır hata, gerçek cihaz kaydı |
| Play → pause → resume → doğal bitiş | Aynı konumdan devam, buton durumu doğru |
| WAV/MP3 kaydet ve diyaloğu iptal | Doğru codec, iptalde dosya yazılmaz |
| Aynı adlı, boş ve bozuk UTF-8 TXT batch | Sıra korunur, tek hata kalanları durdurmaz |
| Üretim sırasında kapat, sonra boşta kapat | İş bitmesi istenir; boşta oynatıcı/geçici dosya temizlenir |

## Gizlilik ve güvenlik

Metin yerel modelde işlenir. İlk kullanımda model/G2P/ses indirmeleri dış ağa
erişir. Model sağlayıcısına kullanıcı metni gönderen bir API uygulanmaz.
Önizlemeler OS geçici klasöründedir; normal kapanışta temizlenir. Beklenmedik
sonlandırma geçici dosya bırakabilir. Kaydedilen dosyaları kullanıcı yönetir.
Upstream debug logları metin içerebilir; ham logları paylaşmadan önce redakte et.

Kanıt/prompt içine anahtar, parola, token, credential, gereksiz kişisel/finansal
veri, UUID ve mutlak kullanıcı yolları konmaz. Kullanıcı ekran görüntüleri
repoya kopyalanmaz. Anonim cihaz bilgisi ve AI'ya verilen veri türleri kaydedilir.
Tezde paylaşılacak artefaktlar için paylaşım izni ayrıca doğrulanır.

Bağımlılık aralıkları yeniden kurulumda değişebilir; ölçümlerde gerçek sürümleri
ayrı kaydet. Model/ses kataloğu dış kaynaktır; güncellemeler yeniden doğrulama ister.
