# AutoTTS mimarisi — yaşayan belge

İnsan kullanıcı İngilizce metin veya UTF-8 TXT dosyaları seçer; uygulama yerel
Kokoro çıkarımıyla ses üretir. Model, ses ağırlıkları ve İngilizce G2P kaynakları
ilk kullanımda indirilir. Hazır önbellekle çıkarım yereldir.

| Dosya | Tek sorumluluk | Sözleşme |
| --- | --- | --- |
| main.py | GUI olayları ve işçi koordinasyonu | TTSEngine enjeksiyonu, Queue olayları |
| ui.py | Stüdyo yerleşimi, görsel stil ve dalga çizimi | build_interface, Waveform |
| tts_engine.py | Motor soyutlaması ve Kokoro adaptörü | Voice, AudioResult, TTSError |
| audio_io.py | WAV/MP3 atomik yazımı | save_audio |
| playback.py | macOS AVAudioPlayer yaşam döngüsü ve konum | load, toggle, seek, stop, position, duration |
| batch.py | Sıralı TXT dönüşüm işi | BatchResult: başarılı ve hatalı dosyalar |
| scripts/smoke_tts.py | Gerçek model doğrulaması | Sayısal ve codec kontrolleri |

Akış: GUI → tek işçi → motor → AudioResult → WAV önizleme / dışa aktarım.
İşçi → Queue → Tk ana iş parçacığı → durum/progress. Tek metinde belirsiz
progress, batch'te tamamlanan dosya oranı gösterilir; parça sayısı yüzde değildir.

Kokoro ABD/Britanya pipeline'ları aynı modeli paylaşır. MPS kullanılabilirlik
kontrolünden sonra seçilir; runtime/not-implemented hatasında CPU ile baştan
denenir. Kullanılan gerçek cihaz motor durumundadır; MPS seçilmesi bütün
operatörlerin GPU üzerinde çalıştığı veya hız artışı ölçüldüğü anlamına gelmez.

Yeni motor `TTSEngine.voices` ve `synthesize` uygular, `AutoTTSApp(engine=...)`
ile verilir. GUI'nin ses kataloğu motordan gelir. Başka motorun örnekleme hızı
`AudioResult.sample_rate` ile taşınır; çıkış katmanı bunu korur.

Aktif değişmezler: [ADR-001](decisions/ADR-001-local-engine-boundary.md).
Kanıt yönetimi: [ADR-002](decisions/ADR-002-append-only-evidence.md).

Zaman çizelgesi oynatıcının gerçek `currentTime` değerini 100 ms aralıkla okur. Sarma mevcut ses üzerinde yapılır; TTS tekrar çağrılmaz. [ADR-003](decisions/ADR-003-native-audio-seeking.md) oynatma kararını günceller.

Tekli dışa aktarmada Kaydet yanındaki format seçimi codec ve uzantının kaynağıdır.
`audio_io.export_path` eski WAV/MP3 uzantısını seçilen formatla eşleştirir;
üzerine yazma onayı düzeltilmiş gerçek hedef için alınır. Batch'in formatı ayrıdır.
