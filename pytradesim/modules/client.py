import quickfix as fix
import quickfix42 as fix42

from .utils import Message

ORDERS = {}


class BaseApplication(fix.Application):
    def logMessage(self, message):
        message = message.__str__()
        return message.replace("\x01", "|")

    def onCreate(self, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n onCreate in work')
        return

    def onLogon(self, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n onLogon in work')
        return

    def onLogout(self, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n onLogout in work')
        return

    def toAdmin(self, message, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n toAdmin message: ', self.logMessage(message), '\n ======================================================')
        self.sessionID = sessionID
        return

    def fromAdmin(self, message, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n fromAdmin message: ', self.logMessage(message), '\n ======================================================')
        return

    def toApp(self, message, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n toApp message: ', self.logMessage(message), '\n ======================================================')
        return

    def fromApp(self, message, sessionID):
        print ('\n--------------------------_______________--------------------- \n ./pytradesimulator/pytradesim/modules/client.py \n fromApp message: ', self.logMessage(message)
        , '\n ======================================================')
        return


ORDER_TABLE = {}


class Client(BaseApplication):

    def logMessage(self, message):
        message = message.__str__()
        return message.replace("\x01", "|")

    def set_logging(self, logger):
        self.logger = logger

    def onCreate(self, sessionID):
        self.logger.info(f"Successfully created session {sessionID}.")
        return

    def onLogon(self, sessionID):
        self.logger.info(f"{sessionID} session successfully logged in.")
        return

    def onLogout(self, sessionID):
        self.logger.info(f"{sessionID} session successfully logged out.")
        return

    def toApp(self, message, sessionID):
        self.logger.debug(f"Sending {self.logMessage(message)} session {sessionID}")

    def fromApp(self, message, sessionID):
        self.logger.info(f"Got message {self.logMessage(message)} for {sessionID}.")
        self.process(message, sessionID)

    def process(self, message, sessionID):
        self.logger.debug("Processing message.")
        msgtype = fix.MsgType()
        # exectype = fix.ExecType()
        message.getHeader().getField(msgtype)
        # message.getField(exectype)
        
        if msgtype.getValue() == "S":
            self.logger.debug("Quote message.")
            self.logger.info("Quote received.")
            (
                quote_req_id,
                quote_id,
                symbol,
                offer_size,
                offer_px
            ) = self.__getQuote(message)

        elif msgtype.getValue() == "8":
            self.logger.debug("Execution Report message.")
            self.logger.info("Execution Report received.")
            (
                order_id,
                cl_ord_id,
                symbol,
                side,
                client_id,
                order_qty,
                exec_id,
                exec_trans_type,
                exec_type,
                ord_status,
                account,
                leaves_qty,
                cum_qty,
                avg_px,
                transact_time,
            ) = self.__getExecutionReport(message)
        # elif msgtype.getValue() == "D":
            self.logger.debug("New Order message.")
            self.logger.info("New Order received.")
            (
                quote_id,
                client_id,
                handl_inst,
                ord_type,
                transact_time,
                side,
                symbol,
                cl_ord_id
            ) =self.__getNewOrder(message)

        
    def __getQuote(self, message):
        self.logger.debug("accept Quote message.")
        quote_req_id = fix.QuoteReqID()
        quote_id = fix.QuoteID()
        symbol = fix.Symbol()
        offer_size = fix.OfferSize()
        offer_px = fix.OfferPx()

        message.getField(quote_req_id)
        message.getField(quote_id)
        message.getField(symbol)
        message.getField(offer_size)
        message.getField(offer_px)
        
        print('!!!!!!!!!!!!!!!!')
        print('quote_id: ', quote_id)
        print('!!!!!!!!!!!!!!!!')

        return (quote_req_id, quote_id, symbol, offer_size, offer_px)

    def __getExecutionReport(self, message):
        self.logger.debug("accept Execution Report.")
        order_id = fix.OrderID()
        cl_ord_id = fix.ClOrdID()
        symbol = fix.Symbol()
        side = fix.Side()
        client_id = fix.ClientID()
        order_qty = fix.OrderQty()
        exec_id = fix.ExecID()
        exec_trans_type = fix.ExecTransType()
        exec_type = fix.ExecType()
        ord_status = fix.OrdStatus()
        account = fix.Account()
        leaves_qty = fix.LeavesQty()
        cum_qty = fix.CumQty()
        avg_px = fix.AvgPx()
        transact_time = fix.TransactTime()
        
        message.getField(order_id)
        message.getField(cl_ord_id)
        message.getField(symbol)
        message.getField(side)
        message.getField(client_id)
        message.getField(order_qty)
        message.getField(exec_id)
        message.getField(exec_trans_type)
        message.getField(exec_type)
        message.getField(ord_status)
        message.getField(account)
        message.getField(leaves_qty)
        message.getField(cum_qty)
        message.getField(avg_px)
        message.getField(transact_time)

        return (order_id, cl_ord_id, symbol, side, client_id, order_qty, exec_id, exec_trans_type, exec_type, ord_status, account, leaves_qty, cum_qty, avg_px, transact_time)

    # def __getNewOrder(self, message):
        self.logger.debug("accept New Order message.")
        quote_id = fix.QuoteID()
        client_id= fix.ClientID()
        handl_inst = fix.HandlInst()
        ord_type = fix.OrdType()
        transact_time =fix.TransactTime()
        side = fix.Side()
        symbol = fix.Symbol()
        cl_ord_id = fix.ClOrdID()

        message.getField(quote_id)
        message.getField(client_id)
        message.getField(handl_inst)
        message.getField(ord_type)
        message.getField(transact_time)
        message.getField(side)
        message.getField(symbol)
        message.getField(cl_ord_id)

        return (quote_id, client_id, handl_inst, ord_type, transact_time, side, symbol, cl_ord_id)


    def __get_attributes(self, message):
        price = fix.LastPx()
        quantity = fix.LastQty()
        symbol = fix.Symbol()
        side = fix.Side()
        client_order_id = fix.ClOrdID()
        exec_id = fix.ExecID()
        order_status = fix.OrdStatus()

        message.getField(client_order_id)
        message.getField(side)
        message.getField(symbol)
        message.getField(price)
        message.getField(quantity)
        message.getField(order_status)
        message.getField(exec_id)

        return (symbol, price, quantity, side, client_order_id, exec_id, order_status)


def get_order_id(sender_comp_id, symbol):
    if symbol in ORDER_TABLE:
        _id = ORDER_TABLE[symbol]
    else:
        _id = 1

    order_id = sender_comp_id + symbol + str(_id)
    ORDER_TABLE[symbol] = _id + 1

    return order_id

# _, quote_id, _, _, _ = Client(BaseApplication).self.__getQuote()

def new_order(
    sender_comp_id, target_comp_id, symbol, quantity, price, side, order_type, quote_id
):
    if side.lower() == "buy":
        side = fix.Side_BUY
    else:
        side = fix.Side_SELL

    message = Message()
    # app = Client()
    # quote_data = app.__getQuote(message)
    # quote_id = quote_data[1]
    header = message.getHeader()
    header.setField(fix.BeginString("FIX.4.2"))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgType("D"))
    ord_id = get_order_id(sender_comp_id, symbol)
    message.setField(fix.ClOrdID(ord_id))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.ClientID('1')) # сделать одинаковым для всех
    if order_type.lower() == "market":
        message.setField(fix.OrdType(fix.OrdType_MARKET))
    else:
        message.setField(fix.OrdType(fix.OrdType_LIMIT)) 
    message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
    message.setField(fix.TransactTime())
    message.setField(fix.QuoteID(quote_id)) #=================
    

    return message

def new_quote_request(
    sender_comp_id, target_comp_id, symbol, quantity, side
):
    if side.lower() == "buy":
        side = fix.Side_BUY
    else:
        side = fix.Side_SELL

    message = Message()
    header = message.getHeader()
    header.setField(fix.BeginString("FIX.4.2"))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    header.setField(fix.MsgType("R"))
    message.setField(fix.Symbol(symbol)) # +++++++
    message.setField(fix.Side(side)) #+++++++++++
    message.setField(fix.ClientID('1')) # +++++++++ сделать одинаковым для всех
    message.setField(fix.OrderQty(float(quantity))) #from replace_order
    message.setField(fix.NoRelatedSym(4)) # ?????????????
    message.setField(fix.QuoteReqID('1')) # Мой id

    return message

def replace_order(
    sender_comp_id, target_comp_id, quantity, price, orig_client_order_id
):
    symbol = ORDERS[orig_client_order_id][0].getValue()
    side = ORDERS[orig_client_order_id][3].getValue()

    message = fix42.OrderCancelReplaceRequest()
    header = message.getHeader()
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    ord_id = get_order_id(sender_comp_id, symbol)
    message.setField(fix.OrigClOrdID(orig_client_order_id))
    message.setField(fix.ClOrdID(ord_id))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.Price(float(price)))
    message.setField(fix.OrdType(fix.OrdType_LIMIT))
    message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
    message.setField(fix.TransactTime())
    message.setField(fix.TransactTime())
    message.setField(fix.OrderQty(float(quantity)))
    message.setField(fix.Text(f"{side} {symbol} {quantity}@{price}"))

    return message


def delete_order(sender_comp_id, target_comp_id, orig_client_order_id):
    symbol = ORDERS[orig_client_order_id][0].getValue()
    side = ORDERS[orig_client_order_id][3].getValue()

    message = fix42.OrderCancelRequest()
    header = message.getHeader()
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    ord_id = get_order_id(sender_comp_id, symbol)
    message.setField(fix.OrigClOrdID(orig_client_order_id))
    message.setField(fix.ClOrdID(ord_id))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.TransactTime())
    message.setField(fix.Text(f"Delete {orig_client_order_id}"))

    return message


def send(message):
    try:
        fix.Session.sendToTarget(message)
    except fix.SessionNotFound:
        raise Exception(f"No session found {message}, exiting...")
