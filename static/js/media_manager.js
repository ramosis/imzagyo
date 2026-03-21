// Media Manager Logic for Imza Gayrimenkul
let currentPortfolioId = null;
let cropper = null;
let uploadingFile = null;

// Opens the Media Manager Modal for a specific Portfolio
async function openMediaManager(portfolioId) {
    currentPortfolioId = portfolioId;
    document.getElementById('media-modal').classList.remove('hidden');
    refreshMediaList();
}

function closeMediaManager() {
    document.getElementById('media-modal').classList.add('hidden');
    currentPortfolioId = null;
    resetUploadForm();
}

// Fetches and displays existing media
async function refreshMediaList() {
    const listContainer = document.getElementById('media-list-container');
    listContainer.innerHTML = '<div class="col-span-full text-center py-8"><i class="fa-solid fa-spinner fa-spin text-2xl text-gold mb-2"></i><p class="text-xs text-gray-500 font-bold uppercase tracking-widest">Yükleniyor...</p></div>';
    
    try {
        const token = localStorage.getItem('imza_admin_token') || ""; 
        const res = await fetch(`${API_BASE}/media/portfolio/${currentPortfolioId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!res.ok) throw new Error("Failed to fetch media");
        const mediaList = await res.json();
        
        if (mediaList.length === 0) {
            listContainer.innerHTML = '<div class="col-span-full text-center py-8"><p class="text-sm text-gray-400">Henüz medya bulunamadı.</p></div>';
            return;
        }

        listContainer.innerHTML = mediaList.map(media => `
            <div class="relative group bg-gray-50 border border-gray-100 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all">
                <div class="aspect-video w-full bg-cover bg-center" style="background-image: url('${media.file_url}'); background-position: ${media.focal_x || 50}% ${media.focal_y || 50}%"></div>
                <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent p-3 pt-6 flex justify-between items-end">
                    <span class="px-2 py-1 bg-gold text-white text-[10px] font-bold uppercase rounded tracking-wider shadow-sm">${media.category}</span>
                    <button onclick="deleteMedia(${media.id})" class="w-8 h-8 flex items-center justify-center bg-white/20 hover:bg-red-500 backdrop-blur-sm text-white rounded-lg transition-colors" title="Sil">
                        <i class="fa-solid fa-trash text-xs"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error("Error fetching media:", err);
        listContainer.innerHTML = '<div class="col-span-full text-center py-8"><p class="text-sm text-red-500">Medyalar yüklenirken hata oluştu.</p></div>';
    }
}

// Delete media
async function deleteMedia(mediaId) {
    if (!confirm('Bu medyayı silmek istediğinize emin misiniz?')) return;
    
    try {
        const token = localStorage.getItem('imza_admin_token') || ""; 
        const res = await fetch(`${API_BASE}/media/${mediaId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            showToast('Medya başarıyla silindi', 'success');
            refreshMediaList();
        } else {
            showToast('Silme işlemi başarısız', 'error');
        }
    } catch(err) {
        console.error(err);
        showToast('Devam edilemedi', 'error');
    }
}

// Handing file selection for upload and enforcing minimum dimensions
function handleMediaSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const url = URL.createObjectURL(file);
    const img = new Image();
    
    img.onload = function() {
        // Enforce 1920x1080 dimension limit
        if (this.width < 1920 || this.height < 1080) {
            showToast(`Hata: Görsel boyutu en az 1920x1080 olmalıdır. Yüklenen: ${this.width}x${this.height}`, 'error');
            resetUploadForm();
            return;
        }

        uploadingFile = file;
        const imgElement = document.getElementById('media-crop-image');
        imgElement.src = url;
        
        document.getElementById('media-crop-container').classList.remove('hidden');
        document.getElementById('media-upload-placeholder').classList.add('hidden');
        
        if (cropper) cropper.destroy();
        
        cropper = new Cropper(imgElement, {
            viewMode: 1,
            dragMode: 'crop',
            autoCropArea: 1,
            restore: false,
            guides: true,
            center: true,
            highlight: false,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: false,
        });
    };
    img.onerror = function() {
        showToast('Geçersiz görsel formatı.', 'error');
    };
    img.src = url;
}

function resetUploadForm() {
    uploadingFile = null;
    document.getElementById('media-upload-input').value = '';
    document.getElementById('media-crop-container').classList.add('hidden');
    document.getElementById('media-upload-placeholder').classList.remove('hidden');
    if (cropper) {
        cropper.destroy();
        cropper = null;
    }
}

// Apply Focal Point settings based on cropper center
function getFocalPoint() {
    if (!cropper) return { focal_x: 50, focal_y: 50 };
    const cropBoxData = cropper.getCropBoxData();
    const canvasData = cropper.getCanvasData();
    
    // Calculate center point of crop box relative to image natural size
    const centerX = cropBoxData.left + cropBoxData.width / 2;
    const centerY = cropBoxData.top + cropBoxData.height / 2;
    
    const xRatio = (centerX - canvasData.left) / canvasData.width;
    const yRatio = (centerY - canvasData.top) / canvasData.height;
    
    return {
        focal_x: Math.round(Math.max(0, Math.min(100, xRatio * 100))),
        focal_y: Math.round(Math.max(0, Math.min(100, yRatio * 100)))
    };
}

// Client side cropping and upload
async function uploadMedia() {
    if (!uploadingFile || !cropper) {
        showToast('Lütfen bir görsel seçin', 'error');
        return;
    }

    const btn = document.getElementById('media-upload-btn');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Yükleniyor...';
    btn.disabled = true;

    try {
        const category = document.getElementById('media-category-select').value;
        const focal = getFocalPoint();
        
        // Use Cropper plugin to get cropped image directly as a blob
        cropper.getCroppedCanvas({
            maxWidth: 4096,
            maxHeight: 4096,
            fillColor: '#fff',
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high',
        }).toBlob(async (blob) => {
            if (!blob) throw new Error("Kırpma işlemi başarısız.");
            
            const formData = new FormData();
            formData.append('file', blob, uploadingFile.name);
            formData.append('portfolio_id', currentPortfolioId);
            formData.append('category', category);
            formData.append('focal_x', focal.focal_x);
            formData.append('focal_y', focal.focal_y);
            
            const token = localStorage.getItem('imza_admin_token') || ""; 
            const res = await fetch(`${API_BASE}/media`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || "Yükleme hatası");
            }
            
            showToast('Medya başarıyla eklendi', 'success');
            resetUploadForm();
            refreshMediaList();
            
            btn.innerHTML = '<i class="fa-solid fa-cloud-arrow-up mr-2 text-sm"></i> Kırp, Yükle & Kaydet';
            btn.disabled = false;
        }, uploadingFile.type, 0.9);
        
    } catch(err) {
        console.error("Upload error:", err);
        showToast(err.message || 'Görsel yüklenirken bir hata oluştu', 'error');
        btn.innerHTML = '<i class="fa-solid fa-cloud-arrow-up mr-2 text-sm"></i> Kırp, Yükle & Kaydet';
        btn.disabled = false;
    }
}    
