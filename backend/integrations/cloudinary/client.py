import cloudinary
import cloudinary.uploader
import os

class CloudinaryClient:
    """Sadece ham Cloudinary API istemcisi."""
    
    def __init__(self):
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        
        if cloud_name and api_key and api_secret:
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            self.configured = True
        else:
            self.configured = False
    
    def upload(self, file_path: str, folder: str = "imza") -> dict:
        """Dosya yükle, ham yanıtı döndür."""
        if not self.configured:
            return {"secure_url": f"https://res.cloudinary.com/demo/image/upload/{folder}/simulated_image.jpg"}
        return cloudinary.uploader.upload(file_path, folder=folder)
    
    def delete(self, public_id: str) -> dict:
        """Dosya sil."""
        if not self.configured:
            return {"result": "ok"}
        return cloudinary.uploader.destroy(public_id)
