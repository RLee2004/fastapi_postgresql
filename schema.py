from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, select
from datetime import datetime

class CategoryBase(SQLModel):
    CategoryName: str
    CategoryDescription: str

class Category(CategoryBase, table=True):
    __tablename__ = "Category"
    CategoryID: int = Field(default=None, primary_key=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    CategoryName: Optional[str]
    CategoryDescription: Optional[str]


class UserBase(SQLModel):
    DisplayName: str
   
class User(UserBase, table=True):
    __tablename__ = "User"
    UserID: int = Field(default=None, primary_key=True)
    Email: str
    Password: str
    IsBanned: bool = False
    IsModerator: bool = False
    IsAdministrator: bool = False
    RegisteredOn: datetime = Field(default_factory = datetime.now)
    
class UserCreate(UserBase):
    Email: str
    Password: str

class UserRead(UserBase):
    UserID: int
    DisplayName: str

class UserUpdate(UserBase):
    DisplayName: Optional[str] = Field(default ="")
    Email: Optional[str] = Field(default ="")
    Password: Optional[str] = Field(default ="")
    IsBanned: Optional[bool] = False
    IsModerator: Optional[bool] = False
    IsAdministrator: Optional[bool] = False


class TopicBase(SQLModel):
    TopicName: str
    
class Topic(TopicBase, table=True):
    __tablename__ = "Topic"
    TopicID: int = Field(default=None, primary_key=True)
    AuthorUserID: int = Field(foreign_key="User.UserID")
    CategoryID: int = Field(foreign_key="Category.CategoryID")
    CreatedOn: datetime = Field(default_factory = datetime.now)
    IsPinned: bool = False

class TopicCreate(TopicBase):
    AuthorUserID: int = Field(foreign_key="User.UserID")
    CategoryID: int = Field(foreign_key="Category.CategoryID")

class TopicUpdate(TopicBase):
    TopicName: Optional[str] = Field(default ="")
    IsPinned: Optional[bool] = False


class PostBase(SQLModel):
    PostContent: str
   
    
class Post(PostBase, table=True):
    __tablename__ = "Post"
    PostID: int = Field(default=None, primary_key=True)
    Rating: int = Field(default=0)
    TopicID: int = Field(foreign_key="Topic.TopicID")
    ParentPostID: Optional[int] = Field(foreign_key="Post.PostID")
    AuthorUserID: int = Field(foreign_key="User.UserID")
    CreatedOn: datetime = Field(default_factory = datetime.now)
    ModifiedOn: datetime = Field(default_factory = datetime.now)

class PostCreate(PostBase):
    TopicID: int = Field(foreign_key="Topic.TopicID")
    ParentPostID: Optional[int] = Field(foreign_key="Post.PostID")
    AuthorUserID: int = Field(foreign_key="User.UserID")

class PostUpdate(PostBase):
    Rating: Optional[int] = Field(default=0)
    PostContent: Optional[str] = Field(default ="")
