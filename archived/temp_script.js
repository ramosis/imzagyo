
>     <script>
          tailwind.config = {
              theme: {
                  extend: {
                      colors: {
                          navy: '#0a192f',
                          gold: '#c5a059',
                          modern: '#e17055',
                          nature: '#1b4d3e',
                          soft: '#f8fafc',
                      },
                      fontFamily: {
                          sans: ['Inter', 'sans-serif'],
                          serif: ['Playfair Display', 'serif'],
                      }
                  }
              }
          }
      </script>
      <style>
          body {
              background-color: #f8fafc;
              overflow-x: hidden;
          }
  
          .glass-panel {
              background: rgba(255, 255, 255, 0.95);
              backdrop-filter: blur(10px);
              border: 1px solid rgba(255, 255, 255, 0.2);
              box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
          }
  
          .glass-dark {
              background: rgba(10, 25, 47, 0.95);
              backdrop-filter: blur(10px);
              border-right: 1px solid rgba(255, 255, 255, 0.1);
          }
  
          .brand-pattern {
              background-image: radial-gradient(#c5a059 1px, transparent 1px);
              background-size: 20px 20px;
              opacity: 0.1;
          }
  
          .gold-glow {
              box-shadow: 0 0 15px rgba(197, 160, 89, 0.3);
          }
  
          /* Tablo Stilleri */
          .premium-table th {
              font-family: 'Playfair Display', serif;
              letter-spacing: 0.05em;
              text-transform: uppercase;
              font-size: 0.75rem;
              color: #64748b;
              background-color: #f8fafc;
          }
  
          .premium-table tr {
              transition: all 0.2s ease;
          }
  
          .premium-table tbody tr:hover {
              background-color: #f1f5f9;
          }
  
          /* MenÃ¼ Aktif Durumu */
          .nav-item.active {
              background: rgba(197, 160, 89, 0.1);
              color: #c5a059;
              border-right: 3px solid #c5a059;
          }
  
          /* GiriÅŸ EkranÄ± Ä°kilik DÃ¼zen */
          .split-layout {
              display: flex;
              min-height: 100vh;
              width: 100%;
          }
  
          .split-left {
              flex: 1;
              background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&
w=2000&q=80');
              background-size: cover;
              background-position: center;
              position: relative;
              display: flex;
              align-items: center;
              justify-content: center;
              overflow: hidden;
          }
  
          .split-left::before {
              content: '';
              position: absolute;
              inset: 0;
              background: linear-gradient(to right, rgba(10, 25, 47, 0.9), rgba(10, 25, 47, 0.4));
          }
  
          .split-right {
              flex: 1;
              background-color: #f8fafc;
              display: flex;
              align-items: center;
              justify-content: center;
              padding: 2rem;
              position: relative;
          }
  
          /* Animasyonlar */
          .fade-in {
              opacity: 0;
              animation: fadeIn 1s ease-out forwards;
          }
  
          .slide-up-anim {
              opacity: 0;
              transform: translateY(30px);
              animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          }
  
          @keyframes fadeIn {
              to {
                  opacity: 1;
              }
          }
  
          @keyframes slideUp {
              to {
                  opacity: 1;
                  transform: translateY(0);
              }
          }
  
          .delay-100 {
              animation-delay: 0.1s;
          }
  
          .delay-200 {
              animation-delay: 0.2s;
          }
  
          .delay-300 {
              animation-delay: 0.3s;
          }
  
          /* Dashboard Entrance */
          #portal-app.show-app {
              display: flex !important;
              animation: fadeIn 0.8s ease-out forwards;
          }
  
          /* Scrollbar */
          ::-webkit-scrollbar {
              width: 8px;
              height: 8px;
          }
  
          ::-webkit-scrollbar-track {
              background: #f1f1f1;
          }
  
          ::-webkit-scrollbar-thumb {
              background: #cbd5e1;
              border-radius: 4px;
          }
  
          ::-webkit-scrollbar-thumb:hover {
              background: #94a3b8;
          }
      </style>
  </head>
  
  <body class="text-slate-800 antialiased font-sans bg-gray-50 flex h-screen overflow-hidden">
  
      <!-- LOGIN EKRANI (VarsayÄ±lan olarak gÃ¶rÃ¼nÃ¼r, giriÅŸ yapÄ±lÄ±nca gizlenir) -->
      <div id="login-section" class="fixed inset-0 z-50 bg-navy transition-all duration-700">
          <div class="split-layout">
              <!-- Sol Taraf: GÃ¶rsel ve Marka MesajÄ± -->
              <div class="split-left hidden md:flex">
                  <div class="absolute inset-0 brand-pattern opacity-20"></div>
                  <div class="relative z-10 p-12 max-w-2xl w-full text-left">
                      <div class="mb-12 slide-up-anim">
                          <i class="fa-solid fa-signature text-gold text-5xl mb-4"></i>
                          <h1 class="text-5xl lg:text-7xl font-bold font-serif text-white leading-tight drop-shadow-xl"
>
                              Sadece Bir Ev DeÄŸil, <br>
                              <span class="text-gold italic">Yeni Bir Hayat.</span>
                          </h1>
                      </div>
  
                      <div class="space-y-6 slide-up-anim delay-100 border-l-2 border-gold/50 pl-6">
                          <p class="text-gray-300 text-sm md:text-base leading-relaxed max-w-md">
                              Ä°mza Gayrimenkul Premium YÃ¶netim paneline hoÅŸ geldiniz. PortfÃ¶yÃ¼nÃ¼zÃ¼, sÃ¶zleÅŸmele
rinizi ve
                              yatÄ±rÄ±mlarÄ±nÄ±zÄ± lÃ¼ksÃ¼n getirdiÄŸi konforla yÃ¶netin.
                          </p>
                          <div class="flex items-center gap-4 text-xs font-bold text-gold uppercase tracking-[0.2em]">
                              <span><i class="fa-solid fa-check mr-2"></i> GÃ¼venli</span>
                              <span><i class="fa-solid fa-check mr-2"></i> Åeffaf</span>
                              <span><i class="fa-solid fa-check mr-2"></i> AyrÄ±calÄ±klÄ±</span>
                          </div>
                      </div>
                  </div>
              </div>
  
              <!-- SaÄŸ Taraf: GiriÅŸ Formu -->
              <div class="split-right">
                  <div class="w-full max-w-md slide-up-anim delay-200">
                      <div class="text-center mb-10 md:hidden">
                          <i class="fa-solid fa-signature text-gold text-5xl mb-3"></i>
                          <h2 class="text-3xl font-serif text-navy font-bold tracking-wider">Ä°mza Portal</h2>
                      </div>
  
                      <div
                          class="bg-white p-10 rounded-2xl shadow-xl shadow-navy/5 border border-gray-100 relative over
flow-hidden">
                          <!-- Dekoratif Ãœst Ã‡izgi -->
                          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-navy via-gold to-navy"></d
iv>
  
                          <div class="mb-8 text-center">
                              <h3 class="text-2xl font-bold text-navy font-serif mb-2">Sisteme GiriÅŸ YapÄ±n</h3>
                              <p class="text-sm text-gray-500">Premium yÃ¶netim alanÄ±na eriÅŸmek iÃ§in yetkili bilgile
rinizi
                                  giriniz.</p>
                          </div>
  
                          <div class="space-y-5">
                              <div>
                                  <label class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">Kullan
Ä±cÄ±
                                      AdÄ±</label>
                                  <div class="relative group">
                                      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"
>
                                          <i
                                              class="fa-regular fa-user text-gray-400 group-focus-within:text-gold tran
sition-colors"></i>
                                      </div>
                                      <input type="text" id="username"
                                          class="w-full pl-11 pr-4 py-3.5 bg-gray-50 border border-gray-200 rounded-lg 
focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold focus:bg-white transition-all text-sm font-medium 
text-navy placeholder-gray-400"
                                          placeholder="admin">
                                  </div>
                              </div>
                              <div>
                                  <div class="flex items-center justify-between mb-2">
                                      <label
                                          class="block text-xs font-bold text-navy uppercase tracking-wider">Åifre</la
bel>
                                      <a href="#"
                                          class="text-[10px] text-gray-400 hover:text-gold transition-colors font-mediu
m">Åifremi
                                          Unuttum</a>
                                  </div>
                                  <div class="relative group">
                                      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"
>
                                          <i
                                              class="fa-solid fa-lock text-gray-400 group-focus-within:text-gold transi
tion-colors"></i>
                                      </div>
                                      <input type="password" id="password"
                                          class="w-full pl-11 pr-4 py-3.5 bg-gray-50 border border-gray-200 rounded-lg 
focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold focus:bg-white transition-all text-sm font-medium 
text-navy placeholder-gray-400"
                                          placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢">
                                      <button
                                          class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:
text-navy transition-colors">
                                          <i class="fa-regular fa-eye-slash text-sm"></i>
                                      </button>
                                  </div>
                              </div>
  
                              <div class="pt-2">
                                  <button onclick="login()"
                                      class="w-full bg-navy hover:bg-slate-800 text-gold font-bold py-4 rounded-lg tran
sition-all gold-glow uppercase tracking-[0.15em] text-xs flex items-center justify-center gap-3">
                                      GÃ¼venli GiriÅŸ <i class="fa-solid fa-arrow-right"></i>
                                  </button>
                              </div>
  
                              <div id="login-error"
                                  class="hidden mt-4 p-3 bg-red-50 border border-red-100 rounded-lg flex items-center g
ap-3 text-red-600 text-xs font-medium">
                                  <i class="fa-solid fa-circle-exclamation text-base"></i>
                                  <span>GiriÅŸ bilgileri hatalÄ±. LÃ¼tfen kontrol edip tekrar deneyin.</span>
                              </div>
                          </div>
                      </div>
  
                      <p class="text-center text-gray-400 text-[10px] uppercase tracking-widest mt-8 font-medium">
                          &copy; 2024 Ä°MZA GAYRÄ°MENKUL. TÃœM HAKLARI SAKLIDIR.
                      </p>
                  </div>
              </div>
          </div>
      </div>
  
      <!-- ANA PORTAL ARAYÃœZÃœ (GiriÅŸ yapÄ±ldÄ±ktan sonra gÃ¶sterilir) -->
      <div id="portal-app" class="flex w-full h-full hidden">
  
          <!-- SIDEBAR -->
          <aside id="sidebar"
              class="w-72 glass-dark flex flex-col h-full shrink-0 fixed inset-y-0 left-0 transform -translate-x-full l
g:translate-x-0 lg:relative lg:inset-0 transition-transform duration-300 z-30">
              <div class="absolute inset-0 brand-pattern pointer-events-none"></div>
  
              <!-- Logo AlanÄ± -->
              <div class="h-20 flex items-center px-8 border-b border-white/10 relative z-10 cursor-pointer"
                  onclick="window.location.href='anasayfa.html'">
                  <i class="fa-solid fa-signature text-gold text-2xl mr-3"></i>
                  <div class="flex flex-col">
                      <span
                          class="font-serif font-bold text-xl tracking-widest text-white leading-none uppercase">Ä°MZA<
/span>
                      <span class="text-gray-400 text-[9px] tracking-[0.3em] uppercase mt-1">Portal</span>
                  </div>
              </div>
  
              <!-- KullanÄ±cÄ± Profili -->
              <div class="px-8 py-6 border-b border-white/5 relative z-10">
                  <div class="flex items-center gap-4">
                      <div
                          class="w-12 h-12 rounded-full bg-gold/20 flex items-center justify-center border border-gold/
50">
                          <i class="fa-regular fa-user text-gold text-xl"></i>
                      </div>
                      <div>
                          <p id="sidebar-user-name" class="text-white font-medium text-sm">YÃ¶netici</p>
                          <p id="sidebar-user-role" class="text-gold text-[10px] uppercase tracking-wider font-bold">Ad
min
                          </p>
                      </div>
                  </div>
              </div>
  
              <!-- Navigasyon -->
              <nav class="flex-1 overflow-y-auto py-6 px-4 space-y-1 relative z-10">
                  <button onclick="showSection('dashboard', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium active">
                      <i class="fa-solid fa-chart-pie w-5 text-center"></i> Dashboard Ã–zet
                  </button>
  
                  <div class="pt-4 pb-2 px-4">
                      <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">ModÃ¼ller</p>
                  </div>
  
                  <button onclick="showSection('portfolios', this)"
                      class="nav-item w-full flex items-center justify-between px-4 py-3 rounded-lg text-gray-400 hover
:text-white hover:bg-white/5 transition-all text-sm font-medium">
                      <div class="flex items-center gap-3">
                          <i class="fa-solid fa-gem w-5 text-center"></i> PortfÃ¶y YÃ¶netimi
                      </div>
                      <span class="bg-gold/20 text-gold text-[10px] py-0.5 px-2 rounded-full">34</span>
                  </button>
  
                  <button onclick="showSection('contracts', this)"
                      class="nav-item w-full flex items-center justify-between px-4 py-3 rounded-lg text-gray-400 hover
:text-white hover:bg-white/5 transition-all text-sm font-medium">
                      <div class="flex items-center gap-3">
                          <i class="fa-solid fa-file-signature w-5 text-center"></i> SÃ¶zleÅŸmeler
                      </div>
                  </button>
  
                  <button onclick="showSection('contract-builder', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium">
                      <i class="fa-solid fa-file-pen w-5 text-center"></i> SÃ¶zleÅŸme HazÄ±rlama
                      <span class="bg-gold/20 text-gold text-[10px] py-0.5 px-2 rounded-full">Yeni</span>
                  </button>
  
                  <button onclick="showSection('taxes', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium">
                      <i class="fa-solid fa-scale-balanced w-5 text-center"></i> Finans & Vergi
                  </button>
  
                  <button onclick="showSection('maintenance', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium">
                      <i class="fa-solid fa-screwdriver-wrench w-5 text-center"></i> BakÄ±m Talepleri
                  </button>
  
                  <button onclick="showSection('appointments', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium">
                      <i class="fa-regular fa-calendar-check w-5 text-center"></i> Randevular
                  </button>
  
                  <div class="pt-4 pb-2 px-4">
                      <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Sistem</p>
                  </div>
  
                  <button onclick="showSection('hero', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium">
                      <i class="fa-solid fa-images w-5 text-center"></i> Vitrin (Hero) YÃ¶netimi
                  </button>
  
                  <button onclick="showSection('users', this)"
                      class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-whit
e hover:bg-white/5 transition-all text-sm font-medium">
                      <i class="fa-solid fa-users-gear w-5 text-center"></i> KullanÄ±cÄ± YÃ¶netimi
                  </button>
              </nav>
  
              <!-- Ã‡Ä±kÄ±ÅŸ Butonu -->
              <div class="p-4 border-t border-white/10 relative z-10">
                  <button onclick="logout()"
                      class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-modern hover:
bg-modern/10 transition-all text-sm font-bold">
                      <i class="fa-solid fa-arrow-right-from-bracket w-5 text-center"></i> GÃ¼venli Ã‡Ä±kÄ±ÅŸ
                  </button>
              </div>
          </aside>
  
          <!-- MAIN CONTENT AREA -->
          <main class="flex-1 flex flex-col h-full overflow-hidden bg-gray-50 relative">
  
              <!-- Header (Top bar) -->
              <header class="h-20 bg-white border-b border-gray-200 flex items-center justify-between px-8 shrink-0 z-1
0">
                  <h1 id="page-title" class="text-xl font-serif font-bold text-navy flex items-center gap-3">
                      <i class="fa-solid fa-chart-pie text-gold text-lg"></i> Dashboard Ã–zet
                  </h1>
  
                  <div class="flex items-center gap-5">
                      <div class="relative">
                          <i
                              class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-40
0 text-sm"></i>
                          <input type="text" placeholder="Sistemde ara..."
                              class="pl-9 pr-4 py-2 bg-gray-100 border-none rounded-full text-sm focus:outline-none foc
us:ring-2 focus:ring-gold/30 w-64">
                      </div>
                      <button id="sidebar-toggle"
                          class="relative text-gray-500 hover:text-navy transition-colors mr-4 lg:hidden">
                          <i class="fa-regular fa-bell text-xl"></i>
                          <span
                              class="absolute -top-1 -right-1 w-3.5 h-3.5 bg-modern rounded-full border-2 border-white"
