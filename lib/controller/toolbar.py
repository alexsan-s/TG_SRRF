def toolbarMenu(toolbar):
    # ! TOOLBAR MENU
    if toolbar == 'home':
        toolbar_menu = [
            ['File', ['Client', 'Operator', 'Product', 'Images', 'Training','Import Data', 'Logout', 'Exit',]],
            ['Recognition', ['Eigenfaces', 'Fisherface', 'LBPH']]
        ]
    return toolbar_menu