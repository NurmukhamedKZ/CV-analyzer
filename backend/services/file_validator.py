import logging
from fastapi import UploadFile
import os

logger = logging.getLogger(__name__)

class FileValidator:
    """Service for validating uploaded files"""
    
    def __init__(self):
        # Maximum file size in bytes (10MB)
        self.max_file_size = 10 * 1024 * 1024
        
        # Allowed file types and their MIME types
        self.allowed_types = {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'application/msword': ['.doc']
        }
        
        # Allowed file extensions
        self.allowed_extensions = ['.pdf', '.docx', '.doc']
    
    def is_valid_file(self, file: UploadFile) -> bool:
        """
        Check if the uploaded file is valid
        
        Args:
            file: Uploaded file object
            
        Returns:
            True if file is valid, False otherwise
        """
        try:
            # Check if file has a name
            if not file.filename:
                logger.warning("File has no filename")
                return False
            
            # Check file extension
            file_extension = self._get_file_extension(file.filename)
            if not self._is_valid_extension(file_extension):
                logger.warning(f"Invalid file extension: {file_extension}")
                return False
            
            # Check MIME type
            if not self._is_valid_mime_type(file.content_type, file_extension):
                logger.warning(f"Invalid MIME type: {file.content_type} for extension {file_extension}")
                return False
            
            logger.info(f"File validation passed for: {file.filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False
    
    def is_valid_size(self, file: UploadFile) -> bool:
        """
        Check if the file size is within limits
        
        Args:
            file: Uploaded file object
            
        Returns:
            True if file size is valid, False otherwise
        """
        try:
            # Check if file size is available
            if not hasattr(file, 'size') or file.size is None:
                logger.warning("File size not available")
                return False
            
            # Check if file size is within limits
            if file.size > self.max_file_size:
                logger.warning(f"File size {file.size} exceeds limit {self.max_file_size}")
                return False
            
            # Check if file size is reasonable (not too small)
            if file.size < 100:  # Less than 100 bytes
                logger.warning(f"File size {file.size} is too small")
                return False
            
            logger.info(f"File size validation passed: {file.size} bytes")
            return True
            
        except Exception as e:
            logger.error(f"Error validating file size: {str(e)}")
            return False
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        try:
            return os.path.splitext(filename)[1].lower()
        except Exception:
            return ""
    
    def _is_valid_extension(self, extension: str) -> bool:
        """Check if file extension is allowed"""
        return extension in self.allowed_extensions
    
    def _is_valid_mime_type(self, mime_type: str, extension: str) -> bool:
        """Check if MIME type matches the file extension"""
        if not mime_type:
            return False
        
        # Check if MIME type is in allowed types
        if mime_type in self.allowed_types:
            # Check if extension matches the MIME type
            return extension in self.allowed_types[mime_type]
        
        # If MIME type is not recognized, check if it's a generic type
        # that might be acceptable for the given extension
        generic_mime_types = {
            '.pdf': ['application/octet-stream', 'binary/octet-stream'],
            '.docx': ['application/octet-stream', 'binary/octet-stream'],
            '.doc': ['application/octet-stream', 'binary/octet-stream']
        }
        
        if extension in generic_mime_types:
            return mime_type in generic_mime_types[extension]
        
        return False
    
    def get_file_info(self, file: UploadFile) -> dict:
        """
        Get comprehensive file information
        
        Args:
            file: Uploaded file object
            
        Returns:
            Dictionary with file information
        """
        try:
            return {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size,
                "extension": self._get_file_extension(file.filename) if file.filename else None,
                "is_valid_type": self._is_valid_file(file),
                "is_valid_size": self.is_valid_size(file),
                "max_allowed_size": self.max_file_size,
                "allowed_extensions": self.allowed_extensions,
                "allowed_mime_types": list(self.allowed_types.keys())
            }
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return {"error": str(e)}
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for security
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        try:
            if not filename:
                return "unnamed_file"
            
            # Remove path traversal attempts
            filename = os.path.basename(filename)
            
            # Remove or replace potentially dangerous characters
            dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
            for char in dangerous_chars:
                filename = filename.replace(char, '_')
            
            # Limit filename length
            if len(filename) > 255:
                name, ext = os.path.splitext(filename)
                filename = name[:255-len(ext)] + ext
            
            return filename or "unnamed_file"
            
        except Exception as e:
            logger.error(f"Error sanitizing filename: {str(e)}")
            return "unnamed_file"
    
    def get_file_category(self, filename: str) -> str:
        """
        Categorize file based on extension
        
        Args:
            filename: Filename to categorize
            
        Returns:
            File category string
        """
        extension = self._get_file_extension(filename)
        
        if extension == '.pdf':
            return 'PDF Document'
        elif extension == '.docx':
            return 'Word Document (DOCX)'
        elif extension == '.doc':
            return 'Word Document (DOC)'
        else:
            return 'Unknown'