></span>
                      </button>
                  </div>
              </header>
  
              <!-- Ä°Ã§erik AlanÄ± (Scrollable) -->
              <div class="flex-1 overflow-y-auto p-8 relative">
  
                  <!-- DASHBOARD SECTION -->
                  <div id="dashboard-section" class="content-section">
                      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                          <!-- Stat Card 1 -->
                          <div
                              class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm flex items-center justify
-between">
                              <div>
                                  <p class="text-xs text-gray-500 uppercase tracking-wider font-semibold mb-1">Aktif
                                      PortfÃ¶y</p>
                                  <h3 class="text-3xl font-bold text-navy font-serif">34</h3>
                              </div>
                              <div
                                  class="w-12 h-12 rounded-full bg-gold/10 flex items-center justify-center text-gold t
ext-xl">
                                  <i class="fa-solid fa-building"></i>
                              </div>
                          </div>
  
                          <!-- Stat Card 2 -->
                          <div
                              class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm flex items-center justify
-between">
                              <div>
                                  <p class="text-xs text-gray-500 uppercase tracking-wider font-semibold mb-1">Bu Ay
                                      SatÄ±lan</p>
                                  <h3 class="text-3xl font-bold text-navy font-serif">2</h3>
                              </div>
                              <div
                                  class="w-12 h-12 rounded-full bg-navy/10 flex items-center justify-center text-navy t
ext-xl">
                                  <i class="fa-solid fa-handshake"></i>
                              </div>
                          </div>
  
                          <!-- Stat Card 3 -->
                          <div
                              class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm flex items-center justify
-between">
                              <div>
                                  <p class="text-xs text-gray-500 uppercase tracking-wider font-semibold mb-1">Bekleyen
                                      BakÄ±m</p>
                                  <h3 class="text-3xl font-bold text-modern font-serif">5</h3>
                              </div>
                              <div
                                  class="w-12 h-12 rounded-full bg-modern/10 flex items-center justify-center text-mode
rn text-xl">
                                  <i class="fa-solid fa-screwdriver-wrench"></i>
                              </div>
                          </div>
  
                          <!-- Stat Card 4 -->
                          <div
                              class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm flex items-center justify
-between">
                              <div>
                                  <p class="text-xs text-gray-500 uppercase tracking-wider font-semibold mb-1">Randevul
ar
                                  </p>
                                  <h3 class="text-3xl font-bold text-nature font-serif">8</h3>
                              </div>
                              <div
                                  class="w-12 h-12 rounded-full bg-nature/10 flex items-center justify-center text-natu
re text-xl">
                                  <i class="fa-regular fa-calendar-check"></i>
                              </div>
                          </div>
                      </div>
  
                      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                          <!-- HÄ±zlÄ± Ä°ÅŸlemler -->
                          <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6 lg:col-span-2">
                              <div class="flex justify-between items-center mb-6">
                                  <h3 class="font-serif font-bold text-lg text-navy">Son Eklenen PortfÃ¶yler</h3>
                                  <button
                                      onclick="showSection('portfolios', document.querySelector('.nav-item[onclick*=\'p
ortfolios\']'))"
                                      class="text-gold text-sm font-medium hover:underline">TÃ¼mÃ¼nÃ¼ GÃ¶r</button>
                              </div>
                              <div class="overflow-x-auto">
                                  <table class="w-full text-left border-collapse premium-table">
                                      <thead>
                                          <tr>
                                              <th class="py-3 px-4 border-b border-gray-100">Referans</th>
                                              <th class="py-3 px-4 border-b border-gray-100">BaÅŸlÄ±k</th>
                                              <th class="py-3 px-4 border-b border-gray-100">Lokasyon</th>
                                              <th class="py-3 px-4 border-b border-gray-100">Fiyat</th>
                                          </tr>
                                      </thead>
                                      <tbody id="dashboard-portfolio-list" class="text-sm">
                                          <!-- Dinamik iÃ§erik gelecek -->
                                          <tr>
                                              <td colspan="4" class="py-8 text-center text-gray-400">YÃ¼kleniyor...</td
>
                                          </tr>
                                      </tbody>
                                  </table>
                              </div>
                          </div>
  
                          <!-- YaklaÅŸan Etkinlikler -->
                          <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                              <h3 class="font-serif font-bold text-lg text-navy mb-6">YaklaÅŸan Etkinlikler</h3>
                              <div class="space-y-4">
                                  <div
                                      class="flex items-start gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors c
ursor-pointer border border-transparent hover:border-gray-100">
                                      <div
                                          class="w-10 h-10 rounded-lg bg-red-50 flex flex-col items-center justify-cent
er shrink-0 border border-red-100">
                                          <span class="text-[10px] font-bold text-red-500 uppercase">Eki</span>
                                          <span class="text-sm font-bold text-red-700 leading-none">24</span>
                                      </div>
                                      <div>
                                          <p class="text-sm font-bold text-navy">SÃ¶zleÅŸme Yenileme</p>
                                          <p class="text-xs text-gray-500 mt-0.5">Cam Oda Penthouse (IMZ-092)</p>
                                      </div>
                                  </div>
                                  <div
                                      class="flex items-start gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors c
ursor-pointer border border-transparent hover:border-gray-100">
                                      <div
                                          class="w-10 h-10 rounded-lg bg-blue-50 flex flex-col items-center justify-cen
ter shrink-0 border border-blue-100">
                                          <span class="text-[10px] font-bold text-blue-500 uppercase">Kas</span>
                                          <span class="text-sm font-bold text-blue-700 leading-none">12</span>
                                      </div>
                                      <div>
                                          <p class="text-sm font-bold text-navy">YÄ±llÄ±k Vergi Ã–demesi</p>
                                          <p class="text-xs text-gray-500 mt-0.5">Ekolojik Orman Evi (IMZ-447)</p>
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
  
                  <!-- CONTRACT BUILDER SECTION -->
                  <div id="contract-builder-section" class="content-section hidden">
                      <div class="max-w-4xl mx-auto">
                          <!-- Wizard Header -->
                          <div class="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm mb-8">
                              <h2 class="text-2xl font-serif font-bold text-navy mb-2">AkÄ±llÄ± SÃ¶zleÅŸme HazÄ±rlama</
h2>
                              <p class="text-gray-500 text-sm">Gayrimenkul seÃ§erek onlarca madde arasÄ±ndan
                                  Ã¶zelleÅŸtirilebilir sÃ¶zleÅŸmenizi saniyeler iÃ§inde hazÄ±rlayÄ±n.</p>
  
                              <!-- Wizard Steps -->
                              <div class="flex items-center justify-between mt-8 relative">
                                  <div class="absolute top-1/2 left-0 w-full h-0.5 bg-gray-100 -translate-y-1/2 z-0">
                                  </div>
                                  <div id="con-wiz-progress"
                                      class="absolute top-1/2 left-0 w-0 h-0.5 bg-gold -translate-y-1/2 z-0 transition-
all duration-500">
                                  </div>
  
                                  <div class="con-wiz-step active relative z-10 flex flex-col items-center gap-2">
                                      <div
                                          class="w-10 h-10 rounded-full bg-navy text-white flex items-center justify-ce
nter font-bold border-4 border-white shadow-md transition-all">
                                          1</div>
                                      <span class="text-[10px] font-bold uppercase tracking-wider text-navy">MÃ¼lk
                                          SeÃ§imi</span>
                                  </div>
                                  <div class="con-wiz-step relative z-10 flex flex-col items-center gap-2">
                                      <div
                                          class="w-10 h-10 rounded-full bg-gray-200 text-gray-500 flex items-center jus
tify-center font-bold border-4 border-white shadow-md transition-all">
                                          2</div>
                                      <span
                                          class="text-[10px] font-bold uppercase tracking-wider text-gray-400">Åablon<
/span>
                                  </div>
                                  <div class="con-wiz-step relative z-10 flex flex-col items-center gap-2">
                                      <div
                                          class="w-10 h-10 rounded-full bg-gray-200 text-gray-500 flex items-center jus
tify-center font-bold border-4 border-white shadow-md transition-all">
                                          3</div>
                                      <span
                                          class="text-[10px] font-bold uppercase tracking-wider text-gray-400">Maddeler
</span>
                                  </div>
                                  <div class="con-wiz-step relative z-10 flex flex-col items-center gap-2">
                                      <div
                                          class="w-10 h-10 rounded-full bg-gray-200 text-gray-500 flex items-center jus
tify-center font-bold border-4 border-white shadow-md transition-all">
                                          4</div>
                                      <span
                                          class="text-[10px] font-bold uppercase tracking-wider text-gray-400">Ã–nizlem
e</span>
                                  </div>
                              </div>
                          </div>
  
                          <!-- Step 1: Property Select -->
                          <div id="con-step-1" class="con-wiz-content">
                              <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
                                  <h3 class="text-lg font-bold text-navy mb-4">SÃ¶zleÅŸme YapÄ±lacak MÃ¼lkÃ¼ SeÃ§in</h3
>
                                  <div class="relative mb-6">
                                      <i
                                          class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 
text-gray-400"></i>
                                      <input type="text" id="prop-search"
                                          oninput="searchPropertiesForContract(this.value)"
                                          placeholder="Ref No veya BaÅŸlÄ±k ile ara..."
                                          class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg fo
cus:ring-2 focus:ring-gold/30 outline-none">
                                  </div>
                                  <div id="prop-list" class="grid grid-cols-1 gap-4 max-h-[400px] overflow-y-auto pr-2"
>
                                      <!-- MÃ¼lkler buraya yÃ¼klenecek -->
                                      <div class="text-center py-10 text-gray-400">YÃ¼kleniyor...</div>
                                  </div>
                              </div>
                          </div>
  
                          <!-- Step 2: Template Select -->
                          <div id="con-step-2" class="con-wiz-content hidden">
                              <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
                                  <h3 class="text-lg font-bold text-navy mb-4">SÃ¶zleÅŸme Tipini Belirleyin</h3>
                                  <div id="template-list" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                      <!-- Åablonlar buraya yÃ¼klenecek -->
                                  </div>
                              </div>
                          </div>
  
                          <!-- Step 3: Clause Select -->
                          <div id="con-step-3" class="con-wiz-content hidden">
                              <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
                                  <h3 class="text-lg font-bold text-navy mb-4">SÃ¶zleÅŸme Maddelerini DÃ¼zenleyin</h3>
                                  <p class="text-sm text-gray-500 mb-6">Ä°ÅŸaretli maddeler sÃ¶zleÅŸmeye dahil edilecek
tir.
                                      BazÄ± maddeler zorunludur.</p>
                                  <div id="clause-list" class="space-y-3">
                                      <!-- Maddeler buraya yÃ¼klenecek -->
                                  </div>
                              </div>
                          </div>
  
                          <!-- Step 4: Preview -->
                          <div id="con-step-4" class="con-wiz-content hidden">
                              <div class="bg-white rounded-xl p-8 border border-gray-100 shadow-sm font-serif">
                                  <div class="text-center mb-8 border-b pb-8">
                                      <h2 class="text-2xl font-bold uppercase tracking-widest text-navy"
                                          id="preview-title">SÃ–ZLEÅME Ã–NÄ°ZLEME</h2>
                                      <p class="text-gray-500 mt-2" id="preview-property-info"></p>
                                  </div>
                                  <div id="preview-content" class="text-sm leading-relaxed space-y-4 text-gray-800">
                                      <!-- Ã–nizleme iÃ§eriÄŸi -->
                                  </div>
                                  <div class="mt-12 pt-8 border-t grid grid-cols-2 gap-12 text-center">
                                      <div class="border-b border-dashed border-gray-300 pb-20">Taraf 1 (SatÄ±cÄ±/Ev Sa
hibi)
                                      </div>
                                      <div class="border-b border-dashed border-gray-300 pb-20">Taraf 2 (AlÄ±cÄ±/KiracÄ
±)
                                      </div>
                                  </div>
                              </div>
                          </div>
  
                          <!-- Wizard Navigation -->
                          <div class="flex items-center justify-between mt-8">
                              <button id="con-prev-btn" onclick="conWizPrev()"
                                  class="px-6 py-2 rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-50 fon
t-bold transition-all opacity-0 pointer-events-none">
                                  Geri
                              </button>
                              <div class="flex gap-4">
                                  <button id="con-next-btn" onclick="conWizNext()"
                                      class="px-8 py-2 rounded-lg bg-navy text-white hover:bg-navy/90 font-bold shadow-
lg shadow-navy/20 transition-all">
                                      Ä°leri
                                  </button>
                                  <button id="con-save-btn" onclick="savePreparedContract()"
                                      class="px-8 py-2 rounded-lg bg-gold text-white hover:bg-gold/90 font-bold shadow-
lg shadow-gold/20 transition-all hidden">
                                      SÃ¶zleÅŸmeyi Kaydet
                                  </button>
                              </div>
                          </div>
                      </div>
                  </div>
  
                  <!-- PORTFOLIOS SECTION -->
                  <div id="portfolios-section" class="content-section hidden">
                      <div class="flex justify-between items-center mb-6">
                          <p class="text-gray-500 text-sm">Sistemdeki tÃ¼m ilanlarÄ± YÃ¶netin.</p>
                          <button onclick="openPortfolioModal()"
                              class="bg-navy hover:bg-slate-800 text-white px-4 py-2 rounded-lg text-sm font-medium tra
nsition-colors shadow-md flex items-center gap-2">
                              <i class="fa-solid fa-plus"></i> Yeni Ä°lan Ekle
                          </button>
                      </div>
                      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                          <div class="overflow-x-auto">
                              <table class="w-full text-left border-collapse premium-table">
                                  <thead>
                                      <tr>
                                          <th class="py-4 px-6 border-b border-gray-200">GÃ¶rsel</th>
                                          <th class="py-4 px-6 border-b border-gray-200">Referans</th>
                                          <th class="py-4 px-6 border-b border-gray-200">Koleksiyon</th>
                                          <th class="py-4 px-6 border-b border-gray-200">BaÅŸlÄ±k</th>
                                          <th class="py-4 px-6 border-b border-gray-200">Fiyat</th>
                                          <th class="py-4 px-6 border-b border-gray-200 text-right">Ä°ÅŸlemler</th>
                                      </tr>
                                  </thead>
                                  <tbody id="portfolios-table-body" class="text-sm text-gray-700">
                                      <!-- JS ile doldurulacak -->
                                  </tbody>
                              </table>
                          </div>
                      </div>
                  </div>
  
                  <!-- USERS SECTION -->
                  <div id="users-section" class="content-section hidden">
                      <div class="flex justify-between items-center mb-6">
                          <p class="text-gray-500 text-sm">Sistem kullanÄ±cÄ±larÄ±nÄ±, Ã§alÄ±ÅŸanlarÄ± ve mÃ¼ÅŸterileri
 yÃ¶netin.</p>
                          <button
                              class="bg-navy hover:bg-slate-800 text-white px-4 py-2 rounded-lg text-sm font-medium tra
nsition-colors shadow-md flex items-center gap-2">
                              <i class="fa-solid fa-user-plus"></i> KullanÄ±cÄ± Ekle
                          </button>
                      </div>
                      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden p-8 text-center"
>
                          <i class="fa-solid fa-users-gear text-4xl text-gray-300 mb-4"></i>
                          <h3 class="text-lg font-bold text-navy mb-2">KullanÄ±cÄ± Listesi YÃ¼kleniyor</h3>
                          <p class="text-gray-500 text-sm max-w-md mx-auto">API entegrasyonu tamamlandÄ±ÄŸÄ±nda sistemd
eki
                              tÃ¼m yÃ¶neticiler, asistanlar ve mÃ¼ÅŸteriler burada gÃ¶rÃ¼ntÃ¼lenecektir.</p>
                      </div>
                  </div>
  
                  <!-- HERO CMS SECTION -->
                  <div id="hero-section" class="content-section hidden">
                      <div class="flex justify-between items-center mb-6">
                          <p class="text-gray-500 text-sm">Anasayfa aÃ§Ä±lÄ±ÅŸ (Hero) ekranÄ± slider gÃ¶rsellerini ve b
