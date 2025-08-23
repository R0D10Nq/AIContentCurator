"""
Сервис для работы с Gemini AI API
"""

import google.generativeai as genai
from typing import Tuple, Optional
from backend.config import settings


class GeminiService:
    """Сервис для анализа текста с помощью Gemini AI"""
    
    def __init__(self):
        """Инициализация сервиса"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY не установлен в переменных окружения")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def analyze_sentiment(self, text: str) -> Tuple[str, Optional[float]]:
        """
        Анализ тональности текста
        Возвращает: (результат_анализа, уверенность)
        """
        prompt = f"""
        Проанализируй тональность следующего текста на русском языке.
        Определи эмоциональную окраску: позитивная, негативная или нейтральная.
        Также оцени уверенность в анализе от 0 до 1.
        
        Текст для анализа:
        "{text}"
        
        Ответь в следующем формате:
        Тональность: [позитивная/негативная/нейтральная]
        Уверенность: [число от 0 до 1]
        Объяснение: [краткое объяснение почему такая тональность]
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Пытаемся извлечь уверенность из ответа
            confidence = self._extract_confidence(result)
            
            return result, confidence
            
        except Exception as e:
            raise Exception(f"Ошибка при анализе тональности: {str(e)}")
    
    async def create_summary(self, text: str) -> Tuple[str, Optional[float]]:
        """
        Создание краткого резюме текста
        Возвращает: (резюме, уверенность)
        """
        prompt = f"""
        Создай краткое резюме следующего текста на русском языке.
        Выдели основные мысли и ключевые моменты в 2-3 предложениях.
        
        Текст для резюмирования:
        "{text}"
        
        Ответь кратким резюме без дополнительных пояснений.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Для резюме уверенность всегда высокая
            confidence = 0.9
            
            return result, confidence
            
        except Exception as e:
            raise Exception(f"Ошибка при создании резюме: {str(e)}")
    
    async def extract_keywords(self, text: str) -> Tuple[str, Optional[float]]:
        """
        Извлечение ключевых слов и тем из текста
        Возвращает: (ключевые_слова, уверенность)
        """
        prompt = f"""
        Извлеки ключевые слова и основные темы из следующего текста на русском языке.
        Выдели 5-10 наиболее важных слов и фраз, которые отражают суть текста.
        
        Текст для анализа:
        "{text}"
        
        Ответь списком ключевых слов через запятую.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Для ключевых слов уверенность средняя
            confidence = 0.8
            
            return result, confidence
            
        except Exception as e:
            raise Exception(f"Ошибка при извлечении ключевых слов: {str(e)}")
    
    def _extract_confidence(self, text: str) -> Optional[float]:
        """Извлечение значения уверенности из текста ответа"""
        try:
            lines = text.split('\n')
            for line in lines:
                if 'уверенность' in line.lower():
                    # Ищем число в строке
                    import re
                    numbers = re.findall(r'0\.\d+|\d+\.\d+', line)
                    if numbers:
                        confidence = float(numbers[0])
                        return min(max(confidence, 0.0), 1.0)  # Ограничиваем от 0 до 1
            return None
        except:
            return None
