import base64
from fastapi import FastAPI, Header, Body
import json
import uvicorn
from pydantic import BaseModel

app = FastAPI()

@app.get("/api")
def read_root():
    return "This is a shop api"


@app.post("/api/role")
def checklp(Authorization: str = Header()) -> dict:

    login, password = base64.b64decode(Authorization.replace("Basic ", "").encode()).decode().split(":")

    with open("users_data.json") as f:
        try:
            json_file = json.load(f)
            f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError":"Something wet wrong"}
    try:
        user = json_file[login]
    except Exception:
        return {"UserError":"UserNotFound"}
    if password == user["password"]:
        role = str(user["role"])
        return {"Role": role}
    return {"UserError":"IncorrectPassword"}

@app.get("/api/goods")
def show_goods() -> dict:
    try:
        with open("goods_data.json") as f:
            goods = json.load(f)
            f.close()
    except Exception as e:
        print(e)
        f.close()
        return {"FileError": "Something wet wrong"}
    return goods

@app.delete("/api/goods/{id}")
def delete_good(id: int, Authorization: str = Header()) -> dict:
    if checklp(Authorization) == {"UserError":"UserNotFound"} or checklp(Authorization) == {"UserError":"IncorrectPassword"}:
        return checklp(Authorization)
    elif checklp(Authorization)["Role"] == "MANAGER":
        return {"RoleError": "You don't have permission"}

    id = str(id)
    try:
        with open("goods_data.json") as f:
            goods = json.load(f)
            print(goods)
            f.close()
    except Exception as e:
        print(e)
        f.close()
        return {"FileError": "Something wet wrong"}
    try:
        del goods[id]
        print(goods)
        try:
            with open("goods_data.json", "w") as f:
                g = str(goods)
                g = g.replace("\'", "\"")
                print(g)
                f.write(g)
                f.close()


                return {"Result": "sucsess!"}
        except Exception as e:

            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}
    except Exception:
        return {"GoodNotFoundError": "Incrorrect id"}

class Good_data(BaseModel):
    name: str
    description: str
    price: int|float


@app.post("/api/goods")
def add_good(Authorization: str = Header(), good_data: Good_data = Body()) -> dict:
    # Check for ADMIN rights
    if checklp(Authorization) == {"UserError":"UserNotFound"} or checklp(Authorization) == {"UserError":"IncorrectPassword"}:
        return checklp(Authorization)
    elif checklp(Authorization)["Role"] == "MANAGER":
        return {"RoleError": "You don't have permission"}
    elif checklp(Authorization)["Role"] == "ADMIN":
        # Open file and convert to json
        try:
            with open("goods_data.json") as f:
                goods: dict = json.load(f)

                f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}

        # Choose the next id fo good
        new_id = str(int(list(goods.keys())[-1]) + 1)

        # Add the good
        goods[new_id] = {"name": good_data.name, "description": good_data.description, "price": good_data.price}

        try:
            with open("goods_data.json", "w") as f:
                goods = str(goods).replace("'", '"')
                f.write(goods)
                f.close()
        except Exception:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}
        return {"Result": "sucsess!"}


@app.put("/api/goods/{id}")
def edit_good(id: int, Authorization: str = Header(), new_data: Good_data = Body()) -> dict:
    # Check for MANAGER or ADMIN rights
    a = checklp(Authorization=Authorization)
    if a == {"UserError":"UserNotFound"} or a == {"UserError":"IncorrectPassword"}:
        return a

    elif a["Role"] == "MANAGER" or a["Role"] == "ADMIN":
        # Open file and convert to json
        try:
            with open("goods_data.json") as f:
                goods: dict = json.load(f)

                f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}

        try:
            current_good = goods[str(id)]
        except Exception:
            return {"IdError": "Incorrect id"}

        new_data = {"name": new_data.name, "description": new_data.description, "price": new_data.price}
        goods[str(id)] = new_data

        try:
            with open("goods_data.json", "w") as f:
                goods = str(goods).replace("'", '"')
                f.write(goods)
                f.close()
        except Exception as e:
            f.close()
            print(e)
            return {"FileError": "Something wet wrong"}

        return {"Result": "sucsess!"}

