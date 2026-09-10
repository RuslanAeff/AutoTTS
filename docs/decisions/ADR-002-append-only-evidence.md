# ADR-002 — Yaşayan rehberler ile eklemeli kanıt kayıtları ayrı tutulur

**Durum:** Accepted · prospective

**Tarih:** 2026-09-10

## Bağlam / problem
Kullanıcı tezde AI katkısının, insan kararının ve doğrulama sınırlarının
izlenebilir olmasını açıkça istedi. Başarılı çıktıların tek başına kaydı yanlılık yaratır.

## Değerlendirilen seçenekler
Tek değiştirilebilir günlük; tam konuşma arşivi; yaşayan rehber ve eklemeli kanıt indeksi.

## Karar
Kullanıcının brifindeki ayrım doğrudan uygulanır. İnsan ürün hedefi ve kanıt
ilkelerinin kaynağıdır; AI dosya organizasyonu ve ilk kayıt taslağını üretir.
İlk uygulamanın insan nihai kabulü henüz yoktur.

## Değişmezler (invariants)
- Uygulandı, test geçti, cihaz doğrulandı ve yayımlandı birbirini ima etmez.
- Kanıt ve ADR sessizce yeniden yazılmaz; düzeltme tarihli ve önceki kayda bağlıdır.
- Bilinmeyen kimlik/tarih/model sürümü uydurulmaz.
- E0–E4 iddiaya göre atanır; typecheck görsel veya işitsel başarı kanıtı değildir.
- Düzeltilen ve kullanılmayan AI çıktıları da kaydedilir.

## Sonuçlar ve trade-off
Daha fazla kayıt bakımı karşılığında akademik atıf sınırı görünür olur.
Hash olmayan başlangıç çalışması E1/E2 asgari şartlarını karşılamaz; başarılı
test sonucu ayrıca kaydedilse de kanıt düzeyi abartılmaz.

## Güvenlik / gizlilik etkisi
Gizli bilgi, kullanıcı ekran görüntüsü ve mutlak kullanıcı yolları kayda alınmaz.
Kontrollü konuşma bağlantısı ve tezde paylaşım izni ayrıca tamamlanmalıdır.

## Etkilenen sözleşmeler ve dosyalar
`AGENTS.md`, `CLAUDE.md`, `docs/templates/`, `docs/evidence/`, `docs/decisions/`,
`docs/QUALITY_AND_SECURITY.md`.

## Doğrulama planı
Şablon bölüm ve tablo kontrolü, göreli bağlantı kontrolü, gizlilik taraması.
Her mimari/domain görevinde oturum ve gereksinim kaydı; insan kabulü ayrı kaynakla.

## Yerini aldığı / aldığı ADR
Yok; ilk kanıt sözleşmesi.
