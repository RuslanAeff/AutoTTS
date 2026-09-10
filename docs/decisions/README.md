# Mimari karar kayıtları

ADR yalnız birden fazla katman/bileşeni etkileyen ve yanlışlıkla geri alınması
yüksek regresyon riski taşıyan kararlar için yazılır. Küçük UI ayrıntıları ADR değildir.
Dosya biçimi `ADR-<NNN>-<kebab-slug>.md`; numaralar sıfır dolgulu ve tektir.

| Status | Anlam |
| --- | --- |
| Accepted | Mevcut mimarinin parçası; yeni işlerde varsayılan. İnsan nihai kabulü anlamına gelmez; karar kaynağı ayrıca yazılır. |
| Proposed | Henüz uygulanmamış öneri |
| Superseded | Yeni ADR ile değiştirildi; geçmiş ve iki yönlü bağ korunur |
| Deprecated | Yeni kullanım için uygun değil |

`prospective`: uygulamadan önce; `retrospective`: olaydan sonra kayıt.
Eski ADR sessizce yazılmaz. Yeni ADR eklenir, eskinin durumu Superseded yapılır
ve `## <tarih> — değişmezin zorlanması` bölümüyle değişiklik açıklanır.

## Aktif kararlar

| ADR | Status | Kapsam | Neden yüksek değerli? |
| --- | --- | --- | --- |
| [001](ADR-001-local-engine-boundary.md) | Accepted · retrospective | Motor, GUI, dosya, işçi | Motor değişimi, Tk güvenliği ve MPS hata davranışı tüm akışı etkiler |
| [002](ADR-002-append-only-evidence.md) | Accepted · prospective | Tüm katkılar ve belgeler | Kanıtın sessiz değiştirilmesi tez atfını geçersiz kılabilir |
| [003](ADR-003-native-audio-seeking.md) | Accepted · retrospective | GUI, oynatıcı, bağımlılıklar | Sarma ve duraklatma durumlarının birlikte korunması |

## ADR ekleme kontrol listesi

1. Çok bileşenli kapsamı ve geri alma regresyon riskini doğrula.
2. İskeletteki bütün bölümleri doldur; insan/AI karar kaynağını ayır.
3. Retrospektifse işaretle; bilinmeyen tarih veya hash uydurma.
4. Gereksinim, kod ve doğrulama kanıt yollarını ekle.
5. ADR ile kod/test aynı çalışmada doğrulansın; cihaz/kabul eksiklerini açık yaz.
