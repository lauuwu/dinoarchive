from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import BlogPost, User
from ..schemas import BlogPostCreate, BlogPostOut
from ..auth_utils import get_current_admin

router = APIRouter(prefix="/blog", tags=["blog"])


def _to_out(post: BlogPost) -> BlogPostOut:
    return BlogPostOut(
        id=post.id,
        title=post.title,
        excerpt=post.excerpt,
        content=post.content,
        image_url=post.image_url,
        created_at=post.created_at,
        author_username=post.author.username,
    )


@router.get("/", response_model=List[BlogPostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()
    return [_to_out(p) for p in posts]


@router.get("/{post_id}", response_model=BlogPostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return _to_out(post)


@router.post("/", response_model=BlogPostOut, status_code=201)
def create_post(
    post: BlogPostCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    new_post = BlogPost(**post.model_dump(), author_id=current_admin.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return _to_out(new_post)


@router.put("/{post_id}", response_model=BlogPostOut)
def update_post(
    post_id: int,
    post: BlogPostCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    existing = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    for key, value in post.model_dump().items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return _to_out(existing)


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    existing = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    db.delete(existing)
    db.commit()
