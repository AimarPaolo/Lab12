import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(f"{i}"))
        countries = self._model.getRetailers()
        for coun in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(f"{coun}"))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        country = self._view.ddcountry.value
        year = self._view.ddyear.value
        if year is None or country is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare delle opzioni nei dropdown!!"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._model.buildGraph(year, country)
        nEdges = self._model.getNumEdges()
        nNodes = self._model.getNumNodes()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi"))
        self._view.btn_volume.disabled = False
        self._view.update_page()



    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        volume = self._model.getVolumeVendita()
        ordinato = dict(sorted(volume.items(), key=lambda item: item[1], reverse=True))
        for (key, value) in ordinato.items():
            nome = self._model._idMap[key].Retailer_name
            self._view.txtOut2.controls.append(ft.Text(f"{nome} --> {value}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        lunghezza = self._view.txtN.value
        try:
            lunghezza_int = int(lunghezza)
            if lunghezza_int < 2:
                self._view.txtOut3.controls.append(ft.Text("ERRORE, hai inserito un intero troppo piccolo!!"))
                self._view.update_page()
                return
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("ERRORE, hai inserito una stringa e non un intero!!"))
            self._view.update_page()
            return
        cammino_mejor, peso_mejor = self._model.getCamminoOttimo(lunghezza_int)
        print(cammino_mejor, peso_mejor)
        self._view.txtOut3.controls.append(ft.Text("Peso cammino massimo: "))

        self._view.update_page()
