class NavigationHelpers():

    def __init__(self, base_url="http://127.0.0.1:5000"):

        self.switch = {
            "the home page": (base_url + "/"),
            "the about page": base_url + "/about",
            "api_health_check": base_url + "/api/health",
            "api_article_create": base_url+"/api/article",
            "api_article_list": base_url+"/api/article"
        }

    def path_to(self, page_name):
        if not self.switch.__contains__(page_name):
            raise Exception(
                "Can\'t find mapping from '{page_name}' - add a mapping in paths.py")

        return self.switch.get(page_name)
