# VAL-2026-09-10 — başlangıç doğrulaması

**Tür:** Değişmez, retrospective. Sonuçlar aynı gün araç çıktılarından özetlendi;
ham terminal dökümü değildir. Kayıt tarihi 2026-09-10, saat dilimi Europe/Warsaw.
Komut bazında kesin saat kaydedilmedi. Git deposu/HEAD/CI yoktur.

## Kaynak ve ortam

Son ürün dosyaları ve test betikleri [SHA-256 manifestinde](SNAPSHOT-2026-09-10.json)
tanımlıdır. Manifest testlerden sonra oluşturulan kaynak fotoğrafıdır; commit
yerine geçmez. İlk CLI MPS denemesi, son hata mesajı/önbellek iyileştirmelerinden
öncedir; son kaynak için MPS kanıtı yeniden çalıştırılmış GUI testidir.

Anonim hedef: Apple M4, arm64, macOS 26.6.2. Cihaz bilgisi son GUI testinde
`platform.mac_ver`, `platform.machine`, `sysctl -n machdep.cpu.brand_string`
ile okundu. Sandbox içindeki ayrı kontrol MPS=False verdi; izinli gerçek
cihaz çalıştırmaları MPS kullandı. Bu fark performans sonucu değildir.

| Bileşen | Gözlenen sürüm |
| --- | --- |
| Python | 3.11.16 |
| Tk | 9.0 |
| kokoro / misaki | 0.9.4 / 0.9.4 |
| soundfile / customtkinter | 0.13.1 / 5.2.2 |
| torch / numpy | 2.14.0 / 2.4.6 |
| transformers / spacy | 5.17.0 / 3.8.16 |
| en_core_web_sm | 3.8.0 |

## Komut ve sonuç kaydı

Tüm yollar proje köküne göredir. Tarih her satır için 2026-09-10.

| ID | Tam komut | Exit | Sonuç | Kanıtlamadığı şey |
| --- | --- | --- | --- | --- |
| V01 | `.venv/bin/python -m unittest discover -s tests -v` | 0 | İlk çalışmada 7 test geçti; SystemExit düzeltmesinden sonra son çalışmada 1 suite / 8 test geçti (0.004 s) | Gerçek model, görsel/işitsel kabul |
| V02 | `.venv/bin/python -m compileall -q main.py tts_engine.py audio_io.py playback.py batch.py scripts tests` | 0 | Belirtilen Python dosyaları derlendi | GUI doğruluğu, üretim başarısı |
| V03 | `HF_HOME=.cache/huggingface .venv/bin/python scripts/smoke_tts.py --device auto` | 0 | Gerçek af_heart, MPS, 24000 Hz, 9.4 s; WAV/MP3 yazıldı ve tekrar okundu | Son kaynak sürümüyle birebir eşleşme; telaffuz veya hızlanma |
| V04 | `.venv/bin/python -u scripts/smoke_tts.py --device cpu --voice bm_george --output outputs/british-cpu` | 0 | Gerçek bm_george, CPU, 24000 Hz, 10.225 s; WAV/MP3 tekrar okuma geçti | Bütün 28 ses, bütün hızlar, insan kabulü |
| V05 | `.venv/bin/python -u scripts/smoke_gui.py` | 0 | Son GUI kaynaklarıyla pencere açıldı; gerçek MPS sentezi, önizleme dosyası, Kaydet etkinliği ve play/pause/resume/stop süreç durumu geçti | Piksel/görsel inceleme, işitilebilirlik, dosya diyalogları ve manuel kabul |
| V06 | `.venv/bin/python scripts/evidence_snapshot.py` | 0 | Kaynak/çıktı hash manifesti oluşturuldu; mevcut kaydın üzerine yazmaz | Git commit veya CI kanıtı |

V01 testleri: giriş doğrulama; MPS CPU yeniden deneme; hassas istisna içeriğini
gizleme; dil indiricisi SystemExit; WAV round-trip; atomik yazımın eski dosyayı
koruması ve geçici dosyayı temizlemesi; batch hata izolasyonu/aynı ad; MP3 yokluğu.

