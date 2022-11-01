import argparse
import inspect
from pprint import pprint

from strategies.StrategyExecutor import Executor
import strategies.strategies as Strategies


class ArgParser:
    @staticmethod
    def classes_in_module(module):
        """
        Returns a list of classes in a module. Classes are returned as a list of tuples.
        Each tuple contains the class name, the class docstring, and the class parameters expected.
        md = module
        c = class
        s = strategy
        """
        md = module.__dict__
        all_strategy_obj = [md[c] for c in md if (isinstance(md[c], type) and md[c].__module__ == module.__name__)]
        return [(s.__name__, s.__doc__, [k for k in inspect.signature(s).parameters.keys()]) for s in all_strategy_obj]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"""
        Strategy Tool.

        This tool will execute a strategy.
        Possible Strategies are:\n
""" + "\n".join(
            [
                f"Strategy: {strategy[0]}\n\t"
                f"Info: {strategy[1]}\n\t"
                f"Params: {strategy[2]}\n" for strategy in classes_in_module(Strategies)
            ]
        )
    )

    parser.add_argument(
        "strategy",
        help="strategy to perform",
        nargs='+',
    )


class Main:
    def __init__(self, strategy_name, strategy_args):
        self.executor = Executor(strategy_name(*strategy_args))
        pprint(self.executor.execute_strategy())


if __name__ == '__main__':
    parser = ArgParser.parser
    args = parser.parse_args()
    strategy_to_execute = args.strategy.pop(0)
    strategy_class = getattr(Strategies, strategy_to_execute)
    main = Main(strategy_class, args.strategy)
