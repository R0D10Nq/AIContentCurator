"""
Роутер для анализа контента с помощью Gemini AI
"""

import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, Analysis
from backend.schemas import AnalysisRequest, AnalysisResponse, AnalysisList
from backend.routers.auth import get_current_user
from backend.services.gemini_service import GeminiService

router = APIRouter()


@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создание нового анализа контента"""
    start_time = time.time()
    
    # Проверяем тип анализа
    valid_types = ["sentiment", "summary", "keywords"]
    if request.analysis_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый тип анализа. Доступные: {', '.join(valid_types)}"
        )
    
    try:
        # Инициализируем сервис Gemini
        gemini_service = GeminiService()
        
        # Выполняем анализ в зависимости от типа
        if request.analysis_type == "sentiment":
            result, confidence = await gemini_service.analyze_sentiment(request.text)
        elif request.analysis_type == "summary":
            result, confidence = await gemini_service.create_summary(request.text)
        elif request.analysis_type == "keywords":
            result, confidence = await gemini_service.extract_keywords(request.text)
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        # Сохраняем результат в БД
        analysis = Analysis(
            user_id=current_user.id,
            original_text=request.text,
            analysis_type=request.analysis_type,
            result=result,
            confidence_score=str(confidence) if confidence else None,
            processing_time=processing_time
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при анализе контента: {str(e)}"
        )


@router.get("/", response_model=AnalysisList)
async def get_user_analyses(
    skip: int = 0,
    limit: int = 20,
    analysis_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение анализов пользователя"""
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)
    
    if analysis_type:
        query = query.filter(Analysis.analysis_type == analysis_type)
    
    total = query.count()
    analyses = query.order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    
    return AnalysisList(analyses=analyses, total=total)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение конкретного анализа"""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Анализ не найден")
    
    return analysis


@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление анализа"""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Анализ не найден")
    
    db.delete(analysis)
    db.commit()
    
    return {"message": "Анализ успешно удален"}
