from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    # prefix="/blog",
    tags=["blogs"],
)

@router.get("/blogs/", response_model=List[schemas.PostResponse])
def read_blogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blogs = db.query(models.Post).offset(skip).limit(limit).all()
    return blogs

@router.post("/blogs/", response_model=schemas.PostResponse)
def create_blog(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    
    existing_post = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id,
        models.Post.content == post.content
    ).first()

    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a post with the same content"
        )
    new_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id,
        tags=",".join(post.tags),
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    new_post.tags = new_post.tags.split(",") if new_post.tags else []
    return new_post


@router.get("/posts/me")
def get_my_posts(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Post).filter(
        models.Post.owner_id == current_user.id
    ).all()

@router.get("/blogs/{post_id}", response_model=schemas.PostResponse, dependencies=[Depends(get_current_user)])
def read_blog(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


# @router.put("/blogs/{post_id}", response_model=schemas.PostResponse, dependencies=[Depends(get_current_user)])
# def update_blog(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
#     db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     if post.title is not None:
#         db_post.title = post.title
#     if post.content is not None:
#         db_post.content = post.content
#     if post.tags is not None:
#         db_post.tags = post.tags
#     db.commit()
#     db.refresh(db_post)
#     return db_post

@router.put("/blogs/{post_id}", response_model=schemas.PostResponse)
def update_blog(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    #
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this post"
        )

    # 
    if post.content is not None:
        existing_post = db.query(models.Post).filter(
            models.Post.owner_id == current_user.id,
            models.Post.content == post.content,
            models.Post.id != post_id
        ).first()

        if existing_post:
            raise HTTPException(
                status_code=400,
                detail="Duplicate content not allowed"
            )

        db_post.content = post.content

    if post.title is not None:
        db_post.title = post.title

    if post.tags is not None:
        db_post.tags = ",".join(post.tags)

    db.commit()
    db.refresh(db_post)

    return db_post





# @router.delete("/blogs/{post_id}", dependencies=[Depends(get_current_user)])
# def delete_blog(post_id: int, db: Session = Depends(get_db)):
#     db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not db_post:
#         raise HTTPException(status_code=404, detail="Post not found")

#     db.delete(db_post)
#     db.commit()
#     return {"detail": "Post deleted"}
@router.delete("/blogs/{post_id}")
def delete_blog(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this post"
        )

    db.delete(db_post)
    db.commit()

    return {"detail": "Post deleted successfully"}
