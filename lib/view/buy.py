import PySimpleGUI as sg
from controller.database import crud
from controller import function

def screenBuy():
    headingTable = ['Cod', 'Product', 'Quantity']
    product = crud.readAllProduct()
    namesProduct = []
    productAdd = []
    selectedClient = []
    selectedProduct = []
    pk_client = None
    for k in product:
        namesProduct.append(k[1])
        

    # ! toolbar
    toolbar_menu = [
        ['File', ['Exit']],
        ['Edit', ['Delete Product']],
    ]

    dataRegister = [
            [sg.Table(values=productAdd, headings=headingTable, num_rows=18, row_height=20, max_col_width=40, justification='left', key='tbProduct', enable_events=True,auto_size_columns=False, col_widths=[10, 40, 10])]
        ]

    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Text("Client", size=(10,1), key='lblClient'), sg.Input(key='IClient'), sg.Button('Find', key='btnFindClient')],
        [sg.Text("Product", size=(10,1), key='lblProduct'), sg.Input(key='IProduct'), sg.Button('Find', key='btnFindProduct')],
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
            if values['IProduct']:
                try:
                    if not selectedProduct:
                        selectedProduct = crud.readProductByPk(values['IProduct'])[0]
                    if function.validadeNumber(values['IQuantity']):
                        if int(values['IQuantity']) >= int(1):
                            count = 0
                            for k in productAdd:
                                if k[0] == selectedProduct[0]:
                                    k[2] = int(k[2]) + 1
                                    count = 1
                            if count == 0:
                                productAdd.append([selectedProduct[0], selectedProduct[1], int(values['IQuantity'])])
                            window.Element('tbProduct').Update(values = productAdd)
                        else:
                            sg.Popup('Just numbers greater than zero')
                    else:
                        sg.Popup('Quatity is just number')
                    selectedProduct = []
                    # else:
                    #     sg.Popup('Chose a product'
                except:
                    sg.Popup('Fail to found the product')                
            else:
                sg.Popup('Inout the product')


        if event == 'Submit':
            try:
                if not selectedClient:
                    selectedClient = crud.readClientByPk(values['IClient'])[0]
                result = crud.insertPurchases(selectedClient[0], productAdd)
                if result == 1:
                    sg.Popup('Register suceffuly')
                else:
                    sg.Popup('Fail to register')
            except:
                sg.Popup('Fail to register')
        if event == 'btnFindClient':
            from view import client
            selectedClient = client.screenClient(find = True)
            window.Element('IClient').Update(value=selectedClient[1])
        if event == 'btnFindProduct':
            from view import product
            selectedProduct = product.screen(find = True)
            if selectedProduct:
                window.Element('IProduct').Update(value=selectedProduct[1])
            

    window.close()
    