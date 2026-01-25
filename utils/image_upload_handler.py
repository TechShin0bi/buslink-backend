import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def upload_to(instance, filename, base_path):
    """
    Generate a unique filename for uploaded files.
    
    Args:
        instance: The model instance where the file is being attached.
        filename (str): The original filename.
        base_path (str): The base path where the file will be stored.
        
    Returns:
        str: A unique file path for the uploaded file.
    """
    ext = filename.split('.')[-1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(base_path, unique_filename)

def handle_uploaded_file(instance, filename):
    """
    Handle file upload for Django's FileField.upload_to
    
    Args:
        instance: The model instance where the file is being attached.
        filename (str): The original filename.
        
    Returns:
        str: The path where the file should be saved.
    """
    validate_and_upload_file(filename)
    return upload_to(instance, filename, base_path="agency_logos/")

def validate_and_upload_file(file, base_path, max_size_mb=5):
    """
    Validate and upload a file with additional checks.
    To be used in views/forms, not in models.
    
    Args:
        file: The uploaded file object (from request.FILES)
        base_path (str): The base path where to store the file
        max_size_mb (int): Maximum allowed file size in MB
        
    Returns:
        dict: {
            'success': bool,
            'path': str,  # relative path if success
            'url': str,   # full URL if success
            'error': str  # error message if failed
        }
    """
    try:
        max_size = max_size_mb * 1024 * 1024  
        if file.size > max_size:
            return {
                'success': False,
                'error': f'File too large. Size should not exceed {max_size_mb}MB.'
            }
            
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in valid_extensions:
            return {
                'success': False,
                'error': 'Invalid file type. Allowed types: ' + ', '.join(valid_extensions)
            }
            
        file_path = upload_to(None, file.name, base_path)
        file_name = default_storage.save(file_path, ContentFile(file.read()))
        
        return {
            'success': True,
            'path': file_name,
            'url': default_storage.url(file_name)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }