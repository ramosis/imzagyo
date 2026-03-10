import sys

# 1. Read takas_sihirbazi_taslak.html
with open('takas_sihirbazi_taslak.html', 'r', encoding='utf-8') as f:
    takas_content = f.read()

start_str = '<div class="max-w-3xl mx-auto'
end_str = '</body>'
start_idx = takas_content.find(start_str)
end_idx = takas_content.rfind(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find the bounds in takas_sihirbazi_taslak.html")
    sys.exit(1)

wizard_html = takas_content[start_idx:end_idx].strip()

section_html = f"""
<!-- BARTER/BUDGET WIZARD SECTION -->
<div id="barter-wizard-section" class="content-section hidden">
    {wizard_html}
</div>
"""

# 2. Read portal.html
with open('portal.html', 'r', encoding='utf-8') as f:
    portal_content = f.read()

if "barter-wizard-section" in portal_content:
    print("Already patched!")
    sys.exit(0)

# Inject Sidebar Button
btn_search = '<button onclick="showSection(\\\'contract-builder\\\', this)"'
btn_start = portal_content.find('contract-builder')
if btn_start != -1:
    btn_start = portal_content.rfind('<button', 0, btn_start)
    btn_end = portal_content.find('</button>', btn_start) + len('</button>')
    
    new_btn = """
                <button onclick="showSection('barter-wizard', this)"
                    class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium">
                    <i class="fa-solid fa-calculator w-5 text-center"></i> Alım Gücü Sihirbazı
                    <span class="bg-gold/20 text-gold text-[10px] py-0.5 px-2 rounded-full">Yeni</span>
                </button>"""
    portal_content = portal_content[:btn_end] + new_btn + portal_content[btn_end:]

# Inject Section Content
sec_search = 'id="users-section"'
sec_start = portal_content.find(sec_search)
if sec_start != -1:
    sec_start = portal_content.rfind('<div', 0, sec_start)
    portal_content = portal_content[:sec_start] + section_html + '\n\n' + portal_content[sec_start:]
    print("Found sec_start!")

# Inject JS Logic for the Wizard
js_logic = """
        // --- BARTER WIZARD LOGIC ---
        function barterNext(stepIndex) {
            document.getElementById('step-' + (stepIndex - 1)).classList.add('hidden');
            document.getElementById('step-' + stepIndex).classList.remove('hidden');
        }
        function barterPrev(stepIndex) {
            document.getElementById('step-' + (stepIndex + 1)).classList.add('hidden');
            document.getElementById('step-' + stepIndex).classList.remove('hidden');
        }
        
"""
logout_idx = portal_content.find('function logout()')
if logout_idx != -1:
    portal_content = portal_content[:logout_idx] + js_logic + portal_content[logout_idx:]

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(portal_content)

print("Injected Barter Wizard successfully into portal.html!")
