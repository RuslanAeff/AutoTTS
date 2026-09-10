# Geliştirme rehberi — yaşayan belge

Kurulum ve kullanıcı komutlarının kaynağı [README](../README.md), bağımlılık
kaynağı `requirements.txt` dosyasıdır. Katkı akışı [AGENTS](../AGENTS.md).

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q main.py tts_engine.py audio_io.py playback.py batch.py scripts tests
.venv/bin/python scripts/smoke_tts.py --device auto
.venv/bin/python scripts/smoke_timeline.py
.venv/bin/python scripts/check_evidence.py
.venv/bin/python main.py
```

Unit testler model indirmez. Smoke gerçek model indirip `outputs/smoke/`
altına WAV ve MP3 yazar; sesin anlaşılabilirliğini değerlendirmez.
Kanıt kontrolü varsayılan güncel UI manifestindeki kaynak ve yerel çıktı dosyalarını arar;
çıktılar silinmişse eksik artefakt raporlar. Yeni ürün değişikliğinde eski manifesti
değiştirmeyin; yeni kayıt/manifest oluşturun ve ilgili doğrulamayı ona bağlayın.

Uzun işlerde widget değerlerini ana iş parçacığında kopyala, işçiye yalnız
Python verisi geçir. İşçiden GUI'ye Queue ile dön. Beklenmeyen hatada
kullanıcı verisini içeren traceback'i arayüze veya kanıt dosyasına yazma.
Model örneğini birden fazla işçide aynı anda kullanma.

Batch UTF-8 / UTF-8 BOM kabul eder. Geçersiz kodlama ve boş dosya o dosyada
hata üretir, sıradaki devam eder. Çıktı isimleri seçili sıraya göre numaralıdır.

ADR ekleme ölçütleri `docs/decisions/README.md`; oturum şablonu
`docs/templates/AI_SESSION_TEMPLATE.md`. Yeni kanıt geçmiş kaydı değiştirmez.

`check_evidence.py --manifest <dosya>` ile tarihli manifest seçilebilir. Eski manifesti güncel kodla karşılaştırmak doğal olarak fark raporlar. Yeni kaynak fotoğrafı: `scripts/evidence_snapshot.py --output docs/evidence/<yeni-kimlik>.json`; mevcut dosyanın üzerine yazılmaz.
