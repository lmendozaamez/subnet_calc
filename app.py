from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

def calcular_subnet(ip_cidr):
    try:
        red = ipaddress.ip_network(ip_cidr, strict=False)
        hosts = list(red.hosts())
        return {
            "ip_cidr": ip_cidr,
            "direccion_red": str(red.network_address),
            "mascara": str(red.netmask),
            "prefijo": red.prefixlen,
            "mascara_binaria": '.'.join(format(octeto, '08b') for octeto in red.netmask.packed),
            "broadcast": str(red.broadcast_address),
            "cantidad_hosts": len(hosts),
            "primer_host": str(hosts[0]) if hosts else None,
            "ultimo_host": str(hosts[-1]) if hosts else None
        }
    except ValueError:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        ip_cidr = request.form.get("ip_cidr")
        resultado = calcular_subnet(ip_cidr)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
