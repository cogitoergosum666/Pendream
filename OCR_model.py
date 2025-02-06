from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

class OCR_model:
    def __init__(self,image_dir = 'handwriting.png') -> None:

        self.image_dir = image_dir

    def start_OCR(self):

        '''
        process the handwriting image for OCR to generate result
        '''
        self.__image = Image.open(self.image_dir).convert("RGB")
        # load pretrained moedl TrOCR 
        processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

        # pre-process image 
        pixel_values = processor(images=self.__image, return_tensors="pt").pixel_values

        # use moedel predict the text
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # return the OCR result
        return(generated_text)

