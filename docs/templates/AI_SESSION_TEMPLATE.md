# AI oturum kaydı — <proje>

Bu şablon teknoloji bağımsızdır. Yer tutucuları kanıta göre doldur; bilinmeyene
`kaydedilmedi`, ölçülmeyene `ölçülmedi` yaz. Tamamlanan kayıt eklemeli korunur.

## 1. Oturum kimliği

| Alan | Kayıt |
| --- | --- |
| Oturum | AI-<YYYY>-<AA>-<GG>-<KONU>-<NNN> |
| Tarih / saat dilimi | <ISO-8601 / saat dilimi> |
| Kayıt zamanı ve niteliği | <prospective / retrospective; olay ve kayıt tarihleri> |
| AI aracı / model sürümü | <doğrulanmış bilgi veya kaydedilmedi> |
| Kontrollü konuşma / issue referansı | <referans veya kaydedilmedi> |

## 2. İnsan talebi ve yetki sınırı

| Alan | Kayıt |
| --- | --- |
| İnsan hedefi | <hedef> |
| İnsan tarafından verilen kabul kriterleri | <kriterler> |
| AI'nın önerdiği ek kriterler | <öneri; insan seçimi ayrı> |
| Yasak alanlar / işlemler | <sınırlar> |

- [ ] Okuma / analiz yetkisi
- [ ] Belirtilen dosyalarda kod yazma yetkisi
- [ ] Test / yerel çalıştırma yetkisi
- [ ] Belge yazma yetkisi
- [ ] Commit yetkisi (varsa kapsam)
- [ ] Dış sistem yazımı / yayın yetkisi (açık referans gerekir)

| Sonradan genişletilen yetki | İnsan kaynağı | Tarih | Kapsam / süre |
| --- | --- | --- | --- |
| <yetki veya yok> | <referans> | <tarih> | <sınır> |

## 3. Girdiler ve gizlilik sınıflandırması

| Girdi türü | Sınıf: public/internal/restricted | Amaç | AI'ya aktarılan bölüm | Redaksiyon |
| --- | --- | --- | --- | --- |
| <gereksinim/kod/log> | <sınıf> | <amaç> | <asgari veri> | <işlem> |

Credential, anahtar, parola, token, gereksiz kişisel/finansal veri ve cihaz UUID'si
eklenmez. Mutlak kullanıcı yolları yazılmaz. Kullanıcı ekran görüntüleri kopyalanmaz.

## 4. Başlangıç kanıtı

| Alan | Kayıt |
| --- | --- |
| `git status --short` | <anonimleştirilmiş sonuç> |
| Branch / HEAD | <kimlik veya kaydedilmedi> |
| Mevcut kullanıcı değişiklikleri | <kapsam> |
| Yeniden üretim adımları | <adımlar> |
| Mevcut davranış / ölçüm | <sonuç veya ölçülmedi> |
| Başlangıç artefaktı | <kontrollü referans> |

Sonradan hafızadan baseline üretme; gözlem ile varsayımı ayır.

## 5. Plan ve insan kontrol noktaları

| Adım | Beklenen çıktı | Yetki kaynağı | İnsan kontrol noktası | Durum |
| --- | --- | --- | --- | --- |
| <adım> | <çıktı> | <talep> | <gerekli ise açık kabul> | <durum> |

## 6. Karar günlüğü

| Karar ID | Bağlam | AI önerisi | İnsan kararı | Gerekçe | ADR/kanıt |
| --- | --- | --- | --- | --- | --- |
| <kimlik> | <problem> | <öneri> | AI önerisi — onay bekliyor | <gerekçe> | <referans> |

İnsan seçmediyse öneriyi insan kararı olarak göstermeyin.

## 7. Uygulama kaydı

| Değişiklik | Kod/diff | Gereksinim | Karar | Uygulama durumu |
| --- | --- | --- | --- | --- |
| <değişiklik> | <referans> | <kimlik> | <kimlik> | <durum> |

### Kullanılmayan veya hatalı AI çıktıları

| Çıktı / öneri | Reddedildi / düzeltildi | Neden | Düzeltme | Kanıt |
| --- | --- | --- | --- | --- |
| <çıktı veya gözlenmedi> | <durum> | <neden> | <yeni çıktı> | <referans> |

## 8. Otomatik doğrulama

| Komut | Commit | Ortam | Tarih | Exit | Sonuç | Log | Kanıtlamadığı şey |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <tam komut> | <hash/kaydedilmedi> | <anonim ortam> | <ISO tarih> | <kod> | <suite/test sayısı> | <referans> | <sınır> |

## 9. Cihaz/entegrasyon doğrulaması

| Build kimliği | Cihaz / OS (anonim) | Senaryo | Tarih | Sonuç | Artefakt | Doğrulayan |
| --- | --- | --- | --- | --- | --- | --- |
| <kimlik> | <cihaz> | <adımlar> | <tarih> | <bekleniyor/geçti/kaldı> | <kontrollü ref> | <rol> |

## 10. Sonuç ve insan kabulü

| Aşama | Durum | Kanıt / eksik |
| --- | --- | --- |
| Uygulandı | <durum> | <referans> |
| Otomatik test geçti | <durum> | <referans> |
| Hedef cihazda doğrulandı | <durum> | <referans> |
| İnsan nihai kabulü | <durum> | <açık kabul referansı> |
| Yayımlandı | <durum> | <sürüm kimliği> |

## 11. Gizlilik kontrol listesi

- [ ] Anahtar/parola/token/credential yok.
- [ ] Gereksiz kişisel veya finansal veri yok.
- [ ] Cihaz UUID'si ve mutlak kullanıcı yolları yok; cihaz anonimleştirildi.
- [ ] Kullanıcı ekran görüntüleri repoya kopyalanmadı.
- [ ] AI'ya aktarılan veri türleri ve redaksiyon belirtildi.
- [ ] Tez artefaktları paylaşım izni ayrı doğrulandı veya bekliyor yazıldı.

## 12. Retrospektif sınırlama beyanı

| Soru | Yanıt |
| --- | --- |
| Kayıt olaydan sonra mı yazıldı? | <yanıt> |
| Olay tarihi kanıtla biliniyor mu? | <yanıt> |
| Başlangıç commit/diff mevcut mu? | <yanıt> |
| Model/araç sürümü doğrulandı mı? | <yanıt> |
| Başarısız veya reddedilmiş çıktılar eksik mi? | <yanıt> |
| Otomatik, cihaz ve insan kabul kanıtları ayrıldı mı? | <yanıt> |
| Kalıcı konuşma/onay ve paylaşım izni referansı var mı? | <yanıt> |

## 13. Kısa akademik katkı özeti

| İnsan | AI | Doğrulama | Atıf sınırı | Retrospektif sınırlama |
| --- | --- | --- | --- | --- |
| <gereksinim/seçim/kabul> | <analiz/plan/kod/test/inceleme/dokümantasyon/araştırma> | <kanıt> | <iddia sınırı> | <eksikler> |

Kalıcı konuşma referansı yoksa: insan onayı kanıtı tezde kullanılacaksa kontrollü
konuşma/issue referansı sonradan eklenmelidir.
