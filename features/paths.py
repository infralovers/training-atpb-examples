import re

class NavigationHelpers():
    def path_to(self, page_name):
        switch = {
            "the home page": "http://127.0.0.1:5000/",
            "the about page": "http://127.0.0.1:5000/about",
            "api_health_check": "http://127.0.0.1:5000/api/health"
        }
        if switch.get(page_name) != None:
            return(switch.get(page_name))
        else:
            raise Exception("Can't find mapping from \"#{page_name}\" to a path.\n" +
                    "Now, go and add a mapping in paths.py")