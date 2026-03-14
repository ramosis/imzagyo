import re

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

# FOMO badge HTML template - will be injected right before the closing </div> of each card's detail section
# We target the pattern: the grid with Oda/Alan/Tip stats, and inject FOMO badges after it

fomo_badges = [
    {
        'views': 145,
        'offers': 2,
        'avg_days': 12,
        'marker': 'Boğaz Manzaralı Villa'
    },
    {
        'views': 89,
        'offers': 1,
        'avg_days': 18,
        'marker': 'Modern Loft Daire'
    },
    {
        'views': 67,
        'offers': 3,
        'avg_days': 9,
        'marker': 'Ekolojik Orman Evi'
    }
]

for badge in fomo_badges:
    badge_html = f'''
                            <div class="mt-6 pt-4 border-t border-gray-100 space-y-2">
                                <div class="flex items-center gap-2 text-[10px] text-gray-500">
                                    <span class="inline-flex items-center gap-1.5 bg-red-50 text-red-600 px-2.5 py-1 rounded-full font-bold">
                                        <i class="fa-solid fa-fire text-[8px]"></i> {badge['views']} kişi inceledi
                                    </span>
                                    <span class="inline-flex items-center gap-1.5 bg-amber-50 text-amber-600 px-2.5 py-1 rounded-full font-bold">
                                        <i class="fa-solid fa-gavel text-[8px]"></i> {badge['offers']} aktif teklif
                                    </span>
                                </div>
                                <p class="text-[9px] text-gray-400 font-medium flex items-center gap-1.5">
                                    <i class="fa-regular fa-clock text-[8px]"></i> Bölgede ort. satış süresi: <span class="text-navy font-bold">{badge['avg_days']} gün</span>
                                </p>
                            </div>'''
    
    # Find the card by its title and inject the badge after the stats grid
    marker = badge['marker']
    marker_idx = content.find(marker)
    if marker_idx == -1:
        print(f"Could not find marker: {marker}")
        continue
    
    # Find the closing </div> of the card's inner content div (p-6 md:p-8)
    # We need to find the grid div with Oda/Alan/Tip and inject after its closing </div>
    # The structure is: <div class="grid grid-cols-3 ..."> ... </div>
    # Find the grid div after this marker
    grid_idx = content.find('grid grid-cols-3 border-t border-gray-100', marker_idx)
    if grid_idx == -1:
        print(f"Could not find grid after marker: {marker}")
        continue
    
    # Find the closing </div> for this grid (count nested divs)
    search_start = content.rfind('<div', 0, grid_idx + 1)
    # Actually, let's find the </div> that closes the grid
    # Count from the <div that contains grid_idx
    pos = grid_idx
    # Find the opening <div
    div_open = content.rfind('<div', 0, pos + 5)
    depth = 1
    scan = content.find('>', div_open) + 1  # after the opening tag
    
    while depth > 0 and scan < len(content):
        next_open = content.find('<div', scan)
        next_close = content.find('</div>', scan)
        
        if next_close == -1:
            break
        
        if next_open != -1 and next_open < next_close:
            depth += 1
            scan = content.find('>', next_open) + 1
        else:
            depth -= 1
            if depth == 0:
                # Found the closing </div> for the grid
                close_div_end = next_close + len('</div>')
                content = content[:close_div_end] + badge_html + content[close_div_end:]
                print(f"Injected FOMO badge for: {marker}")
                break
            scan = next_close + len('</div>')

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
