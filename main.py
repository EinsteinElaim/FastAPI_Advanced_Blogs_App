# Importing parts to be used to create our app, routes, route, error handling and our SQLAlchemy Session
# to define SessionLocal type in our DEPENDENCY
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

# Now, we integrate and use all partd we created before
# importing our package dependencies for creating our database tables for first step
# from . import crud, models, schemas
import crud as crud
import models as models
import schemas as schemas
# imports to use with second step of creating a Dependency using our SessionLocal class created in our database py file
from database import SessionLocal, engine

# First, create our database tables
models.Base.metadata.create_all(bind=engine)


# Initialising our app
app = FastAPI()


# Second, create a Dependency that makes use of the SessionLocal class to give us
# an independent database session/connection ('SessionLocal') per request
# We utilise this same session throughout our requests and close it after the request is finished
# and a new session will be created for the next request
# For this, we need to create a new dependency with 'yield'
# Our dependency will create a new SQLAlchemy 'SessionLocal' that will be used in a single request,
# and then close it once the request is finished
def get_db():
    # We are creating the database session before each request in the dependency with 'yield' and then closing it afters
    # Now we can create the required dependency in the *path operation function* to get that session directly
    db = SessionLocal()
    # we put the creation of the 'SessionLocal' in  'try' block and then finally close it in a 'finally' block
    try:
        yield db
    finally:
        db.close()


# THREE: PATH OPERATIONS
#
# Now, inside path operation function, we use the DEPENDENCY created 'db' in 'get_db()' function by
# declaring the 'db' parameter with the 'Session' we imported directly from SQLAlchemy
# This gives us better editor support since the editor will know that the 'db' parameter
# is of corresponding SQLAlchemy type 'Session' from 'SessionLocal' originally in the database py file

#
#
# IMPORTANT
#
# The values we return from these path operations/ routes are SQLAlchemy models or Lists of SQLAlchemy models
# But, since all path operations have a response model with Pydantic models/ schemas using 'orm_mode',
# the data declared in our Pydantic models/schemas will be extracted from them
# and returned to the client with all filtering and validation done from the function in the path operations
#
# Also notice that there are `response_models` that have standard Python types like `List[schemas.Item]`.
# But as the content/parameter of that `List` is a Pydantic *model* with `orm_mode`,
# the data will be retrieved and returned to the client as normally, without problems.
#
#


# Basic home route
@app.get("/", response_model=dict)
def home():
    return {"Home": "Welcome home!"}


# USER CLASSES ROUTES AND PATH OPERATIONS HANDLING:
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user


@app.get("/users/{user_email}", response_model=schemas.User)
def read_user(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user


# ITEM CLASSES ROUTES AND PATH OPERATIONS
@app.post("/items/create/{user_id}", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_tite(db=db, item_title=item.title)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists! Change The Item Title!")
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# Read all items from all users
@app.get("/items/user", response_model=list[schemas.Item])
def read_items(limit: int = 100, skip: int = 0, db: Session = Depends(get_db)):
    db_items = crud.get_all_items(skip=skip, limit=limit, db=db)
    if db_items is None:
        raise HTTPException(status_code=404, detail="Items not found!")
    return db


# Read user specific items


# BLOG CLASSES ROUTES AMD PATH OPERATIONS
@app.post("/blogs/user/{user_id}", response_model=schemas.Blog)
def create_blog(blog: schemas.BlogCreate, user_id: int, db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_title(db=db, blog_title=blog.title)
    if db_blog:
        raise HTTPException(status_code=400, detail="Blog already Exists! Change blog title and try again!")
    return crud.create_user_blog(owner_id=user_id, blog=blog, db=db)


# Read all blog posts from all users
@app.get("/blogs/", response_model=list[schemas.Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_blog = crud.get_all_blogs(skip=skip, limit=limit, db=db)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="No blogs found! Create new blogs to view them!")
    return db_blog
