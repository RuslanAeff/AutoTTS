# ADR-001 — Yerel TTS, GUI'den bağımsız motor sözleşmesi ve tek işçi ile yürütülür

**Durum:** Accepted · retrospective

**Tarih:** 2026-09-10 (aynı gün uygulama sonrasında kaydedildi)

## Bağlam / problem
Kullanıcı Kokoro, değiştirilebilir motor, macOS MPS/CPU, tepkisel GUI ve batch istedi.
Modeli GUI'ye bağlamak gelecekte motor değişimini ve hata kurtarmayı zorlaştırır.

## Değerlendirilen seçenekler
GUI içinde doğrudan pipeline; ayrı süreç hizmeti; soyut motor ve tek arka plan işçisi.

## Karar
Kullanıcı stack ve motor ayrımını açıkça istedi. AI, `TTSEngine` sözleşmesi,
tek işçi/Queue, atomik dışa aktarım ve afplay uygulama ayrıntılarını seçip yetkili
kapsamda uyguladı. Bunlar insana atfedilen tasarım seçimi veya nihai kabul değildir.
Accepted burada yürürlükteki teknik sözleşmeyi gösterir.

## Değişmezler (invariants)
- Tk nesnelerine yalnız ana iş parçacığı erişir; motor aynı anda tek işte kullanılır.
- MPS başarısızsa kısmi sonuç atılır, tüm metin CPU üzerinde bir kez yeniden denenir.
- Motor `AudioResult` döndürür; GUI Kokoro pipeline API'sini bilmez.
- Yazım tamamlanmadan hedef dosya değiştirilmez; batch her çalışmada yeni klasör kullanır.
- Metin uzak çıkarım servisine gönderilmez. İlk model/ses/G2P indirmeleri internet ister.

## Sonuçlar ve trade-off
Basit motor değişimi ve kontrollü bellek kullanımı; sentez çıktısı tek metin boyunca
RAM'de birikir, çok uzun girdiler belleği zorlayabilir. Tek işçi paralel batch yapmaz.
Çalışırken kapatma bekletilir; iptal özelliği bu sürümde yok. afplay macOS'a özeldir.

## Güvenlik / gizlilik etkisi
Önizleme geçici klasörde, dışa aktarma seçilen yerde tutulur. Hata mesajları
metin/ham istisna içeriği taşımaz. Kullanıcı metni upstream kitaplık debug
çıktısında görünebilir; üretimde debug log açılmaz, ham loglar tez kanıtına alınmaz.

## Etkilenen sözleşmeler ve dosyalar
`tts_engine.py`, `main.py`, `audio_io.py`, `batch.py`, `playback.py`, `tests/test_core.py`.

## Doğrulama planı
Unit: giriş, MPS yeniden deneme, atomik yazım, batch hata izolasyonu.
Gerçek model: `scripts/smoke_tts.py`. GUI, ses kalitesi, pause/resume ve cihaz
performansı ayrı doğrulanır. Sonuçlar `docs/evidence/` kayıtlarına eklenir.

## Yerini aldığı / aldığı ADR
Yok; ilk mimari.

## 2026-09-10 — oynatma seçiminin güncellenmesi

[ADR-003](ADR-003-native-audio-seeking.md), zaman çizelgesi gereksinimi için
afplay yerine AVAudioPlayer kullanır. Bu kaydın motor/işçi/atomik yazım
değişmezleri yürürlüktedir; yalnız oynatıcı uygulama tercihi değiştirilmiştir.
