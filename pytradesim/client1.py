#!/usr/bin/env python

import configparser
import logging
from time import sleep

import click
from modules.client import (Client,
                            fix,
                            new_order,
                            send, 
                            new_quote_request,
                            new_cancel
                        )
from modules.utils import setup_logging


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    options_metavar="[options...]",
)
@click.argument(
    "client_config", type=click.Path(exists=True), metavar="[client config]"
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Print debug messages.",
)
def main(client_config="configs/client1.cfg", debug=None):
    """FIX client

    Sends new order over a FIX session.

    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.info(f"Logging set to debug.")
    else:
        logger.setLevel(logging.INFO)
        logger.info(f"Logging set to info.")

    config = configparser.ConfigParser()

    config.read(client_config)

    sender_compid = config["SESSION"]["SenderCompID"]
    target_compid = config["SESSION"]["TargetCompID"]

    settings = fix.SessionSettings(client_config)
    store = fix.FileStoreFactory(settings)
    app = Client()

    app.set_logging(logger)

    initiator = fix.SocketInitiator(app, store, settings)

    initiator.start()

    sleep(1)

    while True:
        try:
            sleep(1)
            choice = int(
                input(
                    "Enter choice :- "
                    "\n1. New quote request"
                    "\n2. New order"
                    "\n3. Cancel order"
                    "\n> "
                )
            )
            if choice == 1:
                print("Enter quote request:- ")
                symbol = input("Symbol: ")
                quantity = input("Quantity: ")
                side = input("Side: ")

                message = new_quote_request(
                    sender_compid,
                    target_compid,
                    symbol,
                    quantity,
                    side,
                )

                print("Sending new quote request...")
                print(message)
                print('!!!=======================!!!')
                send(message)

            elif choice == 2:
                print("Enter order :- ")
                symbol = input("Symbol: ")
                price = input("Price: ")
                quantity = input("Quantity: ")
                side = input("Side: ")
                order_type = input("Type: ")

                message = new_order(
                    sender_compid,
                    target_compid,
                    symbol,
                    quantity,
                    price,
                    side,
                    order_type,
                )

                print("Sending new order...")
                print(message)
                print('=======================')
                send(message)

            elif choice == 3:
                print("The order request: ")
                print(message, '\nhas been sent.')
                decision = input("Do you want to cancel?: (y/n)")

                if decision == 'y':
                    message = new_cancel(
                        sender_compid,
                        target_compid
                    )

                    print("Sending new order...")
                    print(message)
                    print('=======================')
                    send(message)
                else:
                    print("\nYou didn't cancel the order\n")

        except KeyboardInterrupt:
            initiator.stop()
            print("Goodbye... !\n")


if __name__ == "__main__":
    logger = setup_logging("logs/", "client")
    main()
