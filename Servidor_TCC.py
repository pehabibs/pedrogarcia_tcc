from adafruit_ads1x15.analog_in import AnalogIn
import datetime
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import simpy
import asyncio
from asyncua import Server

#Variaveis Globais
CLOCKWISE = 1
ANTI_CLOCKWISE = 0
STEP_PIN = 17
DIRECTION_PIN = 22
SINAL = 0
AUX3=0


ENDPOINT = "opc.tcp://192.168.0.123:4840"
NAMESPACE = "OPCUA"


# Setup gpio pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)


#Potenciometro
#Inicializa a interface I2C
i2c = busio.I2C(board.SCL, board.SDA)
#Cria o objeto ADC
ads = ADS.ADS1115(i2c)
#Define a leitura das portas analogicas do módulo
canal0 = AnalogIn(ads, ADS.P0)


async def Step(stepsToTake, direction, Pot, Sin):
    GPIO.output(22, direction)
    AUX = 0
    AUX10 = 0
    AUX20 = 0
    global SINAL
    global AUX1
    global AUX2
    global AUX3
    # Take requested number of steps
    for x in range(stepsToTake):
        GPIO.output(17, GPIO.HIGH)
        await asyncio.sleep(0.1)
        GPIO.output(17, GPIO.LOW)
        await asyncio.sleep(0.1)
        if (direction == GPIO.HIGH):
            #SINAL = 100*(SINAL+1)/1410
            SINAL = SINAL -1
        if (direction == GPIO.LOW):
            #SINAL = 100*(SINAL-1)/1410
            SINAL = SINAL +1
        AUX=AUX+1

        #Mostra os valores lidos das portas analogicas
        
        if(AUX3 == 1):
            #if(AUX == 10):
                #await asyncio.sleep(1)
            if(AUX == 14):
                AUX10 = 100*(canal0.value - AUX2)/(AUX1-AUX2)
                #print(AUX10)
                #print(canal0.value)
                await Pot.write_value(int(AUX10))
                #print(100*(canal0.value - AUX2)/(AUX1-AUX2))
                AUX20 = 100*SINAL/1410
                #print(type(SINAL))
                #print(AUX20)
                await Sin.write_value(int(AUX20))
                #print(SINAL)
                #print(type(SINAL))
                AUX=0
                #await asyncio.sleep(1)


async def main() -> None:
    global AUX1
    global AUX2
    global AUX3
    # Start a server.
    server = Server()
    await server.init()
    server.set_endpoint(ENDPOINT)
    idx = await server.register_namespace(NAMESPACE)
    await server.start()
    print(f'Server started: {server}')

    # Create a node.
    myobj = await server.get_objects_node().add_object(idx, 'MyObject')
    
    Pot = await myobj.add_variable(idx, 'Potenciometro', 1)
    await Pot.set_writable()
    
    Sin = await myobj.add_variable(idx, 'Sinal', 1)
    await Sin.set_writable()



    # Go backwards once
    await Step(1410,GPIO.LOW, Pot, Sin)
    AUX1 = canal0.value
    print(canal0.value)
        
    await asyncio.sleep(10)

    # Go forwards once
    await Step(1410,GPIO.HIGH, Pot, Sin)
    AUX2 = canal0.value
    print(canal0.value)

    #print((canal0.value - AUX2)/(AUX1-AUX2))
    AUX3=1
    
    while True:
        print('Rotina')
        await asyncio.sleep(10)

    # Go forwards once
        await Step(1410,GPIO.LOW, Pot, Sin)
        await asyncio.sleep(10)
        print(canal0.value)

    # Go forwards once
        await Step(1410,GPIO.HIGH, Pot, Sin)
        await asyncio.sleep(10)
        print(canal0.value)


if __name__ == '__main__':
    asyncio.run(main())

