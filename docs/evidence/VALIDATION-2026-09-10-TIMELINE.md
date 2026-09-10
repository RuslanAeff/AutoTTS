# VAL-2026-09-10-TIMELINE — zaman çizelgesi doğrulaması

**Tür:** Değişmez, retrospective; 2026-09-10, Europe/Warsaw.
Kaynak fotoğrafı [manifest](SNAPSHOT-2026-09-10-TIMELINE.json), build
`395f6cf55d32780195cddef45f0b9ef16e6cc0aefc04eec421c9f7ee58b1f74d`.
Git deposu/branch/HEAD/CI yok. Manifest commit yerine geçmez.

## Ortam ve kaynak
Mevcut çalışma ortamı Apple M4 / macOS 26.6.2 arm64; aynı ortamın cihaz
ölçümü önceki VAL kaydındadır. Python 3.11.16, PyObjC AVFoundation 12.2.2.
Testte kullanılan kişisel veri içermeyen ses `outputs/smoke/sample.wav`;
hash manifestte. Model tekrar çağrılmadı; GUI test motoru önceki sesi döndürdü.

| Komut (2026-09-10) | Exit | Sonuç | Sınır |
| --- | --- | --- | --- |
| `.venv/bin/python -m unittest discover -s tests -v` | 0 | 2 test sınıfı, toplam 14 test geçti; 6 yeni oynatıcı testi | Native ses kalitesi kanıtı değil |
| `.venv/bin/python -m compileall -q main.py playback.py tests scripts` | 0 | Python derleme kontrolü geçti | Görsel inceleme değil |
| `.venv/bin/python scripts/smoke_timeline.py` | 0 | Gerçek Tk + AVAudioPlayer yükleme, oynatma öncesi konum seçimi, oynarken ileri/geri, pause-seek-resume, uç sınırlar, doğal bitiş, tekrar oynatma geçti | Widget komutları programatik çağrıldı; fiziksel fare sürükleme/görsel ve işitsel insan kabulü yapılmadı |
| `.venv/bin/python scripts/evidence_snapshot.py --output docs/evidence/SNAPSHOT-2026-09-10-TIMELINE.json` | 0 | 14 kaynak ve 4 mevcut ses artefaktı hash'i | Testten sonra kaynak fotoğrafı; commit değildir |

GUI test çıktısı:

```json
{"result":"passed","backend":"AVAudioPlayer","checks":["load","seek-before-play","playing-forward-backward","pause-seek-resume","clamp-start-end","natural-end","replay"],"manual_audio_acceptance":"pending"}
```

## Durum ve gizlilik
Uygulandı: evet. Otomatik test: geçti. Hedef cihaz: yukarıdaki dar otomatik
GUI/native konum senaryoları geçti. İnsan nihai kabulü/yayın: yapılmadı.
Git hash eksik olduğundan E2 asgari paketi tamamlanmış değildir; native
konum davranışı iddiası için build/cihaz/senaryo/sonuç kaydı E3 kapsamındadır.
Kullanıcı ekran görüntüsü ve ham log kopyalanmadı; mutlak kullanıcı yolları
belgelenmedi. Artefaktların tezde paylaşım izni ayrıca bekliyor.

## İnceleme sonucu ve kullanılmayan seçenek
afplay yardım çıktısında başlangıç konumu seçeneği bulunmadığı gözlendi.
Her sarmada WAV parçası oluşturma seçeneği değerlendirildi ve kullanılmadı;
doğrudan native konum API'si seçildi. İnsan tarafından reddedilen bir AI
çıktısı kaydedilmedi. Bu oturumda başarısız uygulama testi gözlenmedi.
