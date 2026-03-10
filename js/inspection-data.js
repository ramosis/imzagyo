const inspectionData = {
    "Grup_1": {
        "title": "Konut",
        "categories": [
            {
                "name": "1. HUKUKİ VE İDARİ KONTROLLER",
                "questions": [
                    "Tapu Tipi (Kat Mülkiyeti / Kat İrtifakı)",
                    "Yapı Kullanım İzin Belgesi (İskan)",
                    "Tapu Takyidat Durumu (İpotek, Şerh, Haciz)",
                    "Enerji Kimlik Belgesi (EKB)",
                    "Aylık Aidat ve Geçmiş Borç Durumu"
                ]
            },
            {
                "name": "2. DIŞ MEKAN VE YAPI ALTYAPISI (Özellikle Villalar İçin)",
                "questions": [
                    "Dış Cephe Boyası ve Isı Yalıtımı (Mantolama)",
                    "Çatı Kaplaması (Kiremit/Şıngıl kırıkları, kaymaları)",
                    "Çatı Olukları ve Yağmur Suyu İniş Boruları",
                    "Temel Su Basmanı (Çevresel su izolasyonu)",
                    "Bahçe Peyzajı ve Sulama Sistemi",
                    "Yüzme Havuzu (Pompa dairesi, filtreler, seramikler)",
                    "Bahçe Duvarları, Ferforjeler ve Dış Aydınlatma"
                ]
            },
            {
                "name": "3. APARTMAN ORTAK ALANLARI",
                "questions": [
                    "Asansör (Kabin durumu, periyodik bakım etiketi)",
                    "Merdiven Dairesi, Sahanlıklar ve Sensörlü Aydınlatmalar",
                    "Kapalı/Açık Otopark (Tahsisli alan, zemin durumu)",
                    "Sığınak, Su Deposu ve Hidrofor Sistemi"
                ]
            },
            {
                "name": "4. İÇ MEKAN: GENEL YAPI VE MİMARİ",
                "questions": [
                    "Çelik Kapı (Kilit mekanizması, menteşe ayarı, fitiller)",
                    "İç Oda Kapıları (Kollar, kilitler, pervaz şişmeleri)",
                    "Pencereler (PVC/Alüminyum mekanizmaları, çift açılım)",
                    "Pencere Camları (Isıcam vakumu, buğulanma, çizik)",
                    "Pencere İzolasyon Fitilleri ve Silikonları",
                    "Sineklikler ve Panjur/Kepenk Sistemleri (Motor/Manuel)",
                    "Zemin Kaplamaları (Parke gıcırdaması, seramik kırıkları)",
                    "Süpürgelikler (Duvardan ayrılma, su alma)",
                    "Duvarlar (Boya kondisyonu, rutubet, kılcal çatlaklar)",
                    "Tavanlar (Kartonpiyer, asma tavan, su/nem izleri)"
                ]
            },
            {
                "name": "5. MEKANİK, ELEKTRİK VE İKLİMLENDİRME",
                "questions": [
                    "Sigorta Panosu (Kaçak akım rölesi testi, sigorta etiketleri)",
                    "Prizler (Elektrik akımı, duvara oturma, topraklama)",
                    "Aydınlatma Anahtarları ve Armatürler/Spotlar",
                    "Doğalgaz Tesisatı ve Kombi (Su basıncı, ateşleme)",
                    "Isıtma Sistemi (Radyatör vanaları, paslanma, su damlatma)",
                    "Klima (Soğutma/ısıtma performansı, dış ünite sesi, kumanda)",
                    "Şebeke Su Basıncı (Ana vana ve saat durumu)"
                ]
            },
            {
                "name": "6. MUTFAK DETAYLARI",
                "questions": [
                    "Mutfak Dolapları (Menteşeler, çekmece rayları, amortisörler)",
                    "Dolap Kapakları (Şişme, çizik, folyo atması)",
                    "Tezgah (Mermer/Çimstone çatlak, yanık, leke durumu)",
                    "Eviye ve Batarya (Sızdırmazlık, su basıncı, gider çekişi)",
                    "Tezgah Arası Seramikler (Derz dolguları, yağ lekeleri)",
                    "Davlumbaz / Aspiratör (Çekiş gücü, filtre temizliği, aydınlatma)",
                    "Ankastre Ocak (Çakmak mekanizması, gaz kaçağı)",
                    "Ankastre Fırın (İç aydınlatma, tepsiler, fan sesi)"
                ]
            },
            {
                "name": "7. ISLAK HACİMLER (Banyo & Tuvalet)",
                "questions": [
                    "Klozet ve Rezervuar (İç takım su kaçırma, kapak amortisörü)",
                    "Duşakabin / Küvet (Sürgü mekanizması, silikon küflenmesi)",
                    "Duş Bataryası ve Ahize (Su kireçlenmesi, sızıntı)",
                    "Banyo Dolabı ve Aynası (Su buharı hasarı)",
                    "Lavabo ve Bataryası (Gider hızı, sifon damlatması)",
                    "Havalandırma (Pencere veya mekanik fan çalışması)",
                    "Zemin Eğim Testi (Su, gidere doğru akıyor mu?)"
                ]
            },
            {
                "name": "8. EŞYALI KİRALAMA/SATIŞ EKSTRALARI (Demirbaşlar)",
                "questions": [
                    "Buzdolabı (Motor sesi, lastik fitiller, soğutma derecesi)",
                    "Bulaşık Makinesi (Pervaneler, sepet tekerlekleri, pas durumu)",
                    "Çamaşır Makinesi (Kazan yatağı, sıkma sırasındaki titreşim/ses)",
                    "Oturma Grubu/Koltuklar (Kumaş yırtığı, leke, iskelet gıcırdaması)",
                    "Yataklar ve Bazalar (Amortisörler, yatak hijyeni)",
                    "Halılar ve Perdeler/Storlar (Mekanizma çalışması, temizlik)",
                    "Televizyon ve Uydu Alıcısı (Kumanda, ölü piksel, panel çiziği)"
                ]
            }
        ]
    },
    "Grup_2": {
        "title": "Ticari/Endüstriyel",
        "categories": [
            {
                "name": "1. TİCARİ YASAL VE İDARİ KONTROLLER",
                "questions": [
                    "Ticari İskan (Yapı Kullanım İzni - Sanari/Ticari onaylı mı?)",
                    "İtfaiye Raporu ve Yangın Güvenlik Uygunluğu",
                    "ÇED (Çevresel Etki Değerlendirmesi) Raporu Uygunluğu",
                    "Ruhsat Durumu (Tehlikeli madde, gıda üretimi vs. uygunluğu)"
                ]
            },
            {
                "name": "2. ENDÜSTRİYEL YAPI VE MİMARİ",
                "questions": [
                    "Tavan Yüksekliği (Makas altı net h: metre kontrolü)",
                    "Kolon Aralıkları (Açıklık mesafeleri lojistiğe uygun mu?)",
                    "Zemin Taşıma Kapasitesi (Ton/m2 uygunluğu ve epoksi/saha betonu durumu)",
                    "Çatı Konstrüksiyonu (Sandviç panel, uzay çatı, izolasyon, sızıntı)",
                    "Vinç Yolları ve Guseler (Tavan vinci altyapısı sağlamlığı)",
                    "Dış Cephe Kaplamaları ve Tabela Asma Alanları"
                ]
            },
            {
                "name": "3. LOJİSTİK VE OPERASYONAL ALANLAR",
                "questions": [
                    "Tır/Kamyon Yanaşma Rampaları ve Körük Sistemleri",
                    "Seksiyonel/Giyotin Endüstriyel Kapılar (Motor ve emniyet sensörleri)",
                    "Manevra Alanı ve Açık Depolama Sahası Zemin Durumu",
                    "İstinat Duvarları ve Çevre Güvenlik Çitleri"
                ]
            },
            {
                "name": "4. ENERJİ VE MEKANİK ALTYAPI (Kritik)",
                "questions": [
                    "Trafo Kapasitesi (kVA yeterliliği ve periyodik bakım durumu)",
                    "Kompanzasyon Panosu (Reaktif ceza durumu kontrolü)",
                    "Jeneratör (Güç, çalışma saati, yakıt tankı, transfer panosu)",
                    "Sanayi Tipi Elektrik Altyapısı (Busbar sistemleri, kablo tavaları)",
                    "Basınçlı Hava Tesisatı ve Kompresör Odası",
                    "Endüstriyel Havalandırma, Toz Toplama ve Egzoz Sistemleri",
                    "Su Deposu Kapasitesi ve Endüstriyel Arıtma Sistemi"
                ]
            },
            {
                "name": "5. İŞ GÜVENLİĞİ VE YANGIN SİSTEMLERİ",
                "questions": [
                    "Yangın Springler (Püskürtme) Sistemi ve Pompa Dairesi",
                    "Duman, Isı Dedektörleri ve Yangın İhbar Paneli",
                    "Yangın Dolapları ve Hidrant Hattı Basıncı",
                    "Acil Çıkış Kapıları (Panik barlar) ve Kaçış Yönlendirmeleri",
                    "Paratoner (Yıldırımsavar) Tesisatı ve Topraklama Ölçümü"
                ]
            },
            {
                "name": "6. İDARİ BÖLÜMLER VE OFİSLER",
                "questions": [
                    "İdari Ofis Kondisyonu (Zemin, tavan, bölme duvarlar)",
                    "Sistem Odası (Server) İklimlendirme ve Yangın Söndürme (FM200 vb.)",
                    "Personel Soyunma Odaları ve Duşlar (Kapasite/Hijyen)",
                    "Yemekhane ve Endüstriyel Mutfak (Gaz kesiciler, havalandırma)",
                    "Engelli Tuvaletleri ve Ulaşım Rampa Uygunluğu"
                ]
            }
        ]
    },
    "Grup_3": {
        "title": "Arsa/Arazi",
        "categories": [
            {
                "name": "1. HUKUKİ VE RESMİ STATÜ",
                "questions": [
                    "Tapu Niteliği (Arsa / Tarla / Zeytinlik / Sit Alanı)",
                    "Mülkiyet Durumu (Müstakil Tapu / Hisseli Tapu - Şufa hakkı riski)",
                    "Kadastral Durum (Aplikasyon krokisi ile sınırlar belirgin mi?)",
                    "Üzerinde Şerh, İpotek, İrtifak Hakkı (Geçiş hakkı vb.) var mı?",
                    "Orman Sınırı veya Kıyı Kenar Çizgisi İhlali Riski",
                    "Kamulaştırma (Yol, baraj vb.) Geçme Riski"
                ]
            },
            {
                "name": "2. İMAR DURUMU (Arsalar İçin)",
                "questions": [
                    "İmar Fonksiyonu (Konut / Ticari / Sanayi / Turizm vb.)",
                    "KAKS (Emsal) Değeri (Toplam inşaat alanı potansiyeli)",
                    "TAKS Değeri (Taban oturum alanı kısıtlaması)",
                    "H-Max (Maksimum kat/yükseklik izni)",
                    "Yola, Komşuya ve Arka Bahçeye Çekme Mesafeleri",
                    "Terk Durumu (Yola/Yeşil alana terk bedelsiz yapılmış mı?)",
                    "Tevhit/İfraz (Birleştirme/Bölme) Şartları ve Gerekli mi?"
                ]
            },
            {
                "name": "3. TOPOĞRAFİK VE COĞRAFİ ÖZELLİKLER",
                "questions": [
                    "Arazi Eğimi (Düz, Hafif Eğimli, Sarp - Hafriyat/İstinat duvarı maliyeti)",
                    "Yola Cephe Uzunluğu ve Geometrik Şekli (Kare, Dikdörtgen, Üçgen, Çaplı)",
                    "Zemin Etüdü Öngörüsü (Kayalık, Dolgu zemin, Balçık/Dere yatağı)",
                    "Sel, Heyelan veya Deprem Fay Hattı Riski",
                    "Cephe Yönü (Kuzey, Güney, Manzara kapanma ihtimali)"
                ]
            },
            {
                "name": "4. TARIMSAL NİTELİK (Tarlalar/Araziler İçin)",
                "questions": [
                    "Toprak Verimliliği ve Sınıfı (Mutlak tarım arazisi mi, marjinal mi?)",
                    "Halihazırdaki Ürün veya Ağaç Durumu (Verimli ağaç var mı?)",
                    "Sulama İmkanları (Artezyen kuyu, DSİ kanalı, baraj, kuru tarım)",
                    "İklim Rüzgar/Güneş Alma Durumu (Sera veya GES/RES potansiyeli)",
                    "Tarımsal Desteklemelere veya Hibe Programlarına Uygunluk"
                ]
            },
            {
                "name": "5. ALTYAPI VE LOKASYON ERİŞİMİ",
                "questions": [
                    "Kadastral Yol veya Asfalt Yola Cephe Durumu",
                    "Elektrik Hattı Uzaklığı (Direk çekme maliyeti)",
                    "Şebeke Suyu ve Kanalizasyon Hattı Mevcudiyeti",
                    "Doğalgaz Hattı Yakınlığı",
                    "Telekomünikasyon / Fiber İnternet Altyapısı",
                    "Ana Arterlere, Otobana, Limana veya Merkeze Uzaklık/Lojistik Ağ"
                ]
            }
        ]
    }
};