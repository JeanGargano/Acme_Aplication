from Model.PromptModel import PromptModel
import google.generativeai as genai
import os
import logging
import json
import re

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

class GeminiRepository:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        logger.info(f"apikey: {self.api_key}")
        if not self.api_key:
            raise ValueError("API_KEY no está configurada. Asegúrate de definirla en el archivo .env.")
        genai.configure(api_key=self.api_key) 
        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def generar_reporte(self, prompt: PromptModel):
        try:
            data = prompt.prompt
            data_str = json.dumps([item.dict() for item in data], ensure_ascii=False, indent=2)
            request = (
                "Necesito que me generes un dashboard en formato JSON puro (sin texto adicional). "
                "Clasifica las respuestas como: 'Cumple' = Bueno (10), "
                "'Medianamente cumple' = Regular (5), 'No cumple' = Malo (0). "
                "El JSON debe incluir: un array llamado 'dashboard' con la información por pregunta, "
                "totales por categoría ('bueno', 'regular', 'malo') y un 'total_general'.\n"
                f"{data_str}"
            )
            response = self.model.generate_content(request)
            # Extraer solo el bloque JSON usando regex, en caso de que Gemini devuelva texto adicional
            match = re.search(r'\{[\s\S]*\}', response.text)
            if not match:
                raise Exception(f"No se encontró un bloque JSON en la respuesta: {response.text}")
            try:
                dashboard = json.loads(match.group())
            except json.JSONDecodeError as e:
                raise Exception(f"Error al decodificar JSON: {str(e)}\nRespuesta: {response.text}")
            return dashboard  # FastAPI lo convierte automáticamente en JSON
        except Exception as e:
            raise Exception(f"Error al consultar la API de Gemini: {str(e)}")
        
    def generate_form(self, prompt: str, context: str) :
        try:
            full_prompt = f"{context}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            match = re.search(r'\{[\s\S]*\}', response.text)
            if not match:
                raise ValueError("No se encontró JSON válido en la respuesta del modelo.")
            try:
                formulario = json.loads(match.group())
            except json.JSONDecodeError as e:
                raise Exception(f"Error al decodificar JSON: {str(e)}\nRespuesta: {response.text}")
            return formulario 
        
        except Exception as e:
            logger.error(f"Error generating form: {e}")
            raise