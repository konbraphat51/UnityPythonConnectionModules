from UnityConnector import UnityConnector

def on_timeout():
    print("timeout")
    
def on_stopped():
    print("stopped")

connector = UnityConnector(
    on_timeout=on_timeout,
    on_stopped=on_stopped
)

def on_data_received(data_type, data):
    print(data_type, data)

connector.start_listening(
    on_data_received
)

print("connected")

while(True):
    input_data = input()
    
    if input_data == "q":
        connector.stop_connection()
        break
    
    data = {
        "testValue0": 334,
        "testValue1": [0.54,0.23,0.12,],
    }
    
    print(data)
    
    connector.send(
        "test",
        data
    )