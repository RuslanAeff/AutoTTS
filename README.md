# AutoTTS

macOS Apple Silicon için yerel İngilizce metin seslendirme uygulaması.
CustomTkinter arayüzü, Kokoro motoru, MPS kullanılabilirlik kontrolü ve CPU geri
dönüşü; 28 ABD/Britanya kadın/erkek sesi, 0.5–2.0 hız, play/pause, WAV/MP3 ve TXT batch.

## Kurulum

Python 3.11 ve Tk gerekir. macOS sistem Python 3.9 yerine Python.org'un
macOS universal2 Python 3.11 dağıtımını veya Homebrew Python + eşleşen Tk kullanın.
Homebrew mevcutsa:

```sh
brew install python@3.11 python-tk@3.11 espeak-ng
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m tkinter
python main.py
```

`python -m tkinter` küçük test penceresi açmalıdır. `_tkinter` bulunamadığında
Tk destekli Python kurup sanal ortamı onunla yeniden oluşturun. `espeak-ng`,
Kokoro'nun sözlük dışı İngilizce sözcükler için kullandığı fallback'i destekler.
MP3 yazımı soundfile/lib­sndfile desteğine bağlıdır; destek yoksa uygulama açık
uyarı verir, WAV kullanılabilir. Ek ffmpeg bağımlılığı gerekmez.

İlk sentez model, seçilen ses ve G2P kaynaklarını internetten indirir; birkaç
dakika sürebilir. Kullanıcı metni uzak bir TTS API'sine gönderilmez. Gerekli
kaynaklar önbellekteyken çıkarım yereldir; henüz indirilmemiş ses internet ister.
Model/ses önbelleği proje içindeki `.cache/huggingface/` klasörüdür; `HF_HOME`
ortam değişkeniyle başka yere taşınabilir. G2P dil paketi sanal ortama kurulur.

Bu çalışma alanında uv ile hazırlanmış `.venv` varsa doğrudan:

```sh
.venv/bin/python main.py
```

## Kullanım

1. İngilizce metni büyük kutuya yapıştırın; ses ve hızı seçin.
2. **Seslendir**: WAV önizleme üretilir; işlem boyunca durum/parça sayısı görünür.
3. **Oynat / Duraklat / Devam et**: macOS `AVAudioPlayer` ile dinleyin. Zaman çizelgesine tıklayarak veya sürükleyerek istediğiniz konuma geçin; **−10 sn / +10 sn** düğmeleriyle geri/ileri sarın. Geçen ve toplam süre altta gösterilir. Duraklatılmışken sarma sesi başlatmaz; sonda Oynat baştan başlatır.
4. **Kaydet** düğmesinin hemen yanındaki **WAV / MP3** menüsünden formatı
   seçin, ardından **Kaydet** ile konumu belirleyin. Dosya uzantısı seçilen
   formatla eşleştirilir; toplu işlem bölümündeki format menüsü yalnız batch içindir.
5. **TXT dosyalarını yükle** ile UTF-8 dosyaları seçin; gösterilen sıra ile
   **Toplu seslendir** çalıştırın. Çıktı formatını ve klasörü seçin. Her çalışma
   ayrı `AutoTTS-…` klasörüne numaralı dosyalar yazar. Hatalı dosyalar sonunda
   listelenir; diğer dosyalar devam eder.

Tek metin sırasında progress belirsizdir; batch'te tamamlanan dosya oranını
gösterir. Çalışma sırasında ikinci iş ve kapatma engellenir; iş bitince kapatın.
Çok uzun metinlerde bütün ses RAM'de birikeceğinden dosyaları bölmek yararlıdır.
Önizleme normal kapanışta silinir; kalıcı çıktı için Kaydet kullanın.

## MPS / CPU

Motor Torch yüklenmeden `PYTORCH_ENABLE_MPS_FALLBACK=1` ayarlar.
`torch.backends.mps.is_available()` doğruysa MPS seçer; değilse CPU.
MPS yükleme/çıkarımında RuntimeError veya NotImplementedError olursa kısmi
çıktı atılır ve tüm metin CPU'da yeniden denenir. MPS seçimi hız artışı garantisi
değildir; desteklenmeyen operatörler CPU'da çalışabilir.

