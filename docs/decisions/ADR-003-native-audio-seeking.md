# ADR-003 — Zaman çizelgesi macOS AVAudioPlayer konumu üzerinden yönetilir

**Durum:** Accepted · retrospective

**Tarih:** 2026-09-10

## Bağlam / problem
İnsan, önceden seslendirilmiş metni zaman çizelgesiyle ileri/geri sararak
dinlemeyi istedi. afplay CLI bir başlangıç konumuna atlama seçeneği sunmuyor.

## Değerlendirilen seçenekler
Her sarmada WAV kesip afplay başlatmak; yeni bir taşınabilir ses kitaplığı;
macOS AVAudioPlayer'ın native zaman ve sarma API'sini kullanmak.

## Karar
AI, kullanıcı tarafından yetkilendirilmiş özellik kapsamında AVAudioPlayer
ve PyObjC bağlantısını uyguladı. Bu teknik seçim insan nihai kabulü değildir.
GUI zaman çizelgesi ve ±10 saniye düğmeleriyle AudioPlayer.seek çağırır.

## Değişmezler (invariants)
- Sarma TTS'yi yeniden çalıştırmaz, mevcut ses üzerinde yapılır.
- Duraklatılmış/başlatılmamış ses sarma nedeniyle kendiliğinden oynamaz.
- Konum 0 ile toplam süre arasındadır; bitişten Oynat başa döner.
- Tk ve native oynatıcı ana GUI thread'inde kullanılır.
- Üretim sırasında oynatma kontrolleri kapalıdır; yeni ses sıfırdan yüklenir.

## Sonuçlar ve trade-off
Ses kesme/geçici parça yazımı gerekmez, gerçek oynatıcı konumu okunur.
Ek macOS bağımlılığı pyobjc-framework-AVFoundation gerekir. Süre göstergesi
100 ms aralıkla güncellenir; konuşulan sözcüğü metinde vurgulama kapsam dışıdır.

## Güvenlik / gizlilik etkisi
Yerel dosya native oynatıcıya yüklenir; ses/veri dış servise gönderilmez.
Önizleme temizliği önceki sözleşmeyle korunur.

## Etkilenen sözleşmeler ve dosyalar
playback.py, main.py, requirements.txt, tests/test_playback.py,
scripts/smoke_timeline.py, README.md ve mimari rehberi.

## Doğrulama planı
Unit: oynarken/duraklatılmışken sarma, sınırlar, doğal bitiş, tekrar oynatma.
Gerçek Tk + AVAudioPlayer: önceden üretilmiş test WAV ile aynı akışlar.
[Sonuç kaydı](../evidence/VALIDATION-2026-09-10-TIMELINE.md); manuel işitsel kabul ayrı.

## Yerini aldığı / aldığı ADR
[ADR-001](ADR-001-local-engine-boundary.md) içindeki afplay uygulama seçimini
değiştirir; motor/işçi ve dosya değişmezleri geçerliliğini korur. ADR-001 kısmen
güncellenmiştir, tüm karar superseded sayılmaz.

Kaynaklar: [Apple currentTime](https://developer.apple.com/documentation/avfaudio/avaudioplayer/currenttime),
[PyObjC framework bağlantıları](https://pyobjc.readthedocs.io/en/latest/notes/framework-wrappers.html).
