import base64
import websocket

def main():
    ws_url = "ws://localhost:24621"
    ws = websocket.create_connection(ws_url)

    fxr_fn = "f000450060.fxr"
    with open(fxr_fn, "rb") as fxr_file:
        fxr_binary_data = fxr_file.read()
        fxr_base64_data = base64.b64encode(fxr_binary_data).decode('utf8')

    fxr_request = {
        "requestID": f"fxr_{fxr_fn[4:-4]}_reload_request",
        "type": 0,
        "data": fxr_base64_data
    }

    ws.send(json.dumps(reload_fxr_request))
    response = ws.recv()
    print("\nResponse:", response)

if __name__ == '__main__': main()
