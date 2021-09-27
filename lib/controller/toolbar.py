def toolbarMenu(toolbar):
    # ! TOOLBAR MENU
    if toolbar == 'home':
        toolbar_menu = [
            ['File', ['Training','Import Data', 'Setting', 'Logout', 'Exit',]],
            ['View', ['Client', 'Operator', 'Product', 'Images', 'Recognition', ['Eigenfaces', 'Fisherface', 'LBPH'], 'Test Algorithms']],
            ['Insert', ['Buy']]
        ]
    return toolbar_menu