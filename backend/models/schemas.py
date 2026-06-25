"""
Schémas Pydantic des entités principales.

Ces modèles ne sont pas encore branchés sur les routes (ce sera fait en
Phase 1+, quand chaque endpoint sera implémenté). Ils sont posés dès le
scaffold pour fixer la forme des données échangées avec le frontend.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

Role = Literal["Utilisateur", "RH", "Admin"]
StatutCandidature = Literal["A analyser", "Entretien", "Retenu", "Refuse"]
StatutOffre = Literal["Ouverte", "En pause", "Fermee"]


# ---------------------------------------------------------------------------
# API Utilisateurs
# ---------------------------------------------------------------------------
class UserCreate(BaseModel):
    prenom: str
    nom: str
    email: EmailStr
    mdp: str = Field(min_length=6)
    role: Role = "Utilisateur"


class UserOut(BaseModel):
    id: str
    prenom: str
    nom: str
    email: EmailStr
    role: Role
    date_creation: datetime


class UserLogin(BaseModel):
    email: EmailStr
    mdp: str


# ---------------------------------------------------------------------------
# API Offres
# ---------------------------------------------------------------------------
class SkillWeighted(BaseModel):
    name: str
    weight: int = Field(ge=1, le=10, default=5)


class OfferCreate(BaseModel):
    title: str
    company: str
    location: str
    contract_type: list[str] = []
    description: str = ""
    missions: list[str] = []
    required_skills: list[SkillWeighted] = []
    preferred_skills: list[str] = []
    education: str = ""
    experience: dict[str, int] = {}
    certifications: list[str] = []
    soft_skills: list[str] = []
    keywords: list[str] = []
    status: StatutOffre = "Ouverte"


class OfferOut(OfferCreate):
    id: str
    created_by: Optional[str] = None
    date_creation: datetime


# ---------------------------------------------------------------------------
# Gestion Candidatures
# ---------------------------------------------------------------------------
class ApplicationCreate(BaseModel):
    offer_id: str
    # Le fichier CV lui-même arrive en multipart, pas dans ce schéma JSON.


class ApplicationOut(BaseModel):
    id: str
    user_id: str
    offer_id: str
    cv_file_id: Optional[str] = None
    score: Optional[float] = None  # rempli par l'ATS IA Engine (Phase 7)
    status: StatutCandidature = "A analyser"
    notes_rh: str = ""
    date_creation: datetime


class ApplicationStatusUpdate(BaseModel):
    status: StatutCandidature
    notes_rh: Optional[str] = None
