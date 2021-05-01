import PySimpleGUI as sg
from controller.database.crud import *

def screen(find = False):

    # ! toolbar
    if not find:
        toolbar_menu = [
            ['File', ['New', 'Edit', 'Delete', 'Exit']],
        ]
    else:
        toolbar_menu = [
            ['File', ['Exit']],
        ]
    data = readAllProduct()
    header = ['Code','Name', 'Description']
    
    # ! layout
    if not data:
        dataRegister = [
            [sg.Text(text='No register')]
        ]
    else:
        dataRegister = [
            [sg.Table(values=data, headings=header, num_rows=15, row_height=20, max_col_width=60, justification='left', key='tbProduct', enable_events=True, auto_size_columns=False, col_widths=[5,30,40])]
        ]
        if find:
            dataRegister.append([sg.Submit()])

    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Column(dataRegister)],
        [sg.Frame(title='Filter', layout=[
            [sg.InputCombo(['Code', 'Product', 'Promotion'], key='cbmFilter', default_value = 'Product'), sg.Input('', key='lblInput')],
            [sg.Button(button_text='Search'), sg.Button(button_text='Clear')]
        ])]
    ]
    window = sg.Window('Product', layout,size=(800,500))

    while True:
        event, value = window.read(timeout=20)
        
        if event == 'New':
            productNewOld()
            data = readAllProduct()
            window.Element('tbProduct').update(values=data)
        if event == 'Edit':
            productNewOld(window.Element('tbProduct').Values[window.Element('tbProduct').SelectedRows[0]][0])
            data = readAllProduct()
            window.Element('tbProduct').update(values=data)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Delete':
            if deleteProduct(window.Element('tbProduct').Values[window.Element('tbProduct').SelectedRows[0]][0]) == 1:
                data = readAllProduct()
                window.Element('tbProduct').update(values=data)
        if event == 'Search':
                data = readProductFilter(value['cbmFilter'], value['lblInput'])
                window.Element('tbProduct').update(values=data)
        if event == 'Clear':
            data = readAllProduct()
            window.Element('tbProduct').update(values=data)
        if event == 'Submit':
            pk_client = window.Element('tbProduct').Values[window.Element('tbProduct').SelectedRows[0]]
            break
    window.close()
    if find:
        try:
            return pk_client
        except:
            return None


#
# * Function that going to see the screen of product
#
#
def productNewOld(pk_product = None):
    if pk_product != None:
        data            = readProductByPk(pk_product)
        product         = data[0][1]
        description     = data[0][2]
        inactive        = data[0][3]
        promotion       = data[0][4]
        if promotion == 1:
            promotionState = True
        else:
            promotionState = False
        rdInactive      = [sg.Checkbox('Inactive', default=inactive, key='IInactive')]
        btnInsertUpdate = 'Update'
        title           = 'Edit Product {}'.format(product)
    else:
        product            = ''
        description        = ''
        promotionState     = False
        rdInactive         = []
        btnInsertUpdate = 'Register'
        title           = 'New Product'

    # ! LAYOUT
    layout = [
        [sg.Text("Product", size=(10,1), key='lblProduct'), sg.Input(product, key = 'IProduct')],
        [sg.Text("Description", size=(10,1), key='lblDescription'), sg.Multiline(default_text = description, key='IDescription')],
        [sg.Checkbox("Promotion", default=promotionState, key='cbPromotion')],
        rdInactive,
        [sg.HorizontalSeparator()],
        [sg.Button(button_text=btnInsertUpdate), sg.Exit(button_text="Cancel")],
    
    ]
    window = sg.Window(title, layout)


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None or event == 'Cancel':  
            break
        if event == 'Register':
            created = createProduct(values)
            if created == 1:
                window.close()
            elif created == 0:
                sg.Popup('Fail in register')
            elif created == -1:
                sg.Popup('Product invalid')
            elif created == -2:
                sg.Popup('Description invalid')
        if event == 'Update':
            updated = updateProduct(values, pk_product)
            if updated == 1:
                window.close()
            elif updated == 0:
                sg.Popup('Fail in register')
            elif updated == -1:
                sg.Popup('Product invalid')
            elif updated == -2:
                sg.Popup('Description invalid')
    window.close()