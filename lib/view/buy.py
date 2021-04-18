import PySimpleGUI as sg
from controller.database import crud
from controller import function

def screenBuy():
    headingTable = ['Product', 'Quantity']
    client = crud.readAllClient()
    product = crud.readAllProduct()
    namesClient = []
    namesProduct = []
    productAdd = []
    print(productAdd)
    for k in client:
        namesClient.append(k[1])
    for k in product:
        namesProduct.append(k[1])
        

    # ! toolbar
    toolbar_menu = [
        ['File', ['Exit']],
        ['Edit', ['Delete Product']],
    ]

    dataRegister = [
            [sg.Table(values=productAdd, headings=headingTable, num_rows=18, row_height=20, max_col_width=40, justification='left', key='tbProduct', enable_events=True,auto_size_columns=False, col_widths=[40, 10])]
        ]

    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Text("Client", size=(10,1), key='lblClient'), sg.Combo(namesClient, key='cmbClient', size=(50,1), readonly=True)],
        [sg.Text("Product", size=(10,1), key='lblProduct'), sg.Combo(namesProduct, key='cmbProduct', size=(50,1), readonly=True)],
        [sg.Text("Quantity", size=(10,1), key='lblQuantity'), sg.Input('1', key = 'IQuantity')],
        [sg.Submit("Add")],
        [sg.Column(dataRegister)],
        [sg.Cancel(), sg.Submit()]
    ]

    window = sg.Window('Buy', layout)

    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None or event == 'Cancel' or event == 'Exit':  
            break
        if event == 'Add':
            if function.validadeNumber(values['IQuantity']):
                if int(values['IQuantity']) >= int(1):
                    count = 0
                    for k in productAdd:
                        if k[0] == values['cmbProduct']:
                            k[1] = int(k[1]) + 1
                            count = 1
                    if count == 0:
                        productAdd.append([values['cmbProduct'], values['IQuantity']])
                    window.Element('tbProduct').Update(values = productAdd)
                else:
                    sg.Popup('Just numbers greater than zero')
            else:
                sg.Popup('Quatity is just number')
            # else:
            #     sg.Popup('Chose a product')

        if event == 'Submit':
            for k in productAdd :
                if int(k[1]) > 1:
                    for x in range(0, int(k[1])):
                        print(k[0])
                print(k[0])

    window.close()
    