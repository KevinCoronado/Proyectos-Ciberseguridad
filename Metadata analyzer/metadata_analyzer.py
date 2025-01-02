from abc import ABC, abstractmethod
from PIL import Image
import mimetypes
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import re
import docx

class MetadataExtractor(ABC):
        @abstractmethod
        def extract(self, filepath):
            pass
        
class ImageMetadataExtractor(MetadataExtractor):
    def extract(self, filepath):
        with Image.open(filepath) as img:
            if img.format in ['JPG','JPEG']:
                exif =  img._getexif()
                if exif:
                    return{Image.ExifTags.TAGS.get(key,key):value
                           for key,value in exif.items() if key in Image.ExifTags.TAGS}
                else:
                    return{"Error": "No EXIF metadata encontrada."}
            elif img.format in ['PNG']:
                if img.info:
                    return img.info
                else:
                    return {"Error": "No se encontro metadata"}
 
class DocxMetadataExtractor(MetadataExtractor):
    def extract(self, filepath):
        doc = docx.Document(filepath)
        prop = doc.core_properties
        attributes = [
            "author", "category", "comments","content_status",
            "created", "identifier", "keywords", "last_modified_by",
            "language", "modified", "subject", "title", "version"
        ]
        
        metadata = {attr: getattr(prop, attr, None) for  attr in attributes}
        return metadata

     
 
class PdfMetadataExtractor(MetadataExtractor):
    def extract(self, filepath):
        metadata={}
        with open(filepath, 'rb') as f:
            parser = PDFParser(f)
            doc =  PDFDocument(parser)
            if doc.info:
                for info in doc.info:
                    for key, value in info.items():
                        #Verificamos is el valo de la clave son bytes
                        if isinstance(value, bytes):
                            try:
                                #Decodificamos en UTF - 16BE
                                decoded_value = value.decode('utf=16be')
                            except UnicodeDecodeError:
                                #Intentamos utf8
                                decoded_value = value.decode('utf-8',errors ='ignore')
                        else:
                            decoded_value = value
                        metadata[key] = decoded_value
                    
            #Procesamos el texto del pdf para obtener otros datos
            text = extract_text(filepath)
            metadata["Emails"] =  self._extract_emails(text)
        return metadata
            
    def _extract_emails(self, text):
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_regex, text)
        
                            
                           
                
class MetadataExtractorFactory(MetadataExtractor):
    @staticmethod
    def get_extractor(filepath):
        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type:
            if mime_type.startswith('image'):
                return ImageMetadataExtractor()
            if mime_type == 'application/pdf':
                return PdfMetadataExtractor()
            if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return DocxMetadataExtractor()
        raise ValueError("Documento no soportado")
            
            
            
def extract_metadata(filepath):
    extractor = MetadataExtractorFactory.get_extractor(filepath)
    return extractor.extract(filepath)
                    
        
