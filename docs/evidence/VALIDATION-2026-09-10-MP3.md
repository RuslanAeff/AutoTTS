# VAL-2026-09-10-MP3 — seçilen kayıt formatının korunması

Retrospective; 2026-09-10 / Europe/Warsaw. Başlangıç `git status --short`:
Git deposu yok; branch/HEAD kaydedilmedi. Kaynak fotoğrafı
[SNAPSHOT-2026-09-10-MP3.json](SNAPSHOT-2026-09-10-MP3.json); commit değildir.

## Sorun ve gözlem
İnsan açıklaması: “MP3 seçsem de WAV kaydediliyor.” Kodda kayıt diyaloğunun
initialfile ve defaultextension değerleri sabit WAV idi; save_audio codec'i
yalnız dönen yolun uzantısından seçiyordu. Kaydedilmiş örnek WAV ile yapılan
ayrı MP3 yazma/okuma kontrolü başarılıydı: soundfile 0.13.1, libsndfile 1.2.2,
MP3/MPEG_LAYER_III, 24000 Hz, 225600 frame, 68856 byte. Codec arızası gözlenmedi.
Kullanıcının fiziksel diyalog etkileşimi birebir yeniden yürütülmedi.

## Düzeltme
Tekli Kaydet yanında açık WAV/MP3 seçimi; diyaloğun adı/uzantısı/filtresi bu
seçimden türetilir. Eski WAV uzantısı dönse bile export_path seçilen MP3 uzantısını
korur. Üzerine yazma onayı düzeltilmiş son hedef için alınır. Durum mesajı
kaydedilen dosyanın adını/formatını gösterir. Yeni yüksek riskli mimari tercih
yok; mevcut atomik dışa aktarma sözleşmesinin hata düzeltmesidir, yeni ADR açılmadı.

## Doğrulama

| Tam komut · 2026-09-10 | Exit | Sonuç | Sınır |
| --- | --- | --- | --- |
| `.venv/bin/python -m unittest discover -s tests -v` | 0 | 3 test sınıfı, 18 test geçti | Fiziksel macOS kayıt diyaloğu veya insan kabulü değil |
| `.venv/bin/python -m compileall -q main.py audio_io.py tests scripts` | 0 | Derleme geçti | Görsel doğruluk değil |
| `.venv/bin/python scripts/evidence_snapshot.py --output docs/evidence/SNAPSHOT-2026-09-10-MP3.json` | 0 | Yeni kaynak/önceki ses artefaktı manifesti | Git commit değildir |

Yeni regresyon testleri: MP3 seçiliyken diyalog WAV döndürdüğünde gerçek MP3
yazımı/yeniden okuma; uzantısız ve noktalı adlar; iptalde iş başlamaması;
düzeltilmiş MP3 hedefindeki mevcut dosyanın “hayır” cevabında korunması.
Dosya diyaloğu mock, MP3 kodlama ve çözümleme gerçektir. Geçici test dosyaları
temizlenmiştir. Git hash yokluğu nedeniyle E2 asgari paketi eksik; izlenebilirlik
düzeyi E0 tutulur. Uygulandı/test geçti ayrı; cihazda manuel onay ve yayın yok.

Kullanıcı ekran görüntüsü/ham log kopyalanmadı. Mutlak kullanıcı yolları ve
kişisel veri kanıta eklenmedi. Tezde paylaşım izni ve kontrollü konuşma referansı bekliyor.
