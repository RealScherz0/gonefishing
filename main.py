from flask import Flask, request

app = Flask(__name__)

BLACKLIST = [ '10.0.0.0/8', '127.0.0.0/8', '169.254.0.0/16', '172.16.0.0/12', '192.0.2.0/24',  '192.168.0.0/16',   '198.18.0.0/15',  '198.51.100.0/24',  '203.0.113.0/24',  '240.0.0.0/4',  '100.64.0.0/10',  '172.64.0.0/10',  '185.159.128.0/18','185.212.3.0/24','185.212.4.0/22', '185.212.8.0/21', '185.244.216.0/22', '185.244.220.0/24', '185.244.221.0/24', ]

def is_proxy(ip_address):
    for subnet in BLACKLIST:
        if ip_address in subnet:
            return True
    return False

@app.route('/')
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        client_ips = x_forwarded_for.split(',')
        client_ip = client_ips[0].strip()
        real_ip = client_ips[-1].strip()
    else:
        client_ip = request.remote_addr
        real_ip = request.headers.get('X-Real-IP') or request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')
    print(f"Detected IP address: {client_ip}")
    print(f"Real IP address: {real_ip}")
    if is_proxy(client_ip):
        print("Detected proxy or VPN server.")
    if user_agent:
        print(f"Browser: {user_agent}")
    if referrer:
        print(f"Referrer: {referrer}")
    return '''
    <!DOCTYPE html>
<html>
<head>
	<title>YOUR IP HAS BEEN LOGGED :)</title>
	<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.2/animate.min.css">
	<style>
		body {
			background-color: #1b1b1b;
			color: #fff;
			font-family: 'Montserrat', sans-serif;
			font-size: 16px;
			line-height: 1.5;
			margin: 0;
			padding: 0;
			text-align: center;
		}

		h1 {
			font-size: 4em;
			margin-top: 10%;
			text-transform: uppercase;
		}

		#trollface {
			margin-top: 5%;
			max-width: 100%;
		}

		p {
			font-size: 1.2em;
			margin-top: 5%;
		}

		button {
			background-color: #ff0066;
			border: none;
			border-radius: 5px;
			color: #fff;
			cursor: pointer;
			font-size: 1.2em;
			margin-top: 5%;
			padding: 1em 2em;
			transition: background-color 0.2s ease;
		}

		button:hover {
			background-color: #ff0055;
		}

		@keyframes trollface {
			5% {
				transform: rotate(0deg);
			}
			100% {
				transform: rotate(500deg);
			}
		}

		@media screen and (min-width: 700px) {
			h1 {
				font-size: 5em;
			}

			#trollface {
				margin-top: 0%;
			}

			p {
				font-size: 1.5em;
			}

			button {
				font-size: 9.5em;
				padding: 9em 9em;
			}
		}
	</style>
</head>
<body>
	<h1 class="animated fadeInDown">YOUR IP HAS BEEN LOGGED :)</h1>
	<img id="trollface" class="animated infinite bounce" src="https://imgs.search.brave.com/r7gjs8x0sxloSohWsfXbxcpuakybGIuFTS2WHVkjmH0/rs:fit:844:225:1/g:ce/aHR0cHM6Ly90c2Ux/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC5a/LUtuY2lITFJxT1Ax/eVkwdEhHMkJnSGFF/SyZwaWQ9QXBp" alt="Trollface">
</body>
</html>
  '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)