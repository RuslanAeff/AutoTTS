# <Proje> — proje dokümantasyonu

| Belge kimliği | Sürüm | Kayıt tarihi | Sorumlu rol | Tür |
| --- | --- | --- | --- | --- |
| <kimlik> | <sürüm> | <ISO tarih> | <rol> | Yaşayan rehber; bağlı kanıtlar değişmez |

## 1. Amaç ve sınırlar

| Ürün amacı | İnsan kabul kriterleri | Kapsam içi | Kapsam dışı |
| --- | --- | --- | --- |
| <amaç> | <kriterler> | <kapsam> | <sınır> |

## 2. Roller ve insan sorumluluğu

| Rol | Yetki | Sorumluluk | Onay kanıtı |
| --- | --- | --- | --- |
| İnsan | Ürün hedefi, kriterler, nihai karar | İnceleme ve kabul | <referans> |
| AI | Yetkilendirilmiş analiz/öneri/kod/test | Çıktı ve sınırlarını kaydetme | İnsan kararı yerine geçmez |

## 3. Sistem bağlamı ve mimari

| Bağlam / aktör | Girdi | Çıktı | Güven sınırı |
| --- | --- | --- | --- |
| <aktör/sistem> | <girdi> | <çıktı> | <sınır> |

| Teknoloji | Sürümün kanonik kaynağı | Amaç | Kısıt |
| --- | --- | --- | --- |
| <teknoloji> | <manifest/lock> | <amaç> | <kısıt> |

| Bileşen | Tek sorumluluk | Bağımlılık / sözleşme | Kod |
| --- | --- | --- | --- |
| <bileşen> | <sorumluluk> | <bağlantı> | <yol> |

| Domain varlığı | Değişmez | İhlal davranışı | ADR / test |
| --- | --- | --- | --- |
| <varlık> | <kural> | <hata> | <referans> |

## 4. Gereksinim izlenebilirliği

| Kimlik | Gereksinim / problem | Karar veya sözleşme | Uygulama referansı | Doğrulama referansı | İnsan/cihaz kabulü | Düzey | Retrospektif sınırlama |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <PROJE-ALAN-NNN> | <gereksinim> | <ADR> | <commit/diff> | <sonuç> | <kanıt/bekliyor> | <E0–E4> | <sınır> |

## 5. ADR

Yalnız çok bileşenli ve geri alınması yüksek regresyon riski taşıyan kararları kaydet.
Durumlar: Accepted (mevcut varsayılan), Proposed (henüz uygulanmamış öneri),
Superseded (yeni ADR ile değişti), Deprecated (yeni kullanım için uygun değil).
Prospective uygulama öncesi, retrospective olay sonrası kayıttır.

### ADR-<NNN> — <kararı bir cümlede söyleyen başlık>

**Durum:** <Accepted | Proposed | Superseded | Deprecated> · <prospective | retrospective>

**Tarih:** <ISO-8601; bilinmiyorsa kaydedilmedi>

#### Bağlam / problem
<problem>
#### Değerlendirilen seçenekler
<seçenekler>
#### Karar
<seçim, AI önerisi ve insan seçimi ayrımı>
#### Değişmezler (invariants)
<kurallar>
#### Sonuçlar ve trade-off
<sonuçlar>
#### Güvenlik / gizlilik etkisi
<etki>
#### Etkilenen sözleşmeler ve dosyalar
<yollar>
#### Doğrulama planı
<test/cihaz/kabul>
#### Yerini aldığı / aldığı ADR
<bağlantı veya yok>

Eski ADR sessizce değiştirilmez. Yeni ADR eklenir; eskiye tarihli durum notu ve
iki yönlü bağlantı eklenir.

## 6. Geliştirme tarihçesi

| Olay tarihi | Kayıt tarihi | Bulgu | Çözüm / karar | Kanıt | Retrospektif sınır |
| --- | --- | --- | --- | --- | --- |
| <tarih/kaydedilmedi> | <tarih> | <bulgu> | <çözüm> | <ref> | <sınır> |

