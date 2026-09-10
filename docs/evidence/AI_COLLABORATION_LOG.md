# AI işbirliği kaydı — eklemeli

## 1. Amaç
AI'nın görevlerini, yetki sınırını, çıktılarını ve doğrulama sınırlarını akademik
olarak izlenebilir kılar. Konuşma dökümü değildir. Eski kayıtlar sessizce
değiştirilmez; yeni tarihli revizyon eski oturuma bağlanır.

## 2. Atıf ve onay kuralları

- İnsan ürün hedefinin sahibidir.
- AI önerisi açık insan seçimi olmadan insan kararı sayılamaz.
- AI kod üretimi doğruluk kanıtı değildir.
- Kesin olmayan model/araç sürümü tahmin edilmez, `kaydedilmedi` yazılır.
- AI katkıları: analiz · plan · kod · test · inceleme · dokümantasyon · araştırma.
- İnsan katkıları: gereksinim · kapsam onayı · tasarım seçimi · kod inceleme · manuel test · nihai kabul.
- Uygulama, otomatik test, cihaz doğrulaması ve yayın ayrı kaydedilir.

## 3. Oturum indeksi

| Oturum | Tarih | Amaç | İnsan onayı | AI katkısı | Ürün kodu değişti mi? | Kanıt/çıktı | Durum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-2026-09-10-AUTOTTS-001 | 2026-09-10 | Yerel TTS ve tez altyapısı kurulumu | Kullanıcı görev brifi; nihai kabul yok | Analiz, plan, araştırma, kod, test, inceleme, dokümantasyon | Evet, boş klasörde ilk uygulama | VAL-2026-09-10, kaynak manifesti, ADR-001/002 | Uygulandı; 8 unit test ve dar cihaz senaryoları geçti; insan kabulü/yayın bekliyor |

## 4. Ayrıntılı oturum kaydı

### AI-2026-09-10-AUTOTTS-001

| Alan | Kayıt |
| --- | --- |
| Tarih / saat dilimi | 2026-09-10 / Europe/Warsaw; başlangıç kesin saati kaydedilmedi |
| Başlangıç çalışma ağacı | `git status --short`: Git deposu değil; branch/HEAD/clean-dirty uygulanamaz. Dosya listesi boştu. |
| İnsan hedefi | Kokoro tabanlı yerel macOS M4 TTS; 9 özellik; soyut motor; tez kanıt ve izlenebilirlik sistemi |
| Onaylanan yazma kapsamı | Proje kodu, requirements, README, tests/scripts, assets ve docs/AGENTS/adaptör altyapısı; venv ve çalıştırma görev kapsamındaydı. Ağ/GUI işlemleri araç izinleriyle yürütüldü. |
| Yasaklanan işlem | Hassas veri kaydı, kullanıcı ekran görüntüsü kopyalama, uydurma tarih/hash/model, sessiz kanıt değişimi; yayın/harici mesaj için yetki verilmedi |
| Sağlanan kanıt | Metinsel görev brifi ve M4 hedef bilgisi; kullanıcı ekran görüntüsü/log sağlamadı, kopyalanmadı |
| İncelenen kaynaklar | Boş çalışma klasörü; resmî Kokoro README/pipeline; Hugging Face VOICES.md; Soundfile API; kurulu misaki en.py/espeak.py |
| AI aracı/modeli | Codex; tam model sürümü kaydedilmedi |
| AI katkısı | [analiz/plan/araştırma] stack ve cihaz davranışı; [kod] tüm uygulama; [test/inceleme] unit, gerçek model ve GUI süreç testleri; [dokümantasyon] rehber/ADR/şablon/kanıt |
| İnsan katkısı | [gereksinim/kapsam onayı] ürün amacı, stack, özellikler ve kanıt ilkeleri. Kod inceleme, manuel test ve nihai kabul kaydedilmedi. |
| AI önerisi ile insan kararı ayrımı | Kokoro/customtkinter/soundfile/torch, GUI-motor ayrımı ve kanıt felsefesi insan brifinden. ABC sözleşmesi, Queue/tek işçi, afplay, atomik yazım, batch alt klasörü ve test tasarımı AI uygulama seçimleri; insanın seçtiği mimari ayrıntılar diye sunulmuyor. |
| Otomatik doğrulama | 2026-09-10: `.venv/bin/python -m unittest discover -s tests -v` exit 0, 1 suite/8 test; compileall exit 0. Tam komutlar, süre ve sınırlar VAL V01–V06 içinde. |
| Cihaz doğrulaması | M4 / macOS 26.6.2 arm64; kaynak build fotoğrafı SNAPSHOT-2026-09-10.json; V04 gerçek CPU bm_george WAV/MP3, V05 gerçek MPS Tk sentez ve oynatıcı süreç akışı geçti. Manuel görsel/işitsel senaryolar bekliyor. |
| Commit/CI | Kaydedilmedi; Git deposu ve CI yok. Kaynak manifesti commit değildir; ilk V03 ara kaynak sürümündeydi. |
| Gizlilik | AI'ya gereksinim, proje kodu ve araç sonuçları verildi; cihaz bilgisi model/OS/mimari ile sınırlandı. Kanıt özetlerinden mutlak kullanıcı yolları çıkarıldı; ham terminal logları kopyalanmadı. Test metni kişisel veri içermez. Tez artefakt paylaşım izni bekliyor. |
| Retrospektif sınırlama | Aynı gün olay sonrası yazıldı. Kalıcı konuşma ID'si, başlangıç commit'i ve tam model sürümü yok. Otomatik test, cihaz akışı ve insan kabulü ayrıldı. |
| Nihai durum | Kod ve belgeler oluşturuldu; otomatik kontroller ve belirtilen dar cihaz senaryoları geçti. Nihai insan kabulü ve yayın yapılmadı. |

