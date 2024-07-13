from flask import Flask, render_template, request, jsonify
from pyXSteam.XSteam import XSteam

app = Flask(__name__)
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enthalpy', methods=['GET', 'POST'])
def calculate_enthalpy():
    try:
        data = request.get_json() if request.get_json() else {}
        app.logger.debug(f"Received data: {data}")

        # Default values if not provided in JSON
        default_pressure = data.get('pressure', '1.0')  # default pressure in MPa (as string)
        default_temperature = data.get('temperature', '100.0')  # default temperature in Celsius (as string)

        # Convert pressure and temperature from string to float
        pressure = float(default_pressure)
        temperature = float(default_temperature)

        enthalpy_in_KJKg = steamTable.h_pt(pressure, temperature)
        enthalpy_in_KcalKg = enthalpy_in_KJKg / 4.184

        result = {
            "enthalpy_KJ_Kg": round(enthalpy_in_KJKg, 2),
            "enthalpy_kcal_Kg": round(enthalpy_in_KcalKg, 2)
        }

        return jsonify(result), 200

    except KeyError as e:
        app.logger.error(f"KeyError: {e}")
        return jsonify({"error": f"Missing key in JSON data: {str(e)}"}), 400

    except ValueError as e:
        app.logger.error(f"ValueError: {e}")
        return jsonify({"error": f"Invalid value provided: {str(e)}"}), 400

    except Exception as e:
        app.logger.error(f"Exception: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
