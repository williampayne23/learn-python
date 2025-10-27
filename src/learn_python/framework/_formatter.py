from colorama import Fore, Style
from ._exercise import ParametrizedResult


def format_results(results):
    """Print formatted and colored summary of test results.

    Args:
        results: List of Result or ParametrizedResult objects
    """
    for result in results:
        if isinstance(result, ParametrizedResult):
            # Show m/n format for parametrized tests
            symbol = (
                f"{Fore.GREEN}✓{Style.RESET_ALL}"
                if result.status == "success"
                else f"{Fore.RED}✗{Style.RESET_ALL}"
            )
            passed = sum(1 for r in result.results if r.status == "success")
            total = len(result.results)
            print(f"{symbol} {result.test_name}: {passed}/{total} complete")
        else:
            # Regular result
            symbol = (
                f"{Fore.GREEN}✓{Style.RESET_ALL}"
                if result.status == "success"
                else f"{Fore.RED}✗{Style.RESET_ALL}"
            )
            print(f"{symbol} {result.test_name}: {result.message}")

    # Final summary line
    total = len(results)
    passed = sum(1 for r in results if r.status == "success")

    if passed == total:
        print(f"{Fore.GREEN}All {total} tests passed!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}{passed}/{total} tests passed{Style.RESET_ALL}")
