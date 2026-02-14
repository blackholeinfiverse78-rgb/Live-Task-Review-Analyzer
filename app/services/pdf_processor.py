import pdfplumber
import logging
from fastapi import UploadFile, HTTPException
import io

logger = logging.getLogger("task_review_system.pdf_processor")

class PDFProcessor:
    """
    Deterministic PDF processing service.
    Extracts text from PDF files using pdfplumber without OCR.
    """

    @staticmethod
    def extract_text(file: UploadFile) -> str:
        """
        Extracts full text from an UploadFile PDF.
        Returns a clean combined string.
        
        Constraints:
        - Rejects corrupted PDFs
        - Rejects empty text
        - Fully deterministic
        """
        try:
            # Read file content into memory
            content = file.file.read()
            if not content:
                logger.error("Empty PDF file uploaded")
                raise HTTPException(status_code=400, detail="The uploaded PDF file is empty.")

            # Reset file pointer for potential subsequent reads
            file.file.seek(0)

            with pdfplumber.open(io.BytesIO(content)) as pdf:
                full_text = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text.append(text.strip())
                    else:
                        logger.debug(f"No text found on page {i+1}")

                combined_text = "\n".join(full_text).strip()

                if not combined_text:
                    logger.warning(f"No text extracted from PDF: {file.filename}")
                    raise HTTPException(
                        status_code=400, 
                        detail="Could not extract any text from the PDF. It might be an image-only PDF (OCR not supported) or contain only non-extractable elements."
                    )

                logger.info(f"Successfully extracted {len(combined_text)} characters from {file.filename}")
                return combined_text

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to process PDF {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=400, 
                detail=f"The PDF file appears to be corrupted or invalid: {str(e)}"
            )

# Example usage block for local testing
if __name__ == "__main__":
    import asyncio
    import io
    
    # Simple mock to simulate FastAPI UploadFile
    class MockUploadFile:
        def __init__(self, filename, content):
            self.filename = filename
            self.file = io.BytesIO(content)
            self.content_type = "application/pdf"

    async def example_run():
        print("--- PDFProcessor Example ---")
        # To run this successfully, you'd need a real PDF binary
        # For demonstration, we show how you would call it:
        # 
        # try:
        #     processor = PDFProcessor()
        #     with open("sample.pdf", "rb") as f:
        #         mock_file = MockUploadFile("sample.pdf", f.read())
        #         text = processor.extract_text(mock_file)
        #         print(f"Extracted: {text[:100]}...")
        # except Exception as e:
        #     print(f"Error: {e}")
        print("Note: Run with a real PDF file for actual text extraction results.")

    asyncio.run(example_run())