V03/V04 sayısal kontrolleri: sonlu örnekler, yeterli uzunluk, sessiz olmayan
üretim, 24000 Hz; iki codec yeniden çözümlemede sonlu ve yeterli uzun ses.

V05 son yapılandırılmış araç çıktısı (anonim):

```json
{"gui":"opened","synthesis":"passed","device":"mps","platform":"26.6.2","architecture":"arm64","processor":"Apple M4","play_pause_resume_stop":"process state passed","manual_visual_audio_acceptance":"pending"}
```

## Artefaktlar ve sınırlar

| Artefakt | Konum | Hash kaynağı | Saklama / gizlilik |
| --- | --- | --- | --- |
| Test metni | assets/sample.txt | Manifest | AI üretimi, kişisel veri yok |
| İlk MPS WAV/MP3 | outputs/smoke/sample.wav ve sample.mp3 | Manifest | Yerel, gitignore; tez paylaşım izni bekliyor |
| CPU Britanya WAV/MP3 | outputs/british-cpu/sample.wav ve sample.mp3 | Manifest | Yerel, gitignore; tez paylaşım izni bekliyor |
| Son GUI önizlemesi | OS geçici klasörü | Kaydedilmedi | Normal kapanışta temizlendi; kalıcı ses artefaktı yok |
| Kaynak fotoğrafı | SNAPSHOT-2026-09-10.json | İç SHA-256 değerleri | Göreli yollar; eklemeli korunur |

Git hash olmadığı için otomatik testlerin E2 asgari paketi tamamlanmış değildir.
Build fotoğrafı + anonim hedef + senaryo + sonuç + bu artefakt kaydı yalnız
dar kapsamlı gerçek CPU üretimi/GUI süreç akışı iddialarını E3 olarak destekler.
Görsel kalite veya sesin iyi olduğu iddiası yapılmaz.

## Başarısız/iyileştirilmiş denemeler

- İlk uv ve Python indirmeleri sandbox DNS kısıtından başarısız oldu. İzinli
  indirme ile tamamlandı. Bu uygulama sentez hatası değildir.
- uv ortamında pip bulunmadığı gözlendi; spaCy kaynak kurulumundan önce pip
  eklendi. README açık dil kaynağı kurulum adımıyla düzeltildi.
- AI incelemesi, upstream dil indiricisinin SystemExit üretebildiğini buldu;
  hata yönetimi ve regresyon testi eklendi. Canlı bir GUI takılması gözlenmedi.
- İlk batch hataları yalnız istisna sınıfı gösteriyordu; açıklayıcı Türkçe
  boş metin/kodlama/erişim mesajlarıyla düzeltildi.
- Upstream dropout, weight_norm ve torch.jit deprecation uyarıları görüldü;
  testler exit 0 ile tamamlandı. Uyarıların giderildiği iddia edilmiyor.

## Açık kontroller

Manuel görsel inceleme, telaffuz/kalite, 0.5x/2x uçları, bütün sesler,
dosya diyalogları, doğal oynatma bitişi, gerçek kullanıcı batch senaryosu,
MPS hız ölçümü, insan nihai kabulü ve yayın bekliyor. Kalıcı konuşma/issue
referansı yok; insan onayı kanıtı tezde kullanılacaksa kontrollü konuşma/issue
referansı sonradan eklenmelidir.

## 2026-09-10 — ek belge doğrulama kaydı V07

İlk kayda ek olarak `.venv/bin/python scripts/check_evidence.py` çalıştırıldı,
exit 0. Sonuç: 15 Markdown belgesi, 11 kaynak hash'i, 4 yerel ses artefaktı hash'i,
0 hata. Göreli Markdown bağlantıları, şablonların 13/12 numaralı bölümü ve
mutlak kullanıcı yolu kalıpları kontrol edildi. Bu sınırlı tarama tam bir sır
tarayıcısı veya belgelerin insan tarafından kabulü değildir. Kontrol betiği
başlangıç kaynak manifestinden sonra eklendi; o manifestin parçası değildir.