uton
                              hedeflerini yÃ¶netin.</p>
                          <button onclick="openHeroModal()"
                              class="bg-navy hover:bg-slate-800 text-gold shadow-gold/20 px-4 py-2 rounded-lg text-sm f
ont-bold transition-all shadow-md flex items-center gap-2 uppercase tracking-wider text-[10px]">
                              <i class="fa-solid fa-plus"></i> Yeni Slide Ekle
                          </button>
                      </div>
                      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                          <div class="overflow-x-auto">
                              <table class="w-full text-left border-collapse premium-table">
                                  <thead>
                                      <tr>
                                          <th class="py-4 px-6 border-b border-gray-200 w-16">SÄ±ra</th>
                                          <th class="py-4 px-6 border-b border-gray-200 w-32">GÃ¶rsel</th>
                                          <th class="py-4 px-6 border-b border-gray-200">Alt BaÅŸlÄ±k</th>
                                          <th class="py-4 px-6 border-b border-gray-200">Ana BaÅŸlÄ±k (1 & 2)</th>
                                          <th class="py-4 px-6 border-b border-gray-200">Hedef Link</th>
                                          <th class="py-4 px-6 border-b border-gray-200 text-right">Ä°ÅŸlemler</th>
                                      </tr>
                                  </thead>
                                  <tbody id="hero-table-body" class="text-sm text-gray-700">
                                      <tr>
                                          <td colspan="6" class="py-8 text-center text-gray-400">YÃ¼kleniyor...</td>
                                      </tr>
                                  </tbody>
                              </table>
                          </div>
                      </div>
                  </div>
  
                  <!-- DÄ°ÄER BÃ–LÃœMLER Ä°Ã‡Ä°N PLACEHOLDERLAR -->
                  <div id="contracts-section" class="content-section hidden">
                      <div
                          class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden p-8 text-center m
t-6">
                          <i class="fa-solid fa-file-signature text-4xl text-gray-300 mb-4"></i>
                          <h3 class="text-lg font-bold text-navy mb-2">SÃ¶zleÅŸme ModÃ¼lÃ¼</h3>
                          <p class="text-gray-500 text-sm max-w-md mx-auto">Kira ve satÄ±ÅŸ sÃ¶zleÅŸmeleri yÃ¶netimi ya
pÄ±m
                              aÅŸamasÄ±nda.</p>
                      </div>
                  </div>
  
                  <div id="taxes-section" class="content-section hidden">
                      <div class="flex justify-between items-center mb-6">
                          <p class="text-gray-500 text-sm">Finansal hesaplamalar ve vergi takip takvimi.</p>
                      </div>
  
                      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                          <!-- TCMB Konut Kredisi Hesaplama ModÃ¼lÃ¼ -->
                          <div
                              class="bg-white rounded-xl border border-gray-100 shadow-sm p-8 relative overflow-hidden 
group">
                              <!-- Dekoratif Gradient Arkaplan -->
                              <div
                                  class="absolute top-0 right-0 w-64 h-64 bg-gold/5 rounded-full blur-3xl -mr-20 -mt-20
 pointer-events-none transition-transform group-hover:scale-110">
                              </div>
  
                              <div class="flex items-center gap-4 mb-6 relative z-10">
                                  <div
                                      class="w-12 h-12 rounded-xl bg-navy/5 flex items-center justify-center text-navy 
shrink-0">
                                      <i class="fa-solid fa-calculator text-xl"></i>
                                  </div>
                                  <div>
                                      <h3 class="text-xl font-serif font-bold text-navy">Konut Kredisi Hesaplama</h3>
                                      <p class="text-xs text-gray-500 uppercase tracking-wider flex items-center gap-2"
>
                                          <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                                          TCMB CanlÄ± Veri Bekleniyor...
                                      </p>
                                  </div>
                              </div>
  
                              <div class="space-y-5 relative z-10">
                                  <div>
                                      <label
                                          class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">Ekspe
rtiz
                                          DeÄŸeri (TL)</label>
                                      <div class="relative">
                                          <div
                                              class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-no
ne">
                                              <i class="fa-solid fa-home text-gray-400"></i>
                                          </div>
                                          <input type="number" id="calc-expertise"
                                              class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-l
g focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold transition-all font-bold text-navy"
                                              value="5000000" oninput="calculateMortgage()">
                                      </div>
                                  </div>
                                  <div class="grid grid-cols-2 gap-4">
                                      <div>
                                          <label
                                              class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">E
nerji
                                              SÄ±nÄ±fÄ±</label>
                                          <div class="relative">
                                              <select id="calc-energy"
                                                  class="w-full pl-4 pr-4 py-3 bg-gray-50 border border-gray-200 rounde
d-lg focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold transition-all font-bold text-slate-700"
                                                  onchange="calculateMortgage()">
                                                  <option value="A-B">A-B SÄ±nÄ±fÄ±</option>
                                                  <option value="C">C SÄ±nÄ±fÄ±</option>
                                                  <option value="Diger">DiÄŸer</option>
                                              </select>
                                          </div>
                                      </div>
                                      <div>
                                          <label
                                              class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">Ä
°kinci
                                              Tapu Durumu</label>
                                          <div class="relative">
                                              <select id="calc-second-title"
                                                  class="w-full pl-4 pr-4 py-3 bg-gray-50 border border-gray-200 rounde
d-lg focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold transition-all font-bold text-slate-700"
                                                  onchange="calculateMortgage()">
                                                  <option value="Hayir">HayÄ±r (Ä°lk Evim)</option>
                                                  <option value="Evet">Evet (Ä°kinci Evim)</option>
                                              </select>
                                          </div>
                                      </div>
                                  </div>
  
                                  <div class="grid grid-cols-2 gap-4">
                                      <div>
                                          <label
                                              class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">T
alep
                                              Edilen Kredi (TL)</label>
                                          <div class="relative">
                                              <div
                                                  class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-event
s-none">
                                                  <i class="fa-solid fa-turkish-lira-sign text-gray-400"></i>
                                              </div>
                                              <input type="number" id="calc-amount"
                                                  class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 round
ed-lg focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold transition-all font-bold text-navy"
                                                  value="2000000" oninput="calculateMortgage()">
                                          </div>
                                      </div>
                                      <div>
                                          <label
                                              class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">V
ade
                                              (Ay)</label>
                                          <div class="relative">
                                              <div
                                                  class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-event
s-none">
                                                  <i class="fa-regular fa-calendar-days text-gray-400"></i>
                                              </div>
                                              <select id="calc-term"
                                                  class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 round
ed-lg focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold transition-all font-bold text-slate-700"
                                                  onchange="calculateMortgage()">
                                                  <option value="12">12 Ay</option>
                                                  <option value="24">24 Ay</option>
                                                  <option value="36">36 Ay</option>
                                                  <option value="48">48 Ay</option>
                                                  <option value="60" selected>60 Ay</option>
                                                  <option value="120">120 Ay</option>
                                              </select>
                                          </div>
                                      </div>
                                  </div>
  
                                  <div>
                                      <label class="block text-xs font-bold text-navy uppercase tracking-wider mb-2">TC
MB
                                          Referans YÄ±llÄ±k OranÄ± (%)</label>
                                      <div class="relative">
                                          <div
                                              class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-no
ne">
                                              <i class="fa-solid fa-percent text-gray-400"></i>
                                          </div>
                                          <input type="text" id="calc-rate"
                                              class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-l
g focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold transition-all font-bold text-slate-700 placehol
der-gray-400"
                                              placeholder="YÃ¼kleniyor..." readonly>
                                      </div>
                                      <p id="tcmb-date-info" class="text-[10px] text-gray-400 mt-1 italic text-right"><
/p>
                                  </div>
  
                                  <!-- SonuÃ§lar -->
                                  <div id="calc-results-container" class="mt-6 pt-6 border-t border-gray-100 hidden">
                                      <div class="mb-4 text-center">
                                          <p
                                              class="text-xs font-bold text-green-600 uppercase tracking-widest bg-gree
n-50 py-1 rounded inline-block px-3">
                                              OnaylandÄ±: LTV <span id="res-ltv"></span></p>
                                      </div>
  
                                      <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                                          <!-- Ä°yimser -->
                                          <div class="bg-blue-50/50 border border-blue-100 p-4 rounded-lg text-center">
                                              <p
                                                  class="text-[10px] text-blue-600 uppercase font-bold tracking-wider m
b-1">
                                                  Ä°yimser (Taban)</p>
                                              <p class="text-xs text-gray-500 mb-2">AylÄ±k: %<span
                                                      id="res-opt-rate"></span></p>
                                              <p id="res-opt-monthly"
                                                  class="text-lg font-serif font-bold text-navy mb-1 leading-none">0 â‚
º</p>
                                              <p class="text-[10px] text-gray-400 uppercase">Toplam: <span
                                                      id="res-opt-total" class="font-bold text-gray-500">0 â‚º</span></
p>
                                          </div>
                                          <!-- GerÃ§ekÃ§i -->
                                          <div
                                              class="bg-gold/5 border border-gold/20 p-4 rounded-lg text-center relativ
e shadow-sm">
                                              <div
                                                  class="absolute -top-2 inset-x-0 mx-auto w-16 bg-gold text-white text
-[8px] font-bold uppercase rounded-full tracking-widest py-0.5">
                                                  Piyasa</div>
                                              <p
                                                  class="text-[10px] text-gold uppercase font-bold tracking-wider mb-1 
mt-1">
                                                  GerÃ§ekÃ§i</p>
                                              <p class="text-xs text-gray-500 mb-2">AylÄ±k: %<span
                                                      id="res-real-rate"></span></p>
                                              <p id="res-real-monthly"
                                                  class="text-xl font-serif font-bold text-gold mb-1 leading-none">0 â‚
º</p>
                                              <p class="text-[10px] text-gray-400 uppercase">Toplam: <span
                                                      id="res-real-total" class="font-bold text-gray-600">0 â‚º</span><
/p>
                                          </div>
                                          <!-- KÃ¶tÃ¼mser -->
                                          <div class="bg-red-50/50 border border-red-100 p-4 rounded-lg text-center">
                                              <p class="text-[10px] text-red-600 uppercase font-bold tracking-wider mb-
1">
                                                  KÃ¶tÃ¼mser (Tavan)</p>
                                              <p class="text-xs text-gray-500 mb-2">AylÄ±k: %<span
                                                      id="res-pes-rate"></span></p>
                                              <p id="res-pes-monthly"
                                                  class="text-lg font-serif font-bold text-navy mb-1 leading-none">0 â‚
º</p>
                                              <p class="text-[10px] text-gray-400 uppercase">Toplam: <span
                                                      id="res-pes-total" class="font-bold text-gray-500">0 â‚º</span></
p>
                                          </div>
                                      </div>
                                  </div>
  
                                  <!-- Reddedildi -->
                                  <div id="calc-rejected-container"
                                      class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg hidden flex items-star
t gap-4">
                                      <div
                                          class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shr
ink-0">
                                          <i class="fa-solid fa-triangle-exclamation text-red-600 text-lg"></i>
                                      </div>
                                      <div>
                                          <h4 class="text-sm font-bold text-red-800">LTV SÄ±nÄ±rÄ± AÅŸÄ±ldÄ±</h4>
                                          <p class="text-xs text-red-600 mt-1 leading-relaxed">Talep edilen kredi mikta
rÄ±
                                              yasal sÄ±nÄ±rlarÄ±n Ã¼zerindedir. BDDK kurallarÄ±na gÃ¶re bu gayrimenkul 
iÃ§in
                                              maksimum LTV oranÄ± <strong>%<span id="rej-ltv"></span></strong> olarak
                                              belirlenmiÅŸtir.</p>
                                          <p class="text-xs font-bold text-red-800 mt-2">Maksimum Ã‡ekilebilir Tutar: <
span
                                                  id="rej-max-loan"></span></p>
                                      </div>
                                  </div>
                              </div>
                          </div>
  
                          <!-- DiÄŸer Finans ModÃ¼lleri (Placeholder) -->
                          <div class="space-y-6">
                              <div
                                  class="bg-white rounded-xl border border-gray-100 shadow-sm p-6 text-center h-full fl
ex flex-col justify-center opacity-70">
                                  <i class="fa-solid fa-scale-balanced text-4xl text-gray-300 mb-4"></i>
                                  <h3 class="text-lg font-bold text-navy mb-2">Vergi Takip ModÃ¼lÃ¼</h3>
                                  <p class="text-gray-500 text-sm max-w-sm mx-auto">Gayrimenkullere ait yÄ±llÄ±k beyann
ame
                                      ve emlak vergisi takvimi yapÄ±m aÅŸamasÄ±nda.</p>
                              </div>
                          </div>
                      </div>
                  </div>
  
                  <div id="maintenance-section" class="content-section hidden">
                      <div
                          class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden p-8 text-center m
t-6">
                          <i class="fa-solid fa-screwdriver-wrench text-4xl text-gray-300 mb-4"></i>
                          <h3 class="text-lg font-bold text-navy mb-2">BakÄ±m Talepleri</h3>
                          <p class="text-gray-500 text-sm max-w-md mx-auto">Rutin mÃ¼lk bakÄ±mlarÄ± modÃ¼lÃ¼ yapÄ±m aÅŸ
amasÄ±nda.
                          </p>
                      </div>
                  </div>
  
                  <div id="appointments-section" class="content-section hidden">
                      <div
                          class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden p-8 text-center m
t-6">
                          <i class="fa-regular fa-calendar-check text-4xl text-gray-300 mb-4"></i>
                          <h3 class="text-lg font-bold text-navy mb-2">Randevu Merkezi</h3>
                          <p class="text-gray-500 text-sm max-w-md mx-auto">Saha gÃ¶rÃ¼ÅŸmesi talep modÃ¼lÃ¼ yapÄ±m aÅŸ
amasÄ±nda.
                          </p>
                      </div>
                  </div>
  
              </div>
  
              <!-- ========================================== -->
              <!-- CONTRACTS SECTÄ°ON -->
              <section id="contracts-section" class="flex flex-col h-full bg-white hidden">
                  <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                      <div class="flex justify-between items-end">
                          <div class="space-y-1">
                              <h2 class="text-2xl font-serif font-bold text-navy">SÃ¶zleÅŸmeler</h2>
                              <p class="text-sm text-gray-500">MÃ¼lklerin kira ve satÄ±ÅŸ durumlarÄ±nÄ±, sÃ¶zleÅŸme sÃ¼
relerini
                                  yÃ¶netin.</p>
                          </div>
                          <button onclick="openContractModal()"
                              class="bg-navy hover:bg-slate-800 text-gold font-bold py-3 px-6 rounded-lg transition-all
 gold-glow uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                              <i class="fa-solid fa-plus"></i> Yeni SÃ¶zleÅŸme
                          </button>
                      </div>
                  </div>
  
                  <!-- Tablo AlanÄ± -->
                  <div class="flex-1 overflow-auto p-8 relative">
                      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                          <table class="w-full text-left premium-table">
                              <thead>
                                  <tr>
                                      <th class="px-6 py-4 font-bold text-xs">SÃ¶zleÅŸme ID</th>
                                      <th class="px-6 py-4 font-bold text-xs">PortfÃ¶y (MÃ¼lk)</th>
                                      <th class="px-6 py-4 font-bold text-xs">Ä°lgili Taraf</th>
                                      <th class="px-6 py-4 font-bold text-xs">Tip</th>
                                      <th class="px-6 py-4 font-bold text-xs">BaÅŸlangÄ±Ã§</th>
                                      <th class="px-6 py-4 font-bold text-xs">BitiÅŸ</th>
                                      <th class="px-6 py-4 text-right">Aksiyonlar</th>
                                  </tr>
                              </thead>
                              <tbody id="contracts-table-body" class="text-sm">
                                  <!-- JS Dinamik Dolduracak -->
                              </tbody>
                          </table>
                      </div>
                  </div>
              </section>
  
              <!-- ========================================== -->
              <!-- TAXES SECTÄ°ON -->
              <section id="taxes-section" class="flex flex-col h-full bg-white hidden">
                  <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                      <div class="flex justify-between items-end">
                          <div class="space-y-1">
                              <h2 class="text-2xl font-serif font-bold text-navy">Finans ve Vergi</h2>
                              <p class="text-sm text-gray-500">MÃ¼lk vergisi, beyanname, aidat ve diÄŸer mali yÃ¼kÃ¼mlÃ