### Kullanılmayan veya düzeltilen AI çıktıları

| Çıktı / deneme | Durum | Gerekçe / düzeltme | Kanıt |
| --- | --- | --- | --- |
| Sandbox üzerinden uv/Python indirme | Başarısız, yeniden denendi | DNS kısıtı; izinli indirme tamamlandı | VAL başarısız denemeler |
| uv venv'in kaynak indirici için yeterli olduğu varsayımı | Düzeltildi | pip yoktu; eklendi ve README dil kurulumu açıklandı | VAL kurulum gözlemi |
| Yalnız Exception yakalayan motor hata yönetimi | Düzeltildi | spaCy SystemExit kullanabilir; özel TTSError ve regresyon testi | tests/test_core.py: test_language_installer_exit_becomes_user_error |
| Batch'te yalnız istisna sınıfı gösterimi | Düzeltildi | Kullanıcı için anlaşılır Türkçe metin/kodlama/erişim açıklamaları eklendi | batch.py |
| Daha fazla insan onayı atfetmek | Kullanılmadı | Yetki ve ürün nihai kabulü ayrıdır | ADR ve oturum kuralları |

Kalıcı konuşma kimliği/transcript bağlanmadı: insan onayı kanıtı tezde kullanılacaksa
kontrollü konuşma/issue referansı sonradan eklenmelidir.

## 2026-09-10 — MP3 kayıt oturumu (ek kayıt)

| Oturum | Tarih | Amaç | İnsan onayı | AI katkısı | Ürün kodu değişti mi? | Kanıt/çıktı | Durum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-2026-09-10-MP3-001 | 2026-09-10 | MP3 seçiminin WAV kaydetmesini düzeltmek | Düzeltme talebi ve hata açıklaması; nihai kabul yok | Analiz, kod, test, inceleme, dokümantasyon | Evet | VAL-MP3, yeni manifest, tests/test_export.py | Uygulandı; 18 test geçti |

### AI-2026-09-10-MP3-001 ayrıntıları

| Alan | Kayıt |
| --- | --- |
| Tarih / saat dilimi | 2026-09-10 / Europe/Warsaw; kesin başlangıç saati kaydedilmedi |
| Başlangıç çalışma ağacı | Git deposu yok; branch/HEAD/clean-dirty uygulanamaz; mevcut kod okundu |
| İnsan hedefi | MP3 dönüştürme/kaydetme düzeltmesi; açıklama: MP3 seçse de WAV kaydediliyor |
| Onaylanan yazma kapsamı | İlgili GUI/çıktı düzeltmesi, regresyon testleri, rehber ve ek kanıt |
| Yasaklanan işlem | Eski kanıtı sessiz değiştirme, hassas veri kaydı; yayın yetkisi yok |
| Sağlanan kanıt | Kullanıcının metinsel hata bildirimi; ekran görüntüsü/log yok |
| İncelenen kaynaklar | AGENTS, mimari, main.py, audio_io.py, batch.py, mevcut testler ve yerel gerçek codec çıktısı |
| AI aracı/modeli | Codex; tam model sürümü kaydedilmedi |
| AI katkısı | [analiz/inceleme] sabit WAV diyaloğu ve uzantıdan codec seçimini saptama; [kod] açık format menüsü/son hedef; [test] gerçek MP3 codec ve mock diyalog regresyonu; [dokümantasyon] kayıtlar |
| İnsan katkısı | [gereksinim] düzeltme talebi ve hata açıklaması; nihai kabul yok |
| AI önerisi ile insan kararı ayrımı | MP3 kaydının düzeltilmesi insan talebi; format menüsünü Kaydet yanına taşıma ve uzantı eşleştirme AI teknik seçimidir |
| Otomatik doğrulama | 2026-09-10: unittest discover exit 0, 18 test; compileall exit 0. Tam komutlar VAL-MP3 |
| Cihaz doğrulaması | Bekleniyor: fiziksel macOS diyaloğuyla MP3 seçip kaydetme. Codec gerçek çalıştırıldı; diyalog mock |
| Commit/CI | Kaydedilmedi; Git yok. Yeni MP3 kaynak fotoğrafı eklendi |
| Gizlilik | Kod, kişisel veri içermeyen mevcut test sesi, metinsel hata bildirimi işlendi; ham log/ekran görüntüsü ve mutlak kullanıcı yolu kaydedilmedi |
| Retrospektif sınırlama | Aynı gün olay sonrası; konuşma/commit kimliği yok; kullanıcının ilk etkileşimi birebir kaydedilmedi |
| Nihai durum | Uygulandı ve otomatik test geçti; insan/manuel cihaz kabulü ve yayın yok |

