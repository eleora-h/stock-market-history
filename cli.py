import os
import polygon

class CLI():
    def __init__(self):
        self.polygon = polygon.Polygon()
        self.run()
        self.first_run = False

    def __build_interface(self):
        while True:
            interface_text = """
            What to do next?
            """
            print(interface_text)
            parsed_input = input().lower()
            if parsed_input in ('-h', '--help'):
                self.__get_help_menu()
            elif parsed_input in ('-t', '--tickers'):
                self.polygon.get_tickers()
                self.__get_ticker_menu()
            elif parsed_input in ('-q', '--quit'):
                break
            else:
                print('Command entered not recognized. Please type -q to quit or -h for more options.')

    def __get_help_menu(self):
        help_text = """
            --help, -h for help                               \t--tickers, -t to get all available tickers
        """
        print(help_text)

    def __get_ticker_menu(self):
        while True:
            ticker_menu_text = """
                If you would like to find out more about a specific stock, please enter --info "ticker_name" or -i "ticker_name".
                Else enter any key to go back. 
            """
            print(ticker_menu_text)
            parsed_input = input().lower()
            if parsed_input.startswith('--info') or parsed_input.startswith('-i'):
                ticker = parsed_input.split('"')[1]
                self.polygon.get_ticker_info(ticker)
            else:
                break

    def run(self):
        print('Starting up program...')
        start_text = """
            Hi! Welcome to the command line interface for exploring the American stock market.
            I recommend getting started by getting a list of available ticker symbols. Do this by inputting --tickers or -t.
        """
        print(start_text)
        self.__build_interface()
        print('Thanks for testing program!')