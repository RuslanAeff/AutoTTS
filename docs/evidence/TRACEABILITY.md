# Gereksinim izlenebilirliği — eklemeli kanıt indeksi

## 1. Amaç ve kapsam
Gereksinim → karar → kod → doğrulama → sonuç bağlantısını gösterir.
Tek başına test raporu, insan onayı veya yayın kanıtı değildir. İlk kayıt
2026-09-10 tarihinde aynı oturum sonrası `retrospective` olarak eklendi.
Eski kayıtlar sessizce değiştirilmez; düzeltme tarihli revizyon ve eski ID ile eklenir.

## 2. Sorumluluk ve onay ilkesi
İnsan ürün hedefi ve kabul kriterlerinin sahibidir. AI uygulama önerisi ve
test taslağı üretir. Kullanıcının görev yetkisi nihai ürün kabulü değildir.

## 3. Kanıt düzeyleri

| Kod | Anlam | Asgari kanıt |
| --- | --- | --- |
| E0 | İddia / retrospektif anlatı | Kaynak belge + sınırlama notu |
| E1 | Depoda gözlemlenen uygulama | Commit hash + dosya/satır veya diff |
| E2 | Otomatik doğrulama | Commit hash + tam komut + tarihli sonuç/CI |
| E3 | Hedef cihazda doğrulama | Build kimliği + cihaz/OS + senaryo + sonuç + artefakt |
| E4 | İnsan kabulü / sürüm kanıtı | Açık kabul kaydı ve/veya yayımlanmış sürüm kimliği |

Kanıt numarası iddiaya göre atanır. Görsel hata düzeldi iddiasını typecheck
desteklemez. Git olmayan bu başlangıçta E1/E2 şartları eksiktir. Kaynak
[manifesti](SNAPSHOT-2026-09-10.json) commit değildir; E3'te kaynak build fotoğrafıdır.

## 4. Durum sözlüğü

| Durum | Anlam |
| --- | --- |
| Uygulandı | Kaynakta mevcut; test veya kabul ima etmez |
| Otomatik test geçti | Adı verilen komut/senaryo geçti; kapsam sınırlıdır |
| Hedef cihazda doğrulandı | Yalnız kayıtlı cihaz ve senaryo |
| İnsan kabulü bekliyor | Nihai kabul kaydı yok |
| Yayımlandı | Açık sürüm kimliği gerekir; bu projede henüz yok |
| Retrospective | Olaydan sonra kayıt; bilinmeyen alanlar uydurulmaz |

## 5. İzlenebilirlik tablosu

Doğrulama referanslarının kaynağı [VAL-2026-09-10](VALIDATION-2026-09-10.md).
Tüm satırlar 2026-09-10 kaydıdır; insan kabulü ve yayın hiçbir satırda yapılmış sayılmaz.

| Kimlik | Gereksinim / problem | Karar veya sözleşme | Uygulama referansı | Doğrulama referansı | İnsan/cihaz kabulü | Düzey | Retrospektif sınırlama |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATT-DOM-001 | Değiştirilebilir motor; GUI ayrı | ADR-001 / TTSEngine | tts_engine.py: TTSEngine; main.py: AutoTTSApp | V01, kaynak manifesti | İnsan bekliyor | E0 | Kod mevcut, test geçti; Git hash yok |
| ATT-PERF-001 | MPS varsa kullan, yoksa CPU | ADR-001 | tts_engine.py: _pipeline, synthesize | V04 CPU ve V05 MPS; manifest | M4 üzerinde dar üretim senaryosu geçti; hız ölçülmedi | E3 | Gerçek MPS arızası zorlanmadı; fallback mock testi V01 |
| ATT-UX-001 | Büyük metin kutusu ve Seslendir | ADR-001 / Queue | main.py: _generate, _poll | V05 | Gerçek Tk üretim akışı geçti; görsel kabul bekliyor | E3 | Piksel incelemesi yok |
| ATT-DOM-002 | Kadın/erkek İngilizce sesler ve hız | Voice / synthesize | tts_engine.py: ENGLISH_VOICES; main.py: settings | V03 af_heart, V04 bm_george; resmî katalog README | Tüm sesler ve hız uçları bekliyor | E0 | Katalog/ayar uygulandı; tam özellik kabulü test edilmedi |
| ATT-DATA-001 | WAV üret ve WAV/MP3 kaydet | ADR-001 / save_audio | audio_io.py; main.py: _save | V04, outputs/british-cpu, manifest | Hedef cihaz codec round-trip geçti; diyalog kabulü bekliyor | E3 | Dialog tıklama testi yok; ses kalitesi iddiası değil |
| ATT-UX-002 | Play/pause ve devam | AudioPlayer | playback.py; main.py: _play | V05 | M4 süreç durumları geçti; işitsel kabul bekliyor | E3 | Duyma/telaffuz ve doğal bitiş doğrulanmadı |
| ATT-DATA-002 | Sıralı TXT batch | ADR-001 / run_batch | batch.py; main.py: _batch | V01: aynı ad, boş dosya, devam | Gerçek kullanıcı batch kabulü bekliyor | E0 | Mock test geçti; commit yok |
| ATT-UX-003 | Progress ve anlaşılır hatalar | Queue / TTSError | main.py: _poll; tts_engine.py; batch.py | V01, V05 | Manuel hata/progress senaryoları bekliyor | E0 | Akış gözlemi tüm durumların görsel kanıtı değil |
| ATT-SEC-001 | Tez kanıtı, insan/AI ayrımı, gizlilik | ADR-002 / AGENTS.md | docs/, CLAUDE.md | Bu indeks, oturum kaydı, taşınabilir şablonlar | İnsan belge kabulü bekliyor | E0 | Kalıcı konuşma ve paylaşım izni yok |

