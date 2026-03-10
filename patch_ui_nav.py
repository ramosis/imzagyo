import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the CSS for 'active' state in the sidebar menus
# Find all occurrences of the base nav-item class structure
old_nav_class = "nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium"

# Replace it with a new base structure that has stronger the active design
# When JS adds the 'active' class, it will trigger specific CSS we will also inject
new_nav_class = "nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium"

# The specific 'portfolios' section has 'justify-between'
old_nav_class_between = "nav-item w-full flex items-center justify-between px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium"
new_nav_class_between = "nav-item w-full flex items-center justify-between px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium"

html = html.replace(old_nav_class, new_nav_class)
html = html.replace(old_nav_class_between, new_nav_class_between)

# 2. Inject CSS for the .active class to make it feel "Premium"
css_to_add = """
        /* Premium Nav Active State */
        .nav-item.active {
            background-color: rgba(197, 160, 89, 0.1); /* bg-gold/10 */
            color: #c5a059 !important; /* text-gold */
            border-left: 3px solid #c5a059;
            font-weight: 700;
        }
        .nav-item.active i {
            color: #c5a059;
        }
    </style>
"""

# Replace the closing style tag with our new CSS + closing style tag
html = html.replace("</style>", css_to_add)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Nav menu styling patched.")
