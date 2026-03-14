import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD OVERFLOW-X TO ALL INSTANCES OF table-responsive containers OR direct tables wrapper
# We will search for <table class="w-full text-left premium-table"> and wrap them if they aren't already wrapped.
# Or if they are in a div, add overflow-x-auto to it.

# Specifically targeting the div wrapping the tables. They currently look like:
# <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
# or <div class="bg-white rounded-[2rem] shadow-sm border border-gray-100 overflow-hidden">
# We want to change the direct parent to have `overflow-x-auto`.

def replacer_table(match):
    # This is a bit tricky, let's just add a generic patch. 
    # Actually, the div class often contains `overflow-hidden`. We can swap `overflow-hidden` for `overflow-hidden overflow-x-auto`.
    return match.group(0).replace("overflow-hidden", "overflow-hidden overflow-x-auto")

# Let's target lines where "rounded-" and "overflow-hidden" are together
html = re.sub(r'<div class="[^"]*bg-white[^"]*rounded-[^"]*overflow-hidden[^"]*">', replacer_table, html)


# 2. LOGOUT CONFIRMATION MODAL
logout_modal_html = """
<!-- ================= LOGOUT CONFIRM MODAL ================= -->
<div id="logout-confirm-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-sm shadow-2xl overflow-hidden p-8 relativetext-center">
        <div class="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
            <i class="fa-solid fa-arrow-right-from-bracket"></i>
        </div>
        <h3 class="text-2xl font-serif font-bold text-navy mb-2 text-center">Çıkış Yap</h3>
        <p class="text-sm text-gray-500 mb-6 text-center">Oturumunuzu sonlandırmak istediğinize emin misiniz?</p>
        <div class="flex gap-3">
            <button onclick="document.getElementById('logout-confirm-modal').classList.add('hidden')" class="flex-1 py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">İptal</button>
            <button onclick="executeLogout()" class="flex-1 py-3 bg-red-500 text-white rounded-lg font-bold shadow-lg shadow-red-500/30 hover:bg-red-600 transition-colors">Evet, Çıkış Yap</button>
        </div>
    </div>
</div>
"""

# Insert modal before </body>
html = re.sub(r'</body>', logout_modal_html + '\n</body>', html, flags=re.IGNORECASE)

# Update the logout button (it was onclick="logout()")
html = html.replace('onclick="logout()"', "onclick=\"document.getElementById('logout-confirm-modal').classList.remove('hidden')\"")

# Rename the actual JS logout function
html = html.replace('function logout() {', 'function executeLogout() {\n            document.getElementById(\'logout-confirm-modal\').classList.add(\'hidden\');')

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Overflow and Logout Modal patched.")