## 7. Doğrulama stratejisi

| Tür | Senaryo / tam komut | Commit/build | Ortam | Tarih | Sonuç | Artefakt | Kanıtlamadığı şey |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Otomatik | <komut> | <hash> | <ortam> | <tarih> | <exit/sayı> | <log> | <sınır> |
| Cihaz/manuel | <senaryo> | <build> | <anonim cihaz/OS> | <tarih> | <sonuç> | <ref> | <sınır> |

| Düzey | Anlam | Asgari kanıt |
| --- | --- | --- |
| E0 | İddia / retrospektif anlatı | Kaynak belge + sınırlama |
| E1 | Depoda gözlemlenen uygulama | Commit hash + dosya/satır veya diff |
| E2 | Otomatik doğrulama | Commit hash + tam komut + tarihli sonuç/CI |
| E3 | Hedef cihaz doğrulaması | Build + anonim cihaz/OS + senaryo + sonuç + artefakt |
| E4 | İnsan kabulü / sürüm | Açık kabul ve/veya yayımlanmış sürüm kimliği |

Düzey iddiayı desteklemelidir: typecheck görsel düzeltmeyi kanıtlamaz.

## 8. AI işbirliği beyanı

| Oturum | İnsan hedefi / yetki | AI katkı sınıfı | İnsan seçimi | Kullanılmayan/hatalı çıktı | Kanıt | Sınır |
| --- | --- | --- | --- | --- | --- | --- |
| <ID> | <hedef> | <analiz/plan/kod/test/inceleme/dokümantasyon/araştırma> | <açık kayıt/bekliyor> | <çıktı> | <ref> | <sınır> |

AI üretimi doğruluk kanıtı değildir. Bilinmeyen model sürümü tahmin edilmez.

## 9. Güvenlik, gizlilik ve etik

| Veri türü / sınıfı | AI'ya aktarım | Redaksiyon | Saklama | Paylaşım izni |
| --- | --- | --- | --- | --- |
| <public/internal/restricted> | <asgari veri> | <işlem> | <süre> | <kanıt/bekliyor> |

Anahtar, parola, token, credential, gereksiz kişisel/finansal veri, cihaz UUID'si
ve mutlak kullanıcı yolları eklenmez. Kullanıcı ekran görüntüleri kopyalanmaz.
Cihaz anonimleştirilir; tezde paylaşım izni ayrıca doğrulanır.

## 10. Kanıt envanteri

| Kanıt ID | Tür | Tarih | Bağlı commit/build | Konum | Hash | Gizlilik | Saklama |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <ID> | <tür> | <tarih> | <kimlik/kaydedilmedi> | <göreli yol> | <hash/kaydedilmedi> | <sınıf> | <politika> |

## 11. Retrospektif sınırlamalar

| Eksik kanıt | Etkilenen iddia | Bilinen / bilinmeyen | Tamamlama yolu |
| --- | --- | --- | --- |
| <eksik> | <iddia> | <sınır> | <yeni kanıt> |

Olaydan sonra yazılan kayıt işaretlenir; hafızadan tarih, commit ve baseline üretilmez.
Kalıcı konuşma referansı yoksa insan onayı için kontrollü issue/konuşma bağlanmalıdır.

## 12. Sürümleme ve bakım

| Belge grubu | Yaşayan/değişmez | Güncelleme tetikleyicisi | Sorumlu |
| --- | --- | --- | --- |
| Mimari / geliştirme / kalite | Yaşayan | İlgili değişiklik | <rol> |
| Kanıt / ADR | Değişmez, eklemeli revizyon | Yeni olay / düzeltme | <rol> |

Görev başında status ve kapsam oku. Mimari/domain değişiminde izlenebilirlik,
oturum ve ADR'yi bağla. Her mantıksal birim ayrı commit; belgeler ayrı `docs:`
commit. Açık dosya listesiyle stage et ve cached dosya listesini doğrula.
