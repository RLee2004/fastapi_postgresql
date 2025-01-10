from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from typing import List
from database import *
from schema import *
import bcrypt

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
    
#Create category
@app.post("/category/", response_model=Category)
def create_category(category: CategoryCreate, session: SessionDep):
    try:
        add_category = Category.model_validate(category)
        session.add(add_category)
        session.commit()
        session.refresh(add_category)
        return add_category
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    
#Read categories
@app.get("/category/", response_model=List[Category])
def read_categories(session: SessionDep):
    category = session.exec(select(Category)).all()
    return category
#Read category
@app.get("/category/{category_id}", response_model=Category)
def read_category(category_id: int, session: SessionDep):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#Update category
@app.patch("/category/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate, session: SessionDep):
    category_db = session.get(Category, category_id)
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        category_data = category.model_dump(exclude_unset=True)
        category_db.sqlmodel_update(category_data)
        session.add(category_db)
        session.commit()
        session.refresh(category_db)
        return category_db
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    
#Delete category
@app.delete("/category/{category_id}")
def delete_category(category_id: int, session: SessionDep):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully"}



#Create user
@app.post("/user/", response_model=User)
def create_user(user: UserCreate, session: SessionDep):
    try:
        salt = bcrypt.gensalt()
        user.Password = bcrypt.hashpw(user.Password.encode('utf-8'), salt)

        user_dict = user.model_dump()
        user_dict['RegisteredOn'] = datetime.now()
        user_dict['Password'] = user.Password.decode('utf-8')
        add_user = User.model_validate(user_dict)
        session.add(add_user)
        session.commit()
        session.refresh(add_user)
        return add_user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    
#Read users
@app.get("/user/", response_model=List[UserRead])
def read_users(session: SessionDep):
    user = session.exec(select(User)).all()
    return user

@app.get("/user/{UserID}", response_model=UserRead)
def read_user(UserID: int, session: SessionDep):
    user = session.get(User, UserID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#Update user
@app.patch("/user/{UserID}", response_model=UserUpdate)
def update_user(UserID: int, user: UserUpdate, session: SessionDep):
    user_db = session.get(User, UserID)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user_data = user.model_dump(exclude_unset=True)
        if "Password" in user_data:
            salt = bcrypt.gensalt()
            user_data["Password"] = bcrypt.hashpw(user_data['Password'].encode('utf-8'), salt).decode('utf-8')
        user_db.sqlmodel_update(user_data)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    
#Delete user
@app.delete("/user/{UserID}")
def delete_user(UserID: int, session: SessionDep):
    user = session.get(User, UserID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}


#Create topic
@app.post("/topic/", response_model=Topic)
def create_topic(topic: TopicCreate, session: SessionDep):
    try:
        topic_dict = topic.model_dump()
        topic_dict['CreatedOn'] = datetime.now()
        add_topic = Topic.model_validate(topic)
        
        session.add(add_topic)
        session.commit()
        session.refresh(add_topic)
        return add_topic
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))

#Read topics
@app.get("/topic/", response_model=List[Topic])
def read_topics(session: SessionDep):
    topic = session.exec(select(Topic)).all()
    return topic
    
@app.get("/topic/{TopicID}", response_model=Topic)
def read_topic(TopicID: int, session: SessionDep):
    topic = session.get(Topic, TopicID)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

#Update topic
@app.patch("/topic/{TopicID}", response_model=Topic)
def update_topic(TopicID: int, topic: TopicUpdate, session: SessionDep):
    topic_db = session.get(Topic, TopicID)
    if not topic_db:
        raise HTTPException(status_code=404, detail="Topic not found")
    try:
        topic_data = topic.model_dump(exclude_unset=True)
        topic_db.sqlmodel_update(topic_data)
        session.add(topic_db)
        session.commit()
        session.refresh(topic_db)
        return topic_db
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))

#Delete topic
@app.delete("/topic/{TopicID}")
def delete_topic(TopicID: int, session: SessionDep):
    topic = session.get(Topic, TopicID)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    session.delete(topic)
    session.commit()
    return {"message": "Topic deleted successfully"}

#Create post
@app.post("/post/", response_model=Post)
def create_post(post: PostCreate, session: SessionDep):
    try:
        if post.ParentPostID == 0:
            post.ParentPostID = None
        
        post_dict = post.model_dump()
        post_dict['CreatedOn'] = datetime.now()
        post_dict['ModifiedOn'] = datetime.now()
        add_post = Post.model_validate(post)
        
        session.add(add_post)
        session.commit()
        session.refresh(add_post)
        return add_post
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    
#Read posts
@app.get("/post/", response_model=List[Post])
def read_posts(session: SessionDep):
    post = session.exec(select(Post)).all()
    return post

@app.get("/post/{PostID}", response_model=Post)
def read_post(PostID: int, session: SessionDep):
    post = session.get(Post, PostID)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

#Update post
@app.patch("/post/{PostID}", response_model=Post)
def update_post(PostID: int, post: PostUpdate, session: SessionDep):
    post_db = session.get(Post, PostID)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        post_data = post.model_dump(exclude_unset=True)
        post_data['ModifiedOn'] = datetime.now()
        post_db.sqlmodel_update(post_data)
        session.add(post_db)
        session.commit()
        session.refresh(post_db)
        return post_db
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(e))

#Delete post
@app.delete("/post/{PostID}")
def delete_post(PostID: int, session: SessionDep):
    post = session.get(Post, PostID)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"message": "Post deleted successfully"}