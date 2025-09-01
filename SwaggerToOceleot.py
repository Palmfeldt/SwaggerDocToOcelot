# Simple Swagger to Ocelot Gateway converter
import json
import sys

def convert_swagger_to_ocelot(swagger_path, ocelot_path, input_address):
	with open(swagger_path, 'r', encoding='utf-8') as f:
		swagger = json.load(f)

	routes = []
	base_path = swagger.get('basePath', '/')
	paths = swagger.get('paths', {})

    # Try to split the address and port
	try:
		address, port = input_address.split(":")
	except ValueError:
		print("Invalid address format. Use <address:port>")
		sys.exit(1)
		
	for path, methods in paths.items():
		for method, details in methods.items():
			route = {
				"DownstreamPathTemplate": base_path + path,
				"DownstreamScheme": "https",
				"UpstreamPathTemplate": path,
				"UpstreamHttpMethod": [method.upper()],
				"DownstreamHostAndPorts": [
					{"Host": address, "Port": int(port)}
				]
			}
			routes.append(route)

	ocelot_config = {
		"Routes": routes,
		"GlobalConfiguration": {
			"BaseUrl": "https://localhost"
		}
	}

	with open(ocelot_path, 'w', encoding='utf-8') as f:
		json.dump(ocelot_config, f, indent=2)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage: python swaggerToOceleot.py <swagger.json> <ocelot.json> <address:port>")
		sys.exit(1)
	convert_swagger_to_ocelot(sys.argv[1], sys.argv[2], sys.argv[3])

