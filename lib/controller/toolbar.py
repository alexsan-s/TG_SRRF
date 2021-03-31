def toolbarMenu(toolbar):
    # ! TOOLBAR MENU
    if toolbar == 'home':
        toolbar_menu = [
            ['File', ['Client', 'Operator', 'Images', 'Training','Import Data', 'Exit']],
            ['Recognition', ['Eigenfaces', 'Fisherface', 'LBPH']]
        ]
    return toolbar_menu