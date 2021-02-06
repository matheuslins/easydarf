from src.core.request import RequestHandler


class LoginHandler(RequestHandler):
    response = None
    selector = None
    login_data = {}
    keys_to_extract = {}

    def start_login(self):
        # self.selector = BeautifulSoup(self.response, 'html.parser')
        # self.extract_values()
        pass

    def extract_values(self):
        for key, extraction_value in self.keys_to_extract.items():
            # data = self.selector.find_all(**extraction_value["params"])
            data_extracted = extraction_value["method_to_extract"](data)
            self.login_data.update(
                **{key: data_extracted}
            )
