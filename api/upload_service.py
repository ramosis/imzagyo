import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Cloudinary Yapılandırması
# Not: Bu değerlerin .env dosyasından okunması önerilir.
# cloudinary.config( 
#   cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
#   api_key = os.getenv("CLOUDINARY_API_KEY"), 
#   api_secret = os.getenv("CLOUDINARY_API_SECRET"),
#   secure = True
# )

def upload_image_to_cloudinary(file_path, folder="imza_gayrimenkul"):
    """
    Yerel bir dosyayı Cloudinary'ye yükler ve optimize edilmiş URL'leri döner.
    """
    try:
        # Yükleme ve otomatik optimizasyon
        upload_result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            use_filename=True,
            unique_filename=True,
            overwrite=False,
            resource_type="image"
        )
        
        # Optimize edilmiş URL'ler oluştur (WebP formatı ve otomatik kalite)
        # s_url: Standart URL
        # o_url: Optimize edilmiş (WebP, Auto Quality) URL
        s_url = upload_result.get("secure_url")
        
        # Cloudinary Transformation URL (WebP ve Otomatik Kalite)
        o_url, options = cloudinary_url(
            upload_result["public_id"],
            format="webp",
            quality="auto",
            fetch_format="auto"
        )
        
        return {
            "success": True,
            "public_id": upload_result["public_id"],
            "url": s_url,
            "optimized_url": o_url
        }
    except Exception as e:
        print(f"Cloudinary Yükleme Hatası: {e}")
        return {"success": False, "error": str(e)}

def get_optimized_url(public_id, width=1200, height=800, crop="fill"):
    """
    Belirli boyutlarda optimize edilmiş bir URL üretir.
    """
    url, options = cloudinary_url(
        public_id,
        width=width,
        height=height,
        crop=crop,
        quality="auto",
        fetch_format="auto",
        secure=True
    )
    return url
