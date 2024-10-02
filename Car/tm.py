#tm.py
from pyscript.js_modules import teach

async def run_model(URL2):
    s = teach.s  # or s = pose.s
    s.URL2 = URL2
    await s.init()     

def get_predictions(num_classes):
    predictions = []
    for i in range (0,num_classes):
        divElement = document.getElementById('class' + str(i))
        if divElement:
            divValue = divElement.innerHTML
            predictions.append(divValue)
    return predictions


import asyncio
await run_model("https://teachablemachine.withgoogle.com/models/P4Vc9NhaJ/")

while True:
    predictions = get_predictions(2)