¼lÃ¼kleri
                                  izleyin.</p>
                          </div>
                          <button onclick="openTaxModal()"
                              class="bg-navy hover:bg-slate-800 text-white font-bold py-3 px-6 rounded-lg transition-al
l uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                              <i class="fa-solid fa-plus text-gold"></i> KayÄ±t Ekle
                          </button>
                      </div>
                  </div>
  
                  <div class="flex-1 overflow-auto p-8 relative">
                      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                          <table class="w-full text-left premium-table">
                              <thead>
                                  <tr>
                                      <th class="px-6 py-4 font-bold text-xs">ID</th>
                                      <th class="px-6 py-4 font-bold text-xs">PortfÃ¶y</th>
                                      <th class="px-6 py-4 font-bold text-xs">Ã–deme Tipi</th>
                                      <th class="px-6 py-4 font-bold text-xs">Tutar (â‚º)</th>
                                      <th class="px-6 py-4 font-bold text-xs">Son Ã–deme</th>
                                      <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                      <th class="px-6 py-4 text-right">Aksiyonlar</th>
                                  </tr>
                              </thead>
                              <tbody id="taxes-table-body" class="text-sm">
                              </tbody>
                          </table>
                      </div>
                  </div>
              </section>
  
              <!-- ========================================== -->
              <!-- MAINTENANCE SECTÄ°ON -->
              <section id="maintenance-section" class="flex flex-col h-full bg-white hidden">
                  <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                      <div class="flex justify-between items-end">
                          <div class="space-y-1">
                              <h2 class="text-2xl font-serif font-bold text-navy">BakÄ±m & OnarÄ±m Talepleri</h2>
                              <p class="text-sm text-gray-500">KiracÄ± veya mÃ¼lk sahibi tarafÄ±ndan aÃ§Ä±lan teknik de
stek ve
                                  tadilat talepleri.</p>
                          </div>
                          <button onclick="openMaintenanceModal()"
                              class="bg-navy hover:bg-slate-800 text-white font-bold py-3 px-6 rounded-lg transition-al
l shadow-xl uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                              <i class="fa-solid fa-screwdriver-wrench text-gold"></i> Talep OluÅŸtur
                          </button>
                      </div>
                  </div>
  
                  <div class="flex-1 overflow-auto p-8 relative">
                      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                          <table class="w-full text-left premium-table">
                              <thead>
                                  <tr>
                                      <th class="px-6 py-4 font-bold text-xs">Talep No</th>
                                      <th class="px-6 py-4 font-bold text-xs">PortfÃ¶y</th>
                                      <th class="px-6 py-4 font-bold text-xs">Talep Veren</th>
                                      <th class="px-6 py-4 font-bold text-xs">Tarih</th>
                                      <th class="px-6 py-4 font-bold text-xs">AÃ§Ä±klama Ã–zeti</th>
                                      <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                      <th class="px-6 py-4 text-right">Cevapla</th>
                                  </tr>
                              </thead>
                              <tbody id="maintenance-table-body" class="text-sm">
                              </tbody>
                          </table>
                      </div>
                  </div>
              </section>
  
              <!-- ========================================== -->
              <!-- APPOINTMENTS SECTÄ°ON -->
              <section id="appointments-section" class="flex flex-col h-full bg-white hidden">
                  <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                      <div class="flex justify-between items-end">
                          <div class="space-y-1">
                              <h2 class="text-2xl font-serif font-bold text-navy">Randevular ve KeÅŸifler</h2>
                              <p class="text-sm text-gray-500">OluÅŸturulan gÃ¶sterim randevularÄ±nÄ± onaylayÄ±n ve tak
ip edin.
                              </p>
                          </div>
                          <button onclick="openAppointmentModal()"
                              class="bg-navy border border-gold hover:bg-slate-800 text-gold font-bold py-3 px-6 rounde
d-lg transition-all uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                              <i class="fa-regular fa-calendar-plus"></i> Manuel Randevu
                          </button>
                      </div>
                  </div>
  
                  <div class="flex-1 overflow-auto p-8 relative">
                      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                          <table class="w-full text-left premium-table">
                              <thead>
                                  <tr>
                                      <th class="px-6 py-4 font-bold text-xs">ID</th>
                                      <th class="px-6 py-4 font-bold text-xs">MÃ¼lk (PortfÃ¶y)</th>
                                      <th class="px-6 py-4 font-bold text-xs">Talep Sahibi</th>
                                      <th class="px-6 py-4 font-bold text-xs">Tarih / Saat</th>
                                      <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                      <th class="px-6 py-4 text-right">Aksiyonlar</th>
                                  </tr>
                              </thead>
                              <tbody id="appointments-table-body" class="text-sm">
                              </tbody>
                          </table>
                      </div>
                  </div>
              </section>
          </main>
      </div>
  
      <!-- SCRIPTS -->
