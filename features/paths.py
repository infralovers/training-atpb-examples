"""
naviation behave module
"""
class NavigationHelpers():
    """
    map behave strings to uri
    """
    def __init__(self, base_url="http://127.0.0.1:5000"):
        """
        init helper class
        args:
            base_url: base url of unit under test
        """
        self.switch = {
            "the home page": (base_url + "/"),
            "the about page": base_url + "/about",
            "api_health_check": base_url + "/api/health",
            "api_article_create": base_url+"/api/article",
            "api_article_list": base_url+"/api/article"
        }

    def add_mapping(self, name, uri):
        """
        add mapping to helper class
        """
        self.switch[name] = uri

    def path_to(self, page_name):
        """
        map a page_name to an uri
        args:
            page_name: name of page used in behave strings
        returns:
            uri of page
        raises:
            exception if page is not found
        """
        if not self.switch.__contains__(page_name):
            raise Exception(
                "Can\'t find mapping from '{page_name}' - add a mapping in paths.py")

        return self.switch.get(page_name)
