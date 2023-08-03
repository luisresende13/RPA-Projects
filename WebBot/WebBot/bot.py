from botcity.web import WebBot, Browser
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *


class Bot(WebBot):
    def action(self, execution=None):
        print('Web bot action started!')
        # Configure whether or not to run on headless mode
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        # self.browser = Browser.FIREFOX

        # Uncomment to set the WebDriver path
        # self.driver_path = "./chromedriver.exe"

        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens a website.
        print('About to open browser.')
        self.browse("https://www.google.com")
        self.paste('Cientista de dados')
        self.enter()

        # Wait for 10 seconds before closing
        # self.wait(4000)
        # Stop the browser and clean up
        # self.stop_browser()

        print('Web bot action about to finish!')
        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )
        # print('Headless bot task finished!')

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()








