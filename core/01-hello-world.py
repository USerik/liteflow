from liteflow.core import *
import logging
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.level = logging.INFO


class Hello(StepBody):
    def __init__(self):
        self.name = self.__str__

    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print("Hello world")
        return ExecutionResult.next()


class Goodbye(StepBody):
    def __init__(self):
        self.in_param: str = ""

    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print("Goodbye")
        raise Exception("Custom error")
        return ExecutionResult.next()


class MyWorkflow(Workflow):

    def id(self):
        return "MyWorkflow"

    def version(self):
        return 1

    def build(self, builder: WorkflowBuilder):
        builder\
            .start_with(Hello)\
            .then(Goodbye)


host = configure_workflow_host()
host.register_workflow(MyWorkflow())
host.start()

wid = host.start_workflow("MyWorkflow", 1, None)

input()
host.stop()