>     <script>
          const API_BASE = '/api';
          // Wizard state - declared at top to avoid TDZ errors
          let currentWizStep = 1;
          const totalWizSteps = 4;
  
          // Sayfa yÃ¼klendiÄŸinde token kontrolÃ¼
          document.addEventListener('DOMContentLoaded', () => {
              const token = localStorage.getItem('imza_admin_token');
              const role = localStorage.getItem('imza_admin_role');
  
              if (token) {
                  // Ã–nceden giriÅŸ yapÄ±lmÄ±ÅŸsa direkt app'i gÃ¶ster
                  document.getElementById('login-section').classList.add('hidden');
  
                  const appNode = document.getElementById('portal-app');
                  appNode.classList.remove('hidden');
                  appNode.classList.add('show-app');
  
                  document.getElementById('sidebar-user-role').innerText = role;
                  // Ä°lk verileri Ã§ek
                  fetchPortfoliosForDashboard();
              }
          });
  
          // MenÃ¼ Gezinme MantÄ±ÄŸÄ±
          function showSection(sectionId, element) {
              // TÃ¼m sectionlarÄ± gizle
              document.querySelectorAll('.content-section').forEach(sec => {
                  sec.classList.add('hidden');
              });
              // Ä°lgili sectionÄ± gÃ¶ster (animasyonlu)
              const activeSection = document.getElementById(sectionId + '-section');
              activeSection.classList.remove('hidden');
              activeSection.classList.add('fade-in');
  
              // MenÃ¼ aktif durumunu gÃ¼ncelle
              document.querySelectorAll('.nav-item').forEach(btn => {
                  btn.classList.remove('active');
              });
              element.classList.add('active');
  
              // BaÅŸlÄ±ÄŸÄ± gÃ¼ncelle
              const titleHtml = element.innerHTML;
              document.getElementById('page-title').innerHTML = titleHtml.replace(/<span.*<\/span>/, ''); // Badge'i ba
ÅŸlÄ±ktan Ã§Ä±kar
  
              // EÄŸer portfolio tÄ±klandÄ±ysa tÃ¼m listeyi Ã§ek (basit versiyon)
              if (sectionId === 'portfolios') {
                  fetchAllPortfolios();
              }
  
              // Finans sekmesi tÄ±klandÄ±ysa hesaplayÄ±cÄ±yÄ± init et
              if (sectionId === 'taxes') {
                  initTcmbCalculator();
              }
          }
  
          // Login Ä°ÅŸlemi
          async function login() {
              const usernameInput = document.getElementById('username').value;
              const passwordInput = document.getElementById('password').value;
              const errorMsg = document.getElementById('login-error');
  
              try {
                  const response = await fetch(`${API_BASE}/login`, {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ username: usernameInput, password: passwordInput })
                  });
  
                  if (response.ok) {
                      const data = await response.json();
                      localStorage.setItem('imza_admin_token', data.token);
                      localStorage.setItem('imza_admin_role', data.role);
  
                      document.getElementById('sidebar-user-role').innerText = data.role;
  
                      // GiriÅŸ animasyonu
                      const loginSection = document.getElementById('login-section');
                      loginSection.style.opacity = '0';
  
                      setTimeout(() => {
                          loginSection.classList.add('hidden');
                          loginSection.style.opacity = '1';
  
                          const appNode = document.getElementById('portal-app');
                          appNode.classList.remove('hidden');
                          appNode.classList.add('show-app');
  
                          // MenÃ¼leri vs slide-up animasyonuyla baÅŸlat
                          document.querySelectorAll('.nav-item').forEach((item, index) => {
                              item.style.animation = `slideUp 0.5s ease forwards ${index * 0.1}s`;
                              item.style.opacity = '0';
                              item.style.transform = 'translateY(15px)';
                          });
  
                          fetchPortfoliosForDashboard();
                      }, 700);
  
                  } else {
                      errorMsg.classList.remove('hidden');
                      setTimeout(() => errorMsg.classList.add('hidden'), 3000);
                  }
              } catch (err) {
                  console.error("Login hatasÄ±:", err);
                  errorMsg.innerText = "Sunucuya baÄŸlanÄ±lamadÄ±.";
                  errorMsg.classList.remove('hidden');
              }
          }
  
          function logout() {
              localStorage.removeItem('imza_admin_token');
              localStorage.removeItem('imza_admin_role');
              document.getElementById('portal-app').classList.add('hidden');
              document.getElementById('login-section').classList.remove('hidden');
              document.getElementById('username').value = '';
              document.getElementById('password').value = '';
          }
  
          // Dashboard iÃ§in son portfÃ¶yleri Ã§ekme Ã¶rneÄŸi
          async function fetchPortfoliosForDashboard() {
              try {
                  const res = await fetch(`${API_BASE}/portfoyler`);
                  const data = await res.json();
  
                  const tableBody = document.getElementById('dashboard-portfolio-list');
                  tableBody.innerHTML = '';
  
                  // Sadece ilk 3 tanesini alalÄ±m
                  const recent = data.slice(0, 3);
  
                  recent.forEach(item => {
                      tableBody.innerHTML += `
                          <tr class="border-b border-gray-50 last:border-0 hover:bg-gray-50 transition-colors">
                              <td class="py-3 px-4"><span class="bg-gray-100 text-gray-500 px-2 py-1 rounded text-xs fo
nt-mono font-bold">${item.refNo}</span></td>
                              <td class="py-3 px-4 font-medium text-navy">${item.baslik1} ${item.baslik2}</td>
                              <td class="py-3 px-4 text-gray-500">${item.lokasyon}</td>
                              <td class="py-3 px-4 font-bold text-slate-700">${item.fiyat}</td>
                          </tr>
                      `;
                  });
              } catch (err) {
                  console.error("PortfÃ¶yler alÄ±namadÄ±", err);
              }
          }
  
          // PortfÃ¶y listesini tam sayfada tablo olarak Ã§ekme
          async function fetchAllPortfolios() {
              try {
                  const res = await fetch(`${API_BASE}/portfoyler`);
                  const data = await res.json();
  
                  const tableBody = document.getElementById('portfolios-table-body');
                  tableBody.innerHTML = '';
  
                  data.forEach(item => {
                      const rowHtml = `
                          <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors group">
                              <td class="py-3 px-6">
                                  <div class="w-12 h-12 rounded bg-cover bg-center border border-gray-200" style="backg
round-image: url('${item.resim_hero}')"></div>
                              </td>
                              <td class="py-3 px-6"><span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs fo
nt-mono font-bold">${item.refNo}</span></td>
                              <td class="py-3 px-6"><span class="text-xs font-bold uppercase tracking-wider ${item.ozel
lik_renk}">${item.koleksiyon}</span></td>
                              <td class="py-3 px-6">
                                  <p class="font-bold text-navy leading-tight">${item.baslik1}</p>
                                  <p class="text-xs text-gray-500">${item.baslik2}</p>
                              </td>
                              <td class="py-3 px-6 font-bold text-slate-700">${item.fiyat}</td>
                              <td class="py-3 px-6 text-right">
                                  <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 tra
nsition-opacity">
                                      <button onclick='editPortfolio(${JSON.stringify(item).replace(/'/g, "&#39;")})' c
lass="w-8 h-8 rounded-full bg-blue-50 text-blue-500 hover:bg-blue-500 hover:text-white transition-colors" title="DÃ¼zen
le">
                                          <i class="fa-solid fa-pen text-xs"></i>
                                      </button>
                                      <button onclick="deletePortfolio('${item.id}')" class="w-8 h-8 rounded-full bg-re
d-50 text-red-500 hover:bg-red-500 hover:text-white transition-colors" title="Sil">
                                          <i class="fa-solid fa-trash text-xs"></i>
                                      </button>
                                  </div>
                              </td>
                          </tr>
                      `;
                      tableBody.innerHTML += rowHtml;
                  });
              } catch (err) {
                  console.error("Portfoyler alÄ±namadÄ±", err);
              }
          }
  
          // TCMB Hesap Makinesi Entegrasyonu
          let tcmbRateFetched = false;
  
          async function initTcmbCalculator() {
              if (tcmbRateFetched) return; // Zaten Ã§ekildiyse tekrar Ã§ekme
  
              const rateInput = document.getElementById('calc-rate');
              const dateInfo = document.getElementById('tcmb-date-info');
              const statusIndicator = document.querySelector('#taxes-section h3 + p span');
              const statusText = document.querySelector('#taxes-section h3 + p');
  
              try {
                  rateInput.value = "YÃ¼kleniyor...";
  
                  const response = await fetch(`${API_BASE}/tcmb-rates`);
                  const data = await response.json();
  
                  if (response.ok) {
                      // TCMB'den gelen faiz verisiÄ±llÄ±k tavan oranÄ±nÄ± ifade eder. 
                      // Ã–nceki implementasyonda sembolik olarak dÃ¼ÅŸÃ¼rmÃ¼ÅŸtÃ¼k, ancak artÄ±k yeni isolated class'Ä
±mÄ±z
                      // bunu "YÄ±llÄ±k TCMB OranÄ±" olarak kabul edip 3'lÃ¼ senaryoyu kendisi Ã¼retecek.
                      let resultRate = parseFloat(data.rate);
                      if (isNaN(resultRate)) {
                          resultRate = 42.00; // Fallback yÄ±llÄ±k enflasyon/faiz
                      }
  
                      rateInput.value = resultRate.toFixed(2);
                      dateInfo.innerText = `Son GÃ¼ncelleme: ${data.date} (YÄ±llÄ±k TCMB - %)`;
                      tcmbRateFetched = true;
  
                      // Status Indicator
                      statusIndicator.classList.remove('bg-green-500', 'animate-pulse');
                      statusIndicator.classList.add('bg-navy');
                      statusText.innerHTML = `<span class="w-2 h-2 rounded-full bg-navy mr-2"></span>TCMB Verisi Aktif`
;
  
                      calculateMortgage();
                  } else {
                      rateInput.value = "3.20"; // Hata durumunda varsayÄ±lan oran
                      dateInfo.innerText = "TCMB'ye ulaÅŸÄ±lamadÄ±. Manuel oran.";
                      calculateMortgage();
                  }
              } catch (error) {
                  console.error("TCMB Fetch Error:", error);
                  rateInput.value = "3.20";
                  dateInfo.innerText = "Offline mod. VarsayÄ±lan oran.";
                  calculateMortgage();
              }
          }
  
          /**
           * SAF FONKSÄ°YON/SINIF YAKLAÅIMI: MortgageCalculator 
           * LTV hesaplamasÄ±nÄ± ve 3'lÃ¼ faiz senaryolarÄ±nÄ± DIÅ dÃ¼nyadan izole hesaplar.
           */
          class MortgageCalculator {
              constructor(annualTcmbRate) {
                  this.annualTcmbRate = parseFloat(annualTcmbRate);
                  if (isNaN(this.annualTcmbRate) || this.annualTcmbRate <= 0) {
                      this.annualTcmbRate = 42.0; // Temel varsayilan
                  }
  
                  // Ä°yimser (Taban Oran) = TCMB YÄ±llÄ±k / 12 (AylÄ±k yÃ¼zde olarak)
                  this.optimisticRatePct = this.annualTcmbRate / 12;
                  // KÃ¶tÃ¼mser = Ä°yimser * 1.7
                  this.pessimisticRatePct = this.optimisticRatePct * 1.7;
                  // GerÃ§ekÃ§i = OrtalamasÄ±
                  this.realisticRatePct = (this.optimisticRatePct + this.pessimisticRatePct) / 2;
              }
  
              getLtvRatio(expertiseValue, energyClass) {
                  let ratioList;
                  if (expertiseValue <= 5000000) {
                      ratioList = [0.90, 0.80, 0.70];
                  } else if (expertiseValue <= 7000000) {
                      ratioList = [0.80, 0.70, 0.60];
                  } else if (expertiseValue <= 10000000) {
                      ratioList = [0.70, 0.60, 0.50];
                  } else if (expertiseValue <= 20000000) {
                      ratioList = [0.50, 0.40, 0.30];
                  } else { // > 20M
                      ratioList = [0.40, 0.30, 0.20];
                  }
  
                  if (energyClass === 'A-B') return ratioList[0];
                  if (energyClass === 'C') return ratioList[1];
                  return ratioList[2];
              }
  
              calculateScenarios(expertiseValue, requestedAmount, termMonths, energyClass, isSecondTitleDeed) {
                  let ltv = this.getLtvRatio(expertiseValue, energyClass);
  
                  if (isSecondTitleDeed) {
                      ltv = ltv * 0.25; // %75 dÃ¼ÅŸÃ¼r, %25 al
                  }
  
                  const maxAllowedLoan = expertiseValue * ltv;
  
                  if (requestedAmount > maxAllowedLoan) {
                      return {
                          status: "REJECTED",
                          maxAllowedLoan: maxAllowedLoan,
                          ltvRatio: ltv
                      };
                  }
  
                  const scenarios = {
                      optimistic: this.calcInstallments(requestedAmount, termMonths, this.optimisticRatePct),
                      realistic: this.calcInstallments(requestedAmount, termMonths, this.realisticRatePct),
                      pessimistic: this.calcInstallments(requestedAmount, termMonths, this.pessimisticRatePct)
                  };
  
                  return {
                      status: "APPROVED",
                      maxAllowedLoan: maxAllowedLoan,
                      ltvRatio: ltv,
                      scenarios: scenarios
                  };
              }
  
              calcInstallments(amount, months, monthlyRatePct) {
                  const r = monthlyRatePct / 100;
                  const compound = Math.pow(1 + r, months);
                  let monthlyPayment = 0;
                  if (r > 0) {
                      monthlyPayment = amount * r * compound / (compound - 1);
                  } else {
                      monthlyPayment = amount / months;
                  }
                  return {
                      ratePct: monthlyRatePct,
                      monthlyPayment: monthlyPayment,
                      totalPayment: monthlyPayment * months
                  };
              }
          }
  
          let currentMortgageCalculator = null;
  
          function calculateMortgage() {
              const expertiseValue = parseFloat(document.getElementById('calc-expertise').value);
              const energyClass = document.getElementById('calc-energy').value;
              const isSecondTitleDeed = document.getElementById('calc-second-title').value === 'Evet';
              const requestedAmount = parseFloat(document.getElementById('calc-amount').value);
              const months = parseInt(document.getElementById('calc-term').value);
              const rateStr = document.getElementById('calc-rate').value;
  
              if (!expertiseValue || !requestedAmount || !months || rateStr === "YÃ¼kleniyor...") return;
  
              const tcmbAnnualRate = parseFloat(rateStr);
              if (isNaN(tcmbAnnualRate)) return;
  
              if (!currentMortgageCalculator || currentMortgageCalculator.annualTcmbRate !== tcmbAnnualRate) {
                  currentMortgageCalculator = new MortgageCalculator(tcmbAnnualRate);
              }
  
              const result = currentMortgageCalculator.calculateScenarios(expertiseValue, requestedAmount, months, ener
gyClass, isSecondTitleDeed);
  
              const resultsContainer = document.getElementById('calc-results-container');
              const rejectedContainer = document.getElementById('calc-rejected-container');
  
              if (result.status === "REJECTED") {
                  resultsContainer.classList.add('hidden');
                  rejectedContainer.classList.remove('hidden');
  
                  document.getElementById('rej-ltv').innerText = (result.ltvRatio * 100).toFixed(0);
                  document.getElementById('rej-max-loan').innerText = formatCurrency(result.maxAllowedLoan);
              } else {
                  rejectedContainer.classList.add('hidden');
                  resultsContainer.classList.remove('hidden');
  
                  document.getElementById('res-ltv').innerText = "%" + (result.ltvRatio * 100).toFixed(0);
  
                  // Opt
                  document.getElementById('res-opt-rate').innerText = result.scenarios.optimistic.ratePct.toFixed(2);
                  document.getElementById('res-opt-monthly').innerText = formatCurrency(result.scenarios.optimistic.mon
thlyPayment);
                  document.getElementById('res-opt-total').innerText = formatCurrency(result.scenarios.optimistic.total
Payment);
  
                  // Real
                  document.getElementById('res-real-rate').innerText = result.scenarios.realistic.ratePct.toFixed(2);
                  document.getElementById('res-real-monthly').innerText = formatCurrency(result.scenarios.realistic.mon
thlyPayment);
                  document.getElementById('res-real-total').innerText = formatCurrency(result.scenarios.realistic.total
Payment);
  
                  // Pes
                  document.getElementById('res-pes-rate').innerText = result.scenarios.pessimistic.ratePct.toFixed(2);
                  document.getElementById('res-pes-monthly').innerText = formatCurrency(result.scenarios.pessimistic.mo
nthlyPayment);
                  document.getElementById('res-pes-total').innerText = formatCurrency(result.scenarios.pessimistic.tota
lPayment);
              }
          }
  
          function formatCurrency(value) {
              return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY', maximumFractionDigits: 0 }).f
ormat(value);
          }
  
          // ==========================================
          // HERO CMS (SLÄ°DER YÃ–NETÄ°MÄ°) JS MANTIÄI
          // ==========================================
  
          async function fetchHeroSlides() {
              try {
                  const res = await fetch(`${API_BASE}/hero`);
                  const data = await res.json();
  
                  const tableBody = document.getElementById('hero-table-body');
                  tableBody.innerHTML = '';
  
                  if (data.length === 0) {
                      tableBody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-gray-400">HenÃ¼z slayt ek
lenmedi.</td></tr>';
                      return;
                  }
  
                  data.forEach(item => {
                      const rowHtml = `
                          <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors group">
                              <td class="py-4 px-6 font-bold text-navy">${item.sira}</td>
                              <td class="py-4 px-6">
                                  <div class="w-24 h-12 rounded bg-cover bg-center border border-gray-200" style="backg
round-image: url('${item.resim_url}')"></div>
                              </td>
                              <td class="py-4 px-6"><span class="bg-gold/10 text-gold px-2 py-1 rounded text-[10px] fon
t-bold uppercase tracking-wider">${item.alt_baslik}</span></td>
                              <td class="py-4 px-6">
                                  <p class="font-bold text-navy text-xs mb-1">${item.baslik_satir1}</p>
                                  <p class="text-xs text-gold font-serif italic">${item.baslik_satir2}</p>
                              </td>
                              <td class="py-4 px-6"><span class="text-xs text-gray-500 font-mono">${item.buton2_link}</
span></td>
                              <td class="py-4 px-6 text-right">
                                  <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 tra
nsition-opacity">
                                      <button onclick='editHeroSlide(${JSON.stringify(item).replace(/'/g, "&#39;")})' c
lass="w-8 h-8 rounded-full bg-blue-50 text-blue-500 hover:bg-blue-500 hover:text-white transition-colors" title="DÃ¼zen
le">
                                          <i class="fa-solid fa-pen text-xs"></i>
                                      </button>
                                      <button onclick="deleteHeroSlide(${item.id})" class="w-8 h-8 rounded-full bg-red-
50 text-red-500 hover:bg-red-500 hover:text-white transition-colors" title="Sil">
                                          <i class="fa-solid fa-trash text-xs"></i>
                                      </button>
                                  </div>
                              </td>
                          </tr>
                      `;
                      tableBody.innerHTML += rowHtml;
                  });
              } catch (err) {
                  console.error("Slaytlar alÄ±namadÄ±", err);
              }
          }
  
          // Modal YÃ¶netimi & Glassmorphic Slide-Over
          function openHeroModal(editData = null) {
              const backdrop = document.getElementById('hero-modal-backdrop');
              const modal = document.getElementById('hero-slide-over');
              const title = document.getElementById('hero-modal-title');
  
              // EÄŸer edit modundaysa formu doldur
              if (editData) {
                  title.innerText = "Slayt DÃ¼zenle";
                  document.getElementById('hero-id').value = editData.id;
                  document.getElementById('hero-img').value = editData.resim_url;
                  document.getElementById('hero-sira').value = editData.sira;
                  document.getElementById('hero-alt').value = editData.alt_baslik;
                  document.getElementById('hero-title1').value = editData.baslik_satir1;
                  document.getElementById('hero-title2').value = editData.baslik_satir2;
                  document.getElementById('hero-btn2').value = editData.buton2_metin;
                  document.getElementById('hero-target').value = editData.buton2_link;
                  updateImagePreview(editData.resim_url);
              } else {
                  title.innerText = "Yeni Slide Ekle";
                  document.getElementById('hero-id').value = "";
                  document.getElementById('hero-img').value = "";
                  document.getElementById('hero-sira').value = "0";
                  document.getElementById('hero-alt').value = "";
                  document.getElementById('hero-title1').value = "";
                  document.getElementById('hero-title2').value = "";
                  document.getElementById('hero-btn2').value = "";
                  document.getElementById('hero-target').value = "";
                  updateImagePreview("");
              }
  
              backdrop.classList.remove('hidden');
              // Timeout ile css transition'Ä± tetikle
              setTimeout(() => {
                  backdrop.classList.remove('opacity-0');
                  modal.classList.remove('translate-x-full');
              }, 10);
          }
  
          function closeHeroModal() {
              const backdrop = document.getElementById('hero-modal-backdrop');
              const modal = document.getElementById('hero-slide-over');
  
              backdrop.classList.add('opacity-0');
              modal.classList.add('translate-x-full');
  
              // Animasyon bittikten sonra gizle
              setTimeout(() => {
                  backdrop.classList.add('hidden');
              }, 500);
          }
  
          function editHeroSlide(data) {
              openHeroModal(data);
          }
  
          // CanlÄ± Resim Ã–nizleme
          document.getElementById('hero-img').addEventListener('input', function (e) {
              updateImagePreview(e.target.value);
          });
  
          function updateImagePreview(url) {
              const preview = document.getElementById('hero-img-preview');
              if (url && url.length > 5) {
                  preview.style.backgroundImage = `url('${url}')`;
                  preview.classList.remove('hidden');
              } else {
                  preview.classList.add('hidden');
              }
          }
  
          async function saveHeroSlide() {
              const id = document.getElementById('hero-id').value;
              const data = {
                  resim_url: document.getElementById('hero-img').value,
                  sira: parseInt(document.getElementById('hero-sira').value) || 0,
                  alt_baslik: document.getElementById('hero-alt').value,
                  baslik_satir1: document.getElementById('hero-title1').value,
                  baslik_satir2: document.getElementById('hero-title2').value,
                  buton1_metin: "DetaylÄ± Arama Yap", // Sabit kalÄ±yor
                  buton2_metin: document.getElementById('hero-btn2').value,
                  buton2_link: document.getElementById('hero-target').value
              };
  
              const method = id ? 'PUT' : 'POST';
              const url = id ? `${API_BASE}/hero/${id}` : `${API_BASE}/hero`;
  
              try {
                  const res = await fetch(url, {
                      method: method,
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify(data)
                  });
                  if (res.ok) {
                      closeHeroModal();
                      fetchHeroSlides();
                  } else {
                      alert("Slayt kaydedilirken bir hata oluÅŸtu.");
                  }
              } catch (err) {
                  console.error("Fetch HatasÄ±", err);
              }
          }
  
          async function deleteHeroSlide(id) {
              if (confirm("Bu slide'Ä± silmek istediÄŸinize emin misiniz?")) {
                  try {
                      const res = await fetch(`${API_BASE}/hero/${id}`, { method: 'DELETE' });
                      if (res.ok) {
                          fetchHeroSlides();
                      } else {
                          alert("Silme baÅŸarÄ±sÄ±z.");
                      }
                  } catch (err) {
                      console.error("Silme HatasÄ±", err);
                  }
              }
          }
  
          // BÃ¶lÃ¼m gÃ¶sterme fonksiyonuna Hero sekmesini inject edelim
          const originalShowSection = showSection;
          showSection = function (sectionId, btnElement) {
              originalShowSection(sectionId, btnElement);
              if (sectionId === 'hero') {
                  fetchHeroSlides();
              }
          }
  
  
          // ==========================================
          // YENÄ° WIZARD: PORTFOLIO CMS JS MANTIÄI
          // ==========================================
  
          function renderInspectionChecklists(mulk_tipi) {
              const container = document.getElementById('dynamic-inspection-container');
              container.innerHTML = '';
  
              let groupKey = "Grup_1"; // Default Konut
              if (mulk_tipi === "Ticari" || mulk_tipi === "EndÃ¼striyel") groupKey = "Grup_2";
              if (mulk_tipi === "Arsa" || mulk_tipi === "Arazi") groupKey = "Grup_3";
  
              if (!typeof inspectionData !== 'undefined' && inspectionData[groupKey]) {
                  const group = inspectionData[groupKey];
                  let html = `<p class="text-[10px] text-gray-500 mb-4 bg-gray-100 p-2 rounded">Denetim Grubu: <b>${gro
up.title}</b></p>`;
  
                  group.categories.forEach((cat, cIdx) => {
                      html += `<div class="mb-6 border-l-2 border-gold pl-3">`;
                      html += `<h4 class="text-xs font-bold text-navy mb-3">${cat.name}</h4>`;
  
                      cat.questions.forEach((q, qIdx) => {
                          const qId = `q_${groupKey}_${cIdx}_${qIdx}`;
                          html += `
                          <div class="mb-3 p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-gold/30 transi
tion-colors">
                              <p class="text-[10px] font-medium text-gray-700 mb-2">${q}</p>
                              <div class="flex gap-2">
                                  <label class="cursor-pointer group flex items-center justify-center bg-green-50 hover
:bg-green-100 border border-green-200 rounded px-2 py-1 flex-1">
                                      <input type="radio" name="${qId}" value="1" class="hidden peer">
                                      <span class="text-[9px] font-bold text-green-700 peer-checked:bg-green-600 peer-c
hecked:text-white px-2 py-1 rounded w-full text-center transition-all">Ä°yi (1)</span>
                                  </label>
                                  <label class="cursor-pointer group flex items-center justify-center bg-yellow-50 hove
r:bg-yellow-100 border border-yellow-200 rounded px-2 py-1 flex-1">
                                      <input type="radio" name="${qId}" value="2" class="hidden peer">
                                      <span class="text-[9px] font-bold text-yellow-700 peer-checked:bg-yellow-500 peer
-checked:text-white px-2 py-1 rounded w-full text-center transition-all">BakÄ±m (2)</span>
                                  </label>
                                  <label class="cursor-pointer group flex items-center justify-center bg-red-50 hover:b
g-red-100 border border-red-200 rounded px-2 py-1 flex-1">
                                      <input type="radio" name="${qId}" value="3" class="hidden peer">
                                      <span class="text-[9px] font-bold text-red-700 peer-checked:bg-red-600 peer-check
ed:text-white px-2 py-1 rounded w-full text-center transition-all">Risk (3)</span>
                                  </label>
                                  <label class="cursor-pointer group flex items-center justify-center bg-gray-100 hover
:bg-gray-200 border border-gray-200 rounded px-2 py-1 flex-1">
                                      <input type="radio" name="${qId}" value="0" class="hidden peer" checked>
                                      <span class="text-[9px] font-bold text-gray-500 peer-checked:bg-gray-500 peer-che
cked:text-white px-2 py-1 rounded w-full text-center transition-all">Bilinmiyor (0)</span>
                                  </label>
                              </div>
                          </div>
                          `;
                      });
                      html += `</div>`;
                  });
                  container.innerHTML = html;
              } else {
                  container.innerHTML = '<p class="text-xs text-red-500">Denetim verisi bulunamadÄ±.</p>';
              }
          }
  
          // Collect answers from generated radio buttons
          function collectInspectionData() {
              const container = document.getElementById('dynamic-inspection-container');
              const inputs = container.querySelectorAll('input[type="radio"]:checked');
              const result = {};
              inputs.forEach(input => {
                  const questionText = input.closest('.mb-3').querySelector('p').innerText;
                  result[questionText] = input.value;
              });
              return result;
          }
  
          function restoreInspectionData(mulk_tipi, jsonStr) {
              renderInspectionChecklists(mulk_tipi);
              if (!jsonStr) return;
              try {
                  const answers = JSON.parse(jsonStr);
                  const container = document.getElementById('dynamic-inspection-container');
                  const pElements = container.querySelectorAll('p.text-\[10px\]');
                  pElements.forEach(p => {
                      const qText = p.innerText;
                      if (answers[qText] !== undefined) {
                          const val = answers[qText];
                          const inputs = p.parentElement.querySelectorAll(`input[value="${val}"]`);
                          if (inputs.length > 0) inputs[0].checked = true;
                      }
                  });
              } catch (e) { console.warn("Restore error", e); }
          }
  
          // --- UPLOAD MANTIÄI ---
          async function handleImageUpload(inputId, hiddenUrlId, previewId) {
              const fileInput = document.getElementById(inputId);
              const file = fileInput.files[0];
              if (!file) return;
  
              const token = localStorage.getItem('imza_admin_token');
              const formData = new FormData();
              formData.append('image', file);
  
              const label = document.getElementById(inputId + '-label');
              label.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> YÃ¼kleniyor...`;
  
              try {
                  const res = await fetch(`${API_BASE}/upload-image`, {
                      method: 'POST',
                      headers: { 'Authorization': `Bearer ${token}` },
                      body: formData
                  });
                  if (res.ok) {
                      const data = await res.json();
                      document.getElementById(hiddenUrlId).value = data.url;
                      document.getElementById(previewId).src = data.url;
                      document.getElementById(previewId).classList.remove('hidden');
                      label.innerHTML = `<i class="fa-solid fa-check text-green-500"></i> YÃ¼klendi!`;
                  } else {
                      alert("YÃ¼kleme baÅŸarÄ±sÄ±z oldu.");
                      label.innerHTML = `Tekrar Dene`;
                  }
              } catch (e) {
                  console.error("Upload error", e);
                  label.innerHTML = `Hata OluÅŸtu`;
              }
          }
  
  
          function updateWizUI() {
              for (let i = 1; i <= totalWizSteps; i++) {
                  const stepDiv = document.getElementById(`wiz-step-${i}`);
                  if (!stepDiv) continue;
  
                  // Indicators
                  const ind = document.getElementById(`step-ind-${i}`);
                  if (ind) {
                      if (i <= currentWizStep) {
                          ind.classList.remove('bg-gray-200');
                          ind.classList.add('bg-gold');
                      } else {
                          ind.classList.add('bg-gray-200');
                          ind.classList.remove('bg-gold');
                      }
                  }
  
                  if (i === currentWizStep) {
                      stepDiv.classList.remove('hidden');
                      // Gecikmeli opacity
                      setTimeout(() => {
                          stepDiv.classList.remove('opacity-0', 'translate-x-[10px]', 'pointer-events-none');
                          stepDiv.classList.add('opacity-100', 'translate-x-0');
                      }, 50);
                  } else {
                      stepDiv.classList.add('opacity-0', 'translate-x-[10px]', 'pointer-events-none');
                      // Animasyon bitince display none yapÄ±p akÄ±ÅŸÄ± rahatlat
                      setTimeout(() => {
                          if (i !== currentWizStep) stepDiv.classList.add('hidden');
                      }, 300);
                  }
              }
  
              const prevBtn = document.getElementById('wiz-prev-btn');
              const nextBtn = document.getElementById('wiz-next-btn');
              const saveBtn = document.getElementById('wiz-save-btn');
  
              if (currentWizStep === 1) {
                  prevBtn.classList.add('hidden');
              } else {
                  prevBtn.classList.remove('hidden');
              }
  
              if (currentWizStep === totalWizSteps) {
                  nextBtn.classList.add('hidden');
                  saveBtn.classList.remove('hidden');
              } else {
                  nextBtn.classList.remove('hidden');
                  saveBtn.classList.add('hidden');
              }
          }
  
          function wizNext() {
              if (currentWizStep === 2) {
                  const tip = document.getElementById('pf-mulktipi').value;
                  renderInspectionChecklists(tip);
              }
              if (currentWizStep < totalWizSteps) {
                  currentWizStep++;
                  updateWizUI();
              }
          }
  
          function wizPrev() {
              if (currentWizStep > 1) {
                  currentWizStep--;
                  updateWizUI();
              }
          }
  
          function openPortfolioModal(editData = null) {
              const backdrop = document.getElementById('portfolio-modal-backdrop');
              const modal = document.getElementById('portfolio-slide-over');
              const title = document.getElementById('portfolio-modal-title');
  
              currentWizStep = 1;
  
              if (editData) {
                  title.innerText = "PortfÃ¶y DÃ¼zenle";
                  document.getElementById('pf-id').value = editData.id;
                  document.getElementById('pf-id').disabled = true;
  
                  document.getElementById('pf-mulktipi').value = editData.mulk_tipi || 'Konut';
                  document.getElementById('pf-koleksiyon').value = editData.koleksiyon;
                  document.getElementById('pf-baslik1').value = editData.baslik1;
                  document.getElementById('pf-baslik2').value = editData.baslik2;
                  document.getElementById('pf-lokasyon').value = editData.lokasyon;
                  document.getElementById('pf-refno').value = editData.refNo;
                  document.getElementById('pf-fiyat').value = editData.fiyat;
  
                  document.getElementById('pf-oda').value = editData.oda;
                  document.getElementById('pf-alan').value = editData.alan;
                  document.getElementById('pf-kat').value = editData.kat;
  
                  document.getElementById('pf-icon-renk').value = editData.icon_renk;
                  document.getElementById('pf-resim-hero').value = editData.resim_hero;
                  document.getElementById('pf-resim-hikaye').value = editData.resim_hikaye;
                  document.getElementById('pf-hikaye').value = editData.hikaye;
  
                  document.getElementById('pf-ozellikler').value = editData.ozellikler ? editData.ozellikler.join(', ')
 : '';
  
                  document.getElementById('pf-danisman-isim').value = editData.danisman_isim;
                  document.getElementById('pf-danisman-unvan').value = editData.danisman_unvan;
                  document.getElementById('pf-danisman-resim').value = editData.danisman_resim;
  
                  restoreInspectionData(editData.mulk_tipi || 'Konut', editData.denetim_notlari);
              } else {
                  title.innerText = "Yeni Ä°lan Ekle (Sihirbaz)";
                  document.getElementById('portfolio-form').reset();
                  document.getElementById('pf-id').disabled = false;
                  document.getElementById('pf-id').value = `IMZ-${Math.floor(Math.random() * 1000)}`;
                  renderInspectionChecklists('Konut'); // Default render
  
                  // Reset Preview Images
                  document.getElementById('preview-hero').src = '';
                  document.getElementById('preview-hero').classList.add('hidden');
                  document.getElementById('pf-upload-hero-label').innerHTML = 'Yerel Dosya SeÃ§';
              }
  
              updateWizUI();
  
              backdrop.classList.remove('hidden');
              setTimeout(() => {
                  backdrop.classList.remove('opacity-0');
                  modal.classList.remove('translate-x-full');
              }, 10);
          }
  
          function closePortfolioModal() {
              const backdrop = document.getElementById('portfolio-modal-backdrop');
              const modal = document.getElementById('portfolio-slide-over');
  
              backdrop.classList.add('opacity-0');
              modal.classList.add('translate-x-full');
  
              setTimeout(() => {
                  backdrop.classList.add('hidden');
              }, 500);
          }
  
          function editPortfolio(data) {
              openPortfolioModal(data);
          }
  
          async function savePortfolio() {
              const token = localStorage.getItem('imza_admin_token');
              if (!token) return alert("Oturum sÃ¼reniz dolmuÅŸ, lÃ¼tfen tekrar giriÅŸ yapÄ±n.");
  
              const isEdit = document.getElementById('pf-id').disabled;
              const id = document.getElementById('pf-id').value;
              const ozelliklerStr = document.getElementById('pf-ozellikler').value;
              const ozellikler = ozelliklerStr.split(',').map(s => s.trim()).filter(s => s.length > 0);
              const denetimNotlari = collectInspectionData();
  
              const data = {
                  id: id,
                  mulk_tipi: document.getElementById('pf-mulktipi').value,
                  koleksiyon: document.getElementById('pf-koleksiyon').value,
                  baslik1: document.getElementById('pf-baslik1').value,
                  baslik2: document.getElementById('pf-baslik2').value,
                  lokasyon: document.getElementById('pf-lokasyon').value,
                  refNo: document.getElementById('pf-refno').value,
                  fiyat: document.getElementById('pf-fiyat').value,
  
                  oda: document.getElementById('pf-oda').value,
                  alan: document.getElementById('pf-alan').value,
                  kat: document.getElementById('pf-kat').value,
  
                  ozellik_renk: "text-gold",
                  bg_renk: "bg-navy",
                  btn_renk: "bg-gold hover:bg-yellow-600 shadow-gold/20",
                  icon_renk: document.getElementById('pf-icon-renk').value || "border-gold",
  
                  resim_hero: document.getElementById('pf-resim-hero').value,
                  resim_hikaye: document.getElementById('pf-resim-hikaye').value,
                  hikaye: document.getElementById('pf-hikaye').value,
                  ozellikler: ozellikler,
                  denetim_notlari: JSON.stringify(denetimNotlari),
  
                  danisman_isim: document.getElementById('pf-danisman-isim').value,
                  danisman_unvan: document.getElementById('pf-danisman-unvan').value,
                  danisman_resim: document.getElementById('pf-danisman-resim').value
              };
  
              const method = isEdit ? 'PUT' : 'POST';
              const url = isEdit ? `${API_BASE}/portfoyler/${id}` : `${API_BASE}/portfoyler`;
  
              try {
                  const res = await fetch(url, {
                      method: method,
                      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                      body: JSON.stringify(data)
                  });
                  if (res.ok) {
                      closePortfolioModal();
                      fetchAllPortfolios();
                      fetchPortfoliosForDashboard();
                  } else if (res.status === 403) {
                      alert("Yetkiniz yok.");
                  } else alert("Hata oluÅŸtu.");
              } catch (err) { console.error(err); }
          }
  
          async function deletePortfolio(id) {
              const token = localStorage.getItem('imza_admin_token');
              if (confirm(`Referens No: ${id} tamamen silinecek?`)) {
                  try {
                      const res = await fetch(`${API_BASE}/portfoyler/${id}`, {
                          method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                      });
                      if (res.ok) {
                          fetchAllPortfolios();
                          fetchPortfoliosForDashboard();
                      } else alert("Silme baÅŸarÄ±sÄ±z.");
                  } catch (err) { console.error(err); }
              }
          }
  
  
          // ==========================================
          // SÃ–ZLEÅMELER (CONTRACTS) JS MANTIÄI
          // ==========================================
          async function fetchContracts() {
              const token = localStorage.getItem('imza_admin_token');
              if (!token) return;
              try {
                  const res = await fetch(`${API_BASE}/contracts`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) {
                      const data = await res.json();
                      const tbody = document.getElementById('contracts-table-body');
                      tbody.innerHTML = '';
                      data.forEach(c => {
                          const tr = document.createElement('tr');
                          tr.className = 'border-b border-gray-100/50';
                          tr.innerHTML = `
                              <td class="px-6 py-4 font-medium text-navy">#${c.id}</td>
                              <td class="px-6 py-4">
                                  <span class="font-bold text-navy block">${c.baslik1 || 'Bilinmiyor'}</span>
                                  <span class="text-[10px] text-gray-400">${c.refNo || '-'}</span>
                              </td>
                              <td class="px-6 py-4">
                                  <span class="font-medium text-navy">${c.username || 'Sistem'}</span>
                                  <span class="text-[10px] text-gray-500 block uppercase">${c.role || '-'}</span>
                              </td>
                              <td class="px-6 py-4"><span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">$
{c.type}</span></td>
                              <td class="px-6 py-4 text-gray-600">${c.start_date.substring(0, 10)}</td>
                              <td class="px-6 py-4 font-medium text-modern">${c.end_date.substring(0, 10)}</td>
                              <td class="px-6 py-4 text-right">
                                  <button onclick="deleteContract(${c.id})" class="text-red-400 hover:text-red-500 tran
sition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                              </td>
                          `;
                          tbody.appendChild(tr);
                      });
                  }
              } catch (err) { console.error(err); }
          }
  
          async function deleteContract(id) {
              const token = localStorage.getItem('imza_admin_token');
              if (confirm('SÃ¶zleÅŸmeyi iptal etmek/silmek istediÄŸinize emin misiniz?')) {
                  const res = await fetch(`${API_BASE}/contracts/${id}`, {
                      method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) fetchContracts();
              }
          }
  
          function openContractModal() {
              alert('SÃ¶zleÅŸme Ekleme ModalÄ± YapÄ±m AÅŸamasÄ±nda.');
          }
  
          // ==========================================
          // VERGÄ° VE FÄ°NANS (TAXES) JS MANTIÄI
          // ==========================================
          async function fetchTaxes() {
              const token = localStorage.getItem('imza_admin_token');
              if (!token) return;
              try {
                  const res = await fetch(`${API_BASE}/taxes`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) {
                      const data = await res.json();
                      const tbody = document.getElementById('taxes-table-body');
                      tbody.innerHTML = '';
                      data.forEach(t => {
                          const isPaid = t.status === 'Ã–dendi';
                          const statusColor = isPaid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700';
                          const tr = document.createElement('tr');
                          tr.className = 'border-b border-gray-100/50';
                          tr.innerHTML = `
                              <td class="px-6 py-4 font-medium text-navy">#${t.id}</td>
                              <td class="px-6 py-4 font-bold text-navy">${t.baslik1 || '-'}</td>
                              <td class="px-6 py-4 text-gray-600">${t.tax_type}</td>
                              <td class="px-6 py-4 font-bold ${isPaid ? 'text-gray-800' : 'text-red-600'}">${t.amount.t
oLocaleString()} â‚º</td>
                              <td class="px-6 py-4 text-gray-600">${t.due_date.substring(0, 10)}</td>
                              <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${
t.status}</span></td>
                              <td class="px-6 py-4 text-right">
                                  <button onclick="deleteTax(${t.id})" class="text-red-400 hover:text-red-500 transitio
n-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                              </td>
                          `;
                          tbody.appendChild(tr);
                      });
                  }
              } catch (err) { console.error(err); }
          }
  
          async function deleteTax(id) {
              const token = localStorage.getItem('imza_admin_token');
              if (confirm('Vergi kaydÄ±nÄ± silmek istediÄŸinize emin misiniz?')) {
                  const res = await fetch(`${API_BASE}/taxes/${id}`, {
                      method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) fetchTaxes();
              }
          }
          function openTaxModal() { alert('Finans Ekleme ModalÄ± YapÄ±m AÅŸamasÄ±nda.'); }
  
          // ==========================================
          // BAKIM TALEPLERÄ° (MAINTENANCE) JS MANTIÄI
          // ==========================================
          async function fetchMaintenance() {
              const token = localStorage.getItem('imza_admin_token');
              if (!token) return;
              try {
                  const res = await fetch(`${API_BASE}/maintenance`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) {
                      const data = await res.json();
                      const tbody = document.getElementById('maintenance-table-body');
                      tbody.innerHTML = '';
                      data.forEach(m => {
                          let statusColor = 'bg-yellow-100 text-yellow-700';
                          if (m.status === 'Ã‡Ã¶zÃ¼ldÃ¼') statusColor = 'bg-green-100 text-green-700';
                          if (m.status === 'Ä°ptal') statusColor = 'bg-gray-100 text-gray-500';
  
                          const tr = document.createElement('tr');
                          tr.className = 'border-b border-gray-100/50';
                          tr.innerHTML = `
                              <td class="px-6 py-4 font-medium text-navy">#${m.id}</td>
                              <td class="px-6 py-4 font-bold text-navy">${m.baslik1 || '-'}</td>
                              <td class="px-6 py-4 text-gray-600">${m.username || 'Bilinmiyor'}</td>
                              <td class="px-6 py-4 text-gray-500">${m.request_date.substring(0, 10)}</td>
                              <td class="px-6 py-4 text-gray-800 text-xs max-w-xs truncate" title="${m.description}">${
m.description}</td>
                              <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${
m.status}</span></td>
                              <td class="px-6 py-4 text-right">
                                  <button onclick="deleteMaintenance(${m.id})" class="text-red-400 hover:text-red-500 t
ransition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                              </td>
                          `;
                          tbody.appendChild(tr);
                      });
                  }
              } catch (err) { console.error(err); }
          }
  
          async function deleteMaintenance(id) {
              const token = localStorage.getItem('imza_admin_token');
              if (confirm('Talebi silmek istediÄŸinize emin misiniz?')) {
                  const res = await fetch(`${API_BASE}/maintenance/${id}`, {
                      method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) fetchMaintenance();
              }
          }
          function openMaintenanceModal() { alert('BakÄ±m Talebi ModalÄ± YapÄ±m AÅŸamasÄ±nda.'); }
  
          // ==========================================
          // RANDEVULAR (APPOINTMENTS) JS MANTIÄI
          // ==========================================
          async function fetchAppointments() {
              const token = localStorage.getItem('imza_admin_token');
              if (!token) return;
              try {
                  const res = await fetch(`${API_BASE}/appointments`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) {
                      const data = await res.json();
                      const tbody = document.getElementById('appointments-table-body');
                      tbody.innerHTML = '';
                      data.forEach(a => {
                          let statusColor = 'bg-blue-100 text-blue-700';
                          if (a.status === 'TamamlandÄ±') statusColor = 'bg-green-100 text-green-700';
                          if (a.status === 'Ä°ptal') statusColor = 'bg-red-100 text-red-700';
  
                          const tr = document.createElement('tr');
                          tr.className = 'border-b border-gray-100/50';
                          tr.innerHTML = `
                              <td class="px-6 py-4 font-medium text-navy">#${a.id}</td>
                              <td class="px-6 py-4 font-bold text-navy">${a.baslik1 || '-'}</td>
                              <td class="px-6 py-4">
                                  <span class="text-navy font-bold block">${a.username || 'Bilinmiyor'}</span>
                                  <span class="text-[10px] text-gray-500">${a.phone || '-'}</span>
                              </td>
                              <td class="px-6 py-4 text-gray-600 font-medium">${a.date}</td>
                              <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${
a.status}</span></td>
                              <td class="px-6 py-4 text-right">
                                  <button onclick="deleteAppointment(${a.id})" class="text-red-400 hover:text-red-500 t
ransition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                              </td>
                          `;
                          tbody.appendChild(tr);
                      });
                  }
              } catch (err) { console.error(err); }
          }
  
          async function deleteAppointment(id) {
              const token = localStorage.getItem('imza_admin_token');
              if (confirm('Randevuyu iptal etmek istediÄŸinize emin misiniz?')) {
                  const res = await fetch(`${API_BASE}/appointments/${id}`, {
                      method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                  });
                  if (res.ok) fetchAppointments();
              }
          }
          function openAppointmentModal() { alert('Randevu ModalÄ± YapÄ±m AÅŸamasÄ±nda.'); }
  
          const originalShowSectionForModules = showSection;
          showSection = function (sectionId, btnElement) {
              originalShowSectionForModules(sectionId, btnElement);
              if (sectionId === 'contracts') fetchContracts();
              if (sectionId === 'taxes') fetchTaxes();
              if (sectionId === 'maintenance') fetchMaintenance();
              if (sectionId === 'appointments') fetchAppointments();
          }
  
          // ==========================================
          // SÃ–ZLEÅME HAZIRLAMA (CONTRACT BUILDER) JS
          // ==========================================
          var conWizStep = 1;
          var selectedProperty = null;
          var selectedTemplate = null;
          var selectedClauses = [];
          var allProperties = [];
  
          // BÃ¶lÃ¼m gÃ¶sterme fonksiyonunu geniÅŸletelim
          const finalShowSection = showSection;
          showSection = function (sectionId, element) {
              finalShowSection(sectionId, element);
              if (sectionId === 'contract-builder') {
                  initContractBuilder();
              }
          };
  
          async function initContractBuilder() {
              try {
                  console.log("initContractBuilder STARTED");
                  conWizStep = 1;
                  selectedProperty = null;
                  selectedTemplate = null;
                  selectedClauses = [];
                  if (document.getElementById('prop-search')) document.getElementById('prop-search').value = '';
                  console.log("calling updateConWizUI...");
                  updateConWizUI();
                  console.log("calling fetchPropertiesForContract...");
                  await fetchPropertiesForContract();
                  console.log("initContractBuilder FINISHED");
              } catch (e) {
                  console.error("Error in initContractBuilder:", e);
              }
          }
  
          async function fetchPropertiesForContract() {
              console.log("fetchPropertiesForContract START");
              try {
                  const res = await fetch(`${API_BASE}/portfoyler?_t=` + new Date().getTime());
                  allProperties = await res.json();
                  console.log("Fetched portfoyler count:", allProperties.length);
                  renderPropertyList(allProperties);
              } catch (err) {
                  console.error("MÃ¼lkler alÄ±namadÄ±", err);
              }
          }
  
          function renderPropertyList(list) {
              console.log("renderPropertyList START", list);
              const container = document.getElementById('prop-list');
              console.log("container element:", container);
              if (!container) return;
              container.innerHTML = '';
  
              if (list.length === 0) {
                  container.innerHTML = '<div class="text-center py-10 text-gray-400 border-2 border-dashed rounded-xl"
>SonuÃ§ bulunamadÄ±.</div>';
                  return;
              }
  
              list.forEach(p => {
                  const div = document.createElement('div');
                  div.className = `p-4 rounded-xl border border-gray-100 hover:border-gold hover:bg-gold/5 transition-a
ll cursor-pointer flex items-center justify-between group ${selectedProperty?.id === p.id ? 'border-gold bg-gold/5' : '
'}`;
                  div.onclick = () => selectPropertyForContract(p);
                  div.innerHTML = `
                      <div class="flex items-center gap-4">
                          <div class="w-12 h-12 rounded bg-cover bg-center border border-gray-100" style="background-im
age: url('${p.resim_hero}')"></div>
                          <div>
                              <p class="text-xs font-bold text-gray-400 font-mono">${p.refNo}</p>
                              <h4 class="font-bold text-navy group-hover:text-gold transition-colors">${p.baslik1}</h4>
                              <p class="text-[10px] text-gray-500">${p.lokasyon}</p>
                          </div>
                      </div>
                      <div class="text-right">
                          <p class="font-bold text-navy">${p.fiyat}</p>
                          <i class="fa-solid fa-chevron-right text-gray-300 group-hover:text-gold transition-all"></i>
                      </div>
                  `;
                  container.appendChild(div);
              });
          }
  
          function searchPropertiesForContract(val) {
              const filtered = allProperties.filter(p =>
                  p.baslik1.toLowerCase().includes(val.toLowerCase()) ||
                  p.refNo.toLowerCase().includes(val.toLowerCase())
              );
              renderPropertyList(filtered);
          }
  
          function selectPropertyForContract(p) {
              selectedProperty = p;
              renderPropertyList(allProperties);
              conWizNext();
          }
  
          async function fetchContractTemplates() {
              const token = localStorage.getItem('imza_admin_token');
              try {
                  const res = await fetch(`${API_BASE}/contract-templates`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                  });
                  const templates = await res.json();
                  const container = document.getElementById('template-list');
                  if (!container) return;
                  container.innerHTML = '';
  
                  templates.forEach(t => {
                      const div = document.createElement('div');
                      div.className = `p-6 rounded-2xl border border-gray-100 hover:border-gold hover:shadow-lg transit
ion-all cursor-pointer text-center group ${selectedTemplate?.id === t.id ? 'border-gold bg-gold/5' : ''}`;
                      div.onclick = () => selectTemplateForContract(t);
                      div.innerHTML = `
                          <div class="w-16 h-16 rounded-full bg-gray-50 flex items-center justify-center mx-auto mb-4 g
roup-hover:bg-gold/10 transition-colors">
                              <i class="fa-solid fa-file-lines text-2xl text-gray-400 group-hover:text-gold"></i>
                          </div>
                          <h4 class="font-bold text-navy text-sm">${t.name}</h4>
                          <p class="text-[10px] text-gray-500 mt-2">Bu ÅŸablonu kullanarak sÃ¶zleÅŸme maddelerini Ã¶zel
leÅŸtirin.</p>
                      `;
                      container.appendChild(div);
                  });
              } catch (err) {
                  console.error("Åablonlar alÄ±namadÄ±", err);
              }
          }
  
          function selectTemplateForContract(t) {
              selectedTemplate = t;
              fetchContractTemplates(); // Re-render to show selection
              conWizNext();
          }
  
          async function fetchClauses(templateId) {
              const token = localStorage.getItem('imza_admin_token');
              try {
                  const res = await fetch(`${API_BASE}/contract-templates/${templateId}/clauses`, {
                      headers: { 'Authorization': `Bearer ${token}` }
                  });
                  const clauses = await res.json();
                  const container = document.getElementById('clause-list');
                  if (!container) return;
                  container.innerHTML = '';
  
                  selectedClauses = clauses.filter(c => c.is_mandatory).map(c => c.id);
  
                  clauses.forEach(c => {
                      const div = document.createElement('div');
                      div.className = `p-4 rounded-xl border border-gray-100 flex items-start gap-4 transition-all ${c.
is_mandatory ? 'bg-gray-50 opacity-80' : 'hover:border-gold/30 cursor-pointer'}`;
                      if (!c.is_mandatory) div.onclick = () => toggleClause(c.id);
  
                      div.innerHTML = `
                          <div class="pt-1">
                              <input type="checkbox" id="clause-${c.id}" ${selectedClauses.includes(c.id) ? 'checked' :
 ''} ${c.is_mandatory ? 'disabled' : ''} class="w-4 h-4 rounded border-gray-300 text-gold focus:ring-gold">
                          </div>
                          <div class="flex-1">
                              <div class="flex items-center gap-2 mb-1">
                                  <h5 class="text-xs font-bold text-navy">${c.title}</h5>
                                  ${c.is_mandatory ? '<span class="text-[8px] bg-red-100 text-red-600 px-1.5 py-0.5 rou
nded font-bold uppercase">Zorunlu</span>' : ''}
                              </div>
                              <p class="text-[11px] text-gray-600 leading-relaxed">${c.content}</p>
                          </div>
                      `;
                      container.appendChild(div);
                  });
              } catch (err) {
                  console.error("Maddeler alÄ±namadÄ±", err);
              }
          }
  
          function toggleClause(id) {
              if (selectedClauses.includes(id)) {
                  selectedClauses = selectedClauses.filter(cid => cid !== id);
              } else {
                  selectedClauses.push(id);
              }
              const checkbox = document.getElementById(`clause-${id}`);
              if (checkbox) checkbox.checked = selectedClauses.includes(id);
          }
  
          function updateConWizUI() {
              // Steps
              document.querySelectorAll('.con-wiz-step').forEach((s, i) => {
                  const stepNum = i + 1;
                  const circle = s.querySelector('div');
                  const text = s.querySelector('span');
  
                  if (stepNum < conWizStep) {
                      circle.className = "w-10 h-10 rounded-full bg-gold text-white flex items-center justify-center fo
nt-bold border-4 border-white shadow-md transition-all";
                      circle.innerHTML = '<i class="fa-solid fa-check"></i>';
                      text.className = "text-[10px] font-bold uppercase tracking-wider text-gold";
                  } else if (stepNum === conWizStep) {
                      circle.className = "w-10 h-10 rounded-full bg-navy text-white flex items-center justify-center fo
nt-bold border-4 border-white shadow-md transition-all";
                      circle.innerHTML = stepNum;
                      text.className = "text-[10px] font-bold uppercase tracking-wider text-navy";
                  } else {
                      circle.className = "w-10 h-10 rounded-full bg-gray-200 text-gray-500 flex items-center justify-ce
nter font-bold border-4 border-white shadow-md transition-all";
                      circle.innerHTML = stepNum;
                      text.className = "text-[10px] font-bold uppercase tracking-wider text-gray-400";
                  }
              });
  
              // Progress Bar
              const progress = (conWizStep - 1) / 3 * 100;
              if (document.getElementById('con-wiz-progress')) document.getElementById('con-wiz-progress').style.width 
= `${progress}%`;
  
              // Content
              document.querySelectorAll('.con-wiz-content').forEach((c, i) => {
                  if (i + 1 === conWizStep) {
                      c.classList.remove('hidden');
                      c.classList.add('fade-in');
                  } else {
                      c.classList.add('hidden');
                  }
              });
  
              // Buttons
              const prevBtn = document.getElementById('con-prev-btn');
              const nextBtn = document.getElementById('con-next-btn');
              const saveBtn = document.getElementById('con-save-btn');
              if (!prevBtn || !nextBtn || !saveBtn) return;
  
              if (conWizStep === 1) {
                  prevBtn.classList.add('opacity-0', 'pointer-events-none');
              } else {
                  prevBtn.classList.remove('opacity-0', 'pointer-events-none');
              }
  
              if (conWizStep === 4) {
                  nextBtn.classList.add('hidden');
                  saveBtn.classList.remove('hidden');
                  renderContractPreview();
              } else {
                  nextBtn.classList.remove('hidden');
                  saveBtn.classList.add('hidden');
                  nextBtn.innerText = 'Ä°leri';
              }
          }
  
          async function conWizNext() {
              if (conWizStep === 1) {
                  if (!selectedProperty) {
                      alert("LÃ¼tfen bir mÃ¼lk seÃ§in."); return;
                  }
                  await fetchContractTemplates();
              }
              if (conWizStep === 2 && !selectedTemplate) {
                  alert("LÃ¼tfen bir ÅŸablon seÃ§in."); return;
              }
  
              if (conWizStep === 2) {
                  await fetchClauses(selectedTemplate.id);
              }
  
              if (conWizStep < 4) {
                  conWizStep++;
                  updateConWizUI();
              }
          }
  
          function conWizPrev() {
              if (conWizStep > 1) {
                  conWizStep--;
                  updateConWizUI();
              }
          }
  
          async function renderContractPreview() {
              const title = document.getElementById('preview-title');
              const info = document.getElementById('preview-property-info');
              const content = document.getElementById('preview-content');
              if (!title || !info || !content) return;
  
              title.innerText = selectedTemplate.name.toUpperCase();
              info.innerText = `${selectedProperty.refNo} - ${selectedProperty.baslik1} (${selectedProperty.lokasyon})`
;
  
              // Get clause texts
              try {
                  const res = await fetch(`${API_BASE}/contract-templates/${selectedTemplate.id}/clauses`);
                  const allClauses = await res.json();
                  const selectedOnes = allClauses.filter(c => selectedClauses.includes(c.id));
  
                  content.innerHTML = selectedOnes.map((c, i) => `
                      <div>
                          <h4 class="font-bold text-navy mb-1 underline">${i + 1}. ${c.title}</h4>
                          <p>${c.content.replace(/\n/g, '<br>')}</p>
                      </div>
                  `).join('');
              } catch (err) {
                  console.error("Ã–nizleme oluÅŸturulamadÄ±", err);
              }
          }
  
          async function savePreparedContract() {
              const token = localStorage.getItem('imza_admin_token');
              const payload = {
                  property_id: selectedProperty.id,
                  template_id: selectedTemplate.id,
                  selected_clauses: selectedClauses,
                  custom_data: {
                      generated_at: new Date().toISOString(),
                      property_ref: selectedProperty.refNo,
                      property_title: selectedProperty.baslik1
                  }
              };
  
              try {
                  const res = await fetch(`${API_BASE}/prepared-contracts`, {
                      method: 'POST',
                      headers: {
                          'Content-Type': 'application/json',
                          'Authorization': `Bearer ${token}`
                      },
                      body: JSON.stringify(payload)
                  });
  
                  if (res.ok) {
                      alert("SÃ¶zleÅŸme baÅŸarÄ±yla kaydedildi!");
                      showSection('contracts', document.querySelector('button[onclick*="contracts"]'));
                  } else {
                      alert("Kaydedilirken bir hata oluÅŸtu.");
                  }
              } catch (err) {
                  console.error("KayÄ±t hatasÄ±", err);
              }
          }
      </script>
      <script src="js/inspection-data.js"></script>