Önceki AI çıktısındaki eksik: codec testleri başarılıyken kayıt diyaloğunun
sabit WAV varsayılanı kapsam dışı kalmıştı. Bu oturumda düzeltildi ve regresyon
testi eklendi. MP3 kodlayıcıyı değiştirme seçeneği yerel codec testi geçtiği için
uygulanmadı. İnsan onayı kanıtı tezde kullanılacaksa kontrollü konuşma/issue
referansı sonradan eklenmelidir.

## 2026-09-10 — UI oturum indeks eki

| Oturum | Tarih | Amaç | İnsan onayı | AI katkısı | Ürün kodu değişti mi? | Kanıt/çıktı | Durum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-2026-09-10-UI-001 | 2026-09-10 | Modern profesyonel tasarım | Tasarım yenileme talebi; nihai kabul yok | Analiz, tasarım, kod, inceleme, test, dokümantasyon | Evet | VAL-UI, UI manifesti | Uygulandı; otomatik ve dar görsel kontroller geçti |

### AI-2026-09-10-UI-001 ayrıntıları

| Alan | Kayıt |
| --- | --- |
| Tarih / saat dilimi | 2026-09-10 / Europe/Warsaw; başlangıç kesin saati kaydedilmedi |
| Başlangıç çalışma ağacı | git status: depo yok; branch/HEAD/clean-dirty uygulanamaz |
| İnsan hedefi | Arayüzü güncel, modern, profesyonel biçimde yeniden tasarlamak |
| Onaylanan yazma kapsamı | GUI tasarımı, görsel bileşenler, gereken doğrulama ve belgeler |
| Yasaklanan işlem | Hassas veri/ekran görüntüsü kopyalama, eski kanıtı sessiz değiştirme; yayın yetkisi yok |
| Sağlanan kanıt | Metinsel tasarım talebi; kullanıcı referans görüntü vermedi |
| İncelenen kaynaklar | AGENTS, main.py, testler, yerel CustomTkinter Textbox API; uygulamanın kendi çizilen penceresi |
| AI aracı/modeli | Codex; tam model sürümü kaydedilmedi |
| AI katkısı | [analiz/kod] stüdyo düzeni ve ui.py; [inceleme/test] unit, oynatma smoke, iki boyutta görsel QA; [dokümantasyon] kayıtlar |
| İnsan katkısı | [gereksinim/kapsam onayı] tasarım hedefi; görsel seçim ve nihai kabul kaydedilmedi |
| AI önerisi ile insan kararı ayrımı | Modern tasarım insan talebi; açık tema, yeşil vurgu, koyu oynatıcı, iki sütun, dalga ve sayaç AI seçimleri |
| Otomatik doğrulama | 18 unit test ve compileall exit 0; komutlar VAL-UI |
| Cihaz doğrulaması | Aynı M4 ortamında native oynatma ve son arayüz 1180×815/980×760 görsel incelemesi; kaynak/build ve sınırlar VAL-UI |
| Commit/CI | Kaydedilmedi; yeni UI manifesti eklendi, eski manifestler korundu |
| Gizlilik | AI'ya proje kodu ve kişisel veri içermeyen örnek ses verildi; yalnız kendi pencere içeriği çizildi, geçici görüntüler repoya kopyalanmadı |
| Retrospektif sınırlama | Aynı gün olay sonrası; kalıcı konuşma/commit yok; görüntüler geçici |
| Nihai durum | Uygulandı; belirtilen test/görsel kontrol geçti; insan kabulü ve yayın yok |