## 2026-09-10 — zaman çizelgesi ek kaydı

ATT-UX-002'nin eski afplay test kaydı tarihsel olarak korunur. Güncel oynatma
kararı ADR-003'tür; yeni gereksinim ve doğrulama aşağıdadır.

| Kimlik | Gereksinim / problem | Karar veya sözleşme | Uygulama referansı | Doğrulama referansı | İnsan/cihaz kabulü | Düzey | Retrospektif sınırlama |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATT-UX-004 | Üretilmiş sesi zaman çizelgesi ve ±10 sn ile sarma; pause durumunu koruma | ADR-003 / AudioPlayer.seek | main.py: _seek, _skip, _update_timeline; playback.py; SNAPSHOT-2026-09-10-TIMELINE.json | [VAL-TIMELINE](VALIDATION-2026-09-10-TIMELINE.md), tests/test_playback.py, scripts/smoke_timeline.py | M4 native konum/Tk akışı geçti; manuel fare ve işitsel kabul bekliyor | E3 | Aynı gün olay sonrası; commit yok; görsel kalite iddiası değil |

## 2026-09-10 — MP3 kayıt düzeltmesi

ATT-DATA-001 codec testleri, kayıt diyaloğundaki format seçimini kanıtlamıyordu.
Önceki kayıt korunur; kullanıcı bildirimiyle bu kapsam eksikliği aşağıda giderilir.

| Kimlik | Gereksinim / problem | Karar veya sözleşme | Uygulama referansı | Doğrulama referansı | İnsan/cihaz kabulü | Düzey | Retrospektif sınırlama |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATT-DATA-003 | MP3 seçilmesine rağmen WAV kaydedilmesi | Seçilen format son uzantı/codec ile eşleşir; atomik yazım korunur | main.py: _save; audio_io.py: export_path; yeni MP3 manifesti | [VAL-MP3](VALIDATION-2026-09-10-MP3.md), tests/test_export.py | Kullanıcı hata bildirimi var; düzeltme nihai kabulü bekliyor | E0 | Otomatik test geçti; commit yok; native diyalog mock |

## 2026-09-10 — stüdyo tasarımı

| Kimlik | Gereksinim / problem | Karar veya sözleşme | Uygulama referansı | Doğrulama referansı | İnsan/cihaz kabulü | Düzey | Retrospektif sınırlama |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATT-UX-005 | Modern profesyonel arayüz | Görsel düzen ayrı ui.py; mevcut motor/oynatıcı sözleşmeleri korunur | ui.py, main.py, UI kaynak manifesti | [VAL-UI](VALIDATION-2026-09-10-UI.md) | İki boyutta uygulama içeriği görsel incelendi; insan kabulü bekliyor | E3 | Görseller geçici; tasarım beğenisi veya tüm cihazlar iddiası değil |
