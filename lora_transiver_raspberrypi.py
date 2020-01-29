 from time import sleep
from SX127x.LoRa import*
from SX127x.board_config import BOARD
BOARD.setup()

class LoRaRcvCont(LoRa):
   
    tx_counter=0
   
    def __init__(self, verbose=False):
	'''this function will initialize the process''' 
    def start(self):
	'''this function make the board as tranceiver(board configuration)'''
        self.reset_ptr_rx()
        sys.stdout.write("\rstart")
        self.set_mode(MODE.TX)
        self.set_mode(MODE.RXCONT)
        self.write_payload([0x0f])#base address to store the received data
        lora.on_tx_done()
        sleep(1)   
        while True:
       
            sleep(1)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            '''lora.on_tx_done()
            sleep(1)'''
            lora.on_rx_done()
            sleep(1)
            '''lora.on_rx_done()
            sleep(1)'''
            sys.stdout.flush()
           
   
           
    def on_rx_done(self):
	''''this function receive values from the arduino'''
        self.set_mode(MODE.STDBY)
        print("Received: ")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)#this line will read the value from arduino
        print(bytes(payload).decode("utf-8",'ignore'))#this line will decode received the data
        #lora.on_tx_done()
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
       
   
   
   
    def on_tx_done(self):
	''''this function transmit values to the arduino'''
        #global args
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        #self.tx_counter += 1
        #sys.stdout.write("\rtx #%d" % self.tx_counter)
        
        rawinput = str(input("Enter the node:")
        
        data =[int(hex(ord(c)), 0) for c in rawinput]#this line will encode the data to be tansmitted
        self.write_payload(data)#this line will transmit the value to arduino
        self.set_mode(MODE.TX)          
       

lora=LoRaRcvCont()
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
'''this is the exception handling block'''
try:
   
    lora.start()


except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