>     <script>
          const sidebar = document.getElementById('sidebar');
          const toggleBtn = document.getElementById('sidebar-toggle');
          toggleBtn.addEventListener('click', () => {
              sidebar.classList.toggle('-translate-x-full');
          });
      </script>
  </body>
  <div id="hero-modal-backdrop"
      class="fixed inset-0 bg-navy/60 backdrop-blur-sm z-40 hidden transition-opacity duration-300 opacity-0"
      onclick="closeHeroModal()"></div>
  
  <div id="hero-slide-over"
      class="fixed top-0 right-0 min-h-screen w-full max-w-md bg-white/95 backdrop-blur-xl shadow-2xl z-50 transform tr
anslate-x-full transition-transform duration-500 cubic-bezier(0.16, 1, 0.3, 1) border-l border-white/20 flex flex-col">
  
      <!-- Dekoratif Ãœst Ã‡izgi -->
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-gold via-navy to-gold"></div>
  
      <div class="flex items-center justify-between p-6 border-b border-gray-100 shrink-0">
          <div>
              <h2 id="hero-modal-title" class="text-xl font-serif font-bold text-navy">Yeni Slide Ekle</h2>
              <p class="text-xs text-gray-500 mt-1">Anasayfa vitrinini Ã¶zelleÅŸtirin.</p>
          </div>
          <button onclick="closeHeroModal()"
              class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-400 hover:text-navy hov
