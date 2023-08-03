from botcity.core import DesktopBot
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *


class Bot(DesktopBot):
    def action(self, execution=None):
        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens the BotCity website.
        self.browse("http://www.google.com")
        self.wait(5000)
        self.paste('Keyword Tools')
        self.enter(1000)

        for element in self.find_all( "anuncio", matching=0.97, waiting_time=10000):
            print(f'Element found: {element}')
            self.wait(1000)
            self.right_click()
            # self.right_click_at(element[0], element[1])
            # self.wait(500)
            self.move_relative(-50, -50)
            self.wait(1000)
            self.type_down()
            self.enter()
        # else:
            # self.not_found("anuncio")

        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()



