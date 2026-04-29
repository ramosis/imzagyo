from backend.integrations.cloudinary.client import CloudinaryClient

class MediaService:
    def __init__(self):
        self.client = CloudinaryClient()
    
    def upload_property_image(self, file_path: str) -> str:
        result = self.client.upload(file_path, folder="properties")
        return result.get('secure_url', '')