er:bg-gray-100 transition-colors">
              <i class="fa-solid fa-xmark"></i>
          </button>
      </div>
  
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
          <input type="hidden" id="hero-id">
  
          <!-- Resim URL -->
          <div>
              <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Arkaplan GÃ¶rsel
                  (URL)</label>
              <input type="text" id="hero-img"
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 
focus:ring-gold/30 focus:border-gold focus:bg-white transition-all text-sm font-medium text-navy"
                  placeholder="https://...">
              <!-- Preview -->
              <div id="hero-img-preview"
                  class="mt-3 w-full h-32 rounded-lg bg-gray-100 border border-gray-200 bg-cover bg-center hidden">
              </div>
          </div>
  
          <!-- SÄ±ra -->
          <div>
              <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">GÃ¶sterim
                  SÄ±rasÄ±</label>
              <input type="number" id="hero-sira"
                  class="w-24 px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 fo
cus:ring-gold/30 focus:border-gold transition-all text-sm font-medium"
                  value="0">
          </div>
  
          <div class="border-t border-gray-100 pt-5">
              <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i
                      class="fa-solid fa-heading mr-2"></i> BaÅŸlÄ±k AlanlarÄ±</p>
  
              <div class="space-y-4">
                  <div>
                      <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Ä°talik Alt
                          BaÅŸlÄ±k (Gold)</label>
                      <input type="text" id="hero-alt"
                          class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus
