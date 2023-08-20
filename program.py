import flask
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


# initialization
def inti():
    global menu
    menu = {'101A': ['Brown rice', 50, 45.50, 41.25],
            '102B': ['Whole wheat', 30, 27.45, 21.50],
            '102C': ['Tomato sauce', 25.50, 20.25, 18.70],
            '103D': ['Mustard', 40, 39.45, 37],
            '104E': ['Barbecue sauce', 45, 43, 41.50],
            '105F': ['Red-wine vinegar', 4000, 3800, 3750],
            '106G': ['Salsa', 200, 189.50, 170],
            '107H': ['Extra virgin olive oil', 500, 478.50, 455.70],
            '108I': ['canola oil', 200, 180, 118],
            '109J': ['Hot pepper sauce', 100, 98.50, 91.25],
            '110K': ['Bananas', 60, 55, 50],
            '111L': ['Apples', 300, 250, 120],
            '112M': ['Oranges', 200, 140, 110],
            '113N': ['Mangoes', 100, 80, 50],
            '114O': ['Strawberries', 100, 90, 80],
            '115P': ['Blueberries', 95, 8, 75],
            '116Q': ['Green teas', 250, 225, 200],
            '117R': ['Sparkling water', 20, 14.50, 11],
            '118S': ['Dried apricots', 270, 250, 230],
            '119T': ['Dried figs', 100, 95, 90],
            '120U': ['Dried prunes', 90, 85, 80],
            '121V': ['Almonds', 900, 870, 850],
            '122W': ['Cashews', 1000, 950, 910],
            '123X': ['Walnuts', 800, 770, 720],
            '124Y': ['Peanuts', 400, 380, 360],
            '125Z': ['Pecans', 350, 320, 300],
            '201A': ['Pistachios', 1200, 1180, 1160],
            '202B': ['Sunflower seeds', 150, 112.50, 103.45],
            '203C': ['Sesame seeds', 120.50, 110.25, 101.40],
            '204D': ['Whole flaxseeds', 95.20, 90.45, 89.20]}
    print(pd.Series(menu))

    global outdict
    outdict = {
        "code": [],
        "item": [],
        "quality": [],
        "quantity": [],
        "price": [],
        "customerid": []
    }
    global detials
    detials = {
        "AAA1001": ["Surian", "9500012345"],
        "AAA1002": ["Nila", "9500023456"],
        "AAA1003": ["Arivazhagan", "9712300078"],
        "AAA1004": ["Nithin Kumar", "9586233333"],
        "AAA1005": ["Aravind", "6931245872"]
    }



def tablemake():
    global tablelist
    tabledata = []
    for i in range(len(outdict["code"])):
        tablelist = []
        tablelist.append(i + 1)
        tablelist.append(outdict["code"][i])
        tablelist.append(outdict["item"][i])
        tablelist.append(outdict["quality"][i])
        tablelist.append(outdict["quantity"][i])
        tablelist.append(outdict["price"][i])
        tabledata.append(tablelist)
    return tabledata


def customercheck(id):

    if len(id) == 0:
        return [0, 0]
    else:
        if id[0] in detials.keys():
            return [1, "Valid Customer", id[0]]
        elif id[0] not in detials.keys():
            return [1, "Not a valid Customer"]


@app.route('/')
def index():
    global tempdict
    tempdict = {
        "code": [],
        "item": [],
        "quality": [],
        "quantity": [],
        "price": []
    }
    return render_template('index.html', tablelen=len(tablemake()), tabledata=tablemake(),
                           hide=customercheck(outdict["customerid"])[0],
                           validity=customercheck(outdict["customerid"])[1])


@app.route('/code/', methods=['POST', 'GET'])
def itemname():
    try:
        a = request.form['code']
        item = menu[a][0]
        tempdict["code"].append(a)
        tempdict["item"].append(item)
        return render_template("quality.html", itemname=item, code=a, tablelen=len(tablemake()), tabledata=tablemake(),
                               hide=customercheck(outdict["customerid"])[0],
                               validity=customercheck(outdict["customerid"])[1])
    except:
        return flask.redirect("/error/")

@app.route('/error/')
def error():
    global tempdict
    tempdict = {
        "code": [],
        "item": [],
        "quality": [],
        "quantity": [],
        "price": []
    }
    return render_template('index.html', tablelen=len(tablemake()), tabledata=tablemake(),
                           hide=customercheck(outdict["customerid"])[0],
                           validity=customercheck(outdict["customerid"])[1],errorcode = "Enter correct code")

@app.route('/quality/', methods=['POST', 'GET'])
def quality():
    a = request.form['quality']
    tempdict['quality'].append(a)
    return render_template("quantity.html", itemname=tempdict['item'][0], code=tempdict['code'][0], quality=a,
                           tablelen=len(tablemake()), tabledata=tablemake(),
                           hide=customercheck(outdict["customerid"])[0],
                           validity=customercheck(outdict["customerid"])[1])


@app.route('/quantity/', methods=['POST', 'GET'])
def quantity():
    a = request.form['quantity']
    tempdict['quantity'].append(a)
    itemprice = menu[tempdict['code'][0]][int(tempdict['quality'][0])] * float(a)
    tempdict["price"].append(itemprice)
    return render_template("price.html", itemname=tempdict['item'][0], code=tempdict['code'][0],
                           quality=tempdict['quality'][0], quantity=a, price=itemprice, tablelen=len(tablemake()),
                           tabledata=tablemake(), hide=customercheck(outdict["customerid"])[0],
                           validity=customercheck(outdict["customerid"])[1])


@app.route('/add/', methods=['POST', 'GET'])
def add():
    print("Added item")
    print(tempdict)
    for i in tempdict.keys():
        outdict[i].append(tempdict[i][0])
    return index()


# done


@app.route('/delete/', methods=['POST', 'GET'])
def delete():
    a = request.form['delete']
    outdict['code'].pop(int(a))
    outdict['item'].pop(int(a))
    outdict['quality'].pop(int(a))
    outdict['quantity'].pop(int(a))
    outdict['price'].pop(int(a))
    tablemake()
    return index()


@app.route('/customer/', methods=['POST', 'GET'])
def customer():
    customerid = request.form["id"]
    outdict["customerid"].append(customerid)
    return index()


def finalamount():
    subtotal = sum(outdict["price"])
    id = outdict["customerid"]
    if subtotal > 10000 and customercheck(id)[1] == "Not a valid Customer":
        discountpercent = 1
    elif subtotal > 10000 and customercheck(id)[1] == "Valid Customer":
        discountpercent = 1.2
    else:
        discountpercent = 0
    return [subtotal, discountpercent, (subtotal - subtotal * discountpercent / 100)]


@app.route('/checkout/', methods=['POST', 'GET'])
def checkout():
    outlist = finalamount()
    if len(outdict["customerid"]) == 0:
        customername = ""
        phonenumber = ""
    elif len(customercheck(outdict["customerid"][0])) == 3:
        customername = detials[outdict["customerid"][0]][0]
        phonenumber = detials[outdict["customerid"][0]][1]
    else:
        customername = "No Data"
        phonenumber = "No Data"
    return render_template("bill.html", tablelist=tablemake(), subtotal=outlist[0], discount=outlist[1],
                           total=outlist[2],customername = customername,phonenumber = phonenumber)


@app.route('/done/', methods=['POST', 'GET'])
def done():
    inti()
    tablemake()
    return index()


if __name__ == '__main__':
    inti()
    tablemake()
    app.run(debug=False)
