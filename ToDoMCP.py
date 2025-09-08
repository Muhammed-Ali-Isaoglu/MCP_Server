from uuid import uuid4
from typing import List
from pydantic import BaseModel,Field
from mcp.server.fastmcp import FastMCP

todos={}

class Todo(BaseModel):
    id:str
    title:str
    completed:bool =False

class CreateTodo(BaseModel):
    title:str

class GetTodo(BaseModel):
    id:str
class UpdateTodo(BaseModel):
    id:str
    title:str
    completed:bool=None
class DeleteTodo(BaseModel):
    id:str

server=FastMCP('Todo_Tool')

@server.tool(name="create_todo",description="createing Todos")

def create_todo(data:CreateTodo)->Todo:
    todo_id=str(uuid4())
    todo=Todo(id=todo_id,title=data.title)
    todos[todo_id]=todo
    return todo

@server.tool(name="list_todo",description="list all the Todos")
def list_todo()->List[Todo]:
    return list(todos.values())

@server.tool(name="get_todo",description="get todo information")
def get_todo(data:GetTodo)->str:
    todo=todos.get(data.id)
    if not todo:
        raise ValueError(f"Todo with id {data.id} not found")
    return todo
    
@server.tool(name="update_todo",description="update todo information")
def update_todo(data:UpdateTodo)->Todo:
    todo=todos.get(data.id)
    if not todo :
        raise ValueError(f"todo with {todo} not found")
    
    if data.title is not None:
        todo.title=data.title
    if data.completed is not None:
        todo.completed =data.completed

    todo[data.id]=todo
    return todo

@server.tool(name="delete_todo",description="delete todo")
def delete_todo(data:DeleteTodo)->dict:
    if data.id not in todos:
        raise  ValueError(f"todo with {data.id}can't be found")
    del todos[data.id]
    return {"completed":"deleted"}
    # return todo.pop(todo_id) if todo_id is not None 

if __name__=="__main__":
    server.run()