:ring-2 focus:ring-gold/30 focus:border-gold transition-all text-sm font-medium"
                          placeholder="Ã–rn: Premium YatÄ±rÄ±m Ã‡Ã¶zÃ¼mleri">
                  </div>
                  <div>
                      <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Ana BaÅŸlÄ±k
                          (SatÄ±r 1)</label>
                      <input type="text" id="hero-title1"
                          class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus
:ring-2 focus:ring-gold/30 focus:border-gold transition-all text-sm font-medium"
                          placeholder="Ã–rn: Sadece Bir Ev DeÄŸil,">
                  </div>
                  <div>
                      <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Ana BaÅŸlÄ±k
                          (SatÄ±r 2 - Vurgulu)</label>
                      <input type="text" id="hero-title2"
                          class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus
:ring-2 focus:ring-gold/30 focus:border-gold transition-all text-sm font-medium"
                          placeholder="Ã–rn: Yeni Bir Hayat.">
                  </div>
              </div>
          </div>
  
          <div class="border-t border-gray-100 pt-5">
              <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i class="fa-solid fa-link mr-2"></
i>
                  YÃ¶nlendirme (Call to Action)</p>
              <div class="space-y-4">
                  <div class="grid grid-cols-2 gap-4">
                      <div>
                          <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Birinci
                              Buton</label>
                          <input type="text" id="hero-btn1"
                              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none t
ext-sm font-medium"
                              value="DetaylÄ± Arama Yap" disabled>
                          <p class="text-[9px] text-gray-400 mt-1">Sabit (Arama ModalÄ±)</p>
                      </div>
                      <div>
                          <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Ä°kinci
                              Buton Metni</label>
                          <input type="text" id="hero-btn2"
                              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none f
ocus:ring-2 focus:ring-gold/30 focus:border-gold transition-all text-sm font-medium"
                              placeholder="Ã–rn: KoleksiyonlarÄ± KeÅŸfet">
                      </div>
                  </div>
                  <div>
                      <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Ä°kinci Buton
                          Linki (Hedef Sayfa)</label>
                      <input type="text" id="hero-target"
                          class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus
:ring-2 focus:ring-gold/30 focus:border-gold transition-all text-sm font-medium"
                          placeholder="Ã–rn: koleksiyon.html?tip=prestij">
                  </div>
              </div>
          </div>
      </div>
  
      <div class="p-6 border-t border-gray-100 bg-gray-50/50 shrink-0">
          <button onclick="saveHeroSlide()"
              class="w-full bg-navy hover:bg-slate-800 text-gold font-bold py-4 rounded-lg transition-all gold-glow upp
ercase tracking-[0.15em] text-xs flex items-center justify-center gap-2">
              <i class="fa-solid fa-check"></i> Kaydet ve YayÄ±nla
          </button>
      </div>
  </div>
  
  
  <!-- ============================================== -->
  <!-- PORTFOLIO WIZARD MODAL -->
  <!-- ============================================== -->
  <div id="portfolio-modal-backdrop"
      class="fixed inset-0 bg-navy/60 backdrop-blur-sm z-40 hidden transition-opacity duration-300 opacity-0"
      onclick="closePortfolioModal()"></div>
  
  <div id="portfolio-slide-over"
      class="fixed top-0 right-0 h-screen w-full lg:max-w-2xl bg-white/95 backdrop-blur-xl shadow-2xl z-50 transform tr
anslate-x-full transition-transform duration-500 cubic-bezier(0.16, 1, 0.3, 1) border-l border-white/20 flex flex-col o
verflow-hidden">
      <!-- Dekoratif Ãœst Ã‡izgi -->
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-navy via-modern to-gold"></div>
  
      <div class="flex items-center justify-between p-6 border-b border-gray-100 shrink-0">
          <div>
              <h2 id="portfolio-modal-title" class="text-xl font-serif font-bold text-navy">Yeni Ä°lan Ekle</h2>
              <!-- Step Indicators -->
              <div class="flex gap-1 mt-2">
                  <div id="step-ind-1" class="w-8 h-1 bg-gold rounded transition-colors"></div>
                  <div id="step-ind-2" class="w-8 h-1 bg-gray-200 rounded transition-colors"></div>
                  <div id="step-ind-3" class="w-8 h-1 bg-gray-200 rounded transition-colors"></div>
                  <div id="step-ind-4" class="w-8 h-1 bg-gray-200 rounded transition-colors"></div>
              </div>
          </div>
          <button onclick="closePortfolioModal()"
              class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-400 hover:text-navy hov
er:bg-gray-100 transition-colors">
              <i class="fa-solid fa-xmark"></i>
          </button>
      </div>
  
      <div class="flex-1 overflow-x-hidden overflow-y-auto p-0 relative">
          <form id="portfolio-form" class="h-full">
  
              <!-- STEP 1 -->
              <div id="wiz-step-1" class="p-6 transition-all duration-300 absolute inset-0 bg-transparent">
                  <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i
                          class="fa-solid fa-circle-info mr-2"></i> AdÄ±m 1: Temel Kimlik</p>
  
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                      <div>
                          <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Sistem ID
                              (URL Path)</label>
                          <input type="text" id="pf-id"
                              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-gold te
xt-sm"
                              placeholder="imz-doga-evleri" required>
                      </div>
                      <div>
                          <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Referans
                              No</label>
                          <input type="text" id="pf-refno"
                              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm"
                              placeholder="IMZ-1234">
                      </div>
                  </div>
  
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                      <div>
                          <label
                              class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Koleksiyon</l
abel>
                          <select id="pf-koleksiyon"
                              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm">
                              <option value="Prestij Koleksiyonu">Prestij Koleksiyonu</option>
                              <option value="Modern Koleksiyon">Modern Koleksiyon</option>
                              <option value="DoÄŸa Koleksiyonu">DoÄŸa Koleksiyonu</option>
                          </select>
                      </div>
                      <div>
                          <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">MÃ¼lk Tipi
                              (Ekspertiz Ä°Ã§in)</label>
                          <select id="pf-mulktipi"
                              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm border-gold 
bg-gold/5">
                              <option value="Konut">Konut (Daire/Villa)</option>
                              <option value="Ticari">Ticari/EndÃ¼striyel</option>
                              <option value="Arsa">Arsa/Arazi</option>
                          </select>
                      </div>
                  </div>
  
                  <div class="space-y-4">
                      <input type="text" id="pf-fiyat"
                          class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm"
                          placeholder="Fiyat (Ã–rn: 15.500.000 â‚º)">
                      <input type="text" id="pf-baslik1"
                          class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm"
                          placeholder="Ana BaÅŸlÄ±k (Ã–rn: BoÄŸaz ManzaralÄ±)">
                      <input type="text" id="pf-baslik2"
                          class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm"
                          placeholder="Alt BaÅŸlÄ±k (Ã–rn: Modern Villa)">
                      <input type="text" id="pf-lokasyon"
                          class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm"
                          placeholder="Tam Lokasyon (Ã–rn: Ä°STANBUL, SARIYER)">
                  </div>
              </div>
  
              <!-- STEP 2 -->
              <div id="wiz-step-2"
                  class="p-6 transition-all duration-300 absolute inset-0 bg-transparent opacity-0 translate-x-[10px] p
ointer-events-none hidden">
                  <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i
                          class="fa-solid fa-house mr-2"></i> AdÄ±m 2: Fiziksel Metrikler</p>
  
                  <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                      <div>
                          <label
                              class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Oda/BÃ¶lÃ
¼m</label>
                          <input type="text" id="pf-oda" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"
                              placeholder="4+1">
                      </div>
                      <div>
                          <label class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Alan
                              (mÂ²)</label>
                          <input type="text" id="pf-alan" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"
                              placeholder="250 mÂ²">
                      </div>
                      <div>
                          <label
                              class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Kat</labe
l>
                          <input type="text" id="pf-kat" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"
                              placeholder="2">
                      </div>
                  </div>
  
                  <div class="space-y-4">
                      <div>
                          <label class="block text-[10px] font-bold text-gray-500 uppercase mb-2">Ekstra Ã–zellikler
                              (VirgÃ¼lle)</label>
                          <textarea id="pf-ozellikler" rows="2"
                              class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"
                              placeholder="GÃ¼venlik, Havuz..."></textarea>
                      </div>
                      <div>
                          <label class="block text-[10px] font-bold text-gray-500 uppercase mb-2">DetaylÄ± Hikaye
                              Metni</label>
                          <textarea id="pf-hikaye" rows="4"
                              class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"></textarea>
                      </div>
                      <div>
                          <label class="block text-[10px] font-bold text-gray-500 uppercase mb-2">Vurgu Ä°kon CSS</labe
l>
                          <input type="text" id="pf-icon-renk"
                              class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="border-gold">
                      </div>
                  </div>
              </div>
  
              <!-- STEP 3 -->
              <div id="wiz-step-3"
                  class="p-6 transition-all duration-300 absolute inset-0 bg-transparent opacity-0 translate-x-[10px] p
ointer-events-none hidden overflow-y-auto pb-20">
                  <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i
                          class="fa-solid fa-clipboard-check mr-2"></i> AdÄ±m 3: Denetim ve Ekspertiz</p>
                  <div id="dynamic-inspection-container">
                      <!-- JS Dinamik GÃ¶mme Yeri -->
                  </div>
              </div>
  
              <!-- STEP 4 -->
              <div id="wiz-step-4"
                  class="p-6 transition-all duration-300 absolute inset-0 bg-transparent opacity-0 translate-x-[10px] p
ointer-events-none hidden">
                  <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i
                          class="fa-regular fa-images mr-2"></i> AdÄ±m 4: Medya & ArÅŸiv</p>
  
                  <div class="mb-6">
                      <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Hero / Vitrin
                          GÃ¶rseli</label>
                      <div class="flex gap-2">
                          <input type="text" id="pf-resim-hero"
                              class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm flex-1"
                              placeholder="DÄ±ÅŸ URL (veya YÃ¼kle)">
  
                          <!-- LOCAL UPLOAD BUTTON -->
                          <div class="relative overflow-hidden inline-block shrink-0">
                              <button type="button"
                                  class="bg-navy hover:bg-slate-800 text-white px-4 py-2 rounded-lg text-xs font-bold w
-32 h-full"
                                  id="pf-upload-hero-label">Yerel Dosya SeÃ§</button>
                              <input type="file" id="pf-upload-hero"
                                  class="absolute left-0 top-0 opacity-0 cursor-pointer h-full" accept="image/*"
                                  onchange="handleImageUpload('pf-upload-hero', 'pf-resim-hero', 'preview-hero')">
                          </div>
                      </div>
                      <img id="preview-hero" class="mt-2 h-24 rounded-lg object-cover hidden" src="" />
                  </div>
  
                  <div class="mb-6">
                      <label class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Hikaye / Ä
°Ã§
                          GÃ¶rsel (DÄ±ÅŸ URL)</label>
                      <input type="text" id="pf-resim-hikaye"
                          class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="https://...">
                  </div>
  
                  <div class="border-t border-gray-100 pt-5">
                      <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i
                              class="fa-solid fa-user-tie mr-2"></i> Sorumlu DanÄ±ÅŸman</p>
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                          <input type="text" id="pf-danisman-isim"
                              class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"
                              placeholder="Ä°sim (Ã–rn: Selim Ã‡Ä±nar)">
                          <input type="text" id="pf-danisman-unvan"
                              class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="Ãœnvan">
                      </div>
                      <input type="text" id="pf-danisman-resim"
                          class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"
                          placeholder="DanÄ±ÅŸman FotoÄŸrafÄ± URL">
                  </div>
              </div>
  
          </form>
      </div>
  
      <!-- WIZARD NAV BUTTONS -->
      <div class="p-6 border-t border-gray-100 bg-gray-50/50 shrink-0 flex gap-4">
          <button type="button" id="wiz-prev-btn" onclick="wizPrev()"
              class="hidden w-1/3 bg-white border border-gray-300 hover:bg-gray-50 text-navy font-bold py-3 rounded-lg 
transition-all uppercase tracking-widest text-xs shadow-sm">
              <i class="fa-solid fa-arrow-left mr-1"></i> Geri
          </button>
          <button type="button" id="wiz-next-btn" onclick="wizNext()"
              class="flex-1 bg-navy hover:bg-slate-800 text-gold font-bold py-3 rounded-lg transition-all uppercase tra
cking-widest text-xs shadow-xl shadow-navy/20">
              Devam Et <i class="fa-solid fa-arrow-right ml-1"></i>
          </button>
          <button type="button" id="wiz-save-btn" onclick="savePortfolio()"
              class="hidden flex-1 bg-gold hover:bg-yellow-600 text-white font-bold py-3 rounded-lg transition-all uppe
rcase tracking-widest text-xs shadow-xl shadow-gold/20 gold-glow">
              <i class="fa-solid fa-cloud-arrow-up mr-1"></i> YayÄ±na Al
          </button>
      </div>
  </div>
  
  </html>