```sh
.venv/bin/python scripts/smoke_tts.py --device auto
.venv/bin/python scripts/smoke_tts.py --device cpu --output outputs/cpu
.venv/bin/python scripts/smoke_tts.py --voice bm_george --output outputs/british
.venv/bin/python -m unittest discover -s tests -v
```

Smoke testi gerçek model ile `assets/sample.txt` metnini üretir, WAV/MP3'ü tekrar
açar; örnekleme hızı, süre, sonlu ve sessiz olmayan örnekleri kontrol eder.
Telaffuz, işitilebilir play/pause ve insan kabulü ayrıca değerlendirilmelidir.
Bu oturumun gerçek sonuçları: [doğrulama kaydı](docs/evidence/VALIDATION-2026-09-10.md).

## Proje düzeni

```text
main.py             GUI giriş noktası ve işçi koordinasyonu
ui.py               Stüdyo tasarımı, bileşen stilleri ve dalga görünümü
tts_engine.py       Soyut TTSEngine ve KokoroEngine
audio_io.py         Atomik WAV/MP3 dışa aktarma
playback.py         macOS AVAudioPlayer ve zaman çizelgesi
batch.py            Sıralı TXT işleme
requirements.txt    Bağımlılıklar
assets/sample.txt   Kişisel veri içermeyen test metni
tests/              Model indirmeyen unit testler
scripts/            Gerçek model testi
docs/               Yaşayan rehberler, ADR, kanıt, tarihçe, şablonlar
```

Yeni motor `TTSEngine` sözleşmesini uygulayıp `AutoTTSApp(engine=...)` ile
verilebilir. GUI dosyasına yeni motorun pipeline ayrıntıları eklenmez.

## Tez kanıt altyapısı

[AGENTS.md](AGENTS.md) kanonik katkı sözleşmesidir. Yaşayan rehberler
[mimari](docs/ARCHITECTURE.md), [geliştirme](docs/DEVELOPMENT_GUIDE.md) ve
[kalite/güvenlik](docs/QUALITY_AND_SECURITY.md) dosyalarındadır.
[ADR indeksi](docs/decisions/README.md), [izlenebilirlik](docs/evidence/TRACEABILITY.md)
ve [AI oturum kaydı](docs/evidence/AI_COLLABORATION_LOG.md) kararları kanıta bağlar.
`docs/templates/` altındaki iki şablon başka projelere taşınabilir.

Uygulama, otomatik doğrulama, hedef cihaz testi, insan kabulü ve yayın ayrı
durumlardır. Kanıtlar eklemeli tutulur; bilinmeyen kimlikler uydurulmaz.

## Kaynaklar

- [Kokoro resmî depo ve kurulum](https://github.com/hexgrad/kokoro)
- [Resmî İngilizce ses kataloğu](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
- [Kokoro pipeline cihaz davranışı](https://github.com/hexgrad/kokoro/blob/main/kokoro/pipeline.py)
- [Soundfile API](https://python-soundfile.readthedocs.io/en/latest/)

Ses kataloğu 2026-09-10 tarihinde kontrol edildi. Bağımlılık aralıkları tam
kilit dosyası değildir; ölçümde gerçek kurulu sürümleri kanıt kaydına ekleyin.

Zaman çizelgesi güncellemesi için mevcut sanal ortamda `python -m pip install -r requirements.txt` çalıştırın. Oynatma köprüsü `pyobjc-framework-AVFoundation` paketidir. [Sarma doğrulaması](docs/evidence/VALIDATION-2026-09-10-TIMELINE.md).

## Stüdyo arayüzü

Açık renkli metin çalışma alanı, sağda ses/toplu işlem ayarları ve altta koyu
oynatıcı paneli bulunur. Dalga görünümü üretilmiş sesten çizilir. Editör kelime
ve karakter sayısını gösterir; **⌘+Enter** seslendirmeyi başlatır. Minimum
pencere boyutu 980×760; tasarım sabit açık tema kullanır.