Düzeltilen AI çıktıları: kesilen batch kartı, dar WAV menüsü ve sürekli metin
okuyan sayaç. İlk sistem ekran yakalama başarısız oldu; kendi NSView çizimiyle
inceleme tamamlandı. Ayrıntılar VAL-UI. İnsan onayı kanıtı tezde kullanılacaksa
kontrollü konuşma/issue referansı sonradan eklenmelidir.

### 2026-09-10 — AI-2026-09-10-AUTOTTS-001 ek doğrulama

`scripts/check_evidence.py` eklendi ve çalıştırıldı (exit 0): 15 Markdown,
11 kaynak hash'i, 4 artefakt hash'i, 0 hata. Tam komut ve sınırlar VAL V07'de.
Bu ek kayıt insan nihai kabulünü veya yayın durumunu değiştirmez.

## 2026-09-10 — yeni oturum indeks eki

| Oturum | Tarih | Amaç | İnsan onayı | AI katkısı | Ürün kodu değişti mi? | Kanıt/çıktı | Durum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-2026-09-10-TIMELINE-001 | 2026-09-10 | Önceden seslendirilmiş sesi zaman çizelgesiyle sarma | Kullanıcı özellik talebi; nihai kabul yok | Analiz, araştırma, kod, test, dokümantasyon | Evet | ADR-003, VAL-TIMELINE, yeni manifest | Uygulandı; 14 unit test ve native GUI testi geçti |

### AI-2026-09-10-TIMELINE-001

| Alan | Kayıt |
| --- | --- |
| Tarih / saat dilimi | 2026-09-10 / Europe/Warsaw; kesin başlangıç saati kaydedilmedi |
| Başlangıç çalışma ağacı | git status: Git deposu yok; branch/HEAD/clean-dirty uygulanamaz. Mevcut dosyalar okundu ve korundu. |
| İnsan hedefi | Üretilmiş sesi zaman çizelgesiyle ileri/geri sararak dinlemek |
| Onaylanan yazma kapsamı | Oynatıcı, GUI, gereken bağımlılık, testler ve mimari/kanıt belgeleri |
| Yasaklanan işlem | Hassas veri kaydı, geçmiş kanıtı sessiz değiştirme; dış yayın/mesaj yetkisi yok |
| Sağlanan kanıt | Metinsel özellik talebi; kullanıcı ekran görüntüsü veya log vermedi |
| İncelenen kaynaklar | AGENTS, ADR-001, mimari, main/playback; yerel afplay -h; Apple currentTime ve PyObjC resmî belgeleri (ADR-003 bağlantıları) |
| AI aracı/modeli | Codex; tam model sürümü kaydedilmedi |
| AI katkısı | [analiz/araştırma] sarma API'si; [kod] AVAudioPlayer, timeline, süre, ±10 sn; [test] 6 yeni unit test ve gerçek GUI testi; [dokümantasyon] ADR ve ek kanıt |
| İnsan katkısı | [gereksinim/kapsam onayı] zaman çizelgesi talebi; manuel test ve nihai kabul kaydedilmedi |
| AI önerisi ile insan kararı ayrımı | Sarma gereksinimi insana ait. AVAudioPlayer/PyObjC, ±10 saniye adımı ve sona gelince yeniden başlama AI teknik seçimleridir; insanın açık tasarım seçimi diye sunulmaz. |
| Otomatik doğrulama | 2026-09-10 unittest discover exit 0, toplam 14 test; compileall exit 0; tam komutlar VAL-TIMELINE |
| Cihaz doğrulaması | Aynı Apple M4/macOS ortamında gerçek Tk/AVAudioPlayer smoke_timeline exit 0; build ve senaryolar VAL-TIMELINE. Fiziksel fare/görsel/işitsel kabul bekliyor. |
| Commit/CI | Kaydedilmedi; Git deposu yok. Yeni kaynak manifesti eskiyi değiştirmeden eklendi. |
| Gizlilik | AI'ya proje kodu ve test sonuçları verildi; test sesi önceki kişisel veri içermeyen örnek. Kullanıcı yolları/ham log/ekran görüntüsü kanıta konmadı. Tez paylaşım izni bekliyor. |
| Retrospektif sınırlama | Aynı gün olay sonrası kayıt; kalıcı konuşma ID'si ve commit yok |
| Nihai durum | Uygulandı; otomatik ve dar native cihaz kontrolleri geçti; insan kabulü/yayın yok |

Kullanılmayan AI seçeneği: her sarmada WAV kesip afplay başlatma, native seek
lehine elendi. Başarısız uygulama testi veya insan tarafından reddedilmiş çıktı
gözlenmedi. Kalıcı konuşma kimliği yok: insan onayı kanıtı tezde kullanılacaksa
kontrollü konuşma/issue referansı sonradan eklenmelidir.
