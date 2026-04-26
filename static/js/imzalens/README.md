# İmza Lens (Akıllı Karşılama Enjeksiyonu)

"İmza Lens", bir web sitesini statik bir vitrinden, kullanıcıyı tanıyan ve ona göre şekil alan "canlı" bir organizmaya dönüştüren enjeksiyon kütüphanesidir.

## Klasör Yapısı

```
imzalens/
├── imza-lens.core.js  (Analiz ve Takip Motoru)
├── imza-lens-ui.js    (Görsel Bileşen Motoru)
└── imza-lens.css      (Animasyonlar ve Stiller)
```

## Nasıl Kullanılır? (Enjeksiyon)

Herhangi bir HTML sayfasına şu 3 dosyayı dahil edin:

```html
<link rel="stylesheet" href="../static/js/imzalens/imza-lens.css">
<script src="../static/js/imzalens/imza-lens.core.js"></script>
<script src="../static/js/imzalens/imza-lens-ui.js"></script>
```

### 1. Niyet Takibi (Tracking)
Kullanıcı bir kategoriyi incelediğinde:
```javascript
ImzaLens.track('arsa'); // 'prestij', 'kiralik', 'konut' vb.
```

### 2. SSS Ticker Enjeksiyonu
```javascript
const questions = [
    { text: "Soru metni", link: "/blog-linki", cat: "kiralik" },
    // ...
];
ImzaLensUI.initFaqTicker('container-id', questions);
```

### 3. Kişiselleştirilmiş Banner
```javascript
ImzaLensUI.renderPersonalizedBanner('banner-container-id');
```

## Neden Bu Mimari?
Bu kütüphane, **"Digital Forensic"** (Dijital Adli Tıp) prensiplerini kullanarak kullanıcının çerez ve referrer izlerini sürer. Hiçbir veri sunucuya gitmeden tarayıcıda işlenir, bu da hem gizlilik hem de hız sağlar.
