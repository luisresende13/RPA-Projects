from botcity.web import WebBot, Browser
# from botcity.web.browsers.edge import default_options, default_capabilities
from botcity.web.browsers.chrome import default_options, default_capabilities
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *

#

keyword_for_search = 'Cursos online'

def center_of(element):
    return {'x': element[0]+element[2]/2, 'y': element[1]+element[3]/2}

class Bot(WebBot):
    def action(self, execution=None):
        self.headless = False
        self.browser = Browser.CHROME
        # self.driver_path = "./msedgedriver.exe"
        self.driver_path = "./chromedriver.exe"
        self.options = default_options(
            headless=self.headless,
            download_folder_path=self.download_folder_path,
            user_data_dir="C:\\Users\\luisr\\Desktop" # Informing None here will generate a temporary directory
        )
        self.capabilities = default_capabilities()

        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens the BotCity website.
        self.browse("http://www.google.com")
        self.wait(1000)
        self.maximize_window()
        self.wait(1000)
        self.paste(keyword_for_search)
        self.enter()
        self.wait(1000)
        
        i=-1
        for element in self.find_all( "anuncio", matching=0.97, waiting_time=10000):
            i+=1; print(f'Opening screen element {i} -> {element}')
            self.set_current_element(element)
        #     self.right_click(1000)
        #     self.type_down()
        #     self.enter()
            # if not self.find( "nova_guia", matching=0.97, waiting_time=10000):
            #     self.not_found("nova_guia")
            # else: self.click()
            



        # self.not_found("anuncio")
        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

        # Wait for 10 seconds before closing
        self.wait(10000)

        # Stop the browser and clean up
        # self.stop_browser()
        print('Landing page search task finished!')

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()