@app.post("/api/basket")
def add_to_basket(id: int, basketid: int = None) -> dict:
    if basketid == None:
        try:
            with open("orders_data.json") as f:
                orders: dict = json.load(f)
                f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}


        try:
            with open("goods_data.json") as f:
                goods: dict = json.load(f)

                f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}

        try:
            goods[str(id)]
        except Exception:
            return {"IdError": "Incorrect id"}


        new_id = str(int(list(orders.keys())[-1]) + 1)
        orders[new_id] = {"status": 0, "in": [str(id)], "email": ""}


        try:
            with open("orders_data.json", "w") as f:
                orders = str(orders).replace("'", '"')
                f.write(orders)
                f.close()
        except Exception as e:
            f.close()
            print(e)
            return {"FileError": "Something wet wrong"}

        return {"Result": "sucsess!", "New basket id": int(new_id)}


    else:
        try:
            with open("orders_data.json") as f:
                orders: dict = json.load(f)
                f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}
        try:
            with open("goods_data.json") as f:
                goods: dict = json.load(f)

                f.close()
        except Exception as e:
            print(e)
            f.close()
            return {"FileError": "Something wet wrong"}

        try:
            goods[str(id)]
        except Exception:
            return {"IdError": "Incorrect id"}
        id = str(id)
        try:
            if id in orders[str(basketid)]["in"]:
                return {"OrderError": "you already have this good in your basket"}
            elif orders[str(basketid)]["status"] == 0:
                orders[str(basketid)]["in"].append(id)
            elif orders[str(basketid)]["status"] == 1:
                return {"OrderError": "You can't add a good when you confirmed your order"}
        except Exception:

            return {"IdError": "Incorrect id"}

        try:
            with open("orders_data.json", "w") as f:
                orders = str(orders).replace("'", '"')
                f.write(orders)
                f.close()
        except Exception as e:
            f.close()
            print(e)
            return {"FileError": "Something wet wrong"}
        return {"Result": "sucsess!"}


@app.delete("/api/basket")
def delete_from_basket(id: int, basketid: int) -> dict:
    try:
            with open("orders_data.json") as f:
                orders: dict = json.load(f)
                f.close()
    except Exception as e:
        print(e)
        f.close()
        return {"FileError": "Something wet wrong"}


    id = str(id)
    try:
        if orders[str(basketid)]["status"] == 0:
            orders[str(basketid)]["in"].remove(id)
        else:
            return {"OrderError": "You can't delete a good when you confirmed your order"}
    except Exception:
        return {"IdError": "Incorrect id"}

    try:
        with open("orders_data.json", "w") as f:
            orders = str(orders).replace("'", '"')
            f.write(orders)
            f.close()
    except Exception as e:
        f.close()
        print(e)
        return {"FileError": "Something wet wrong"}
    return {"Result": "sucsess!"}


@app.post("/api/order/")
def confirm_order(email: str, basketid: int) -> dict:
    try:
            with open("orders_data.json") as f:
                orders: dict = json.load(f)
                f.close()
    except Exception as e:
        print(e)
        f.close()
        return {"FileError": "Something wet wrong"}


    try:
        if orders[str(basketid)]["status"] == 0:
            orders[str(basketid)]["status"] = 1
            orders[str(basketid)]["email"] = email
        else:
            return {"OrderError": "You have already confirmed your order"}
    except Exception:
        return {"IdError": "Incorrect id"}


    try:
            with open("orders_data.json", "w") as f:
                orders = str(orders).replace("'", '"')
                f.write(orders)
                f.close()
    except Exception as e:
        f.close()
        print(e)
        return {"FileError": "Something wet wrong"}


    return {"Info": "sucsessfully confirmed your order"}

@app.get("/api/basket/{basketid}")
def show_basket(basketid: int):
    try:
            with open("orders_data.json") as f:
                orders: dict = json.load(f)
                f.close()
    except Exception as e:
        print(e)
        f.close()
        return {"FileError": "Something wet wrong"}


    try:
            with open("goods_data.json") as f:
                goods: dict = json.load(f)

                f.close()
    except Exception as e:
        print(e)
        f.close()
        return {"FileError": "Something wet wrong"}



    try:
        basketgoodsid = orders[str(basketid)]["in"]
    except Exception:
        return {"IdError": "Incorrect id"}
    goodstoshow = {}
    for gid in basketgoodsid:
        goodstoshow[gid] = goods[gid]


    return goodstoshow



if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)