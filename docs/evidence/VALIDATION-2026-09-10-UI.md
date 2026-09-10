# VAL-2026-09-10-UI — stüdyo arayüzü

Retrospective; 2026-09-10 / Europe/Warsaw. Git deposu/HEAD yok.
[Kaynak manifesti](SNAPSHOT-2026-09-10-UI.json) build kimliği:
`b9335956ceb900b2dbe2b3004e608a1cd1e4c1208a58c278142e5e763bf0ad2c`.

## Değişiklik
Görsel düzen ui.py içine alındı: açık stüdyo çalışma alanı, sağ ayar kartları,
koyu oynatıcı, gerçek örneklerden dalga görünümü, editör sayacı ve ⌘+Enter.
Motor ve codec sözleşmesi değişmedi. Yüksek riskli yeni domain kararı yok;
yeni ADR oluşturulmadı. İnsan tasarım talebinin sahibi; renk/yerleşim AI seçimi.

## Doğrulama

| Tam komut · 2026-09-10 | Exit | Sonuç | Sınır |
| --- | --- | --- | --- |
| `.venv/bin/python -m unittest discover -s tests -q` | 0 | 18 test geçti | Görsel inceleme değil |
| `.venv/bin/python -m compileall -q main.py ui.py scripts` | 0 | Derlendi | İnsan kabulü değil |
| `.venv/bin/python scripts/smoke_timeline.py` | 0 | Yeni arayüzde gerçek oynatma/sarma/pause/resume/bitiş/replay geçti | Son boşluk düzenlemesinden önce çalıştı; motor davranışı değişmedi |
| `.venv/bin/python scripts/preview_ui.py` | 0 | Son kaynakla gerçek Tk/native önizleme açıldı; 1180×815 ve 980×760 içerik görüntüleri incelendi | İnsan tasarım ve işitsel kabulü değil |
| `.venv/bin/python scripts/evidence_snapshot.py --output docs/evidence/SNAPSHOT-2026-09-10-UI.json` | 0 | 17 kaynak, 4 mevcut ses artefaktı hash'i | Commit değildir |

Aynı Apple M4/macOS ortamı. Görsel QA, uygulamanın kendi NSView içeriğinin
AppKit bitmap çiziminden yapıldı; ekranın başka uygulamaları yakalanmadı.
Son görüntüler OS geçici klasöründeki `autotts-ui-1180.png` ve
`autotts-ui-980.png`; depoya kopyalanmadı, kalıcı arşiv garantisi yok.
İncelenenler: kartların kesilmemesi, etiketler, dalga, süre, etkin kayıt/oynatma
kontrolleri, gerçek test metni ve sayaç. Test sesi önceki kişisel veri içermeyen örnektir.

## Düzeltilen/başarısız AI çıktıları
İlk tasarımda sağ toplu işlem kartı küçük pencerede kesiliyordu; görsel
incelemeyle tespit edilip boşluk/kontrol yükseklikleri düzeltildi. İlk dar
format menüsü WAV etiketini kırpıyordu; genişletildi. İlk screencapture denemesi
görüntü üretemedi; uygulamanın kendi NSView çizimiyle QA tamamlandı.
İlk sayaç yaklaşımı her 100 ms tüm metni okuyordu; yalnız metin değişikliği
olayında güncellenerek gereksiz tekrar kaldırıldı.

Uygulandı ve yukarıdaki kontroller geçti. İnsan nihai kabulü/yayın yok.
Git kimliği olmayan unit sonuçlar E2 asgari paketini tamamlamaz; görsel
kontrol dar cihaz/build/görüntü senaryosudur. Tez paylaşım izni bekliyor.
