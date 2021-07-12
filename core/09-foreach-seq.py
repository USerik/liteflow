from liteflow.core import *


class Hello(StepBody):
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print("Hello")
        return ExecutionResult.next()


class DoStuff(StepBody):

    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print(f"doing stuff...{context.execution_pointer.context_item}")
        return ExecutionResult.next()


class DoStuff2(StepBody):

    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print(f"doing stuff 2...{context.execution_pointer.context_item}")
        return ExecutionResult.next()
    


class DoStuff3(StepBody):

    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print(f"doing stuff 3...{context.execution_pointer.context_item}")
        return ExecutionResult.next()
class Goodbye(StepBody):
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        print("Goodbye")
        return ExecutionResult.next()

class Data:
    def __init__(self):
        self.list = ["abc", "def", "xyz"]


class MyWorkflow(Workflow):

    def id(self):
        return "MyWorkflow"

    def version(self):
        return 1

    def build(self, builder: WorkflowBuilder):
        builder\
            .start_with(Hello)\
            .for_each_seq(lambda data, context: [1,2,3])\
                .do(lambda x:\
                    x.start_with(DoStuff).then(DoStuff2).then(DoStuff3))\
            .then(Goodbye)


host = configure_workflow_host()
host.register_workflow(MyWorkflow())
host.start()
data = Data()
wid = host.start_workflow("MyWorkflow", 1, None)

input()
host.stop()

